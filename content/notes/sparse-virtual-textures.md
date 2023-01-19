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

## Tile Visibility

We can determine the observed tiles by rendering the scene to an off-screen frame buffer with a special shader that computes the tile for each fragment. Since we are only interested in the tile data, we can get away with rendering to a downsized frame buffer. In my implementation, the tile determination frame buffer is 4 times smaller than the main render buffer in width and height (16 times smaller in area). This is probably still too large. This factor will be important later.

A first approach might be just outputting the \\((x,y)\\) coordinates of the tile, together with the tile id. In the following code we put the tile coordinates in the red and green channels, and the SVT id in the blue channel.

```glsl
uniform float u_svtId;
uniform vec2 u_svtDimensionInTiles;

in vec2 texCoords;

out vec4 fragColor;

void main() {
  fragColor.xy = floor(texCoords * u_svtDimensionInTiles);
  fragColor.z = u_svtId;
}
```

{{< fig src="/img/2023/01/tiledetect-nomipmap-l4.jpg" class="fig-center" width="55%" title="The tile determination pass frame buffer of the Earth with a virtual texture with 2048 (64x32, with a 2:1 virtual texture) tiles." loading="lazy" >}}

The image above shows the tile detection frame buffer (with channels scaled for visibility) for a virtual texture with 2048 tiles. This approach has some issues:

- No matter how close to or away from each fragment we are, we always end up hitting the same tile. 
- Since tiles are loaded on demand, when a tile is not yet available in the cache the system won't know what to render and leave a blank space.

The solution to both these problems is introducing levels of detail. In textures, levels of detail are implemented through mipmaps.

### Mipmapping

We modify our original formulation, and instead of dividing the texture into only a bunch of tiles that all cover the same area, we will generate a tree, with the whole texture at the root. Each level contains 4 times the amount of tiles that the level above, and each tile covers 4 times less area. The resolution of all tiles in all levels is still the same though. We have a quadtree!

{{< fig src="/img/2023/01/vt-lod.png" class="fig-center" width="65%" title="The different levels of subdivision in the virtual texture quadtree. Note that the first level (left) covers the whole area. Credit: Albert Julian Mayer." loading="lazy" >}}

In our quadtree, level 0 contains one or two tiles (depending on SVT aspect ratio) which cover the whole area (left tile in the image), and the level numbers for each tile indicate its depth. In the image, pictured left to right are levels 0, 1, 2 and 3.

If we incorporate the quadtree with different levels, the shader we showed before gets a bit more complicated. First of all, we need to determine the LOD level of the fragment. To do so, we could use the GLSL function `textureQueryLod(sampler2D s, vec2 texCoords)`, but we'd need a texture bound in that fragment shader, which we do not have. However, that function can be easily implemented with some partial derivatives,

$$\begin{eqnarray} 
D_x &=& \left(\frac{\partial u}{\partial x}, \frac{\partial v}{\partial x}\right), \\\\\\
D_y &=& \left(\frac{\partial u}{\partial y}, \frac{\partial v}{\partial y}\right), \\\\\\\\
L   &=& log_2(max(|D_x|, |D_y|)),
\end{eqnarray}$$

where \\(u\\) and \\(v\\) are the UV texture coordinates, and \\(x\\) and \\(y\\) are the window x and y coordinates. We can use `dFdx()` and `dFdy()`, which do precisely that, to get the mipmap level:

```glsl
float mipmapLevel(in vec2 texelCoord, in float bias) {
    vec2  dxVtc        = dFdx(texelCoord);
    vec2  dyVtc        = dFdy(texelCoord);
    float deltaMaxSqr  = max(dot(dxVtc, dxVtc), dot(dyVtc, dyVtc));
    return               0.5 * log2(deltaMaxSqr) + bias;
}
```

And then, we can implement the tile detection like this:

```glsl
uniform float u_svtId;
uniform float u_svtDepth;
uniform vec2 u_svtResolution;

in vec2 texCoords;

out vec4 fragColor;

// Scale factor of our tile detection frame buffer w.r.t. the window.
const float svtDetectionScaleFactor = -log2(4.0);

void main() {
    // Aspect ratio of virtual texture.
    vec2 ar = vec2(u_svtResolution.x / u_svtResolution.y, 1.0);

    // Get mipmap LOD level.
    float mip = clamp(floor(mipmapLevel(texCoords * u_svtResolution, svtDetectionScaleFactor)), 0.0, u_svtDepth);
    // In our tree, level 0 is the root.
    float svtLevel = u_svtDepth - mip;
    fragColor.w = svtLevel;

    // Compute tile XY at the current level.
    float nTilesLevel = pow(2.0, svtLevel);
    vec2 nTilesDimension =  ar * nTilesLevel;
    fragColor.xy = floor(texCoords * nTilesDimension);

    // ID.
    fragColor.z = u_svtId;
}
```

There are a few things to unpack here:

- The mipmap LOD level 0 is the base level with the highest resolution. This is reversed in our quadtree, where the level 0 is the root with the lowest pixel/unit area ratio. That is why we convert from mip level to SVT level using the tree depth.
- The `u_svtResolution` contains the base resolution of the SVT, i.e., the resolution of the deepest level.
- `nTilesDimension` contains the size of the level in tiles.
- Here, we put the tile coordinates in the red and green channels, the SVT id in the blue channel and the level in the alpha channel.
- Finally, the `svnDetectionScaleFactor` is computed from the frame buffer reduction factor with respect to the window (4). The area of a frame buffer scales with the square of the sides, so we use `log2()`. The factor is negative because we need to move to more detailed levels (closer to 0 in the mipmap LOD level scale) when rendering to a larger frame buffer.

{{< fig src="/img/2023/01/tiledetect-mipmap-l4.jpg" class="fig-center" width="55%" title="The tile determination pass frame buffer, with channels scaled for visibility, with LOD levels. The different levels show as rings on the Earth, starting with level 0 (outermost ring, darker), down to level 4 (innermost ring, brighter)." loading="lazy" >}}

### Frame Buffer Format

I use a frame buffer with a depth attachment and a floating point texture attachment with 32 bits per channel. This allows for \\(~2^{32}\\) values per channel, which provides ample precision to accommodate trees with up to 31 levels. To put this in perspective, if we map the Earth with a tree with 31 levels, each tile covers ~1cm. Any tile resolution greater than 100x100 provides sub-millimeter precision on the whole planet.

Note that, in order to be able to read back the pixels cleanly, we need to disable alpha blending, especially if we have concave objects or we support more than one SVT. Also, it is important to enable depth testing and attach a depth buffer to our frame buffer so that the depth test is performed.


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
