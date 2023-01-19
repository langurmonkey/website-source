+++
author = "Toni Sagristà Sellés"
title = "Sparse Virtual Textures"
description = "My implementation of Sparse Virtual Textures in Gaia Sky"
categories = ["Computer Graphics"]
tags = ["gaia sky", "programming", "graphics", "opengl", "glsl", "svt", "megatexture", "english"]
date = "2023-01-19"
featured = "vt_earth_feature.jpg"
featuredalt = "Real time rendering of the Earth in Gaia Sky with surface, cloud and height virtual textures."
featuredpath = "date"
type = "post"
+++

Implementing proper virtual texture support in Gaia Sky has been on my to-do list for many years. And for many years I have feared that very item, as the virtual texture mechanism is notoriously hard to implement and to get right. However, once working, they are very cool. This post is a write-up about my implementation of virtual textures in Gaia Sky, and a detailed discussion about some of the most interesting details.  

<!-- More -->

## Basics on Sparse Virtual Textures

**Sparse Virtual Textures** (SVT), also known as **MegaTexture**[^3], and **Partially Resident Textures** (PRT)[^4], have at their core the idea of splitting large textures into several tiles and only streaming the necessary ones (i.e. the ones required to render the current view) to graphics memory in order to optimize memory usage and enable the display of textures so large that they can't be handled effectively by the graphics hardware.

This is a *relatively* new technique that aims at drastically increasing the size of usable textures in real time rendering applications by splitting them up in tiles and streaming only the *necessary* ones to graphics memory. It was initially described in a primitive form by Chris Hall in 1999[^1] and has subsequently been improved upon. My understanding is that most modern implementations are based on Sean Barret's GDC'08 talk on the topic[^2].

Virtual texturing is the CG memory counterpart to the operating system virtual memory. In virtual memory, a process' memory address space is divided into pages, which are moved in and out of a cache space depending on whether and when they are needed. In virtual texturing, textures (images) are split up into smaller tiles and paged in and out of a cache texture when needed. 

Virtual texturing requires some pre-processing to be done: the large texture needs to be split up into tiles. Ideally, these tiles have a 1:1 aspect ratio (i.e. are square). After that, we can use the SVT in our application with these few steps:

1. **Tile determination** -- first, we need to detect or determine what are the tiles that we actually need to render the current scene with the current camera position, orientation and field of view.
2. **Cache** -- then, use the information in the first step to fetch the observed tiles and put them into a *cache texture*, that we'll send to graphics memory.
3. **Indirection** -- after that, we update an indirection (lookup) table with the location of the tile in the cache, and also send it to graphics memory.
4. **Rendering** -- finally, we can use the cache and indirection textures to render our scene.




## More

OpenGL has some SVT extensions.



[^1]: Hall, C. --- Virtual Textures: Texture Management in Silicon [[pdf](https://www.graphicshardware.org/previous/www_1999/presentations/v-textures.pdf)].
[^2]: Barrett, S. --- Sparse Virtual Textures [[html](https://silverspaceship.com/src/svt/)].
[^3]: https://en.wikipedia.org/wiki/Id_Tech_4#MegaTexture_rendering_technology
[^4]: https://www.anandtech.com/show/5261/amd-radeon-hd-7970-review/6
