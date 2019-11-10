+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "programming", "opengl", "release", "version", "english" ]
date = 2019-08-01
description = "Planetary surfaces, keyframed camera, new scripting and more"
linktitle = ""
title = "Gaia Sky 2.2.0"
featuredpath = "date"
type = "post"
+++

<!-- Loading MathJax -->
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML' async></script>

Today we are releasing a brand new version (`2.2.0`) of Gaia Sky with several major changes and new features. To sum up, github reports **1071** changed files, with **81672** additions and **31763** deletions. Gitlab displays a "Too many changes to show" banner, as their cap is at a 1000 files. This makes it by far the largest release ever, followed by version `1.5.0` in the summer of 2017.

<!--more-->

So, what are all these changes? What are the new features? This post attempts to answer this questions in somewhat detail. 

If you are impatient, go ahead and [download Gaia Sky 2.2.0](https://zah.uni-heidelberg.de/institutes/ari/gaia/outreach/gaiasky/downloads/). The program should recognize your data is outdated (if you come from `2.1.7`) and offer an update. Otherwise, you can just go ahead and remove the data folder altogether and redownload everything again.

## Teaser trailer


<video width="60%" style="display: block; margin: auto;" controls>
  <source src="/img/2019/08/teaser-20200.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

<p style="text-align: center;" class="caption">Teaser trailer (<a href="https://www.youtube.com/watch?v=2faYAuKQ1cE">YouTube link</a>)</p>


## Planetary surfaces

We have been working to enable the representation of height using elevation maps and tessellation and/or parallax mapping. Long story short, both options are now available in Gaia Sky, which bundles elevation maps for the Earth, Moon, Mars and Mercury. Additionally, we have included the possibility to procedurally generate the elevation maps. Right now it is only used for Callisto, the moon of Jupiter.

This has been a long and arduous path, entailing the introduction of a new pipeline of tessellation shaders, as well as a rewrite of the existing shaders to represent elevation via parallax mapping.

In all cases, a map is also generated in CPU memory, so that the elevation data is also available to the camera to avoid clips into the planets and moons.


<a href="/img/2019/08/tess.jpg">
<img src="/img/2019/08/tess_s.jpg"
     alt="The surface of the Earth"/>
</a>
<p style="text-align: center;" class="caption">The surface of Earth</p>

Check out the videos [here](https://www.youtube.com/watch?v=RDkA3MWbpz8) and [here](https://www.youtube.com/watch?v=BWD4OyE87qo) for tessellation, and [here](https://www.youtube.com/watch?v=sf3ya8uHXIw) for parallax mapping.

## Logarithmic depth buffer and Milky Way model

We have implemented a logarithmic depth buffer to eliminate the depth buffer problems at especially large scales. Usually, the depth buffer is implemented with this non-linear function

$$d = {{{1 \over z} - {1 \over z_n}} \over {{1 \over z_f}  - {1 \over z_n}}},$$

where \\(z_n\\) is the near clipping value of the visible frustum, and \\(z_f\\) is the far value. \\(z\\) is the fragment distance from the camera and \\(d\\) is the depth value that we'll put in the z-buffer. Instead, we changed it to this:

$$d = {log(K * z + 1) \over log(K * z_f + 1)}$$

where \\(K\\) is a constant that controls the resolution close to the viewer.

![Regular depth buffer vs logarithmic depth buffer](/img/2019/08/zdepth.png)

<p style="text-align: center;" class="caption">Logarithmic depth function (red) and the regular depth function (green)</p>


This allows us to better utilize the depth buffer at galactic and extracgalactic scales. In particular, paired with a few [dither shaders](https://en.wikipedia.org/wiki/Dither), it enabled us to update the old, image-based Milky Way model to a new particle-based one sporting different components for gas, dust, HII regions and stars:

<a href="/img/2019/08/gs_mw.jpg">
<img src="/img/2019/08/gs_mw_s.jpg"
     alt="The new Milky Way"/>
</a>
<p style="text-align: center;" class="caption">The new Milky Way</p>

Also, using the new z-buffer we could rework the mesh rendering to better represent the galactic dust. Here is a video:

<video width="60%" style="display: block; margin: auto;" controls>
  <source src="/img/2019/08/dust-map.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>
<p style="text-align: center;" class="caption">Galactic dust map (data: <a href="http://galaxymap.org">@galaxy_map</a>)</p>

## Game mode

A new game mode has been implemented. This mode uses the default `WASD` + `Mouse` control scheme of most games to control the camera. Additionally, when the camera is in Game mode and close to a planet or moon, gravity will kick in and suck the player towards the surface. Use `SPACE` to move up (and fly), and `C` to move down. Use `SHIFT` to 'run'.

## Reflections

We have implemented skydome reflections into the shaders to be able to represent the metallic materials of Gaia with more fidelity. The skydome cubemap has been generated using the 360 mode of Gaia Sky. See [this tweet](https://twitter.com/GaiaSky_Dev/status/1154715483888902145) for a video, or the image below to a debug showcase.


<a href="/img/2019/08/reflections.jpg">
<img src="/img/2019/08/reflections_s.jpg"
     alt="Some reflections debug objects"/>
</a>
<p style="text-align: center;" class="caption">Debugging the reflections shader</p>


## Orbits

The orbits have been revamped. In addition to a new fading orbit trail rendering mode, we have a background updater which recomputes the orbits when they get outdated. This ensures the planetary orbits based on a sampled VSOP87 stay up to date at all times.

<a href="/img/2019/08/orbits.jpg">
<img src="/img/2019/08/orbits_s.jpg"
     alt="The new orbit trails"/>
</a>
<p style="text-align: center;" class="caption">New orbit trails</p>

Check out this [twitter thread](https://twitter.com/GaiaSky_Dev/status/1142042076915412992) for more information and videos of the new orbits.

## Tone mapping

This feature could still be considered experimental. We have implemented a few post-processing tone mapping algorithms to attempt a high dynamic range output. The most interesting of them all is the **automatic tone mapping**, which computes the average and maximum luminosity values of the previous frame and uses them to automatically adjust the exposure. True HDR required to move the back buffer to a float buffer (with 16 bits per channel) instead of the regular 8-bit buffer.

The tone mapping options available are:

- None -- no tone mapping will be applied
- Manual -- user-set exposure value
- Filmic
- Uncharted
- ACES
- Automatic

## Velocity vectors

Proper motion representation has gotten a bit of an overhaul. Here are the changes.

- Velocity vectors are now part of the component types
- Velocity vector coloring can no be choosen
    - Direction -- encodes different directions in different colors
    - Speed -- color map using the speed as input
    - Has radial velocity -- stars with RV are in red, the rest are in blue
    - Redshift from Sun -- red-blue colormap representing the redshift from the sun (RV)
    - Redshift from camera -- red-blue colormap representing the redshift from the camera (RV)
    - Single color -- use a plain blue for all stars
- Arrowheads

## Scripting

We have moved away from Jython and to Py4J for scripting. Please see [this dedicated post](/blog/2019/gaia-sky-scripting/) on the topic for more information.

## Additional features

- Improved debug interface with information on Video memory (only ATI and NVIDIA).
- Comprehensive warnings in object search.
- Startup object can be configured in the properties file.
- Tooltips padded.
- Decouple keyboard bindings from actions. Definition is now in `keyboard.mappings` file.
- Checksums from MD5 to SHA256.
- Info panel on mode switches.
- New Ultra graphics quality mode with +8K textures. Download the hi-resolution texture pack to enjoy it. Beefy graphics card recommended.
- Added starburst texture to lens flare.
- Improved skins and theming by setting the input fields, select boxes and check boxes to the theme color.
- Moved all shaders and pipeline to **OpenGL 4.x**.
- Integer mesh indices for larger meshes.
- Sane crash reporting. If Gaia Sky crashes, you can find the crash log in `$GS_DATA/crashreports`, which is usually at `~/.local/share/gaiasky/crashreports` in Linux, and `[HOME]\.gaiasky\crashreports` in Windows/macOS.
- Migration to Java 11. Please make sure you are using Java 11+ to run Gaia Sky. Windows and macOS versions already bundle their own JVM.
- We have moved on to [LWJGL3](www.lwjgl.org) as the backend, fixing the issues present mostly in macOS due to pixel scaling.
- Scripting API parameter checks.
- Many bug fixes and some code refactorings.

## Full change log

- [CHANGELOG.md](https://gitlab.com/langurmonkey/gaiasky/blob/dec26b2f18091204cd7a371eccd9c9afad021fec/CHANGELOG.md) -- generated from the commit history of Gaia Sky.
- [2.1.7-2.2.0 compare](https://gitlab.com/langurmonkey/gaiasky/compare/2.1.7-vr...2.2.0#) -- in the repository.

