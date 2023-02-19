+++
author = "Toni Sagrista Selles"
categories = ["Image formats"]
tags = ["open source", "image", "visualization", "formats", "english"]
date = 2023-02-19
linktitle = ""
title = "JPEG XL vs AVIF: Fight!"
description = "An unscientific analysis of these two image formats based on file size and image quality."
featuredpath = "date"
type = "post"
+++

JPEG XL and AVIF are arguably the two main contenders in the battle to replace JPEG as the next-generation image format. Others are also well positioned, like HEIC and WebP 2, but the former is subject to licensing patents, and the second is still in development and seems that it [may never see the light of day](https://chromium.googlesource.com/codecs/libwebp2/+/1251ca748c17278961c0d0059b744595b35a4943^%21/) as a fully-featured image format anyway.

In this post, I do a quick comparison of lossless and lossy compression between JPEG XL and AVIF, and evaluate how they fare in terms of file size and visual quality.

<!--more-->

## Methodology

I have selected three different test images that we will run through both the JPEG XL and the AVIF encoders:

- **Flag** --- a sunset with a smooth red-yellow gradient in the sky and a quiet sea with lots of detail. There is a flag in the foreground, which is mostly black due to it being lit from behind.
{{< fig src="/img/2023/02/jxl-avif/flag-s.jpg" class="fig-center" width="50%" title="Flag. Taken from free-images.com, downsampled to full HD and losslessly saved to PNG." loading="lazy" >}}

- **BW cityscape** --- a black-and-white cityscape at night. It has a lot of contrast.
{{< fig src="/img/2023/02/jxl-avif/city-s.jpg" class="fig-center" width="50%" title="BW cityscape. Taken from free-images.com, downsampled to full HD and losslessly saved to PNG." loading="lazy" >}}

- **Plot** --- a simple plot created with matplotlib. Should offer plenty of room for compression.
{{< fig src="/img/2023/02/jxl-avif/plot-s.jpg" class="fig-center" width="50%" title="Plot. Directly produced by matplotlib in lossless PNG at 5760x4320." loading="lazy" >}}

The first two images (flag and cityscape) are in the public domain, CC0, and have been downloaded from [free-images.com](https://free-images.com). The were originally in 4K (or close) resolution and in JPEG. I loaded them in GIMP, downsampled to full HD and saved to lossless PNG. The final image, plot, was directly produced by matplotlib with a high resolution, which I kept, in lossless PNG.

All the images used in this post (source `.png`, encoded `.jxl` and `.avif`) are available in [this repository](https://codeberg.org/langurmonkey/jpegxl-avif-comparison) for you to inspect. 

In this post we use upscaled crops of the images. The percentage by which they are upscaled is mentioned when they appear. The cropped versions themselves are, unless stated otherwise, encoded in JPEG with a 95% quality setting.

## Lossy compression

In this section we analyze how well JXL and AVIF compress images, in relation to file size and visual quality compared to the PNG original inputs. 

In order to encode the **JXL** versions, I have used the `cjxl` provided with `libjxl`. In general, I have not used options other than the quality. For instance, all JXL images use effort 7, which is the default.

```bash
cjxl input.png output.jxl -q 60 --num_threads=-1
```

Playing around with the quality setting (`-q`) produces larger, higher quality images for higher quality settings, and smaller, lower quality ones for lower quality settings. The `-q` goes from 0 to 100.

To encode the **AVIF** images I used `avifenc` provided by `libavif`, the reference AVIF open-source implementation. Here, I have used the following command line arguments:

```bash
avifenc -j 4 --min 0 --max 63 -a end-usage=q -a cq-level=12 input.png output.avif
```

The `--min` and `--max` set the minimum and maximum quantizer for color. We use the full range here. When paired with `-a end-usage=q`, the encoder uses the rate control mode to constant quality, given by `cq-level`. So, adjusting `cq-level`, in 0-63, adjust the quality for the color channels. Playing around with this quality, we can get images which are the same size as their JXL counterparts for comparison.

{{< notice "Note" >}}
It would have been easier to use `libvips`, which offers a unified interface for JXL and AVIF encoding with `vips jxlsave -Q QUALITY` and `vips heifsave -Q QUALITY`, but I wanted to eliminate any hiccups or additional hidden processing introduced by vips itself, and thus went to the 'official' encoders directly.
{{</ notice >}}

### Flag

Compare flag image.

### BW cityscape

Compare cityscape black-and-white image.

### Plot

Compare plot.

## Lossless compression

Compare all in lossless compression.

## Encoding speed



## Conclusion
