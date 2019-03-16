+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "simulation", "astronomy", "astrophysics", "gaia", "opengl" ]
date = "2016-04-28"
description = "New version 0.800b of Gaia Sky out now"
linktitle = ""
title = "Gaia Sky hits version 0.800b"
type = "post"
+++

Today I'm releasing **version 0.800b** of [Gaia Sky](http://ari-zah.github.io/gaiasky), probably the last beta version before version one, which will come in late summer with GDR1 (Gaia data release 1).

This time around we bring on loads of improvements, bug fixes and new features. Here is a comprehensive change log:

-  Reimplemented star render algorithm, now all stars are shaded as points in the GPU.
-  New [Milky Way](http://ari-zah.github.io/gaiasky/images/screenshots/screenshot_00028.jpg) rendering with 40K particles and 100 nebulae.
-  Three graphics quality settings, low, normal and high, which have an impact in the size of textures, the complexity of the models and the quality of the graphical effects.

<!--more-->

-  New embedded music player in the Gaia Sky interface to play your favourite songs when Gaiaing!
-  Improved mouse interactions.
-  Stereoscopic mode effects have been fixed and now work properly in 3D.
-  Improved scripting system.
-  New volumetric light rendering system.
-  Time pace substituted by time warp, which sets the time speed as a function of real time.
-  Added new UI themes. Now HiDPI screens (retina) are supported.
-  Migrated most GUI elements to internal system. Swing is now only used for preferences.
-  FOV mode fixed with correct field of view angles. This corrects stars taking only ~3.2 secs to cross a CCD.
-  Implemented interface to Gaia archive (now using mockup data), Simbad and Wikipedia.
-  Implemented responsive positioning giving `RA/DEC` or `Lat/Lon` of mouse position.
-  Lots of bug fixes and other minor improvements.
-  As usual, check the [full changelog](https://github.com/ari-zah/gaiasandbox/compare/0.707b...0.800b) for more detailed info.

You can get the new version for **Linux**, **Windows** and **OS X** in the official [Gaia Sky page](https://zah.uni-heidelberg.de/gaia/outreach/gaiasandbox/downloads/).
