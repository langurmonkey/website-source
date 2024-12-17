+++
author = "Toni Sagrista Selles"
categories = ["gaia sky"]
tags = ["rendering", "opengl", "glsl", "aurora", "northern lights", "nebulae", "gaia sky", "programming", "volume rendering", "astronomy", "english"]
date = 2029-12-13
linktitle = ""
title = "Rendering volume aurorae and nebulae"
description = "Some notes on my trials and tribulations adding aurorae to Gaia Sky"
featuredpath = "date"
type = "post"
+++

A few weeks ago someone created an [issue](https://codeberg.org/gaiasky/gaiasky/issues/784#issuecomment-2512129) in the Gaia Sky Codeberg repository requesting the addition of aurorae to the Earth. They used as an example the aurora add-on in Cosmographia[^cosmographia], which, at the time, looked to me like it was using some kind of billboard particle system to generate the effect. I never thought it looked particularly good for an aurora; I thought Gaia Sky could do better. So I set on a quest to implement a *good looking* aurora object in Gaia Sky. This wee quest would involve implementing three very different approaches to aurora rendering over the span of a few weeks, but I did not know this at the time.

In this post, I go over the different methods I implemented to achieve a more or less convincing aurora effect in Gaia Sky.


<!--more-->

## Li'l Nebulae Detour

If every story should start at the beginning and be told in full, I must first relate how this little quest took a little detour at the beginning to explore the rendering of volume nebulae. The OP mentioned in the Codeberg issue that he also gets requests to fly into nebulae during his tours, and Gaia Sky only contained billboards so far. Since Gaia Sky already contained the necessary infrastructure to render ray-marched volumes using a screen quad in a post-processing effect, I decided that solving this issue first made sense, as it involved *much* less work.

I browsed through [shadertoy](https://shadertoy.com) in search for a good implementation of a ray-marched shader that I could use as a base for my nebulae. I found several, like the [Dusty Nebula 4](https://www.shadertoy.com/view/MsVXWW) by Duke, and the [Supernova Remnant](https://www.shadertoy.com/view/MdKXzc), also by Duke. This [Duke](https://www.shadertoy.com/user/Duke) guy seems to be the most prolific shadertoy author when it comes to large-scale dusty objects, and by a large margin. It's not even close, so props to him and thank you very much for your work. All of his shaders seem to be licensed under [CC-BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/deed.en), which is perfect for modification and reuse in Gaia Sky.

So, taking some of these shaders as a baseline, I created new ones for the *Cat's Eye* nebula, the *Hourglass* nebula, the *Trifid* nebula, the *Butterfly* nebula, and the *Crab* nebula, among others.

<figure class="fig-center">
<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/MfcBzH?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>
<figcaption>My implementation of Crab nebula (M1) in shadertoy.</figcaption>
</figure>

Once the shadertoy shaders were ready, I had to do a little more work on the post-processing ray-marching infrastructure to accommodate the new members. So far, I had only ever used it for the black holes.

## Back to Aurorae

[^cosmographia]: SPICE-Enhanced Comosgraphia Mission Visualization Tool, NAIF: https://naif.jpl.nasa.gov/naif/cosmographia.html
