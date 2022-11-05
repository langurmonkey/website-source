+++
author = "Toni Sagrista Selles"
categories = ["Photography"]
tags = ["pixelfed", "fediverse", "mastodon", "pleroma", "federation", "photo", "english"]
date = 2022-11-05
linktitle = ""
title = "Pixelfed"
description = "The photo sharing project of the fediverse"
featuredpath = "date"
type = "post"
+++

Yesterday I created [an account](https://pixelfed.social/jumpinglangur) in [pixelfed.social](https://pixelfed.social), one of the many instances of [Pixelfed](https://github.com/pixelfed), the distributed image sharing open source project which federates with Mastodon and others. Anyone can set up its own instance and have it 'talk' to all the others. So, I created an account and started sharing some of my shots. For the most part, it works very well and I'm eternally grateful that something like this exists, free from the claws of big corporations hungry for your data.

<!--more-->

In the future, Pixelfed may just replace my [statically generated photo gallery](/blog/2021/static-photo-gallery/). Currently I'm hosting the full-resolution pictures in my institute's web server, but that is just a temporary solution. The only little issue that keeps me back is the treatment of EXIF metadata done by Pixelfed. It is actually very simple, they just remove all of it. This may make sense for other non-photography centered services such as Mastodon or Pleroma, or even for pictures captured and shared directly from cellphones. But for cameras with respectable sensor sizes and lenses, they should be kept. You see, more often than not the EXIF metadata contains important information such as the license, the copyright and the author's name. Without forgetting about all the technical information that is lost, such as camera model, shutter speed, focal length, aperture and so on.

But there is hope. It seems that the discussion ongoing [in this issue](https://github.com/pixelfed/ideas/issues/3), with some users advocating for keeping the EXIF, or at least offering an option for doing. The discussion looks quite dead though, with the last response being from mid-2019.
