+++
author = "Toni Sagristà Sellés"
title = "From SteamVR to OpenXR"
description = "The tale of Gaia Sky's migration from one API to the other"
date = "2023-05-09"
linktitle = ""
featured = ""
featuredpath = ""
featuredalt = ""
categories = ["Programming"]
tags = ["graphics", "linux", "vr", "virtualreality", "openxr", "steamvr", "english"]
type = "post"
draft = true
+++

[Gaia Sky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky) has been using the [OpenVR API](https://github.com/ValveSoftware/openvr) from SteamVR for the last few years to power its Virtual Reality mode. However, the API is notoriously poorly documented, and it only works with the SteamVR runtime.[^1] That leaves out most of the existing VR headsets. Luckily, the main vendors and the community at large joined efforts to come up with an API that would be adopted by all and backed by the Khronos Group: [OpenXR](https://www.khronos.org/openxr/). Obviously, since Gaia Sky is actively maintained, it is only natural that a migration to the newer and widely supported API would happen sooner or later. But such a migration is not for free. Both APIs are wildly different, with OpenXR being much more verbose and explicit. This post explores, at a technical level, the migration from OpenVR to OpenXR.

[^1]: actually, it is possible to use a translation layer like [OpenComposite](https://gitlab.com/znixian/OpenOVR), which translates calls from OpenVR to a modern API like OpenXR.
