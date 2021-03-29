+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "simulation", "astronomy", "astrophysics", "gaia", "opengl", "gaia sky" ]
date = "2017-08-02"
description = "Jumbo release 1.5.0 brings lots of new features and improvements"
linktitle = ""
title = "Gaia Sky jumbo summer release 1.5.0"
featured = "gaiasky1.5.0.jpg"
featuredalt = "Gaia Sky v1.5.0"
featuredpath = "date"
type = "post"
+++

This time around we've had a slightly longer development cycle so Gaia Sky `1.5.0`  '*Jumbo Summer Release*' is here with a ton of new features, enhancements and bug fixes. Most importantly, we have essentially **refactored the way star catalogs are handled**, so that we can now stream data from disk when it is needed. Also, we've been working hard to make **better use of the GPU** and we are proud to announce that we've increased the performance fourfold while being able to display many more objects on screen at once.

Here is the list of the most important **enhancements**:

- Implemented **particle groups** and **star groups** to optimize GPU usage
- Added **on-demand streaming** of data for LOD (levels of detail) datasets
- Particle/star groups integration with LOD
- Enabled additive blending by default
- New **parallel view** stereoscopic profile
- **GUI refactoring** to enable proper **HiDPI support**
- GUI animations
- Added **French** and **Slovene** languages
- Proper motion vectors color coded by direction and mangitude
- Debug info greatly improved
- Added **Oort cloud**
- Added **Nearby Galaxies Catalog** (NBG)
- Added some **SDSS** objects
- Added **Saturn moons**
- Added **Pluto**
- Enabled **high accuracy positions** as an option
- Implemented **land on** and **land at coordinates** functions and exposed them in GUI
- New **target mode** In free camera which scales velocity according to distance to closest object
- Implemented **proper controller/gamepad mapping** system
- Added **invert Y axis** option
- Reimplemented **spacecraft camera mode** from the ground up
- Network checker made asynchronous
- Some components' initializations moved to go through the asset manager
- Added **non cinematic camera mode**, which is now the default

And here a list of the most important **closed bugs and issues**:

- Fixed lots of bugs in scripting interface
- Fixed eye separation in spacecraft+stereo mode
- Fixed random crashes at startup
- Scale point primitives by ratio
- Fixed Milky Way texture misalignment
- Fixed controller input in non-cinematic mode
- Fixed quad line renderer artifacts
- Fixed label flickering
- Greatly improved octant detection
- Config file version check

As always, you can **download** Gaia Sky for your operating system (Linux, Windows, macOS) from our [home page](http://www.zah.uni-heidelberg.de/gaia/outreach/gaiasky/downloads).
