+++
author = "Toni Sagrista Selles"
categories = ["Particle Physics Simulator"]
tags = [ "android", "programming"]
date = "2011-10-05"
description = "Version 2.6 is now out"
linktitle = ""
title = "Released version 2.6 of Particle Physics Simulator for Android"
type = "post"
+++

The new version of the [Particle Physics Simulator](https://play.google.com/store/apps/details?id=com.tss.android) for Android is now out in the Market. The main new feature is the addition of *background images* to the simulations. Here's how they work:

First, go to Settings and scroll down to the Background Image entry. Then, click on it and select the image you desire from your gallery/external storage. And yup, that's all!
The images are conveniently cropped and scaled so that *OpenGL ES* can handle them. OpenGL ES only accepts square textures whose side length is a power of two, so what the app does is basically calculate the largest square-of-two-sided area that fits in the selected image and then crops it.

<!--more-->

You'll notice a new folder in the root of your SD card named com.tss.android/. It contains the cropped image currently selected as background. You can delete it but then your background will be gone in the application.

**Whats next in v3.0**: Particle-Mesh force calculator method! Now the simulation uses the direct method, which is physically accurate but kind of slow. The new release will include the possibility to change the method to Particle-Mesh, which does not have particle-particle interactions but is much faster and can accommodate a larger number of particles.
