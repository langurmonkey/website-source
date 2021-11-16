+++
author = "Toni Sagrista Selles"
categories = ["Photography"]
tags = ["gear", "photo", "lens", "english"]
date = 2021-11-16
linktitle = ""
title = "Viltrox EF FX1 lens adapter review"
description = "Does this adapter work well? Is auto focus usable? Is it worth it?"
featuredpath = "date"
type = "post"
+++

A few days ago [I got my new camera](/blog/2021/fuji-x-s10-first-impressions), a brand new Fujifilm X-S10. Since I'm coming from the [Canon ecosystem](/photography) I have a few EF and EF-S lenses which I like. In order to use them with my new system I also acquired the auto focus lens mount adapter Viltrox EF-FX1, which allows EF/EF-S Canon lenses to be used with Fuji-X mount mirrorless cameras. This is an adapter with electronics, so it enables not only auto focus but also aperture control. But does it really work? Is it useful? And more importantly, is it worth the asking price of 120€? In this post I document my experience after some tests.

<!--more-->

## Lenses and body

These are the lenses and the camera body I have tested the adapter with.

- **Body**: Fujifilm X-S10

- **Lenses**:
    - Canon EF 28-105mm f/3.5-4.5 USM II
    - Canon EF 50mm f/1.8 II
    - Sigma 10-20mm f/4-5.6 EX DC HSM

Officially, the Fuji X-S10 is **not supported**, and **nor is the Canon 28-105mm**, so take this review with a grain of salt. Both the Canon 50mm and the Sigma 10-20mm are supported, though.

{{< fig src="/img/2021/11/viltrox-ef-fx1-compat.jpg" title="Lens compatibility list for the Viltrox EF-FX1 adapter." width="50%" class="fig-center" loading="lazy" >}}

## Build quality

The adapter is very well built. It feels durable and sturdy and it fits into the X mount perfectly. Canon lenses attach to the other end equally as fine. There is absolutely no wobbling once both the adapter and the lens have 'clicked'. It is made of metal with surface plating treatment and has a Micro-USB port to upgrade the firmware. It supports auto focus, aperture adjustment from the camera and EXIF data transmission.

{{< fig src="/photo-gallery/media/small/gear/viltrox-ef-fx1-side.jpg" link="http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/gear/viltrox-ef-fx1-side.jpg" title="Side view of the adapter. It does not look bad, does it?" width="50%" class="fig-center" loading="lazy" >}}

## The firmware problem

The first thing I did after receiving the adapter was test it quickly. It looked like it worked more or less fine with the Canon 50mm and the Sigma, but not so much with the 28-105. So I updated its firmware to the latest version at the time, `2.29`, just in case things improved. I was not expecting it, but they did not, they actually got worse. Now, with a fully updated firmware, the 28-105 was faring much better, but the others could hardly even get focus.

So obviously I had no alternative but to go on a quest to capture the old firmware versions. Maybe one of them would work *fine* with my body and lenses. I started by the [official website](http://viltrox.com) (on a side note, how is a website serving firmware files not using HTTPS in 2021?), but it wasn't gonna be that easy. The web only offers the latest versions. So I sent them an email asking for old versions for testing purposes, but they ignored me. Then I found a reddit comment thread where someone mentioned being able to get past firmware versions for the EF-FX1 from the manufacturer, so I contacted him and he was kind enough to send me a *zip* file with some firmware files.

## Flashing firmwares like there's no tomorrow

Then I set up a table to methodically test and document my findings. I would rate the performance of each lens with each firmware version using a scale from 1 to 5:

- **1** --- Not working, can't auto focus at all.
- **2** --- Auto focus barely works, it hunts a lot.
- **3** --- Almost usable. Focus still hunts, but it lands some good ones from time to time.
- **4** --- Quite usable. It takes a bit more to focus than with native hardware, but it works.
- **5** --- Performance is like native.

Here is the table.

| Firmware version     | Canon 50mm     | Canon 28-105mm     | Sigma 10-20mm       |
|    :----:            |     :----:     |     :----:         |     :----:          |
| `2.29`               | 2              | 3.8                | 1                   |
| `2.28`               | 4.5            | {{< sp red >}}"turn off" ERR{{</ sp >}}     | {{< sp red >}}black screen ERR{{</ sp >}}    |
| `2.26`               | 4.5            | {{< sp red >}}"turn off" ERR{{</ sp >}}     | 4.1    |
| `2.23`               | 4.5            | 4.5                | {{< sp red >}}"turn off" ERR{{</ sp >}}                   |
| `2.21`               | {{< sp red >}}"turn off" ERR{{</ sp >}}              | 4.1                | {{< sp red >}}"turn off" ERR{{</ sp >}}                   |
| `2.18`               | 4.5/{{< sp red >}}"turn off" ERR{{</ sp >}}              | 4.5               | 4.5/{{< sp red >}}"turn off" ERR{{</ sp >}}                   |
| `2.14`               | 3.5              | 4               | 4/{{< sp red >}}"turn off" ERR{{</ sp >}}                   |

I was perplexed. Results are vastly different depending on the firmware version. One would think of firmware as something incremental where each new version builds on and refines what was already there in previous versions. This does not seem to be the case here, as errors come and go, and autofocus performance changes run wild.

{{< fig src="/photo-gallery/media/small/gear/viltrox-ef-fx1-canon-50mm.jpg" link="http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/gear/viltrox-ef-fx1-canon-50mm.jpg" title="The Viltrox EF-FX1 attached to the Canon 50mm f/1.8 II." width="30%" class="fig-center" loading="lazy" >}}

I encountered two types of error. In the first, which I call {{< sp red >}}"turn off" error{{</ sp >}}, the camera displays a notice that reads "TURN OFF THE CAMERA AND TURN ON AGAIN", after a while. It does not happen when the camera is switched on, but rather at random when focusing. It happens more often with some versions than others too. Turning of the camera and on again seems to do the trick in this case.
The second error, {{< sp red >}}black screen ERR{{</ sp >}}, is a show stopper. The camera screen is frozen and all operation ceases. I couldn't even turn it off with the switch button, so I had to take out the battery pack and put it back in again. Fortunately this only happened with firmware `2.28`.

{{< fig src="/img/2021/11/viltrox-error_s.jpg" link="/img/2021/11/viltrox-error.jpg" title="The 'turn off' erro in the table looks like this." width="60%" class="fig-center" loading="lazy" >}}

As you can see in the table, I had to go pretty deep, all the way down to `2.14`, to find something minimally usable. This version works respectably with both Canons, and shows the "turn off" error some times with the Sigma. It works though.

## Wrap-up

I'm keeping the adapter. It might seem shocking, but It works well enough for me to justify its asking price. Also, I think a lot of the errors in my tests are due to the X-S10 being unsupported, as it's a relatively new body. Hopefully support will come in time via firmware updates, and life will be good again. I'll make sure to publish and update if this happens.

{{< fig src="/photo-gallery/media/small/gear/viltrox-ef-fx1-standing.jpg" link="http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/gear/viltrox-ef-fx1-standing.jpg" title="The Viltrox EF-FX1 standing on the tripod mount. Note the Micro-USB port in the inner ring." width="50%" class="fig-center" loading="lazy" >}}
