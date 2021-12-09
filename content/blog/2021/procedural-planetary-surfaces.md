+++
author = "Toni Sagrista Selles"
categories = ["Programming"]
tags = ["programming", "procedural", "graphics", "opengl", "english"]
date = 2021-12-09
linktitle = ""
title = "Procedural generation of planetary surfaces"
description = "Generating realistic planet surfaces and moons"
featuredpath = "date"
type = "post"
+++

I have recently implemented a procedural generation system for planetary surfaces and moons into [Gaia Sky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky). In this post, I ponder about different methods and techniques I have used to this purpose. The following image shows a procedurally generated planet using the process described in this article.

{{< fig src="/img/2021/12/procedural-surfaces/teaser-s.png" link="/img/2021/12/procedural-surfaces/teaser.png" title="Left: a wide view of a procedurally generated planet. Right: the same planet viewed from the surface." class="fig-center" width="60%" loading="lazy" >}}

<!--more-->

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

## All is noise

We start with a noise algorithm. A noise algorithm is essentially a function that returns a *random* value when sampled using coordinates. Obviously, a pure RNG (random number generator) won't cut it, as the noise we need to generate mountains and valleys and seas is not totally random. There needs to be some structure to it for it to successfully approximate reality. There are very many noise algorithms to choose from, but all essentially fall into one of these two categories:

1. **value noise**---based on the interpolation of random values assigned to a lattice of points.
2. **gradient noise**---based on the interpolation of random gradients assigned to a lattice of points.

One of the most common realization of gradient noise is Perlin noise, developed by Ken Perlin. Let\'s have a look at some noise generated with this algorithm.

{{< fig src="/img/2021/12/procedural-surfaces/maps/perlin-height.png" link="/img/2021/12/procedural-surfaces/maps/perlin-height.png" title="Good old Perlin noise." class="fig-center" width="20%" loading="lazy" >}}

It looks alright, but something is not right. Let\'s interpret each pixel in that image as the elevation value at the coordinates of that pixel. This gives us an elevation map. Darker pixels have lower elevations, while brighter pixels have higher elevation. We can then map colors to elevation ranges. For example, black areas are assigned blues, for water. Gray areas are green, and bright areas are white, for snow. That would give us the following image:

{{< fig src="/img/2021/12/procedural-surfaces/maps/perlin-diffuse.png" link="/img/2021/12/procedural-surfaces/maps/perlin-diffuse.png" title="Perlin noise colored with a simple mapping." class="fig-center" width="20%" loading="lazy" >}}

Again, it is alright, but it is not super good. We can try with other kinds of noise. For example, (open) simplex noise is an evolution of Perlin noise with fewer artifacts. Its open implementation is multi-dimensional and it is also quite fast. Let\'s see:

<table width="50%" style="margin: 0 auto 0 auto;">
<tr style="background-color:#00000000;border-width: 0px;"><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/simplex-height.png" link="/img/2021/12/procedural-surfaces/maps/simplex-height.png" title="Open simplex noise." class="fig-center" width="90%" loading="lazy" >}}
</td><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/simplex-diffuse.png" link="/img/2021/12/procedural-surfaces/maps/simplex-diffuse.png" title="Noise colored with same process." class="fig-center" width="90%" loading="lazy" >}}
</td></tr></table>

Maybe it's a bit better, but there's something missing. We can also generate the normal maps from the elevation data. Doing so involves computing the horizontal and vertical gradients at each point. The normal map encodes the direction of the surface normal vector at each point, and works a little better at visualizing the gradients.

<table width="50%" style="margin: 0 auto 0 auto;">
<tr style="background-color:#00000000;border-width: 0px;"><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/perlin-normal.png" link="/img/2021/12/procedural-surfaces/maps/perlin-normal.png" title="Normal map for the Perlin noise above." class="fig-center" width="90%" loading="lazy" >}}
</td><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/simplex-normal.png" link="/img/2021/12/procedural-surfaces/maps/simplex-normal.png" title="Normal map for the Simplex noise." class="fig-center" width="90%" loading="lazy" >}}
</td></tr></table>

At this point we can start playing around with fractals, and re-applying the noise algorithm at different scales with higher frequencies and lower amplitudes. These different scales or levels are called octaves. We compute them by sampling the same noise algorithm multiple times on top of each other and modulating its amplitude and frequency. If we compute 4 octaves with the simplex noise, we get something like this:

<table width="50%" style="margin: 0 auto 0 auto;">
<tr style="background-color:#00000000;border-width: 0px;"><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/simplex-4oct-height.png" link="/img/2021/12/procedural-surfaces/maps/simplex-4oct-height.png" title="Open Simplex noise with 4 octaves." class="fig-center" width="90%" loading="lazy" >}}
</td><td>
{{< fig src="/img/2021/12/procedural-surfaces/maps/simplex-4oct-diffuse.png" link="/img/2021/12/procedural-surfaces/maps/simplex-4oct-diffuse.png" title="Same noise colored with same process." class="fig-center" width="90%" loading="lazy" >}}
</td></tr></table>

If you zoom in into the left image, you will see that there are additional levels of detail at smaller scales compared to the regular simplex noise shown before. This is very good, as it mimics nature much more closely. How do we set up a surface generation process, then? Read on to the next section.

## Surface generation

The first thing that we need to address is the simplistic looks of the colored images. We see that simply assigning colors to elevation ranges won\'t cut it. We can improve the process by generating a humidity map in exactly the same way we are generating our elevation map. Then we can use this humidity data to manipulate the colors in a clever way to add an extra layer of randomness. We\'ll see about that later.

The surface generation process starts, then, with the generation of the
elevation and humidity data. The elevation data is a 2D array containing
the elevation value in \\([0,1]\\) at each coordinate. The humidity data is
the same but it contains the humidity value, which will come in handy
for the coloring. But first, let\'s visit our sampling process.

### Seamless (tilable) noise

Usually, noise sampled directly is not tileable. The features do not
repeat, and you just can\'t extend the noise indefinitely because seams
are visible. In the case of one dimension, usually one would sample the
noise using the only dimension available, \\(x\\).

{{< fig src="/img/2021/12/procedural-surfaces/figures/noise-sampling-1d.png" link="/img/2021/12/procedural-surfaces/figures/noise-sampling-1d.png" title="Sampling noise in 1D leads to seams." class="fig-center" width="50%" loading="lazy" >}}

However, if we go one dimension higher, 2D, and sample the noise along a
circumference embedded in this two-dimensional space, we get seamless,
tileable noise.

{{< fig src="/img/2021/12/procedural-surfaces/figures/noise-sampling-2d.png" link="/img/2021/12/procedural-surfaces/figures/noise-sampling-2d.png" title="Sampling noise along a circumference in 2D space is seamless" class="fig-center" width="50%" loading="lazy" >}}

We can apply this same principle with any dimension \\(d\\) by sampling in \\(d+1\\). Since we need to create spherical 2D maps (our aim is to produce textures to apply to UV spheres), we do not sample the noise algorithm with the \\(x\\) and \\(y\\) coordinates of the pixel in image space. That would produce higher frequencies at the poles and lower around the equator. Additionally, the noise would contain seams, as it does not tile by default. Instead, we sample the 2D surface of a sphere of radius 1 embedded in a 3D volume, so we sample 3D noise. To do so, we iterate over the spherical coordinates \\(\varphi\\) and \\(\theta\\), and transform them to cartesian coordinates to sample the noise:

$$
\begin{align}
x &= \cos \varphi \sin \theta \nonumber \\\
y &= \sin \varphi \sin \theta \nonumber \\\
z &= \cos \varphi \nonumber
\end{align}
$$

The process is outlined in this code snippet. If the final map
resolution is \\(N \times M\\), we use N \\(\theta\\) steps and M \\(\varphi\\)
steps.

``` c
// Map is NxM
for (phi = -PI / 2; phi < PI / 2; phi += PI / M){
    for (theta = 0; theta < 2 * PI; theta += 2 * PI / N) {
        n = noise.sample(cos(phi) * cos(theta), // x
                         cos(phi) * sin(theta), // y
                         sin(phi));             // z
        theta += 2 * PI / N;
    }
}
```

### Noise parametrization

We carry out the generation by sampling configurable noise algorithms (Perlin, Open Simplex, etc.) at different levels of detail, or octaves. In Gaia Sky, we have some important noise parameters to adjust:

-   **seed**---a number which is used as a seed for the noise RNG.
-   **type**---the base noise type. Can be any algorithm, like **gradient (Perlin)
    noise**[^1], **gradval noise**[^2], **simplex**[^3], **value**[^4]
    or **white**[^5]. For examples, see
    [here](https://joise.sudoplaygames.com/modules/#modulebasisfunction).
-   **fractal type**---the algorithm used to modify the noise in each
    octave. It determines the persistence (how the amplitude is
    modified) as well as the gain and the offset. Can be **billow**,
    **deCarpenterSwiss**, **FBM**, **hybrid multi**, **multi** or
    **ridge multi**. For examples, see
    [here](https://joise.sudoplaygames.com/modules/#modulefractal).
-   **scale**---determines the scale of the sampling volume. The noise
    is sampled on the 2D surface of a sphere embedded in a 3D volume to
    make it seamless. The scale stretches each of the dimensions of this
    sampling volume.
-   **octaves**---the number of levels of detail. Each octave reduces
    the amplitude and increases the frequency of the noise by using the
    lacunarity parameter.
-   **frequency**---the initial frequency of the first octave.
    Determines how much detail the noise has.
-   **lacunarity**---determines how much detail is added or removed at
    each octave by modifying the frequency.
-   **range**---the output of the noise generation stage is in \\([0,1]\\)
    and gets map to the range specified in this parameter. Water gets
    mapped to negative values, so adding a range of \\([-1,1]\\) will get
    roughly half of the surface submerged in water.
-   **power**---power function exponent to apply to the output of the
    range stage.

{{< fig src="/img/2021/12/procedural-surfaces/maps/noise-types-annotated.jpg" link="/img/2021/12/procedural-surfaces/maps/noise-types-annotated.jpg" title="Different noise types. Value and white noise are mostly useless for our purposes." class="fig-center" width="100%" loading="lazy" >}}

The final stage of the procedural noise generation clamps the output to \\([0,1]\\) again, so that all negative values are mapped to 0, and all values greater than 1 are clamped to 1.

We use the elevation directly as the height texture for the tessellation or parallax mapping shaders (this is out of the scope of this article). We use the humidity, together with the elevation, to determine the color using a look-up table. This allows us to color different regions atthe same elevation differently depending on the humidity value. We map the humidity value to the \\(x\\) coordinate and the elevation to \\(y\\). Both coordinates are normalized to \\([0,1]\\).

Additionally, since the look-up table is just an image in disk, we can have many of them and use them in different situations, or even randomize which one is picked up. A simple look-up table would look like this. From left to right it maps less humidity (hence the yellows, to create deserts, and grays at the top, for rocky mountains) to more humidity (as we go right it gets greener, and the mountain tops get white snow).

{{< fig src="/img/2021/12/procedural-surfaces/figures/procedural-lut.png" link="/img/2021/12/procedural-surfaces/figures/procedural-lut.png" title="The look-up table mapping dimensions are elevation and humidity." class="fig-center" width="40%" loading="lazy" >}}

We can also hue-shift the look-up table by an extra **hue shift** parameter (in \\([0^{\circ}, 360^{\circ}]\\)) in order to produce further variation. The shift happens in the HSL color space, so we convert from RGB to HSL, modify the H (hue) value, and convert it back to RGB. Once the shift is established, we generate the diffuse texture by sampling the look-up table and shifting the hue. The specular texture is generated by assigning all heights equal to zero to a full specular value. Remember that all negative values were clamped to zero, so zero essentially equals water in the final height map.

Finally, we can also generate a normal map from the height map by determining elevation gradients in both \\(x\\) and \\(y\\). We use the normal map only when tessellation is unavailable or disabled. Otherwise it is not generated at all. The generation of the normal map is out of the scope of this article.

## Cloud layer generation

We can generate the clouds with the same algorithm and the same parameters as the surface elevation. Then, we can use an additional `color` parameter to color them. For the clouds to look better one can set a larger \\(z\\) scale value compared to \\(x\\) and \\(y\\), so that the clouds are stretched in the directions perpendicular to the rotation axis of the planet.


## Putting it all together

This article may be a bit rushed, but I believe all the right ingredients are in. Below you can see an example of what Gaia Sky currently generates.

{{< fig src="/img/2021/12/procedural-surfaces/maps/procedural-maps-s.png" link="/img/2021/12/procedural-surfaces/maps/procedural-maps.png" title="Left to right and top to bottom, clouds map, diffuse texture, elevation map, normal map and specular map procedurally generated with Gaia Sky." class="fig-center" width="80%" loading="lazy" >}}


More information on the topic can be found in the [official documentation](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Procedural-generation.html) of Gaia Sky.
