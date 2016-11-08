+++
author = "Toni Sagrista Selles"
categories = ["Particle Physics Simulator"]
tags = [ "android", "programming"]
date = "2011-11-24"
description = "New version 3.1 out now"
linktitle = ""
title = "Particle Physics Simulator 3.1 just released"
featured = "all-small.png"
featuredalt = "Particle Physics Simulator 3.1"
featuredpath = "date"
type = "post"
+++

The new version of the Particle Physics Simulator for Android, the **version 3.1.2**, has just been released to the Android Market. Among the several new features it contains, I'd like to single out the possibility to **change the mesh density in the Particle-Mesh mode**, and also the option to **display the mesh points**. Mesh density values range from 0 to 3, being 0 the less dense and 3 the denser. Increasing the mesh density means more mesh points scattered over the simulation area, where actual values of mass density are computed, which leads to a more accurate simulation with the drawback that it is also slower. Feel free to fiddle with the app, setting different mesh densities and observing how particles react to the new values. In the post image are the four mesh densities included in the simulator.

You may have also noticed that in these screenshots there are no particles. That's because now the starting number of particles can be set to 0, and the black hole does not count as one. This is cool to create particle systems from scratch, such as a couple of particles orbiting each other, or a system of particles and antiparticles.

Additionally, some other improvements have been made, like disabling the *pan* and *centering* buttons in the screen area mode and not allowing antiparticles in the particle-mesh mode. The latter is pretty obvious, for in this mode there are no particle-particle direct interactions and thus particles and antiparticles can't possibly 'detect' each other.
