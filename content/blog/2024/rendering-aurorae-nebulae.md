+++
author = "Toni Sagrista Selles"
categories = ["gaia sky"]
tags = ["rendering", "opengl", "glsl", "aurora", "northern lights", "nebulae", "gaia sky", "programming", "volume rendering", "astronomy", "english"]
date = 2024-12-11
linktitle = ""
title = "Rendering volume aurorae and nebulae"
description = "Some notes on my trials and tribulations adding aurorae to Gaia Sky"
featuredpath = "date"
type = "post"
+++

A few weeks ago someone created an [issue](https://codeberg.org/gaiasky/gaiasky/issues/784#issuecomment-2512129) in the Gaia Sky Codeberg repository requesting the addition of aurorae to the Earth. They used as an example the aurora add-on in Cosmographia[^cosmographia], which, at the time, looked to me like it was using some kind of billboard particle system to generate the effect. I never thought it looked particularly good for an aurora; I thought Gaia Sky could do better. So I set on a quest to implement a *better looking* aurora object in Gaia Sky. This wee quest would involve implementing three very different approaches to aurora rendering over the span of a few weeks, plus more than half a dozen 3D volume nebulae.

In this post, I present the three different methods I implemented to render aurorae. But before anything, I need to take a small detour and talk about nebulae.


<!--more-->

## Li'l nebulae detour

If every story should start at the beginning and be told in full, I must first relate how this little quest took a little detour, at the beginning, to explore the rendering of volume nebulae. The OP mentioned in the Codeberg issue that he also gets requests to fly into nebulae during his tours, and Gaia Sky only contained billboards so far. Since Gaia Sky already contained the necessary infrastructure to render ray-marched volumes using a screen quad in a post-processing effect, I decided that solving this issue first made sense, as it involved *much* less work.

I browsed through [shadertoy](https://shadertoy.com) in search for a good implementation of a ray-marched shader that I could use as a base for my nebulae. I found several, like the [Dusty Nebula 4](https://www.shadertoy.com/view/MsVXWW) by Duke, and the [Supernova Remnant](https://www.shadertoy.com/view/MdKXzc), also by Duke. This [Duke](https://www.shadertoy.com/user/Duke) guy seems to be the most prolific shadertoy author when it comes to large-scale dusty objects, and by a large margin. It's not even close, so props to him and thank you very much for your work. All of his shaders seem to be licensed under [CC-BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/deed.en), which is perfect for modification and reuse in Gaia Sky.

So, taking some of these shaders as a baseline, I created new ones for the *Cat's Eye* nebula, the *Hourglass* nebula, the *Trifid* nebula, the *Butterfly* nebula, and the *Crab* nebula, among others.

<figure class="fig-center">
<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/MfcBzH?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>
<figcaption>My implementation of Crab nebula (M1) in shadertoy.</figcaption>
</figure>

Once the Shadertoy shaders were ready, I did a little more work on the post-processing ray-marching infrastructure to accommodate the new members. So far, I had only ever used it for the black holes. The final step was translating the shaders from Shadertoy to Gaia Sky. This was not too difficult, as they were already created with that step in mind.

### Anatomy of a nebula shader

As we mentioned, currently the nebulae are implemented in the post-processor. This means that they are rendered in *image space* after the main rendering stage, which renders the geometry, has finished.Post-processors get as input data the current frame buffer, the depth buffer, and whatever additional textures are needed for the particular effect (such as one or more noise textures). Additionally, they get positions and orientations as uniforms or varyings computed in the vertex stage.

All nebula shaders have the same main parts:

- **Set up** -- here we prepare the data for the raymarching step. The ray direction, the camera position and the object position are all computed/fetched here. We also recover the depth for the current fragment from the depth buffer. The set-up is typically done in the ``main()`` function. In the following code we have an example of how the set-up stage is done.
{{< collapsedcode file="/static/shader/2024/nebula/shader-setup.glsl" language="glsl" summary="set-up example" >}}

- **Ray marching** -- here is where the actual ray-marching happens. In ray marching, we shoot a ray for every pixel, divide it into samples, and gather information at every step. This information is usually the density and color of the medium we are rendering.
  - **Intersection check** -- since we implement this in image space (we shoot a ray for each pixel in our window), we first need to check whether our ray intersects the bounding volume containing the object or not. In nebulae, this volume is typically a sphere. Simply enough, this is done with a straightforward ray-sphere intersection function, which returns the intersection near and far distances if there is an intersection at all, or nothing if the ray does not hit the sphere. The code below shows how to do the ray-sphere intersection.
{{< collapsedcode file="/static/shader/2024/nebula/shader-intersection.glsl" language="glsl" summary="ray-sphere intersection example" >}}

  - **Main loop** -- here we loop over a maximum number of iterations and accumulate the density. Every cycle advances our position through the ray by a given step distance. The code below illustrates a rather typical main loop. The following code completes the ``main()`` function to include the call to the main loop (``raymarching()``) and the alpha blending at the very bottom.
{{< collapsedcode file="/static/shader/2024/nebula/shader-mainloop.glsl" language="glsl" summary="main loop example" >}}

- **Blending** -- finally, we have the blending. Most nebulae are blended using regular alpha blending, but implementing additive blending is trivial.
{{< collapsedcode file="/static/shader/2024/nebula/shader-blend.glsl" language="glsl" summary="alpha blending example" >}}

This covers the basics of our nebulae shaders. The video below shows some examples of the final product.

{{< vid src="/img/2024/12/nebulae-raymarch.mp4" poster="/img/2024/12/nebulae-raymarch.jpg" class="fig-center" width="75%" title="Six of the new nebulae implemented in Gaia Sky." >}}

Now, back to the aurora.

## Back to aurorae


### Number one

### Number two

### Number three

## Future work

- Render the aurorae to an off-screen buffer.
  - Lower resolution.
  - Apply blur and glow to mitigate jittering artifacts.
  - Full control over blending.
- Model different aurora colors.

## Conclusions



[^cosmographia]: SPICE-Enhanced Comosgraphia Mission Visualization Tool, NAIF: https://naif.jpl.nasa.gov/naif/cosmographia.html
