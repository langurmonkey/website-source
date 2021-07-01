+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = ["programming", "opengl", "release", "version", "english", "gaia sky"]
date = 2021-06-17
linktitle = ""
title = "What's new in Gaia Sky 3.1"
description = "Short rundown of what's in this major release"
featuredpath = "date"
type = "post"
+++

Over the last two weeks I have released the feature-packed version `3.1.0` of [Gaia Sky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky). Two bugfix releases (`3.1.1` and `3.1.2`) followed shortly to fix bugs and regressions introduced in the former. This post contains a small rundown of the most interesting [features in these three new versions](https://gitlab.com/langurmonkey/gaiasky/-/releases). Let's get started.

<!--more-->

<!-- Loading MathJax -->
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML' async></script>

## Enabling absolute positioning

The first and most important feature is the re-implementation of the core positioning module of Gaia Sky. We have moved the arithmetics to arbitrary-precision floating point numbers. This enables global positioning anywhere in the Universe without loss of precision. This feature has actually been sitting in a branch since before the submission of the paper [Gaia Sky: Navigating the Gaia Catalog](https://ieeexplore.ieee.org/document/8440086), but it never quite made into the main branch due to some minor problems. This is mainly under-the-hood work, invisible to the user. Yet, it enables the eventual addition of extrasolar systems, or the spacecraft to wander off from the Solar System without hacks.

{{< figure src="/img/2021/06/kepler-exoplanets.jpg" link="/img/2021/06/kepler-exoplanets.jpg" title="An exoplanet in Gaia Sky 3.1, orbiting a double system" class="fig-center" width="60%" >}}

### Catastrophic cancellation

So, **what is essentially the problem?** Well, for starters, graphics cards usually work with single and double-precision floating point numbers, with single-precision (32-bit) numbers being generally much more performant. The precision of these numbers (i.e. the number of significant digits in the mantissa or significand) is usually very limited, with around 7 decimal digits (24 bits) for single-precision and some 16 decimal digits (53 bits) for double-precision. This is not nearly enough to position *smallish* objects within a few parsecs (usually much less) without significant precision issues.

Practically, if we just use raw floating point arithmetics, we will run into [catastrophic cancellation](https://en.wikipedia.org/wiki/Catastrophic_cancellation), which is essentially the dramatic relative errors occurring when subtracting two large (in magnitude) and similar limited-precision floating point numbers. In such cases, the result is usually a much smaller number than the operands, but the errors are huge due to the increasingly sparse representativity of floating point. In Gaia Sky we do this all the time to work out the position of an object with respect to our camera.

In the image below, both \\(\vec{C}\\), the position of the camera, and \\(\vec{G}\\), the position of the object (the Gaia satellite in this example), are very far away from the origin of the reference system, which in this case is at the barycenter of the Solar System. The magnitude of \\(\vec{C}\\) and \\(\vec{G}\\) is around 1 AU (for Astronomical Unit, around 1.49E11 meters), since Gaia is only about 300000 km from Earth. Note that Gaia is comparatively very small, with a 'wingspan' of about 10 meters. 

{{< figure src="/img/2021/06/cancellation1.png" link="/img/2021/06/cancellation1.png" title="Catastrophic cancellation. Both the camera and Gaia are far away from the origin of the reference system. In this case, C and G are similar and very large. V=G-C, which leads to catastrophic cancellation." class="fig-center" width="40%" >}}

When trying to work out \\(\vec{V}\\) as \\(\vec{V}=\vec{G} - \vec{C}\\) we encounter this cancellation problem, which manifests as heavy vertex jittering. Pictured below is that jittering, but since the original position at 1 AU completely broke down the rendering, we had to be more conservative and put Gaia at some 1200 kilometers from it.

{{< figure src="/img/2021/06/float_jitter.gif" link="/img/2021/06/float_jitter_origin.mp4" title="Jittering occuring in Gaia when it is positioned only a thousand kilometers from the origin." class="fig-center" >}}

### The solution: floating camera

The solution we have adopted is to use the method known as floating camera. You see, instead of having a fixed position for the reference system origin and moving the objects in the scene around, we always keep the origin at the camera. Practically, we offset the whole scene graph by the inverse of the camera position at every frame.

{{< figure src="/img/2021/06/cancellation2.png" link="/img/2021/06/cancellation2.png" title="The same example as before, but now with a floating camera. Note that the camera is at the origin and Gaia is very close to it." class="fig-center" width="30%" >}}

The trick is to send the transformation matrices to the GPU from the point of view of the camera, being it at the origin. This ensures maximum precision around the area of interest, which is, of course, close to the camera. But still, we need to compute the position of the object with respect to the position of the camera with sufficient accuracy. Doing so using single or double precision numbers in the CPU will just nod to. Instead, our system uses **arbitrary precision** floating point numbers, with a configurable number of significant digits. This allow us to mitigate or eliminate the devastating effects of catastrophic cancellation. Since arbitrary precision floating point operations are typically not hardware-accelerated even in modern CPUs, they are much slower than their native counterparts. Due to that, Gaia Sky only uses them in very few key points in our processing pipeline. For instance, only objects which are close by get this special treatment. Objects which are far away from the camera do not need it and do not get it. This allows us to still provide high frame rates while keeping the global positioning pipeline working.

This very part is exactly what has been enabled in Gaia Sky `3.1.0`.

## Per-object visibility

We have also implemented proper per-object visibility, so that it is now possible to hide individual objects. You can do so by using the dedicated button in the type visibility pane of the control panel, or by using the eye toggle in the focus information panel, to the bottom-right.

## Location log

We have also introduced a location log, which keeps track of the visited locations during a session. This is so far a feature preview containing only a basic implementation. For instance, the log is not persisted between sessions, and location addition is totally automated (no manual 'add' button). This will be built upon in future releases.

{{< figure src="/img/2021/06/location-log.jpg" link="/img/2021/06/location-log.jpg" title="The new location log panel." class="fig-center" >}}

## Bulgarian translation

This version sees the addition of a new language. The Bulgarian translation has been contributed by [Georgi Georgiev](https://gitlab.com/RacerBG), and is pretty much 100% complete.

## Other features

Other (minor) new features are listed below:

- Add apparent magnitude as seen from the camera to focus info interface.
- Improve solar system objects' magnitude computation.
- Condense date/time panel into a single line.
- Improve shader compilation logging.
- UI tweaks.
- Multiple directional lights in `per-pixel-lighting` shader.
- Dynamic resolution flag added to configuration file for testing purposes.
- Improve error dialog with saner defaults.
- Expose RGB color attributes to filters.

## Bug fixes

These releases also contain a lot of bug fixes:

- Update list of JRE modules for appimage.
- Fix untranslatable strings.
- Mmusic module omited if initialization fails.
- Attitude indicator ball UI scaling.
- Free camera stops when very close to stars.
- Particle passing parent translation to children instead of its own.
- Minimap crash due to shader version not found on some macOS systems.
- Free mode coordinate command gets doubles instead of floats.
- Reformulate plx/plx_e > crti.
- Pad catalog num in launch script.
- Fix metadata binary version 1 with long children IDs.
- Keyframes arrow caps, leftover focus when exiting keyframe mode.
- Dataset highlight size factor  limits consolidated across UI and scripting.
- STIL loader fails if stars have no extra attributes.
- Octant ID determination in creator.
- Typo 'camrecorder' to 'camcorder'
