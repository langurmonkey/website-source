+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "simulation", "astronomy", "astrophysics", "gaia", "opengl" ]
date = "2016-09-14"
description = "Gaia Sky hits version 1.0.0"
linktitle = ""
title = "First version of Gaia Sky released in conjunction with Gaia DR1"
featured = "version1.jpg"
featuredalt = "Gaia Sky version 1.0.0"
featuredpath = "date"
type = "post"
+++

Last September 14 the first [Gaia](http://sci.esa.int/gaia/) catalog, Gaia Data Release 1, was made public. To celebrate the occasion, we also released **version 1.0.0** of our virtual Universe software, [Gaia Sky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky). This time around, the software comes with big improvements and lots of new features, the most prominent of which is the addition of the [TGAS catalog](http://www.cosmos.esa.int/web/gaia/iow_20150115), a part of Gaia DR1 which contains 3D positions for approximately 2 million objects. Check out the release trailer.

{{< youtube LcHgvjx4nuA >}}

Here is the changelog. As always, for a full list of changes see [here](https://github.com/ari-zah/gaiasandbox/blob/master/CHANGELOG.md).

-  TGAS is now the default catalog. HYG can still be selected from the data tab in the config dialog
-  We can now also lock the orientation of the camera to that of the focus
-  Added new options to control star appearance (point size, minimum opacity, etc.)
-  Added sliders to control draw distance in Level-of-detail catalogues such as TGAS.
-  Added new Planetarium mode
-  Added new red-cyan anaglyphic 3D mode
-  Added distortion in VR-headset 3D mode
-  Lots of bug fixes and adjustments

You can download the Linux (`deb`, `rpm`, installer, `aur`), Windows (32 and 64 bit version) or MacOS X versions [here](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky/downloads/).
