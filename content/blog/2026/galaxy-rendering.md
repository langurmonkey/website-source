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

The Milky Way is an essential component in any 3D Universe software. The rendering of our and other galaxies has always been a hot topic in Gaia Sky. Initially, we used a single two-faced billboard with the artist's impression by Nick Risinger, coupled with a generated star field. This was featured in the September 26, 2016 Astronomy Picture of the Day, titled "Here comes the Sun"[^1]. Later, after Gaia DR2 and DR3 landed in 2018 and 2022 respectively, the data were used by Stefan Payne-Wardenaar[^2] to produce a high-quality representation of the whole Galaxy[^3] in Blender. At that time, I worked with Stefan to produce a particle-based version that would fit in the existing billboard systems in Gaia Sky. Initially, it was based on textured additive billboards and dithering occlusion. Later on, inspired by an [article on galaxy rendering](https://dexyfex.com/2016/09/09/galaxy-rendering-revisited/), this was updated to rely on blobs and subtractive blending. The main issue was that the emissive parts blended additively in a very unrealistic way, and the occlusion did not respect the depth order in the scene. Several attempts were made afterwards to implement Weighted Blended Order-Independent Transparency (WBOIT)[^4], as suggested by the article, but this was very difficult to tune and produced underwhelming results.

<!--more-->


{{< fig src="/img/2026/10/milky-way-risinger.jpg" class="fig-center" width="50%" loading="lazy" caption="Nick Risinger's impression of the Milky Way" >}}


## A little bit of history

## The volume renderer

## Particles to volume

## Infrastructure in Gaia Sky

## Results

## Conclusion



[^1]: Astronomy Picture of the Day: Here comes the Sun

      https://science.nasa.gov/image-article/apod-2016-september-26-gaia-here-comes-the-sun/

[^2]: Stefan Payne-Wardenaar BlueSky profile

      https://bsky.app/profile/stefanpw.bsky.social

[^3]: Gaia's Milky Way map

      https://www.cosmos.esa.int/web/gaia/milky-way

[^4]: *Morgan McGuire and Louis Bavoil*, **Weighted Blended Order-Independent Transparency**, *Journal of Computer Graphics Techniques* (JCGT), vol. 2, no. 2, 122-141, 2013.

      Available online: http://jcgt.org/published/0002/02/09/
