+++
author = "Toni Sagrista Selles"
categories = ["open-source"]
tags = ["chromium", "chrome", "google", "programming", "open-source", "english"]
date = 2022-12-14
title = "Google kills JPEG XL"
description = "Why Google controlling Chrome/Blink development is bad for everyone"
featuredpath = "date"
type = "post"
+++

The web is currently based around the JPEG, PNG and GIF image formats. These are all very old and suboptimal formats which were never designed in the first place with the modern web in mind. A few newer competing formats have popped up recently, aiming to dethrone the original trio to postulate themselves as the standard web image format of the future. These are, essentially, **WebP** (`.webp` extension), developed by Google and hated by almost everyone else, **AVIF** (`.avif` extension), based on the AV1 container and developed by the 'Alliance for Open Media', a conglomerate of big tech companies that are anything but open, and **JPEG XL** (`.jxl` extension), developed by the Joint Photographic Experts Group, the same people that developed the original JPEG.

So what's the fuss all about? Recently, Google decided to kill JPEG XL support in Chrome. A full report follows.

<!--more-->

It is clear that whatever format succeeds in positioning itself as the new de-facto standard must be supported by the major web browsers, and whether we like it or not, [Google Chrome and its derivatives represent an overwhelming majority of the market share](https://en.wikipedia.org/wiki/Usage_share_of_web_browsers). The web is an essential part of the image sharing process, and an unsupported format won't ever be able to take off.

If we strictly go by each format's merits, it is quite apparent that JPEG XL comes out on top. WebP is not even a contender, as it offers, quite frankly, [shitty image quality](https://eng.aurelienpierre.com/2021/10/webp-is-so-great-except-its-not/) and sub-par compression ratios. Between AVIF and JPEG XL, the latter is faster at encoding and decoding, more parallelizable, offers better lossy compression ratios in most real-world use cases, and has more features. 

Quoting a [cloudinary user](https://bugs.chromium.org/p/chromium/issues/detail?id=1178058#c56),

> Overall, JPEG XL achieves better lossy compression (quality vs filesize) than existing browser-supported formats (JPEG, JPEG 2000, WebP and AVIF). In particular for photographic images featuring nature, humans, clothes (which includes image content relevant for many web use cases), the gap between JPEG XL and the next-best available codec (typically AVIF) tends to be very significant. Overall, I estimate JPEG XL to be about 17% smaller than AVIF for the same visual quality, which is about the same gap as between AVIF and WebP and as the gap between WebP and (moz)JPEG. For some specific types of images like lossy non-photographic images, AVIF does perform better than JPEG XL, but on many types of photographic images, JPEG XL outperforms AVIF by over 20%.

Well, Blink, Chrome's rendering engine, added JPEG XL decoding via a flag in early 2021 (as [reported in this issue](https://bugs.chromium.org/p/chromium/issues/detail?id=1178058)). However, after gathering the support and endorsements from various major players in the tech world (Facebook, Adobe, Intel, etc.), Google decided to just drop this support for obviously bullshit reasons and just remove the JPEG XL code and flag from Chromium with [this meager response](https://bugs.chromium.org/p/chromium/issues/detail?id=1178058#c84):

> Thank you everyone for your comments and feedback regarding JPEG XL. We will be removing the JPEG XL code and flag from Chromium for the following reasons:
> 
> - Experimental flags and code should not remain indefinitely
> - There is not enough interest from the entire ecosystem to continue experimenting with JPEG XL
> - The new image format does not bring sufficient incremental benefits over existing formats to warrant enabling it by default 
> - By removing the flag and the code in M110, it reduces the maintenance burden and allows us to focus on improving existing formats in Chrome


Exqueeze-me, what? If you want to kill JPEG XL in favour of your inferior WebP or AVIF formats, at least be honest about the reasons. Offering some half-assed and patently and factually incorrect statements as your reasons does not help your case, as promptly pointed out by hundreds of comments in the issue thread.

The takeaway here is that we should never trust Google, or any other centralized, opaque and essentially evil organization with such a fundamental and important part of today's internet such as Chrome. They will ruin it. They have shown repeatedly that they will put their interests and their organization's over the interests of their users any day. Everyone can see that removing JPEG XL from Chrome is a bad call, which essentially kills the superior format in favor of their own backed projects.

We can only hope that they reconsider their decision and restore JPEG XL support in Chrome ASAP. I would not hold my breath though...
