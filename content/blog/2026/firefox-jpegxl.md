+++
author = "Toni Sagrista Selles"
categories = ["JPEG XL"]
tags = ["firefox", "jpeg xl", "jxl", "avif", "webp", "jpeg", "png", "programming", "open-source", "image", "formats", "english"]
date = 2026-06-17
linktitle = ""
title = "JPEG XL lands in Firefox"
description = "Version 152 of the popular browser includes an option to enable JXL in Labs"
featuredpath = "date"
type = "post"
+++

Yesterday, Firefox 152 was released. In the [release notes](https://www.firefox.com/en-US/firefox/152.0/releasenotes/), under the Firefox Labs section, it states:

{{< fig src1="/img/2026/06/jpegxl-firefox-labs.jxl" type1="image/jxl" src="/img/2026/06/jpegxl-firefox-labs.jpg" class="fig-center" width="100%" loading="lazy" caption="The Firefox Labs section of the release notes of Firefox 152. If you see <span style='font-weight: 800;color:yellow'>JPEG-XL works!</span>, it means your browser is JPEG-XL capable. If you see <span style='font-weight: 800;color:red'>JPG :(</span>, it means your browser does not support it." >}}

<!--more-->

> Firefox now offers experimental support for the new JPEG XL image format, which generally provides better compression than WebP, JPEG, PNG, and GIF and is designed to supersede them. You can enable it from the Firefox Labs panel in Settings. 


Finally! I have written about this image format [here](/blog/2022/jpeg-xl-chrome), [here](/blog/2023/jpegxl-vs-avif), and [here](/blog/2025/google-unkills-jpegxl). The latter entry is particularly important because Google set the ball rolling by announcing that they would look into adding a memory-safe JPEG XL decoder into Chromium. It was only a matter of time before the other browsers would follow suit.

I have not had the chance to test this myself, as at the time of writing, `firefox-152` has not yet landed on the Arch repositories. However, it won't be long. I'm just happy that it is finally happening. That's all.

{{< sp orange >}}Edit (2026-06-17 09:26 UTC):{{</ sp >}} Well, a little over an hour after I wrote the post, and version 152 is live on the Arch extra repository. I tested it quickly and it seems to work. The [JPEG XL test page](https://jpegxl.info/resources/jpeg-xl-test-page.html) indicates that alpha transparency and animation work. I can't test the wide gamut feature as I don't have a P3 display.
