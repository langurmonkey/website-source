+++
author = "Toni Sagrista Selles"
categories = ["JPEG XL"]
tags = ["chrome", "jpeg xl", "jxl", "avif", "webp", "jpeg", "png", "programming", "open-source", "image", "formats", "english"]
date = 2026-10-07
linktitle = ""
title = "JPEG XL finally lands in Chrome!"
description = "Version 155 of the popular web browser will ship with a JPEG XL decoder"
featuredpath = "date"
type = "post"
js = ["/js/mathjax3.js"]
+++

Today, I was browsing [Hacker News](https://news.ycombinator.com), when a particular item caught my eye:

{{< fig src="/img/2026/10/hn-jpegxl-chrome.jpg" class="fig-center" width="50%" loading="lazy" caption="Hacker News post with the [Chrome JPEG XL announcement](https://developer.chrome.com/blog/jpeg-xl-in-chrome)." >}}

I opened it promptly and, indeed, it was not a prank. Finally, after [years](/blog/2022/jpeg-xl-chrome) and [years](/blog/2023/jpegxl-vs-avif) of bull**** from the Chrome team, they are shipping it. They are shipping a JPEG XL decoder.

{{< notice "JPEG XL in a nutshell" >}}
For those of you who don't know, JPEG XL is a new image codec that includes most of, if not all, the features we'd want in the image codec of the future:

- File size reduction by \\(~20-60\\%\\) w.r.t JPEG.
- Lossless JPEG transcoding.
- Progressive decoding.
- Wide gamut, HDR and 32-bit support.
- Animations and transparency (alpha channel).
- Shines with high-fidelity photographic images.
- Fast-ish encoding and decoding.
- Royalty-free and FOSS.
- Support for super high-resolution images, of up to 1 terapixels ( \\(2^{30}-1\\) pixels per side).
{{</ notice >}}

<!--more-->

This is awesome news *for the codec*. Whether we like it or not, Chrome is the dominant web browser, with ~66.5% of the [market share](https://gs.statcounter.com/browser-market-share/), very far from its competitors (Safari, Edge, and Firefox, in that order).

<div id="all-browser-ww-monthly-202509-202609" class="div-center" width="600" height="400" style="width:600px; height: 400px; margin: auto;"></div><!-- You may change the values of width and height above to resize the chart --><figcaption>Source: <a href="https://gs.statcounter.com/browser-market-share/">StatCounter Global Stats - Browser Market Share</a></figcaption><script type="text/javascript" src="https://www.statcounter.com/js/fusioncharts.js"></script><script type="text/javascript" src="https://gs.statcounter.com/chart.php?all-browser-ww-monthly-202509-202609&chartWidth=600"></script>

Now, I don't use Chrome at all, but I still think that this was just the final piece of the puzzle needed to help the format go mainstream.

So, what finally pushed them over the edge? If you read [their announcement](https://developer.chrome.com/blog/jpeg-xl-in-chrome), they cite "consistent feedback and requests from web developers" and its massive popularity in the Interop 2026 project. Translated from corporate PR-speak: the community simply refused to let it go. Web developers, photographers, and open-source advocates kept pushing, complaining on bug trackers, and demanding a truly superior image format instead of settling for Google's own WebP or the heavily pushed AVIF. 

The technical excuse the Chrome team used for years was that a C++ decoder was too much of an attack surface to run safely in the browser. Well, it has now been elegantly sidestepped. To bring JPEG XL to Chrome 155, they have integrated `jxl-rs`, a pure Rust reimplementation of the decoder. This tackles the memory safety issues head-on, eliminating the risk of out-of-bounds reads and use-after-free bugs of other decoders. And to make sure it doesn't run sluggishly, they built a SIMD abstraction layer (`jxl_simd`) to maximize hardware performance without compromising Rust's safety guarantees.

This is a massive victory. Not just for JPEG XL, but for the open web. 

As I demonstrated in my [comparison back in 2023](/blog/2023/jpegxl-vs-avif),JXL has significant advantages over older formats and, in many cases, over AVIF as well, especially for high-fidelity photography, lossless compression, and progressive decoding. The fact that it allows lossless transcoding of existing JPEG files is of special importance. It means that we can finally upgrade our backlog of old images without losing a single pixel of quality, while saving a big chunk of disk space and/or bandwidth in the process.

With [Firefox adding it to Labs](/blog/2026/firefox-jpegxl/) earlier this year, and Chrome finally capitulating, Safari is left as the major outlier with only partial support.

{{< notice Notice >}}
Firefox 158 will include the JPEG XL decoder **enabled by default**. See the [beta release notes](https://www.firefox.com/en-US/firefox/158.0beta/releasenotes/).
{{</ notice >}}


The dark days of ["Google kills JPEG XL"](/blog/2022/jpeg-xl-chrome) are officially over. It's time to start converting your image libraries, updating your `<picture>` tags, and serving `.jxl`. The future of (high-quality) web imagery is finally here, and I'll be ready for it.

