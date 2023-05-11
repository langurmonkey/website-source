+++
author = "Toni Sagristà Sellés"
title = "MangoHud and Java"
description = "A little tip to launch Java programs directly from your IDE using MangoHud"
date = "2023-05-11"
linktitle = ""
featured = ""
featuredpath = "date"
featuredalt = ""
categories = ["Linux"]
tags = ["graphics", "linux", "mangohud", "english"]
type = "post"
+++

[MangoHud](https://github.com/flightlessmango/MangoHud) is an overlay for monitoring frame rates, frame times, temperatures and CPU/GPU loads on Vulkan and OpenGL applications in Linux. It is also the default performance overlay used in the Steam Deck, and it is awesome.

I know the amount of people using Java for high performance graphics is not very high, but they are there, of that I'm sure. I'm actually one of them. Gaia Sky is written in Java, and even though it has its own [rudimentary debug overlay](/blog/2021/gaiasky-3-tutorial#debug-panel), MangoHud goesfar beyond it. When I'm not editing in neovim, I use IntelliJ IDEA CE to do a little refactoring and deubgging. It is during these times that being able to run the JVM with MangoHud directly from the IDE comes in handy. But most IDEs do not allow customizing the launch command directly to use the `mangohud /path/to/app` approach, so how do we do it?

It turns out we just need to set one single environment variable to inject the necessary libraries. To that effect, we just need to locate the location of the MangoHud library in our system (`/usr/lib/mangohud` in ArchLinux), and point the variable `$LD_PRELOAD` to the files `libMangoHud.so` and `libMangoHud_dlsym.so`, like so:

```bash
LD_PRELOAD=/usr/lib/mangohud/libMangoHud.so:/usr/lib/mangohud/libMangoHud_dlsym.so
```

You can do that from the run configuration dialog in IDEA or Eclipse. Look for a section or text feield that reads "environment variables".

Here is how to do it in IDEA:


<figure class="fig-center">
<video controls autoplay loop muted width="80%">
  <source src="/img/2023/05/idea-mangohud.mp4" type="video/mp4">
  This browser does not display the video tag.
</video>
<figcaption style="margin: 0 auto; width:60%;">
  <h4>Running Java application with MangoHud in IDEA</h4>
</figcaption>
</figure>
