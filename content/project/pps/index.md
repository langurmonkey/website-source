+++
categories = ["Particle Physics Simulator"]
date = "2011-09-20"
tags = ["android", "physics", "simulator", "n-body"]
title = "Particle Physics Simulator"
description = "Fully-feature physics simulator in your pocket"
showpagemeta = "false"
+++

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

The **Particle Physics Simulator** is a physics application for [Android](http://www.android.com/) devices (v2.2+) in which real gravitational systems of particles can be created, simulated and interacted with in real time. It is an [N-body particle simulator](http://en.wikipedia.org/wiki/N-body_simulation) where the behaviour of the system is driven only by each particle's gravity and its interaction with all the other particles in it. It is turning more into a physics playground lately though, with the addition of accelerometer support, elastic collisions, ability to create walls, anti-particles and more.

## Source code

The source code can be found in this <i class="fa fa-gitlab"></i> [Gitlab repository](https://gitlab.com/langurmonkey/particle-physics-sim).

## Download

Get the apk for the latest versions right here:

-  Particle Physics Simulator -- [apk 3.8.0](/apk/pps/nbodyandroid-3.8.0.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `3791dd08b688e688b4d99a848eb7f6d9e966296c468b0dcf556a78069d5ee2dd`</sup></sub>
-  Particle Physics Simulator -- [apk 3.7.4](/apk/pps/nbodyandroid-3.7.4.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `24297a48af13d9e9cbd8c159c36861c39e6f0b9b84c2e92d46838ccd58ae6a77`</sup></sub>
-  Particle Physics Simulator -- [apk 3.7.3](/apk/pps/nbodyandroid-3.7.3.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `4c6c598b4018d73df01edeaf2471cf00a4845fa9f51f613eb89833abbd377c85`</sup></sub>
-  Particle Physics Simulator -- [apk 3.7.2](/apk/pps/nbodyandroid-3.7.2.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `caddd8e1a3bc5fc8192d90dff8bd02b88f8a9c749475312822fb2608b387207b`</sup></sub>
-  Particle Physics Simulator -- [apk 3.7.1](/apk/pps/nbodyandroid-3.7.1.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `5da85b692b6d075abd67e93d399f8df7ce9f16d9dc1828ee69fb8ff126e656dd`</sup></sub>
-  Particle Physics Simulator -- [apk 3.7.0](/apk/pps/nbodyandroid-3.7.0.apk) &nbsp;&nbsp; <sub><sup>**sha256:** `954ca2e7a1d5d264cc423d61de547f14498d778997afc2c7ec9f195671df7a8b`</sup></sub>

Or get it from [F-Droid](https://f-droid.org/en/packages/com.tss.android/) or [Google Play](https://play.google.com/store/apps/details?id=com.tss.android).

## Changelog

Find the changelog [here](/pps/changelog).

## Features

Follows the current list of features of the Particle Physics Simulator.

*   Real **n-body physics simulation**, pure gravitational interactions between particles.
*   Start with any number of particles from 2 to 100. Then you can add up to 200 particles in real time during the simulation.
*   Two force calculator methods:
    *   _Particle-Particle_, the direct method \\(\sim O(n^2)\\), which is very accurate but also computationally expensive.
    *   _Particle-Mesh_, where forces are calculated using a mesh of potnentials, very efficient \\(\sim O(n \cdot log n)\\) but not as accurate as PP.
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

## Videos

See [here](/pps/videos).


## Screenshots


<div class="row">
  <div class="column">
    <a href="/img/pps/screenshots/particles01.png" style="float:left"><img src="/img/pps/screenshots/small/particles01.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles02.png" style="float:left"><img src="/img/pps/screenshots/small/particles02.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles03.png" style="float:left"><img src="/img/pps/screenshots/small/particles03.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles04.png" style="float:left"><img src="/img/pps/screenshots/small/particles04.png" /></a>
  </div>
</div>
<div class="row">
  <div class="column">
    <a href="/img/pps/screenshots/particles05.png" style="float:left"><img src="/img/pps/screenshots/small/particles05.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles06.png" style="float:left"><img src="/img/pps/screenshots/small/particles06.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles07.png" style="float:left"><img src="/img/pps/screenshots/small/particles07.png" /></a>
  </div>
  <div class="column">
    <a href="/img/pps/screenshots/particles08.png" style="float:left"><img src="/img/pps/screenshots/small/particles08.png" /></a>
  </div>
</div>

## User guide

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


<img src="/img/pps/pan.png" title="Pan" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Pans the view**. Only works in the big simulation area mode.

<img src="/img/pps/shoot.png" title="Shoot" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Enables shooting mode**, where particles can be shot into the screen. Tap once to shoot a regular particle. Tap twice to shoot an anti-particle, which is the same button but the particle has a spot inside.

<img src="/img/pps/repel.png" title="Repel" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Enables the repelling mode**, which creates a repelling force to all particles at the position of your tap.

<img src="/img/pps/wall.png" title="Wall" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Activates the wall mode**, with which you can create walls in real time that particles can't trespass.

<img src="/img/pps/center.png" title="Center" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Resets the view** to its initial state of zoom and pan.

<img src="/img/pps/zoom.png" title="Zoom" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Use two fingers to zoom in** the big simulation area mode. Separate fingers to zoom in, join them to zoom out.

<img src="/img/pps/velocity.png" title="Velocity" style="margin-left: 0; margin-right: 1em; float: left"></img>
**Use the upper slider bar to adjust the simulation velocity** in real time.

<a href="#privacy-polciy"></a>

# Privacy policy

The Particle Physics Simulator and the N-Body Live Wallpaper do not collect any user data or contain any trackers. It does not serve advertisements or start any internet connection. In this sense, it is a fully privacy respecting application. You can inspect the source code or build it yourself if you like.
