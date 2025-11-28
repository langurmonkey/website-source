+++
author = "Toni Sagrista Selles"
categories = ["JPEG XL"]
tags = ["open-source", "image", "visualization", "formats", "jpeg xl", "jxl", "avif", "jpeg", "png", "webp", "english"]
date = 2023-02-19
title = "JPEG XL vs AVIF: a comparison"
description = "An unscientific analysis of these two image formats based on file size and image quality."
featuredpath = "date"
type = "post"
+++

{{< sp orange >}}Edit (2024-01-24):{{</ sp >}} Following a [comment](https://mastodon.social/@cking@mastodon.world/111807707018032003) on Mastodon, I have added a reference on the good performance of lossless WebP.

{{< sp orange >}}Edit (2023-03-30):{{</ sp >}} Added a couple extra images to test for high-quality encoding and illustrations. Introduce SSIM and MSE measures.

{{< sp orange >}}Edit (2023-03-03):{{</ sp >}} Fixed mistake, as [AVIF does in fact NOT support progressive decoding](https://avif.io/blog/comparisons/avif-vs-jpegxl/#speed).

{{< notice "Disclaimer" >}}
This is **a subjective look** at JPEG XL and AVIF. All comparisons in this post (except the ones using SSIM and MSE) are perceptual and based on my own opinion only. This is **not a scientific study**! I just grabbed a bunch of images, encoded them and looked at the results.
For a more careful and methodical comparison between these formats (and more), have a look at [CID22](https://cloudinary.com/labs/cid22).
{{</ notice >}}


JPEG XL and AVIF are arguably the two main contenders in the battle to replace JPEG as the next-generation image format. There are other formats in the race, like HEIC and WebP 2, but the former is subject to licensing patents (and possibly not royalty-free), and the second is still in development and seems that it [may never see the light of day](https://chromium.googlesource.com/codecs/libwebp2/+/1251ca748c17278961c0d0059b744595b35a4943^%21/) as a production-ready image format anyway. The original WebP is not even a contender as it is inferior to AVIF in almost all aspects[^3] (although it may be ok in lossless compression[^6]), and you should probably **never** use it for photography anyway[^1], or at all if you are not ok with mediocre image quality.[^2]

First, a quick browser support test:

{{< fig src1="/img/2023/02/jxl-avif/support-jxl-yes.jxl" type1="image/jxl" src="/img/2023/02/jxl-avif/support-jxl-no.jpg" class="fig-center" width="50%" loading="lazy" >}}
{{< fig src1="/img/2023/02/jxl-avif/support-avif-yes.avif" type1="image/avif" src="/img/2023/02/jxl-avif/support-avif-no.jpg" class="fig-center" width="50%" loading="lazy" >}}

If you are browsing this page around 2023, chances are that your browser supports AVIF but does not support JPEG XL. This is mainly due to the [Chrome team dropping support for JPEGL XL](/blog/2022/jpeg-xl-chrome) against the opinion the community at large. In this post, I hope to convince you why this is a bad move. Below, I perform a quick analysis of lossless and lossy compression with JPEG XL and AVIF, and evaluate how they fare in terms of file size and visual quality.

<!--more-->

## Methodology

I have selected five different test images to run through both the JPEG XL and the AVIF encoders:

- **Flag** --- a sunset with a smooth red-yellow gradient in the sky and a quiet sea with lots of detail. There is a flag in the foreground, which is mostly black due to it being lit from behind.
{{< fig src="/img/2023/02/jxl-avif/flag-s.jpg" class="fig-center" width="50%" title="Flag. Taken from free-images.com, downsampled to full HD and losslessly saved to PNG." loading="lazy" >}}

- **BW cityscape** --- a black-and-white cityscape at night. It has a lot of contrast.
{{< fig src="/img/2023/02/jxl-avif/city-s.jpg" class="fig-center" width="50%" title="BW cityscape. Taken from free-images.com, downsampled to full HD and losslessly saved to PNG." loading="lazy" >}}

- **Red panda** --- a photo of a red panda with some green leaves on the foreground and a green bokeh in the background.
{{< fig src="/img/2023/02/jxl-avif/redpanda-s.jpg" class="fig-center" width="50%" title="Red panda. Taken from free-images.com, at the original resolution of 4407x2919 and losslessly saved to PNG." loading="lazy" >}}

- **Fireman wedding** --- a vector illustration of a newly wed couple.
{{< fig src="/img/2023/02/jxl-avif/firemanwedding-s.jpg" class="fig-center" width="50%" title="Vector wedding. PNG created from the SVG at 1500x1380." loading="lazy" >}}

- **Plot** --- a simple plot created with matplotlib.
{{< fig src="/img/2023/02/jxl-avif/plot-s.jpg" class="fig-center" width="50%" title="Plot. Directly produced by matplotlib in lossless PNG at 5760x4320." loading="lazy" >}}

The first four images (flag, cityscape, red panda and vector wedding) are in the public domain, CC0, and have been downloaded from [free-images.com](https://free-images.com). For the first two, the originals are in 4K (or close) resolution and JPEG format. I loaded them in GIMP, downscaled them to full HD and saved them using lossless PNG. I kept the red panda image at the original resolution to test high quality JPEG XL and AVIF encoding. The fireman wedding image was encoded in lossless PNG from the SVG at 1500x1380. The final image, plot, was directly produced by matplotlib with a high resolution, which I kept, in lossless PNG.

All the images used in this post (source `.png`, encoded `.jxl` and `.avif`) are available in [this repository](https://codeberg.org/langurmonkey/jpegxl-avif-comparison) for you to inspect. 

In this post we use upscaled crops of the images. The percentage by which they are upscaled is mentioned when they appear. The cropped versions themselves are, unless stated otherwise, encoded in JPEG with a 100% quality setting.

## Lossy compression

In this section we analyze how well JXL and AVIF compress images, in relation to file size and visual quality compared to the PNG original inputs. 

In order to encode the **JXL** versions, I have used the `cjxl` provided with `libjxl`. In general, I have not used options other than the quality. For instance, all JXL images use effort 7, which is the default. Increasing the effort setting would surely improve results at the expense of speed for the JXL encoder, but would add an extra dimensionality to the analysis, which I intend to keep as simple and default as possible. This is an *unscientific* first look, after all.

```bash
cjxl input.png output.jxl -q 60 --num_threads=4
```

Playing around with the quality setting (`-q`) produces larger, higher quality images for higher quality settings, and smaller, lower quality ones for lower quality settings. The `-q` goes from 0 to 100.

To encode the **AVIF** images I used `avifenc` provided by `libavif`, the reference AVIF open-source implementation. Here, I have used the following command line arguments:

```bash
avifenc -j 4 --min 0 --max 63 -a end-usage=q -a cq-level=12 input.png output.avif
```

The `--min` and `--max` set the minimum and maximum quantizer for color. We use the full range here. When paired with `-a end-usage=q`, the encoder uses the rate control mode to constant quality, given by `cq-level`. So, setting `cq-level`, in 0-63, we adjust the quality for the color channels. Playing around with this quality, we can get images which are the same size as their JXL counterparts, for comparison.

Additionally, this analysis is purely subjective. I encode the images and then look at them, trying to compare them to the original PNGs. I could have used a formal comparison measure, like the [structural similarity](https://wikiless.northboot.xyz/wiki/Structural_similarity) (SSMI), but my understanding is that this is purely based on the image levels and disregards perceptual factors, which are very important in compression. A good overview on image quality assessment is provided by Wang et al.[^5] in their 2004 IEEE Image Processing paper. A Python utility which takes in two images and outputs the SSIM and the MSE (mean squared error) is included in the repository of this post (`compare.py`, [here](https://codeberg.org/langurmonkey/jpegxl-avif-comparison/src/branch/main/compare.py)). Whenever I can't visually find substantial perceptual differences in the image files, I'll be resorting back to SSIM and MSE.

{{< notice "Note" >}}
It would have been easier to use `libvips`, which offers a unified interface for JXL and AVIF encoding with `vips jxlsave -Q QUALITY` and `vips heifsave -Q QUALITY`, but I wanted to eliminate any hiccups or additional hidden processing introduced by vips itself, and thus went to the 'official' encoders directly.
{{</ notice >}}

### Flag

For the flag image I have used a crop around the small boat in the distance, to the very left of the scene. The crop is upscaled by 200%. Here are the results.

<center>

| Image (200% crop) | Description  | 
|-------|-------|
| <img src="/img/2023/02/jxl-avif/crop-lossy/flag-png.jpg" loading="lazy" /> | Original, 6.9 Mb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/flag-jxl.jpg" loading="lazy" /> | JXL, 146 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/flag-avif.jpg" loading="lazy" /> | AVIF, 146 Kb |

</center>

I used some pretty heavy compression in this one. This means that the quality parameter was rather low. We compressed the image from the original 6.9 Mb to only 146 Kb. Right off the bat, we see that the JXL version is **more true to the original**, being able to retain more of the detail. For instance, the sky looks washed-out in the AVIF version when compared to the JXL, which retains some grain.

Also, I find it very funny that in the AVIF version the mast at the front end of the boat is completely gone, and **a new, non-existing mast has appeared out of nowhere** on top of the bridge! This is not the case in the JXL version, which is able to retain the original mast.

JXL wins this round, as it is able to provide a higher fidelity representation of the original image at the same size.

### BW cityscape

In this case I did not upscale the crops, so they are shown at the original resolution.
Compare cityscape black-and-white image.

<center>

| Image (100% crop) | Description  | 
|-------|-------|
| <img src="/img/2023/02/jxl-avif/crop-lossy/city-png.jpg" loading="lazy" /> | Original, 7.8 Mb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/city-jxl.jpg" loading="lazy" /> | JXL, 224 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/city-avif.jpg" loading="lazy" /> | AVIF, 235 Kb |

</center>

In this case the AVIF version is 11 Kb larger than the JXL version. I couldn't get it at the exact same size as the JXL version, so I erred on the side that favours AVIF. Here the results are closer, but we can see some artifacts on the sky surrounding the pointy structure in the AVIF, which are not present in the JXL. After carefully reviewing several spots I can say that this behaviour is consistent across the whole image. This, coupled with the fact that the AVIF image is larger, also gives the edge to JXL.


### Red panda

I used a `cjxl` quality of 62, producing `redpanda.jxl` at 563 Kb. The `avifenc` uses a `cq-level` of 34, producing a slightly smaller image at 552 Kb. Both versions produce visible artifacts, but I could not decide on a single crop-in to compare, as both did pretty well with this image. Instead, I computed the SSIM and MSE for each image.

- AVIF -- MSE: 35.33327184406321, SSIM: 0.7737482075763144
- JXL -- MSE: 39.86481836605985, SSIM: 0.7504872295500076

In this metric, the AVIF version is 0.02 percent closer to the original lossless image. Practically, this does not translate to a perceptible visual improvement in my opinion. 

## Fireman wedding

I used a quality setting of 50 for the JXL version, producing a file of 78 Kb, and a setting of 44 for the AVIF version, producing a 77 Kb file. This is an interesting one. The AVIF version presents some bad fuzziness in the transitions from the black outlines to the dark blue uniform, but the JXL version contains a weird gradient in the yellow part. The crops are at 200%.

<center>

| Image (200% crop) | Description  | 
|-------|-------|
| <img src="/img/2023/02/jxl-avif/crop-lossy/firemanwedding-png.jpg" loading="lazy" /> | Original, 312 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/firemanwedding-jxl.jpg" loading="lazy" /> | JXL, 78 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/firemanwedding-avif.jpg" loading="lazy" /> | AVIF, 77 Kb |

</center>

Curiously, the structural similarity in this case is a little bit in favour of JXL, when it is supposed to be worse than AVIF for illustrations. This only goes to show that the SSIM index is not very reliable for these kinds of comparisons.

- JXL -- MSE: 18.794290338164252, SSIM: 0.9873632725975594
- AVIF -- MSE: 11.44317922705314, SSIM: 0.9813691392049559

### Plot

This is a very simple image. I used a 500% upscale crop around a specific site which has a little hole at the top left. This hole is retained in both versions (see white pixels to the top-left).

<center>

| Image (500% crop) | Description  | 
|-------|-------|
| <img src="/img/2023/02/jxl-avif/crop-lossy/plot-png.jpg" loading="lazy" /> | Original, 399 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/plot-jxl.jpg" loading="lazy" /> | JXL, 173 Kb |
| <img src="/img/2023/02/jxl-avif/crop-lossy/plot-avif.jpg" loading="lazy" /> | AVIF, 176 Kb |

</center>

Again, the AVIF version is a bit larger. Achieving a good compression ratio is much harder with this image. In general, both the AVIF and JXL present very few artifacts. I would say that the color artifacts in AVIF are a bit worse, but this is kind of subjective. I think this is a draw.

## Lossless compression

Finally, I also took a look at lossless compression to evaluate the differences in file size when encoding mathematically identical images without any information loss.

<center>

| Image | Original | JXL     | AVIF     |
|-------|----------|---------|----------|
| Flag  | 6.9 Mb   | 2.0 Mb  | 2.7 Mb   |
| BW cityscape  | 7.8 Mb   | 1.2 Mb  | 4.3 Mb   |
| Red panda  | 23 Mb   | 15 Mb  | 14 Mb   |
| Fireman wedding  | 312 Kb   | 145 Kb  | 270 Kb   |
| Plot  | 399 Kb   | 113 Kb  | 853 Kb   |

</center>

As you can see, there is no contest. JXL wins every time but one, with some abysmal results, like the BW cityscape, where the lossless JXL image is four times smaller than its AVIF counterpart. Interestingly, the lossless AVIF is twice the size of the original PNG. I'm not sure what the deal with this is, but it is for sure bad. It may be obvious, but let's state it: **If I had to store lots of lossless images I would definitely go for JXL**.

## Encoding speed

What about encoding speed? Well, I did not capture that data (reasons later), but my totally subjective and unscientific impression is that, again JXL has the edge here as well. However, there are many parameters that affect encoding speed, like effort, multithreading, etc., and they are different for the different encoders. So finding a common comparison ground is not always easy. This is a multi-dimensional problem which requires a careful analysis and probably lots of time, so I'll leave it for another post. Cloudinary and Google both run similar tests concerning encoding speed ([here](https://cloudinary.com/blog/contemplating-codec-comparisons) and [here](https://storage.googleapis.com/avif-comparison/index.html) respectively), and they came up with contradicting results, so the battle's still on.

## Conclusion

According to the results presented above, my subjective opinion is that JXL is the superior format for both lossy and lossless operations. It is indeed very hard to visually compare image formats by just compressing a bunch of images and looking at them, so we can also compare them by the features they offer. In this aspect, JXL is the clear winner. Let's see: 

- Max image size is limited to 4K (3840x2160) in AVIF, which is a deal breaker to me. You can tile images, but seams are visible at the edges, which makes this unusable. JPEG XL supports image sizes of up to 1,073,741,823x1,073,741,824. You won't run out of image space anytime soon.
- JXL offers lossless recompression of JPEG images. This is important for compatibility, as you can re-encode JPEG images into JXL for a 30% reduction in file size for free. AVIF has no such feature.
- JXL has a maximum of 32 bits per channel. AVIF supports up to 10.
- JXL is more resilient to generation loss.[^4]
- JXL supports progressive decoding, which is essential for web delivery, IMO. AVIF has no such feature.
- AVIF is notoriously based on the AV1 video encoder. That makes it far superior for animated image sequences, outperforming JXL in this department by a wide margin. However, JXL also supports this feature.
- AVIF is supported in most major browsers. This includes Chrome (and derivatives) and Firefox (and forks). JXL is supported by almost nobody right now. Only **Thorium**, **Pale Moon**, **LibreWolf**, **Waterfox**, **Basilisk** and **Firefox Nightly** incorporate it. Most of these are community-maintained forks of Firefox. That is a big downside for adoption, as I already ranted about in [this post](/blog/2022/jpeg-xl-chrome).
- Both formats support transparency and wide gamut (HDR).


If I had to choose a format to re-encode all of my photos, I would for sure choose JXL. My image viewers of choice support it (Gnome image viewer, nsxiv, feh) and my image processors of choice support it (GIMP, DarkTable). As seen, it provides better image quality and better compression ratios than AVIF, more features and is generally faster. That said, I don't think AVIF is completely useless. It is a better option to replace animated GIFs than JXL, and it is quite good at very lossy compressions targeting the smallest file sizes possible, which makes it a good contender for web delivery.

[^1]: https://eng.aurelienpierre.com/2021/10/webp-is-so-great-except-its-not/
[^2]: https://siipo.la/blog/is-webp-really-better-than-jpeg
[^3]: https://afosto.com/blog/avif-vs-webp-format/
[^4]: https://youtu.be/qc2DvJpXh-A
[^5]: https://ieeexplore.ieee.org/document/1284395
[^6]: https://siipo.la/blog/whats-the-best-lossless-image-format-comparing-png-webp-avif-and-jpeg-xl
