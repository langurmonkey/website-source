+++
author = "Toni Sagristà Sellés"
title = "Libvips is a good image processor"
description = "Libvips' resource usage and speed are unmatched, especially compared to ImageMagick."
date = "2023-01-22"
linktitle = ""
featured = ""
featuredpath = ""
featuredalt = ""
categories = ["Programming"]
tags = ["graphics", "linux", "commandline", "cli", "image", "english"]
type = "post"
+++

{{< sp orange >}}Edit (2023-04-05):{{</ sp >}} Added some suggestions by the author/developer of libvips.


Today I discovered [libvips](https://libvips.org), a command line utility and library to manipulate and process images, and I am impressed. I've been using ImageMagick and its fork, GraphicsMagick, for as long as I have had to process images from the CLI, and they work well for moderately-sized images. But lately, I have been preparing [virtual texture datasets](/blog/2023/sparse-virtual-textures) for Gaia Sky and the sizes of my images have increased exponentially. Right now I'm processing 64K and 128K images on the regular (that is 131072x65536 pixels), and ImageMagick just can't do it reliably. It uses so much memory that it can't even split a 64K image in a 32 GB RAM machine without running out of it. Running it with the suggested options to limit memory usage (`--limit memory xx mb`, etc.) and use a disk cache never works for me. It just produces blank images for some reason. So after implementing a couple of Python scripts based on OpenCV and NumPy to do some basic cropping, I took on the task of finding a proper, capable replacement. And found it I did. Libvips is the perfect tool, it seems. Based on my few first tests, it performs much better than ImageMagick and GraphicsMagick. It is super fast and never seems to use much memory, no matter how big an image I throw at it.

Here are a few handy commands to do some basic tasks with the command line tool.

Use the `resize` operation to scale images up and down:

```bash
# Resize the INPUT image using the double scale value and save it to OUTPUT
vips resize INPUT OUTPUT scale
```

However, resizing using the `thumbnail` operation can be quicker, as it uses shrink-on-load tricks:

```bash
# Resize the INPUT image to the given WIDTH, aspect ratio is kept
vips thumbnail INPUT OUTPUT WIDTH
```

Converting formats is easy with the `copy` operation:

```bash
# Simple format conversion
vips copy image.png image.jpg

# Attributes can be added to load and save operations
vips copy image.png image.jpg[Q=85]
```

You can also use the dedicated save operations for each format:

```bash
# Convert to JPEG XL
vips jxlsave image.jpg image.jxl

# Convert to PNG
vips pngsave image.jpg image.png

# Convert to JPEG
vips jpegsave image.png image.jpg

# Convert to TIFF
vips tiffsave image.jpg image.tiff

# Convert to WebP
vips webpsave image.jpg image.webp

# Convert to GIF
vips gifsave image.jpg image.gif

# Convert to FITS
vips fitssave image.jpg image.fits
```

Extract an area (crop):

```bash
# Crop an area of width x height starting at pixel [left, top]
vips crop INPUT OUTPUT left top width height
```

In general, you can discover all the subcommands by doing:

```bash
vips -l
```

This outputs a list of all subcommands, which you can parse. Then, just do `vips command` to get help as to how to use a particular command.

The official documentation for the libvips command line interface is [here](https://www.libvips.org/API/current/using-cli.html).


