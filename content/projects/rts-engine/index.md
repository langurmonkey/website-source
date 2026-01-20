+++
categories = ["Projects"]
date = "2013-07-22"
tags = ["rts", "java", "game", "project"]
title = "RTS engine"
description = "A real time strategy game engine written in Java"
showpagemeta = "false"
+++

{{< notice Disclaimer >}}
This is a work-in-progress. The master branch is up to date with the latest development and may very possibly crash. Use it at your own risk.
{{</ notice >}}

**Repository:** [https://codeberg.org/langurmonkey/rts-engine](https://codeberg.org/langurmonkey/rts-engine)

This is an **RTS engine** project that I used to enjoy working on. It is a testing sandbox and does not have much focus.

{{< fig src="/img/rts/rts-engine.avif" title="Screenshot of the RTS engine running." width="60%" class="fig-center" loading="lazy" >}}

I started playing around with the idea as a time killer some years ago, kicking off the development with a fast version of the A* path-finding algorithm backed not by a grid (as usual) but by a quad-tree. Quad-trees make path-finding superfast because of their hierarchical division of space and their adaptive partition sizes. Even though I used visibility graphs to store the navigable nodes from one given point, quad-trees are also fast for checking the properties/elements of a position's surroundings, for child nodes are always spatially contained in parent nodes. However, the tree rebalancing operation is too costly, so I ended up implementing a regular grid based approach, which is the one in use today. A* is also quite fast in a regular grid.

Once I got this path-finding on a quad-tree thing up and running, It was time to implement the movement of my entities. I dove a bit into the topic and stumbled upon [Craig Reynolds steering behaviors](http://www.red3d.com/cwr/papers/1999/gdc99steer.html). They turned out to be an excellent method of implementing movement, but they come with caveats. I found these steering behaviors very powerful at producing organic-like movements that do not look forced at all. However, they are usually hard to implement and need A LOT of tweaking to really get them rolling. If you are interested in the topic you can check out Reynolds' original paper or take a look at the book "Programming game AI by example" by Matt Buckland.

It looks like LibGDX itself provides nowadays an implementation of steering behaviors, which is probably nicer than mine. I implemented my version before, so that's what is used in this project.

I wrote a [blog post](/blog/2013/rts-engine-preview) about this project.

## Current features

- Shiny, not so good looking 2D graphics.
- Backed by a fully 3D model.
- Real time selection and movement of units and groups.
- Unit life bars.
- Fog of war comes in two flavors: tile-based (bad) and mesh-based (awesome).
- Own implementation of steering behaviors that work (with a lot of tweaking).
- Zoom and pan freely.
- [Tiled](https://www.mapeditor.org) tile map integration.
- Quad-tree and regular grid implementations for spatial awareness.
- Some basic graphical and lighting effects.
- [Ashley ECS](https://github.com/libgdx/ashley) as entity component system.
- Pretty fast, above 500 FPS on decent hardware. Around 130 FPS on 7th gen Intel laptop graphics.
- Theoretically, Android support.

## Running

In order to run the RTS engine on the desktop, first clone the repository:

```bash
git clone https://codeberg.org/langurmonkey/rts-engine.git
cd rts-engine
```

Then, just run the following command:

```bash
$ gradlew desktop:run
```


## Video

Here is a video demonstrating a few of the features available as of now.

<div class="videowrapper">
<iframe id="odysee-iframe" width="90%" height="400" src="https://odysee.com/$/embed/rts-fogwar-zoom-pathfinding/16072a7fdd4569bc72d20494a7e471fbfd618e27?r=621u1MynW1hV1p9kTVvSiB3pZyjj9tJW" allowfullscreen></iframe>
</div>
<figcaption><h4>
A screencast of the RTS engine in all its glory.
</h4></figcaption>

## Licensing

This software is distributed under the [MIT](https://choosealicense.com/licenses/mit/) license.

