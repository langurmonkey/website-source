+++
author = "Toni Sagrista Selles"
categories = [ "RTS engine" ]
tags = [ "programming", "game" ]
date = "2013-06-10"
description = "Video preview of Real Time Strategy engine"
linktitle = ""
title = "RTS engine preview"
featured = "rtspreview.jpg"
featuredalt = "Screenshot of my real-time strategy game engine featuring fog of war and several units."
featuredpath = "date"
type = "post"
+++

Today I want to introduce a very different piece of software I have been putting together lately. It is a [**RTS (real time strategy) engine**](https://codeberg.org/langurmonkey/rts-engine). I started playing with the idea as a time killer some years ago, kicking off the development with a fast version of the A\* pathfinding algorithm backed not by a grid (as usual) but by a quadtree. **Quadtrees make pathfinding super-fast** because of their hierarchical division of space and their adaptive partition sizes. Even though I used visibility graphs to store the navigable nodes from one given point, **quadtrees are also fast for checking the properties/elements of a position's surroundings**, for child nodes are always spatially contained in parent nodes.

<!--more-->

Once I got this path finding on quadtree thing up and running, It was time to implement the movement of my entities. I dove a bit into the topic and stumbled upon [**Craig Reynolds' steering behaviours**](http://www.red3d.com/cwr/papers/1999/gdc99steer.html). They turned out to be an **excellent method of implementing movement**. I found these steering behaviours very powerful at producing organic-like movements that do not look forced at all. However, they are usually hard to implement and **need A LOT of tweaking** to really get them rolling. If you are interested in the topic you can check out Reynolds' original paper [here](http://www.red3d.com/cwr/papers/1999/gdc99steer.html) or have a look at the book `Programming game AI by example` by Mat Buckland. I highly recommend it, it is very comprehensive and well written, with clear examples and fun explanations, and it is packed with interesting stuff from cover to cover.

Abut the tech, I'm using Java as a programming language and started with Slick (http://slick.javaunlimited.net/) as a base framework but chose to migrate to libgdx (http://libgdx.badlogicgames.com/) because it is actively maintained and offers a more advanced functionality set. Maybe I'll post something one day about the migration process, which was worth it but wasn't easy at all. For the map I'm using the TMX tiled map format from Tiled (www.mapeditor.org) and the sprites uploaded by Daniel Cook from [Hard Vacuum](http://lunar.lostgarden.com/game_HardVacuum.htm).

I recorded a **short video** demonstrating some unit movement and the real time quadtree partitioning and pathfinding in action. As you may observe, it is still very early in its development but the basics are already there.

{{< youtube 17fDqcZ0mu8 >}}

The source code is free software, published under the GPLv3 license. Find it in this <i class="fa fa-gitea"></i> [repository](https://codeberg.org/langurmonkey/rts-engine).

*Edit March 2021:*

I have since been working on this project on and off, especially lately, dusting it off and polishing it a lot. There is now a private fork with many more features, and most of the development efforts will be focused on that. However, the public repository will still host the open source project. The new features include arbitrary zoom ins and outs, an ECS-backed model (entity component system) or a lot of awareness features concerning the map and the units. Below is a video of the state of the project before the private fork was created.

<iframe id="lbry-iframe" width="100%" height="500" src="https://lbry.tv/$/embed/rts-fogwar-zoom-pathfinding/16072a7fdd4569bc72d20494a7e471fbfd618e27?r=621u1MynW1hV1p9kTVvSiB3pZyjj9tJW" allowfullscreen></iframe>

