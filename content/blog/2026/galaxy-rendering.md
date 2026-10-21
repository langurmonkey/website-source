+++
author = "Toni Sagrista Selles"
categories = ["Graphics"]
tags = ["gaiasky", "opengl", "rendering", "visualization", "volume rendering", "computer graphics", "english"]
date = 2026-10-25
linktitle = ""
title = "Galaxy rendering: particles to volume"
description = "Improving the Milky Way in Gaia Sky with volume rendering"
featuredpath = "date"
type = "post"
js = ["/js/mathjax4.js"]
draft = true
+++

The Milky Way is an essential component in any 3D Universe software. Rendering a realistic (i.e. science-based) and visually appealing galaxy is paramount to the user experience, and to the cohesion of the simulated universe as a whole. Galaxies are made of gas and dust clouds, so they are volumetric in nature. In Gaia Sky we have been using particle-based representations for a long time, even though we have had the volumetric rendering infrastructure in place also for a while. This post describes the rendering technique we use in Gaia Sky 3.9.0 to render the volumetric Milky Way, and how we have constructed the dataset that enables it. Interested? Keep reading.

<!--more-->

{{< fig src="/img/2026/10/milky-way-risinger.jpg" class="fig-center" width="50%" loading="lazy" caption="Nick Risinger's impression of the Milky Way" >}}


## A little bit of history

The rendering of our and other galaxies has always been a topic I dreaded. I never felt that the solutions we found were good enough. I always knew that the right way to do it was with volume rendering, but the main issue was that we did not have the volumetric data.

So, for a long time, we have used approximations to render the Milky Way, some more gracious than others.
- **Enhanced flat image** --- Initially, we used a single two-faced billboard with the artist's impression by Nick Risinger, coupled with a generated star field. This was featured in the September 26, 2016 Astronomy Picture of the Day, titled "Here comes the Sun"[^1].
- **Textured billboard approach** --- After Gaia DR3 landed in 2018 and 2022 respectively, the catalog data were used by Stefan Payne-Wardenaar[^2] to produce a high-quality representation of the whole Galaxy[^3] in Blender. At that time, I worked with Stefan to produce a particle-based version that would fit in the existing billboard systems in Gaia Sky. The first version was based on textured additive billboards and dithered depth buffer occlusion. The depth was correct, but the look of the galaxy was rather cartoonish and unrealistic. Additive blending was used for all channels except the dust, which was purely occlusive in a binary sense (no sorting, so no transparency).
- **Billboards with additive and subtractive blending** --- Later on, inspired by [this article](https://dexyfex.com/2016/09/09/galaxy-rendering-revisited/), the textured billboards were updated to rely on blobs and additive/subtractive blending. The main issue was that the emissive parts blended additively in a very unrealistic way, and the occlusion did not respect the depth order in the scene. Several attempts were made afterwards to implement Weighted Blended Order-Independent Transparency (WBOIT)[^4], as suggested by the article, but this was very difficult to tune and produced underwhelming results.

All these issues finally tipped me into seriously consider approaching the project of converting the particle data to a volume and implementing a proper volume renderer with emission and occlusion.

## Particles to volume

The first step is to convert the particle data to a volume in the form of a voxel grid. This step is crucial, as it can make or break the whole project. Having a good dataset is the difference between a bland-looking visual and an awesome one. Here I detail the process of converting particles to the volume, and talk a bit about the formats (R8 density/RGB8 color/RGBA8 color+density).

## The volume renderer

Here we go over the galaxy shader. It works in two steps: depth and emission. Depth runs early, emission runs late in the pipeline. Explain the reasons. Explain the shader structure at high level, give some pseudocode.

## Infrastructure in Gaia Sky

Loading infrastructure, data format (JSON), etc. THis should be rather short, already covered in the Gaia Sky docs. Add pointers.

## Results

Compare results at different resolutions (200, 400, 800), and with different number of iterations (low/normal/high/ultra presets).

Add some images, add the gaia sky volume MW video (youtube).

## Conclusion

Write a good conclusion.



[^1]: Astronomy Picture of the Day: Here comes the Sun

      https://science.nasa.gov/image-article/apod-2016-september-26-gaia-here-comes-the-sun/

[^2]: Stefan Payne-Wardenaar BlueSky profile

      https://bsky.app/profile/stefanpw.bsky.social

[^3]: Gaia's Milky Way map

      https://www.cosmos.esa.int/web/gaia/milky-way

[^4]: *Morgan McGuire and Louis Bavoil*, **Weighted Blended Order-Independent Transparency**, *Journal of Computer Graphics Techniques* (JCGT), vol. 2, no. 2, 122-141, 2013.

      Available online: http://jcgt.org/published/0002/02/09/
