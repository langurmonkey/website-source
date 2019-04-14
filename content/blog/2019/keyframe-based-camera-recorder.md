+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "programming", "camera", "opengl", "astronomy", "videos" ]
aliases = [ "/blog/keyframe-based-camera-recorder/" ]
date = "2019-03-01"
description = "Gaia Sky gets keyframe-based camera paths"
linktitle = ""
title = "Keyframe-based camera paths"
featuredalt = "Keyframe camera paths"
featuredpath = "date"
type = "post"
+++


During the last months I have been working on a QOL improvement for Gaia Sky video production. Currently, Gaia Sky offers a couple of ways to persist and reproduce camera behaviours: scripting and camera paths.

**Scripting** offers a high level API which allows for the interaction and manipulation of the internal state. Conceptually, a running script is no different from a regular user. A script runs in its own thread and, like a user, interacts with Gaia Sky's core through the event manager, a message-passing entity which encapsulates the core functionality.

**Camera paths** are very different from scripting in which they are integrated into the core and run synchronously with the main loop. Camera paths can be recorded at a given frame rate, producing a file which contains a series of camera states [position, orientation, time] and that can be played later on. Right now, the only way to record camera paths is by clicking on the record button in the GUI and directly interacting with the program with the keyboard+mouse or a gamepad to produced the desired behaviour in real time. This brings us to the new keyframe-based system.

## Keyframe-based paths

In the next version, Gaia Sky will get a brand new keyframe-based camera path mode. This mode enables the interactive definition of camera paths in the scene space. Basically, the user defines a set of locations, or keyframes, which must be hit by the camera at a certain time. Each keyframe contains the position and orientation of the camera, in addition to the simulation timestamp and time delay. Keyframes can be saved to keyframe files `.gkf`, which can later be loaded directly from the keyframes mode UI, and exported to regular Gaia Sky camera path files `.gsc` to be played back.

<a href="/img/2019/03/keyframes.jpg">
<img src="/img/2019/03/keyframes.jpg"
     alt="Keyframe-based camera paths"
     style="width: 70%" />
</a>

The conversion from keyframes to camera path is done using either linear interpolation or Catmull-Rom splines (depending on the configuration settings). In the latter case, keyframes can be set to act as seams. Seam keyframes effectively *break* the path into two. In spline mode, this allows us to define subpaths and avoid spline overshooting.

About the user interface, we put some effort into making sure the addition and edition of keyframes is easy from either the GUI or the 3D scene space itself. Individual keyframes are focusable (right click) and dragged around in the scene 3D space. Whenever a keyframe is in focus, the camera can rotate around it a zoom in/out as if it were any other scene object. Also, the orientation of every keyframe can be rotated around the direction vector (hold CTRL and drag mouse right), the up vector (hold SHIFT and drag mouse right), and around cross(direction, up) (hold ALT while dragging mouse right).

Below is an early video of the state as of a month ago:

<video width="70%" style="display: block; margin: auto;" controls>
  <source src="/img/2019/03/keyframes.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

<br/>
Obviously, this still need some work and polish, but It has the potential to be a much nicer and convenient way to define camera paths in certain situations. A couple of problems to be addressed come to mind:

- **Keyframe timing** - It is very difficult to adjust the keyframe time, as it should ideally depend on the distance between the current keyframe and the last. But this does not awlays work, as setting a constant camera speed is problematic in high distance range situations. Think of orbiting the Earth and then moving to Mars. You want the transition to Mars to happen smoothly with an ideally exponential dependency of speed upon distance to closest object (detach from Earth and attach to Mars halfway through). For that, the granularity (number of keyrames per unit space) must be just right, since the speed between two keyframes is essentially constant.

- Already hinted above, **distance range problem** - Usually, 3D scenes have a contained distance range which makes regular movements and speeds also contained. In the case of Gaia Sky, the distance range is vast and that causes problems with the camera velocity if the granularity of keyframes in a path is not right. A trip from Earth to the Moon in 10 seconds, setting one keyframe in each body, produces a constant speed of 30000 Km/s. And that is a very small system when compared to distances in the Solar System, or distances between stars, or distances between galaxies. Ideally, one would set a series of keyframes along the path where the camera speeds up and slows down. Is there a way to do this automatically?

All in all, I will release the next version of Gaia Sky with the keyframe camera recorder active and see if I get some feedback from users. Maybe nobody ever uses the system and it's pointless to improve it further, who knows.

