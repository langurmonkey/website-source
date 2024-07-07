+++
author = "Toni Sagrista Selles"
categories = ["gaia sky"]
tags = ["gaia sky", "simulation", "technical", "programming", "procedural", "astronomy", "exoplanets", "english"]
date = 2024-06-11
linktitle = ""
title = "Supercharging Exoplanets"
description = "A short report on the new developments in exoplanet datasets in Gaia Sky"
featuredpath = "date"
type = "post"
js = ["/js/GlslCanvas.js"]
+++


A couple of years ago I wrote about the [procedural planetary surfaces generation process](/blog/2021/procedural-planetary-surfaces/) in Gaia Sky. In this post, I provided a more or less detailed technical overview of the process used in Gaia Sky to procedurally generate planetary surfaces (elevation, diffuse, specular and normal maps) and cloud layers.

Since then, we have used the system to spice up the planets in the planetary systems for which Gaia could determine reasonable orbits (see the data [here](https://www.cosmos.esa.int/web/gaia/exoplanets), and some Gaia Sky datasets for some of those systems [here](https://gaia.ari.uni-heidelberg.de/gaiasky/repository/systems/dr3/), including HD81040, Gl876, and more). 

However, with the upcoming Gaia DR4 release, the number of candidate exoplanets is expected to [increase significantly](https://www.cosmos.esa.int/web/gaia/iow_20240422), rendering the "one dataset per system" approach obsolete. In this post I describe some of the improvements made with regards to exoplanets in Gaia Sky, in both the handling of large numbers of extrasolar systems seamlessly, and in the new, improved procedural generation of planetary surfaces.

<!--more-->

So far, Gaia Sky has been able to represent extrasolar systems via additional datasets containing the system objects and metadata (barycentre, stars, planets, orbits, etc.). These datasets are distributed as standalone downloads via the integrated download manager, which serves data from our [data repository](https://gaia.ari.uni-heidelberg.de/gaiasky/repository). This approach was only good as far as the number of systems was kept low, which was true until now. However, with the advent of DR4, this number is expected to reach four digits, so a new solution is in order.

{{< fig src1="/img/2024/07/planet-surface.jxl" type1="image/jxl" src2="/img/2024/07/planet-surface.avif" type2="image/avif" src="/img/2024/07/planet-surface.jpg" class="fig-center" width="75%" title="A screenshot from the surface of a procedurally generated planet, in Gaia Sky. In the picture we can see elevation, clouds, atmosphere and fog. This uses the new system." loading="lazy" >}}

## Representing Exoplanets

Gaia Sky has supported a representation of exoplanets *locations* since 3.6.0, released in March 2024. It is based on the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), which contains some 5600 confirmed planets. Up to now, this was implemented as a glorified point cloud, where the glyph for each system is chosen according to the number of candidate planets in said system. Broman et al. develop a more extensive use of glyphs in ExoplanetExplorer[^broman2023].

{{< fig src1="/img/2024/07/exoplanet-glyphs.jxl" type1="image/jxl" src2="/img/2024/07/exoplanet-glyphs.avif" type2="image/avif" src="/img/2024/07/exoplanet-glyphs.jpg" class="fig-center" width="75%" title="The textures used for exoplanets, sorted from 1 to 8 candidates (1-4 top, 5-8 bottom)." loading="lazy" >}}

Below is a view of the NASA Exoplanet Archive from the outside. The elongated arm to the left is the [Kepler field of view](https://science.nasa.gov/resource/kepler-field-of-view/).

{{< fig src1="/img/2024/07/nasa-exoplanets-gaiasky.jxl" type1="image/jxl" src2="/img/2024/07/nasa-exoplanets-gaiasky.avif" type2="image/avif" src="/img/2024/07/nasa-exoplanets-gaiasky.jpg" class="fig-center" width="75%" title="The NASA Exoplanet Archive in Gaia Sky, represented as a point cloud with glyphs." loading="lazy" >}}

This representation is useful to indicate the position and number of planets of each system. It works using the *particle set* object, which is essentially a point cloud. An extension was necessary, in order to select a texture for each system according to the value of one of the table columns. In this case, the texture is selected according to the number of planets in the system.

## Seamless Fly-In

The first objective in this little project was to achieve a seamless navigation from the "global" view to the "local" view in a seamless way without having to preload all systems' descriptors at startup. The global view is represented by the full dataset, while the local view is from within a particular system. Additionally, the mechanism used for this should be, if possible, generic for all particle sets.

The base data file is a VOTable as downloaded from the NASA Exoplanet Archive website. This VOTable contains all the available information for each of the planets: name, host name, position, physical characteristics, orbital information, etc. Essentially, we had two options at this point:

1. Generate the system objects transparently directly in Gaia Sky whenever the camera gets close enough to them.
2. Pre-compute the system descriptor files beforehand and order Gaia Sky to load them whenever the camera nears an object.

**Option one** has the advantage that the dataset to distribute is much smaller. It only contains the metadata and the VOTable data file. However, this one solution is, by design, very ad-hoc to this dataset in particular. In other words, it would not be easily extensible to other exoplanet datasets (e.g. Gaia DR4) without major code changes.

**Option two** is much more general, in the sense that it can be applied to all exoplanet catalogs, provided all the Gaia Sky descriptor files are generated. However, the distributed package is a bit heavier, as it needs to include an extra JSON descriptor file for each system. But those are usually small, and compress well. 

### Proximity Loading

In the end, the positives of the second option vastly outweigh the negatives, so that's what we went with. We generated the descriptor files with a [Python script](https://codeberg.org/gaiasky/gaiasky/src/branch/master/core/scripts/other/nasa-exoplanets-aggregator.py) that aggregates all planets in the same system and produces a series of JSON files. Then, we added a couple of attributes to [particle sets](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/_generated/Components.html#particleset):

- "proximityDescriptorsLocation" -- the location of the descriptor files for the objects of this particle set. The descriptor files *must* have the same name as the objects.
- "proximityThreshold" -- solid angle, in radians, above which the proximity descriptor loading is triggered.

In principle, any particle set can define these two attributes to enable **proximity loading**. In it, when the solid angle of a particle overcomes the proximity threshold, the load operation is triggered, where the JSON descriptor file corresponding to the particle gets loaded, if it exists and is found at the location given by the proximity descriptors location attribute. The matching is done using the particle's name, which must be the same as the file name plus extension.

There are a few requirements for it to work:

- Particles in the particle set must have a name.
- The proximity descriptors location, and optionally the proximity threshold angle, must be defined for the particle set.
- The JSON files to load must be prepared and available at the given location.

The loading itself happens in a background thread. When it is done, the scene graph and the indices are updated. Then, if the camera is in focus mode, and the focus object is the trigger particle, the camera automatically switches focus to the first object in the dataset. Ideally, the first object in the dataset should have the same position as the particle in order to prevent a sudden seeking camera pan.

{{< vid src="/img/2024/07/nasa-exoplanets-seamless-hd.mp4" class="fig-center" width="75%" title="Proximity loading in Gaia Sky. Each of the extrasolar systems visited in the video gets loaded on-demand when the camera gets close enough to it. Disregard the slow procedural generation in the video, this version is using the old CPU based code. The next chapters in this article contain a description of how we made this much better." >}}

The video above shows the concept of proximity loading in motion. As the camera gets near an object, the proximity loading is triggered and new objects are loaded. When they become available, the camera switches focus to the new object. This results in a seamless exploration from the global dataset to the individual planets of each system.

## Procedural Generation Revisited

As mentioned in the beginning, back in 2021 we had a [first look](/blog/2021/procedural-planetary-surfaces/) at the procedural generation of planetary surfaces. This first approach was based on CPU code that ran rather slowly, so we had to add some progress bars at the bottom of the screen for each of the channels to provide some feedback to the user about the status of the generation. This was less than ideal.

This project had the following aims:

1. Replace the CPU-based code with a GPU implementation that runs much faster.
2. Improve the procedural generation to produce higher fidelity, more believable planets.
3. Enhance and simplify the procedural generation module and window so that it is easier to use and understand.

### GPU Noise and Surface Generation

The first step is straightforward to explain. Essentially, we moved the code from the CPU to the GPU. But the devil is in the details, so let's dive in.

Previously, we were basing on the [Joise library](https://joise.sudoplaygames.com/), a pure Java implementation of some common noise functions and layering strategies. From that, we created matrices in the main RAM for the elevation and the moisture, and we filled them up in the CPU using this library. From that, we generated the diffuse, specular and normal bitmaps, created the textures and set up the material. Easy enough.

Now, in the GPU we have two options: 

- Pixel shaders.
- Compute shaders.

On the one hand, **pixel shaders** are ubiquitous and supported everywhere, but they are a bit difficult to use for compute operations, and typically require encoding and decoding information using textures. On the other hand, **compute shaders** are perfect for this task, as they accept data inputs directly, but they are only in OpenGL since version 4.3. This leaves out, for example, macOS (only supports 4.1) and many systems with older graphics cards.

For the sake of compatibility, we decided to use pixel shaders in favor of compute shaders. They are more difficult to work with, but they should be universally compatible. Moreover, we can embed them directly in a website, like this curl noise, which is pretty neat:

{{< shader src="/shader/2024/curl.frag" class="fig-center" width="200" height="200" title="Curl noise shader, with turbulence and ridge, running in the browser." >}}

{{< collapsedcode file="/static/shader/2024/curl.frag" language="glsl" summary="Snippet: curl.glsl" >}}

But back to the topic:

- [gl-Noise as base](https://github.com/FarazzShaikh/glNoise).
- fBM as main method to do recursive detail.
- Types: simplex, perlin, curl, voronoi, white.
- Biome shader: elevation, moisture, (optional) temperature in RGB channels.
- Surface generation: 3/4 render targets with diffuse, specular, normal and emissive maps.

### Noise Parametrization

The noise parametrization changed a little bit in the migration process.

Amplitude, persistence, terraces (w. coarseness), turbulence and ridge, civilization lights.

### Presets and UI design

Finally, I want to write a few words about the way the procedural generation window has changed in Gaia Sky as a result of this migration.

- Presets.
- Hide noise in collapsible pane.
- More?

## Conclusion

Here be the conclusion.


<!---------------------------------------------------------------------------------->
[^broman2023]: E. Broman et al., "ExoplanetExplorer: Contextual Visualization of Exoplanet Systems," 2023 IEEE Visualization and Visual Analytics (VIS), Melbourne, Australia, 2023, pp. 81-85, doi: [10.1109/VIS54172.2023.00025](https://ieeexplore.ieee.org/document/10360923).  

