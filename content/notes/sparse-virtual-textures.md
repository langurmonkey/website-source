+++
author = "Toni Sagristà Sellés"
title = "Sparse Virtual Textures"
description = "My implementation of Sparse Virtual Textures in Gaia Sky"
categories = ["Computer Graphics"]
tags = ["gaia sky", "technical", "programming", "graphics", "opengl", "glsl", "svt", "megatexture", "english"]
date = "2023-01-19"
featured = "vt_earth_feature.jpg"
featuredalt = "Real time rendering of the Earth in Gaia Sky with surface, cloud and height virtual textures."
featuredpath = "date"
type = "post"
+++

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

Implementing proper virtual texture support in Gaia Sky has been on my to-do list for many years. And for many years I have feared that very item, as the virtual texture mechanism is notoriously hard to implement and to get right. However, once working, they are very cool. This post is a write-up about my implementation of virtual textures in Gaia Sky, and a detailed discussion about some of the most interesting details. If you need to know how to define or use virtual texture datasets in Gaia Sky, please refer to the [official documentation](https://gaia.ari.uni-heidelberg.de/gaiasky/docs). 

<!-- More -->

## Overview

**Sparse Virtual Textures** (SVT), also known as **MegaTexture**[^3], and **Partially Resident Textures** (PRT)[^4], have at their core the idea of splitting large textures into several tiles and only streaming the necessary ones (i.e. the ones required to render the current view) to graphics memory in order to optimize memory usage and enable the display of textures so large that they can't be handled effectively by the graphics hardware.

This is a *relatively* new technique that aims at drastically increasing the size of usable textures in real time rendering applications by splitting them up in tiles and streaming only the *necessary* ones to graphics memory. It was initially described in a primitive form by Chris Hall in 1999[^1] and has subsequently been improved upon. My understanding is that most modern implementations are based on Sean Barret's [GDC 2008 talk](https://silverspaceship.com/src/svt/) on the topic[^2].

## How Do They Work?

Virtual texturing is the CG memory counterpart to the operating system virtual memory. In virtual memory, a process' memory address space is divided into pages, which are moved in and out of a cache space depending on whether and when they are needed. In virtual texturing, textures (images) are split up into smaller tiles and paged in and out of a cache texture when needed. 

Virtual texturing requires some pre-processing to be done, as the large texture needs to be split up into tiles beforehand. The tiles in my implementation need to have a 1:1 aspect ratio (i.e. must be square). After that, we can use the SVT in our application with these few steps:

1. **Tile determination** -- first, we need to detect or determine what are the tiles that we actually need to render the current scene with the current camera position, orientation and field of view.
2. **Cache** -- then, use the information in the first step to fetch the observed tiles and put them into a *cache texture*, that we'll send to graphics memory.
3. **Indirection** -- after that, we update an *indirection (lookup) table* with the location of the tile in the cache, and also send it to graphics memory.
4. **Rendering** -- finally, we can use the cache and indirection textures to render our scene.

## Tile Determination Pass

## Tile Cache

## Indirection Table

Possibilities:

- Updating all lower levels when a tile is added.
- Use mipmaps with the indirection texture. Loop in the fragment shader, querying higher mipmap levels in the indirection table until a valid tile is found.

## Additional Coolness

- Tessellation shaders to query the SVT for height data.
- Structure to allow multiple SVTs on a single object for the different maps (diffuse, specular, normal, elevation, emissive, metallic, roughness, clouds).

## Limitations

Here are some of the limitations with my implementation I can think of:

- Due to the fact that all SVTs in the scene share the same cache, right now we can't have SVTs with different tile sizes in the same scene.
- Similarly, only square tiles are supported. Actually, I can't think of a single good use case for non-square tiles.
- Supported virtual texture aspect ratios are \\(n:1\\), with \\(n\geq1\\). This is due to the fact that VT quadtrees are square by definition (\\(1:1\\)), and we have an array of root quadtree nodes that stack horizontally in the tree object. It is currently not possible to have a VT with a greater height than width.
- Performance is not very good, especially with many SVTs running at once. This may be due to the shader mimpmap level lookups. This produces $depth$ texture lookups (mipmap levels) in the worst-case scenario when only the root node is available in the cache. A workaround would be to fill lower levels, additionally to the tile level, in the indirection buffer whenever a tile enters the cache. This would also have a (CPU) overhead. Might be faster.
- All SVTs in the scene share the same tile detection pass. This means that there is only one render operation in that pass.
- Still need to figure out exactly how the tile detection buffer affects the determined tile levels.

## More

If you want to read more on the topic or expand on what is described here, I suggest the following resources.

- Albert Julian Mayer's [master thesis](https://www.cg.tuwien.ac.at/research/publications/2010/Mayer-2010-VT/) on the topic is a very good academic resource which thoroughly describes the technique and discusses several topics in detail. I have used it as a valuable resource in my implementation.
- OpenGL defines `ARB_sparse_texture`[^20], a vendor-agnostic extension for virtual texturing. I have not used it in my implementation, but probably could. It is based on an original extension by AMD, `AMD_sparse_texture`[^21]. [Here](http://www.tinysg.de/techGuides/tg9_prt2.html) is a nice comparison.



[^1]: Hall, C. --- Virtual Textures: Texture Management in Silicon [[pdf](https://www.graphicshardware.org/previous/www_1999/presentations/v-textures.pdf)].
[^2]: Barrett, S. --- Sparse Virtual Textures [[html](https://silverspaceship.com/src/svt/)].
[^3]: https://en.wikipedia.org/wiki/Id_Tech_4#MegaTexture_rendering_technology
[^4]: https://www.anandtech.com/show/5261/amd-radeon-hd-7970-review/6
[^20]: `ARB_sparse_texture` [extension documentation](https://registry.khronos.org/OpenGL/extensions/ARB/ARB_sparse_texture.txt).
[^21]: `AMD_sparse_texture` [extension documentation](https://registry.khronos.org/OpenGL/extensions/AMD/AMD_sparse_texture.txt).
