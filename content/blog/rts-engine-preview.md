+++
author = "Toni Sagrista Selles"
categories = [ "RTS engine" ]
tags = [ "programming", "game" ]
date = "2013-06-10"
description = "Video preview of Real Time Strategy engine"
linktitle = ""
title = "RTS engine preview"
featured = "rtspreview.jpg"
featuredalt = "RTS engine preview"
featuredpath = "date"
type = "post"
+++

Today I want to introduce a very different piece of software I have been putting together lately. It is a **RTS (real time strategy) engine**. I started playing with the idea as a time killer some years ago, kicking off the development with a fast version of the A* pathfinding algorithm backed not by a grid (as usual) but by a quadtree. **Quadtrees make pathfinding super-fast** because of their hierarchical division of space and their adaptive partition sizes. Even though I used visibility graphs to store the navigable nodes from one given point, **quadtrees are also fast for checking the properties/elements of a position's surroundings**, for child nodes are always spatially contained in parent nodes.

<!--more-->

Once I got this pathfinding on quadtree thing up and running, It was time to implement the movement of my entities. I dove a bit into the topic and stumbled upon [**Craig Reynolds' steering behaviours**](http://www.red3d.com/cwr/papers/1999/gdc99steer.html). They turned out to be an **excellent method of implementing movement**. I found these steering behaviours very powerful at producing organic-like movements that do not look forced at all. However, they are usually hard to implement and **need A LOT of tweaking** to really get them rolling. If you are interested in the topic you can check out Reynolds' original paper [here](http://www.red3d.com/cwr/papers/1999/gdc99steer.html) or have a look at the book `Programming game AI by example` by Mat Buckland. I highly recommend it, it is very comprehensive and well written, with clear examples and fun explanations, and it is packed with interesting stuff from cover to cover.

Abut the tech, I'm using Java as a programming language and started with Slick (http://slick.javaunlimited.net/) as a base framework but chose to migrate to libgdx (http://libgdx.badlogicgames.com/) because it is actively maintained and offers a more advanced functionality set. Maybe I'll post something one day about the migration process, which was worth it but wasn't easy at all. For the map I'm using the TMX tiled map format from Tiled (www.mapeditor.org) and the sprites uploaded by Daniel Cook from [Hard Vacuum](http://lunar.lostgarden.com/game_HardVacuum.htm).

I recorded a **short video** demonstrating some unit movement and the real time quadtree partitioning and pathfinding in action. As you may observe, it is still very early in its development but the basics are already there.

{{< youtube 17fDqcZ0mu8 >}}

If you are interested, the source code is public in this [GitHub repository](https://github.com/langurmonkey/rts-engine).
