+++
author = "Toni Sagrista Selles"
categories = ["Rust"]
tags = [ "rust", "programming"]
date = "2021-02-26"
description = "How to handle memory mapped files in Rust using the memmap crate"
linktitle = ""
title = "Memory mapped files in Rust"
type = "post"
+++

In my re-implementation of the Gaia Sky level-of-detail (LOD) catalog generation in Rust I have been able to roughly **halve the processing time**, and, even though I do not have concrete numbers yet, everything points towards a **drastic decrease in memory usage** as well. In this project, I need to read a metric ton of gzipped ``csv`` Gaia catalog files, parse and process them into a functional in-memory catalog with cartesian positions, velocity vectors, RGB colors, etc. Then I need use them to [generate an octree](https://doi.org/10.1109/TVCG.2018.2864508) that represents the LOD structure, and finally write another metric ton of binary files back to disk. Using memory mapped files helps a lot in avoiding copies and speeding up the reading and writing operations; that's something I tried out in the Java version and have come to also re-implement in Rust. Here's the thing though: working with memory mapped files in Java is super straightforward. In Rust? Not so much. And the lack of available documentation and examples does not help. I was actually unable to find any working snippets with all the parts I needed, so I'm documenting it in this post in case someone else is in the same situation I was.

<!--more-->

To that purpose, we will use the [``memmap``](https://docs.rs/memmap/0.7.0/memmap/index.html) crate. 

## Reading memory mapped text files

In my case, since I only need to read text files line by line, reading is the easy part. My input files may or may not be gzipped, so my ``Read`` objects need to be wrapped up in a ``Box``, since its size is not known at compile time. Other than that, we need to create a memory mapped buffer and pass it on to the actual reader creation.
 
The snippet below shows how to read a text file by memory mapping it (memory map creation highlighted).

{{< highlight rust "linenos=table,hl_lines=5 6" >}}
pub fn load_file(&self, file: &str) {
    let mut skipped: usize = 0;
    let is_gz = file.ends_with(".gz") || file.ends_with(".gzip");
    let f = File::open(file).expect("Error: file not found");
    // Create the memory mapped buffer
    let mmap = unsafe { Mmap::map(&f).expect(&format!("Error mapping file {}", file)) };

    let reader: Box<dyn io::BufRead>;
    if is_gz {
        // pass buffer slice to GzDecoder if we're reading a gzip file
        reader = Box::new(io::BufReader::new(GzDecoder::new(&mmap[..])));
    } else {
        // otherwise, just box the slice!
        reader = Box::new(&mmap[..]);
    }

    for line in reader.lines() {
        match self.parse_line(line.expect("Error reading line")) {
            Some(part) => {
                // process line here
            }
            None => skipped += 1,
        }
    }
}
{{< /highlight >}}


## Writing memory mapped binary files

Once the generation of the octree (octree node) has finished, I need to dump the contents of each octant to a file so that they can later be loaded and used by Gaia Sky. These files contain the information of all the stars in the octant, and the more compact they are, the faster the loading and streaming to VRAM will be when Gaia Sky is running. 

The file format used is a binary format, [described here](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Data-streaming.html#version-2), and below's an overview of the contents, in order.

* 1 single-precision integer (32-bit) – token number -1
* 1 single-precision integer (32-bit) – version number (2 in this case)
* 1 single-precision integer (32-bit) – number of stars in the file
* For each star:
    * 3 double-precision floats (64-bit * 3) – X, Y, Z cartesian coordinates in internal units
    * 3 single-precision floats (32-bit * 3) – Vx, Vy, Vz - cartesian velocity vector in internal units per year
    * 3 single-precision floats (32-bit * 3) – mualpha, mudelta, radvel - proper motion
    * 4 single-precision floats (32-bit * 4) – appmag, absmag, color, size - Magnitudes, colors (encoded), and size (a derived quantity, for rendering)
    * 1 single-precision integer (32-bit) – HIP number (if any, otherwise negative)
    * 1 double-precision integer (64-bit) – Gaia SourceID
    * 1 single-precision integer (32-bit) – namelen -> Length of name
    * namelen * char (16-bit * namelen) – Characters of the star name, where each character is encoded with UTF-16

Writing to a memory mapped file in rust is really almost the same as writing to a byte buffer. You need to know the exact size of the file beforehand, and then fill the buffer with the right bytes at the right positions. As you can see below, that's exactly what I'm doing. I first compute the final size of the file (lines 9 to 39) and only then I create the mapped buffer (highlighted lines) and fill it up, making sure that each element is in the right position (lines 62 through end).

Most of the code below pertains to my particular binary format, but it beautifully exemplifies how to fill up the buffer with different data types and variable numbers of them.

{{< highlight rust "linenos=table,hl_lines=58 59" >}}
pub fn write_particles_mmap(octree: &Octree, list: Vec<Particle>, output_dir: &str) {
    let mut file_num = 0;
    for node in octree.nodes.borrow().iter() {
        if node.deleted.get() {
            // Skip deleted
            continue;
        }

        // COMPUTE FILE SIZE
        // header 3 * i32
        let mut size = 32 * 3;
        // particles
        for star_idx in node.objects.borrow().iter() {
            if list.len() > *star_idx {
                // 3 * f64
                size += 8 * 3;
                // 10 * f32
                size += 4 * 10;
                // 1 * i32 hip
                size += 4 * 1;
                // 1 * i64 source_id
                size += 8 * 1;
                // 1 * i32 name_len
                size += 4 * 1;

                let sb = list
                    .get(*star_idx)
                    .expect(&format!("Star not found: {}", *star_idx));
                let mut name_size = 0;
                for name in sb.names.iter() {
                    name_size += name.len() + 1;
                }
                if name_size > 0 {
                    name_size -= 1;
                }
                // 1 * u16 * name_len
                size += 2 * name_size;
            }
        }

        // File name
        let id_str = format!("particles_{:06}", node.id.0);
        let particles_dir = format!("{}/particles", output_dir);
        std::fs::create_dir_all(Path::new(&particles_dir))
            .expect(&format!("Error creating directory: {}", particles_dir));
        let file_path = format!("{}/{}.bin", particles_dir, id_str);

        let f = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .open(file_path)
            .expect("Error opening memory mapped file");

        f.set_len(size as u64)
            .expect("Error setting size to memory mapped file");

        // create memory mapped buffer to write to
        let mut mmap = unsafe { MmapMut::map_mut(&f).expect("Error creating memory map") };

        let mut i: usize = 0;
        // version marker
        (&mut mmap[i..i + 4])
            .write_all(&(-1_i32).to_be_bytes())
            .expect("Error writing");
        i += 4;

        // version = 2
        (&mut mmap[i..i + 4])
            .write_all(&(2_i32).to_be_bytes())
            .expect("Error writing");
        i += 4;

        // size
        (&mut mmap[i..i + 4])
            .write_all(&(node.objects.borrow().len() as i32).to_be_bytes())
            .expect("Error writing");
        i += 4;

        // particles
        for star_idx in node.objects.borrow().iter() {
            if list.len() > *star_idx {
                let sb = list
                    .get(*star_idx)
                    .expect(&format!("Star not found: {}", *star_idx));

                // 64-bit floats
                (&mut mmap[i..i + 8])
                    .write_all(&(sb.x).to_be_bytes())
                    .expect("Error writing");
                i += 8;
                (&mut mmap[i..i + 8])
                    .write_all(&(sb.y).to_be_bytes())
                    .expect("Error writing");
                i += 8;
                (&mut mmap[i..i + 8])
                    .write_all(&(sb.z).to_be_bytes())
                    .expect("Error writing");
                i += 8;

                // 32-bit floats
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.pmx).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.pmy).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.pmz).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.mualpha).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.mudelta).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.radvel).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.appmag).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.absmag).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.col).to_be_bytes())
                    .expect("Error writing");
                i += 4;
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.size).to_be_bytes())
                    .expect("Error writing");
                i += 4;

                // 32-bit int
                (&mut mmap[i..i + 4])
                    .write_all(&(sb.hip).to_be_bytes())
                    .expect("Error writing");
                i += 4;

                // 64-bit int
                (&mut mmap[i..i + 8])
                    .write_all(&(sb.id).to_be_bytes())
                    .expect("Error writing");
                i += 8;

                // names
                let mut names_concat = String::new();
                for name in sb.names.iter() {
                    names_concat.push_str(name);
                    names_concat.push_str("|");
                }
                names_concat.pop();

                // names length
                (&mut mmap[i..i + 4])
                    .write_all(&(names_concat.len() as i32).to_be_bytes())
                    .expect("Error writing");
                i += 4;

                // characters
                let mut buf: [u16; 1] = [0; 1];
                for ch in names_concat.chars() {
                    ch.encode_utf16(&mut buf);
                    (&mut mmap[i..i + 2])
                        .write_all(&(buf[0]).to_be_bytes())
                        .expect("Error writing");
                    i += 2;
                }
            } else {
                log::error!(
                    "The needed star index is out of bounds: len:{}, idx:{}",
                    list.len(),
                    *star_idx
                );
            }
        }
        mmap.flush().expect("Error flushing memory map");
        file_num += 1;
    }
    log::info!("Written {} particle files", file_num);
}
{{< /highlight >}}

## Conclusion

That is all. The repository that contains this code is here: [``gaiasky-catgen``](https://gitlab.com/gaiasky/gaiasky-catgen). It constitutes my very first foray into Rust, so a lot of the code may not be fully idiomatic (or idiomatic at all), and I'm sure it's not the fastest also. However, it works well and performs much better than the Java counterpart, both in speed and in memory usage. 

In this post we have seen how to deal with memory mapped files in Rust to both read and write data faster, avoiding memory copies.
