+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = ["opengl", "gaiasky", "rendering", "stars", "english"]
date = 2021-10-24
linktitle = ""
title = "Variable stars and new render systems"
description = "What is currently going on in Gaia Sky development?"
featuredpath = "date"
type = "post"
+++

In the past few weeks I have been implementing a couple of features into Gaia Sky. The first is the addition of variable star rendering. The second is the re-implementation of all point cloud render systems to use actual geometry (triangles) instead of point primitives. This post briefly offers a preview of these features.

<!--more-->

## Variable stars

This is quite straightforward. Instead of representing a star with a single static magnitude, we use the light curve (time series) and fold it with the period into a phase diagram. Then, we anchor it in time using its epoch. All this data is then sent into the shader as new vertex attributes for each star. The shader then finds the right point in the phase diagram and interpolates the right magnitude to render at every frame.

Star time series in the Gaia DR2 catalog can be pretty big, with some having over 50 data points. GLSL only guarantees 16 4-component attributes per vertex. That is 64 floating-pont values per vertex. If we subtract all the data we need for position, proper motion, color, etc. we're left with roughly 10 `vec4` attributes, or 20 data points (each data point has a time and a magnitude). This means that we need to re-sample the light curves of all stars with more than 20 data points, and that is an overwhelming majority of them. Note that this is only done once when the catalog is being loaded. Below is a video of what the final feature looks like ([source](https://gaia.ari.uni-heidelberg.de/gaiasky/files/videos/20211019_variables_static)).

<video width="60%" style="display: block; margin: auto;" controls>
  <source src="https://gaia.ari.uni-heidelberg.de/gaiasky/files/videos/20211019_variables_static/20211019_variables_static.mp4" type="video/mp4"></source>
Your browser does not support the video tag.
</video>

## Point cloud render systems

Since we started using `GL_POINTS` for rendering point clouds (stars, particles, etc.), I have been aware that there were problems with the projection and re-projection with the cubemap mode. The solution was to rewrite the rendering systems so that all objects that used point primitives use now triangles which are billboard-oriented in the shaders. This provides consistent geometry through any re-projection. In the video below I compare the old mode with the new one. Especially look at the transitions between cubemap faces (marked with yellow lines). In the old method, the seams are clearly visible and the orientation of stars changes from face to face. The new mode does not have this problem.

<div class="videowrapper">
<iframe id="lbry-iframe" width="80%" height="500" src="https://odysee.com/$/embed/cubemap-quads/fe088e204f70dd93defd1829bb04cb08c6298e81?r=621u1MynW1hV1p9kTVvSiB3pZyjj9tJW" allowfullscreen></iframe>
</div>

I have implemented two versions for each system---three if we count the old point-base systems. Which one will be the default is subject to upcoming performance and memory tests.

1. **Direct vertex buffers with VAOs**, where all vertices and attributes are passed in buffers. This is kind of wastful, as it multiplies the memory by a factor of a little over 4, since now each star has 4 vertices, and 6 indices. All vertex attributes (star position, proper motion, magnitudes, etc.) need to be replicated for each vertex.
2. **[Instancing](https://learnopengl.com/Advanced-OpenGL/Instancing)**. In this mode, I am only sending 6 vertices (for the two triangles that compose a quad) in total. They contain the vertex position and the texture coordinates. Then, the rest of attributes (object position, proper motion, color, magnitude, etc.) are stored in buffers and sent to the GPU once per instance. This does not waste any memory and so far it is the most promising mode for obvious reasons.
3. **Good old points**. This is what is already implemented as of Gaia Sky `3.1.6`.

Now, so far I have observed that the new rendering with the straightforward VAOs (no instancing) is a tad faster when run with decent hardware, but it slows down to a crawl on less powerful devices. Still need to do more tests, but the instancing looks promising so far.

## Conclusion

These two features still have to mature a bit, especially the new render systems. They will hopefully make it into the next release of Gaia Sky.
