+++
categories = ["projects"]
date = "2011-09-20"
tags = ["android", "physics", "simulator", "n-body"]
title = "Particle Physics Simulator"
description = "Fully-feature physics simulator in your pocket"
showpagemeta = "false"
+++

The **Particle Physics Simulator** is a physics application for [Android](http://www.android.com/) devices (v2.2+) in which real gravitational systems of particles can be created, simulated and interacted with in real time. It is an [N-body particle simulator](http://en.wikipedia.org/wiki/N-body_simulation) where the behaviour of the system is driven only by each particle's gravity and its interaction with all the other particles in it. It is turning more into a physics playground lately though, with the addition of accelcerometer support, elastic collisions, ability to create walls, anti-particles and more.

You can download the application from [Google Play](https://play.google.com/store/apps/details?id=com.tss.android). If you like it very much you can even [buy me a beer](/donate)!

![Particle Physics SImulator QR Code](http://qrcode.kaywa.com/img.php?s=6&d=https%3A%2F%2Fmarket.android.com%2Fdetails%3Fid%3Dcom.tss.android)

### Features

Follows the current list of features of the Particle Physics Simulator.

*   Real **n-body physics simulation**, pure gravitational interactions between particles.
*   Start with any number of particles from 2 to 100. Then you can add up to 200 particles in real time during the simulation.
*   Two force calculator methods:
    *   _Particle-Particle_, the direct method <img class="inline" src="https://chart.googleapis.com/chart?cht=tx&amp;chl=\sim O(n^2)">, which is very accurate but also computationally expensive.
    *   _Particle-Mesh_, where forces are calculated using a mesh of potnentials, very efficient <img class="inline" src="https://chart.googleapis.com/chart?cht=tx&amp;chl=\sim O(n \cdot log n)"> but not as accurate as PP.
*   Two simulation area modes:
    *   _Screen area_, which takes only the space of your cellphone screen.
    *   _Big area_, in which the simulation area extends well beyond the screen limits.
*   **Zoom** and **pan** in big simulation area mode.
*   Create **walls** particles can't trespass. Watch them bounce off. In the current version there is a top limit of 10 walls per simulation so that the performance does not decay.
*   Set the collision policy to **elastic collisions**, **mergers** or **no collisions** at all.
*   Choose particle **colours**.
*   Set **background** colour or image.
*   Set gravity strength and particle mass.
*   **Accelerometer support** enables for adding real-world gravity to the simulations.
*   Shoot particles or create repulsive forces using touch screen.
*   Also create **anti-particles**, which are repelled by regular particles but attracted between them.
*   Enable or disable the central **black hole** which exerts a neat attractive force towards the center. Also, you can change its appearance.
*   Enable or disable **particle trails**. Disable trails to improve performance, for computing and drawing trails is one of the more expensive operations.
*   Modify **simulation velocity** in real time using the top slider.
*   Display system information such as the number of particles and the frames per second.

### Videos

See [here](/pps/videos).

### Screenshots

<div style="text-align:center;">
<embed type="application/x-shockwave-flash" src="https://picasaweb.google.com/s/c/bin/slideshow.swf" width="350" height="622" flashvars="host=picasaweb.google.com&hl=en_US&feat=flashalbum&RGB=0x000000&feed=https%3A%2F%2Fpicasaweb.google.com%2Fdata%2Ffeed%2Fapi%2Fuser%2FToniNoni%2Falbumid%2F5661063123461778177%3Falt%3Drss%26kind%3Dphoto%26authkey%3DGv1sRgCIKK2-GDg5_4Zw%26hl%3Den_US" pluginspage="http://www.macromedia.com/go/getflashplayer"></embed>
</div>

### User guide

Go to Menu > Settings to change other preferences, such as:

*   The initial number of particles.
*   Display or not particle trails.
*   Use accelerometer to add real gravity to the simulation.
*   Set the simulation area to the screen or use a big area.
*   Enable particles to bounce-off simulation boundaries.
*   Display particle count and FPS.
*   Put a black hole in the center.
*   Select the collision policy to elastic collisions, mergers or no collisions at all.
*   Enable and disable collision effects.
*   Set the particle mass and gravity force.
*   Choose particle and background colours.


The on-screen controls of the Particle Physics Simulator available are the following:


<img src="/img/pps/pan.png" title="Pan" style="margin-left: 0"/>
**Pans the view**. Only works in the big simulation area mode.

<img src="/img/pps/shoot.png" title="Shoot" style="margin-left: 0"/>
**Enables shooting mode**, where particles can be shot into the screen. Tap once to shoot a regular particle. Tap twice to shoot an anti-particle, which is the same button but the particle has a spot inside.

<img src="/img/pps/repel.png" title="Repel" style="margin-left: 0"/>
**Enables the repelling mode**, which creates a repelling force to all particles at the position of your tap.

<img src="/img/pps/wall.png" title="Wall" style="margin-left: 0"/>
**Activates the wall mode**, with which you can create walls in real time that particles can't trespass.

<img src="/img/pps/center.png" title="Center" style="margin-left: 0"/>
**Resets the view** to its initial state of zoom and pan.

<img src="/img/pps/zoom.png" title="Zoom" style="margin-left: 0"/>
**Use two fingers to zoom in** the big simulation area mode. Separate fingers to zoom in, join them to zoom out.

<img src="/img/pps/velocity.png" title="Velocity" style="margin-left: 0"/>
**Use the upper slider bar to adjust the simulation velocity** in real time.


### Changelog

Find the changelog [here](/pps/changelog).
