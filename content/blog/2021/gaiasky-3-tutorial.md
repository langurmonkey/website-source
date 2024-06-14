+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "programming", "opengl", "release", "version", "english", "tutorial", "gaia sky" ]
date = 2021-03-16
linktitle = ""
title = "Gaia Sky 3 tutorial for complete beginners"
featuredpath = "date"
type = "post"
+++

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

In this post, I'm mirroring the Gaia Sky 3 tutorial I wrote for the official [Gaia Sky documentation](https://gaia.ari.uni-heidelberg.de/gaiasky/docs) to use as a rough script for the workshop given in a splinter session of the 2021 DPAC consortium online meeting held on March 17 and 18, 2021. You can find the original page [here](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/workshops/dpac-plenary-online-2021.html).

{{< hint >}}
This article is best viewed in **light mode**: <a href="javascript:darkModeToggle()">lights on</a>!
{{</ hint >}}

<!--more-->

The main aim of this tutorial is to provide a comprehensive introduction on the usage of the most common features of Gaia Sky (versions 3 and up). By the end of the tutorial you will be able to:

- Use the basic controls to navigate the scene
- Find your way around the Gaia Sky user interface
- Locate basic information like the current focus, the nearest object to the camera, etc.
- Display and understand the debug information panel
- Activate/deactivate time and change the time warp factor
- Change camera modes and camera settings
- Use the special render modes (3D, planetarium, 360)
- Enable/disable components' visibility
- Show and modify the properties of proper motion vectors
- Control star appearance using the visual settings panel
- Load additional datasets in ``.vot``, ``.csv`` or ``.fits``
- Hide/show and highlight datasets, and map attributes to color
- Apply basic filters to datasets
- Use the archive view and the extra information panel
- Record and play back a camera file
- Use keyframes to define a camera path
- Write and run very basic Python scripts using the Gaia Sky API

This tutorial does **not** deal with the following items:

- Installation in different operating systems
- Performance tuning and optimization (memory, GPU, etc.)
- Data descriptors and formats
- Internal workings of Gaia Sky
- Internal reference system
- Level-of-detail catalogs
- VR mode setup and configuration
- System folders (location, content, etc.)
- Running Gaia Sky from source, CLI arguments, etc.
- In-depth video production
- Bookmarking system
- Connecting Gaia Sky instances in master-slave configuration
- Multi-display setups, dome, MPCDI, etc.
- External view mode

*Estimated duration:* 1.5 hours

## Before starting...

In order to follow the course it is recommended, albeit not required, to have a local installation of Gaia Sky so that you can explore and try out the teachings for yourself. In order to install Gaia Sky, follow the instructions for your operating system in [the installation section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Installation.html#installation) of the Gaia Sky documentation.


When you start Gaia Sky for the first time, you will be greeted with the welcome screen pictured below. Initially the <kbd>Start Gaia Sky</kbd> button will be {{< sp gray >}}grayed out{{</ sp >}}, as you need to download the data packages before Gaia Sky can start. To do so, click on the <kbd>Dataset manager</kbd> button.


{{< fig src="/img/2021/03/gs-tut/welcome-initial.jpg" link="/img/2021/03/gs-tut/welcome-initial.jpg" title="Welcome window at the first start of Gaia Sky." class="fig-center" width="60%" loading="lazy" >}}

Then select at least the following data packages:

- ``Base data pack`` -- Should be selected by default, contains the Solar System and some other basic data
- ``Gaia eDR3 small``, ``Hipparcos`` or another star catalog -- The star catalog. Note that usually only one star catalog should be loaded at once. {{< sp blue >}}The Gaia eDR3 catalogs for Gaia Sky already contain Hipparcos!{{</ sp >}}
- ``NBG catalog`` -- Nearby Galaxies Catalog
- ``SDSS DR12`` (small) or ``SDSS DR14`` (large) -- Sloan Digital Sky Survey catalog, distant galaxies
- ``Open Clusters DR2`` -- Open clusters catalog based on DR2 data
- ``Nebulae`` -- Some nebulae textures

{{< fig src="/img/2021/03/gs-tut/welcome-download.jpg" link="/img/2021/03/gs-tut/welcome-download.jpg" title="The download manager of Gaia Sky." class="fig-center" width="60%" loading="lazy" >}}

Then click on <kbd>Download selected</kbd> and wait for Gaia Sky to download and extract your catalogs. Once the downloads have finished, close the window  with <kbd>Ok</kbd>. Then you can go ahead and start Gaia Sky by clicking on <kbd>Start Gaia Sky</kbd>. 

{{< hint >}}
By default **Gaia Sky automatically selects all downloaded packages** for you. However, you can override this by selecting/unselecting packages each session using the <kbd>Dataset selection</kbd> button in the welcome screen.
{{</ hint >}}


## Basic controls

When Gaia Sky is ready to go, you will be presented with this screen:

{{< fig src="/img/2021/03/gs-tut/ui-initial.jpg" link="/img/2021/03/gs-tut/ui-initial.jpg" title="Gaia Sky default scene" class="fig-center" width="60%" loading="lazy" >}}

In it you can see a few things already. To the right the **focus panel** tells you that you are in focus mode, meaning that all our movement is relative to the focus object. The default focus of Gaia Sky is the Earth. You can also see in the **quick info bar** at the top that our focus is the {{< sp green >}}Earth{{</ sp >}}, and that the closest object to our location is also the {{< sp blue >}}Earth{{</ sp >}}. Additionally you see that your home object is again the {{< sp orange >}}orange{{</ sp >}}. Finally the **control panel** is collapsed at the top left. If you click on it, the panel opens. We will use it later.

### Movement

But right now let's try some movement. In **focus mode** the camera will by default orbit around the focus object. **Try clicking and dragging with your left mouse button**. The camera should orbit around the Earth showing parts of the surface which were previously hidden. You will notice that the whole scene rotates. Now **try scrolling with your mouse wheel**. The camera will move either farther away from (scroll down) or closer up to (scroll up) the Earth. Now, if you **click and drag with your right mouse button**, you can offset the focus object from the center, but your movement will still be relative to it.

You can also use your keyboard arrows <kbd>←</kbd> <kbd>↑</kbd> <kbd>→</kbd> <kbd>↓</kbd> to orbit left or right around the focus object, or move closer to or away from it.

You can use <kbd>shift</kbd> with a **mouse drag** in order to roll the camera. 

More information on the controls is available in the [controls section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Controls.html#controls) of the Gaia Sky user manual.

### Selection

You can change the focus by simply **double clicking** on any object on the scene. You can also press <kbd>f</kbd> to bring up the **search** dialog where you can look up objects by name. Try it now. Press <kbd>f</kbd> and type in "mars", without the quotes, and hit <kbd>esc</kbd>. You should see that the camera now points in the direction of {{< sp red >}}Mars{{</ sp >}}. To actually go to {{< sp red >}}Mars{{</ sp >}} simply scroll up until you reach it, or click on the {{< img "/img/2021/03/gs-tut/go-to.png" >}} icon next to the name in the focus info panel. If you do so, Gaia Sky takes control of the camera and brings you to {{< sp red >}}Mars{{</ sp >}}. 

If you want to move instantly to your current focus object, hit <kbd>ctrl</kbd> + <kbd>g</kbd>.

At any time you can use the <kbd>home</kbd> key in your keyboard to return back to Earth or whatever {{< sp orange >}}home{{</ sp >}} object you have defined in the [configuration file](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Properties-file.html#properties-file).

## The User Interface

The user interface of Gaia Sky consists of basically two components: keyboard shortcuts and a graphical user interface in the form of the **control panel**.

{{< fig src="/img/2021/03/gs-tut/ui-all.jpg" link="/img/2021/03/gs-tut/ui-all.jpg" title="Gaia Sky user interface with the most useful functions." class="fig-center" width="60%" loading="lazy" >}}

### Control panel

{{< hint >}}
The control panel is described in detail in [its own section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Control-panel.html#user-interface) of the Gaia Sky user manual.
{{</ hint >}}

The control panel is made up of different panes: *Time*, *Camera*, *Type visibility*, *Visual settings*, *Datasets*, *Bookmarks* and *Music*. In this tutorial we will only explore the first six. Each pane can be **expanded** (with {{< img "/img/2021/03/gs-tut/iconic-caret-right.png" >}}), **collapsed** (with {{< img "/img/2021/03/gs-tut/iconic-caret-bottom.png" >}}) and **detached** (with {{< img "/img/2021/03/gs-tut/detach-icon.png" >}}).

To the bottom of the control panel we can find a few buttons to perform special actions like:

- <i class="fa fa-map-o"></i> Toggle the minimap
- <i class="fa fa-folder-open"></i> Load a dataset
- <i class="fa fa-gear"></i> Open the preferences window
- <i class="fa fa-file-o"></i> Show the session log
- <i class="fa fa-question"></i> Show the help dialog
- <i class="fa fa-close"></i> Exit Gaia Sky

### Quick info bar

To the top of the screen you can see the **quick info bar** which provides information on the current time, the {{< sp green >}}current focus{{</ sp >}} object (if any), the {{< sp blue >}}current closest{{</ sp >}} object to our location and the {{< sp orange >}}current home{{</ sp >}} object. The colors of these objects ({{< sp green >}}green{{</ sp >}}, {{< sp blue >}}blue{{</ sp >}}, {{< sp orange >}}orange{{</ sp >}}) correspond to the colors of the crosshairs. The crosshairs can be enabled or disabled from the interface tab in the preferences window (use <kbd>p</kbd> to bring it up).


### Debug panel

Gaia Sky has a built-in debug information panel that provides system information and is hidden by default. You can bring it up with <kbd>ctrl</kbd> + <kbd>d</kbd>, or by ticking the "*Show debug info*" check box in the system tab of the preferences window. By default, the debug panel is collapsed.

{{< fig src="/img/2021/03/gs-tut/debug-collapsed.jpg" link="/img/2021/03/gs-tut/debug-collapsed.jpg" title="Collapsed debug panel." class="fig-center" loading="lazy" >}}

You can expand it with the ``+`` symbol to get additional information.

{{< fig src="/img/2021/03/gs-tut/debug-expanded.jpg" link="/img/2021/03/gs-tut/debug-expanded.jpg" title="Expanded debug panel." class="fig-center" width="60%" loading="lazy" >}}

As you can see, the debug panel shows information on the current graphics device, system and graphics memory, the amount of objects loaded and on display, the octree (if a LOD dataset is in use) or the SAMP status.

Additional debug information can be obtained in the system tab of the help dialog (<kbd>?</kbd> or <kbd>h</kbd>).

## Time controls

Gaia Sky can simulate time. Play and pause the simulation using the {{< img "/img/2021/03/gs-tut/play-icon.png">}}/{{< img "/img/2021/03/gs-tut/pause-icon.png">}} `Play`/`Pause` buttons in the time pane, or toggle using <kbd>Space</kbd>. You can also change the time warp, which is expressed as a scaling factor, using the provided **Warp factor** slider. Use <kbd>,</kbd> or {{< img "/img/2021/03/gs-tut/minus-icon.png">}} and <kbd>.</kbd> or {{< img "/img/2021/03/gs-tut/plus-icon.png">}} to divide by 2 and double the value of the time warp, respectively.

{{< fig src="/img/2021/03/gs-tut/warp-factor.jpg" link="/img/2021/03/gs-tut/warp-factor.jpg" title="Warp factor slider." class="fig-center" loading="lazy" >}}


Now, go ahead and press <kbd>home</kbd>. This will bring us back to Earth. Now, start the time with {{< img "/img/2021/03/gs-tut/play-icon.png">}} or <kbd>space</kbd> and **drag the slider slightly to the right** to increase its speed. You will see that the Earth rotates faster and faster as you move the slider to the right. Now, **drag it to the left** until time is reversed and the Earth starts rotating in the opposite direction. Now time is going backwards!

If you set the time warp high enough you will notice that as the bodies in the Solar System start going crazy, the stars start to slightly move. That's right: Gaia Sky also simulates proper motions.

## Camera modes

We have already talked about the **focus camera mode**, but Gaia Sky provides many more [camera modes](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Camera-modes.html#camera-modes):

- <kbd>0</kbd> - **Free mode**: the camera is not locked to a focus object and can roam freely. The movement is achieved with the scroll wheel of your mouse, and the view is controlled by clicking and draggin the left and right mouse buttons
- <kbd>1</kbd> - **Focus mode**: the camera is locked to a focus object and its movement depends on it
- <kbd>2</kbd> - **Game mode**: similar to free mode but the camera is moved with <kbd>w</kbd><kbd>a</kbd><kbd>s</kbd><kbd>d</kbd> and the view (pitch and yaw) is controlled with the mouse. This control system is commonly found in FPS (First-Person Shooter) games on PC
- <kbd>3</kbd> - **Gaia mode**: the camera can't be controlled, as it follows Gaia only
- <kbd>4</kbd> - **Spacecraft mode**: take control of a spacecraft (outside the scope of this tutorial)
- <kbd>5</kbd>, <kbd>6</kbd>, <kbd>7</kbd>  - **Fov modes**: project the fields of view of Gaia on the screen

The most interesting mode is **free mode** which lets us roam freely. Go ahead and press <kbd>0</kbd> to try it out. The controls are a little different from those of **focus mode**, but they should not be to hard to get used too. Basically, use your **left mouse button** to yaw and pitch the view, use <kbd>shift</kbd> to roll, and use the **right mouse button** to pan.


## Special render modes

There are three special render modes: [3D mode](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Stereoscopic-mode.html#d-mode), [planetarium mode](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Planetarium-mode.html#planetarium-mode) and [panorama mode](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Panorama-mode.html#panorama-mode). You can access these modes using the buttons at the bottom of the camera pane or the following shortcuts:

- {{< img "/img/2021/03/gs-tut/3d-icon.png" >}} or <kbd>ctrl</kbd> + <kbd>s</kbd> - 3D mode
- {{< img "/img/2021/03/gs-tut/dome-icon.png" >}} or <kbd>ctrl</kbd> + <kbd>p</kbd> - Planetarium mode
- {{< img "/img/2021/03/gs-tut/cubemap-icon.png" >}} or <kbd>ctrl</kbd> + <kbd>k</kbd> - Panorama mode

## Toggle visibility of components

The visibility of most graphical elements can be switched off and on using the buttons in the **type visibility pane** in the control panel.
For example you can hide the stars by clicking on the
``stars`` {{< img "/img/2021/03/gs-tut/ct/icon-elem-stars.png" >}} button. The object types available are the following:

-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-stars.png" >}} -- Stars
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-planets.png" >}} -- Planets
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-moons.png" >}} -- Moons
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-satellites.png" >}} -- Satellites
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-asteroids.png" >}} -- Asteroids
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-clusters.png" >}} -- Star clusters
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-milkyway.png" >}} -- Milky Way
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-galaxies.png" >}} -- Galaxies
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-nebulae.png" >}} -- Nebulae
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-meshes.png" >}} -- Meshes
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-equatorial.png" >}} -- Equatorial grid
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-ecliptic.png" >}} -- Ecliptic grid
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-galactic.png" >}} -- Galactic grid
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-labels.png" >}} -- Labels
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-titles.png" >}} -- Titles
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-orbits.png" >}} -- Orbits
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-locations.png" >}} -- Locations
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-countries.png" >}} -- Countries
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-constellations.png" >}} -- Constellations
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-boundaries.png" >}} -- Constellation boundaries
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-ruler.png" >}} -- Ruler
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-effects.png" >}} -- Particle effects
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-atmospheres.png" >}} -- Atmospheres
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-clouds.png" >}} -- Clouds
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-axes.png" >}} -- Axes
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-arrows.png" >}} -- Velocity vectors
-  {{< img "/img/2021/03/gs-tut/ct/icon-elem-others.png" >}} -- Others

### Velocity vectors

One of the elements, the **velocity vectors**, enable a few properties when selected. See the [velocity vectors section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Control-panel.html#velocityvectors) in the Gaia Sky user manual for more information on that.

*  **Number factor** -- control how many velocity vectors are rendered. The stars are sorted by magnitude (ascending) so the brightest stars will get velocity vectors first
*  **Length factor** -- length factor to scale the velocity vectors
*  **Color mode** -- choose the color scheme for the velocity vectors
*  **Show arrowheads** -- Whether to show the vectors with arrow caps or not

{{< hint >}}
Control the width of the velocity vectors with the **line width** slider in the **visual settings** pane.
{{</ hint >}}

{{< fig src="/img/2021/03/gs-tut/velocity-vectors.jpg" link="/img/2021/03/gs-tut/velocity-vectors.jpg" title="Velocity vectors in Gaia Sky" class="fig-center" width="60%" loading="lazy" >}}

## Visual settings

The **visual settings** pane contains a few options to control the shading of stars and other elements:

-  **Brightness power** -- exponent of power function that controls the brightness of stars. Makes bright stars brighter and faint stars fainter
-  **Star brightness** -- control the brightness of stars
-  **Star size (px)** -- control the size of point-like stars
-  **Min. star opacity** -- set a minimum opacity for the faintest stars
-  **Ambient light** -- control the amount of ambient light. This only
   affects the models such as the planets or satellites
-  **Line width** -- control the width of all lines in Gaia Sky (orbits, velocity vectors, etc.)
-  **Label size** -- control the size of the labels
-  **Elevation multiplier** -- scale the height representation for planets with elevation maps

{{< fig src="/img/2021/03/gs-tut/visual-settings.jpg" link="/img/2021/03/gs-tut/visual-settings.jpg" title="The visual settings pane." class="fig-center" loading="lazy" >}}

## Loading external datasets

Gaia Sky supports the loading of external datasets at runtime. Right now, ``VOTable``, ``csv`` and ``FITS`` formats are supported. Gaia Sky needs some metadata in the form of UCDs or column names in order to parse the dataset columns correctly. Refer to the [STIL data provider section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/SAMP.html#stil-data-provider) of the Gaia Sky user manual for more information on how to prepare your dataset for Gaia Sky.

The datasets loaded in Gaia Sky at a certain moment can be found in the [datasets](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Datasets.html#datasets) pane of the control panel.

{{< fig src="/img/2021/03/gs-tut/ds-1.jpg" link="/img/2021/03/gs-tut/ds-1.jpg" title="Datasets pane of Gaia Sky." class="fig-center" width="60%" loading="lazy" >}}

There are three main ways to load new datasets into Gaia Sky:

* Directly from the UI, using the <i class="fa fa-folder-open"></i> button or pressing <kbd>ctrl</kbd> + <kbd>o</kbd>
* Through SAMP, via a connection to another astronomy software package such as Topcat or Aladin
* Via a script (addressed later on in the workshop if time allows)

**Loading a dataset from the UI** -- Go ahead and remove the current star catalog (either eDR3 or hipparcos) by clicking on the <i class="fa fa-trash"></i> icon in the datasets pane. Now, download a raw [Hipparcos dataset VOTable](https://gaia.ari.uni-heidelberg.de/gaiasky/files/catalogs/hip/hipparcos.vot), click on the <i class="fa fa-folder-open"></i> icon (or press <kbd>ctrl</kbd> + <kbd>o</kbd>) and select the file. In the next dialog just click <kbd>Ok</kbd> to start loading the catalog. In a few moments the Hipparcos new reduction dataset should be loaded into Gaia Sky.

**Loading a dataset via SAMP** -- This section presupposes that Topcat is installed on the machine and that the user knows how to use it to connect to the VO to get some data. The following video demonstrates how to do this ([mirror](https://youtu.be/sc0q-VbeoPE)):

{{< fig src="/img/2021/03/gs-tut/samp.jpg" link="/img/2021/03/gs-tut/samp.jpg" title="Loading a dataset from Topcat through SAMP (click for video)." class="fig-center" width="50%" loading="lazy" >}}

**Loading a dataset via scripting** -- Wait for the scripting section of this course.

### Working with datasets

All datasets loaded are displayed in the datasets pane in the control panel.
A few useful tips for working with datasets:

-  The visibility of individual datasets can be switched on and off by clicking on the {{< img "/img/2021/03/gs-tut/eye-s-on.png" >}} button
-  Remove datasets with the {{< img "/img/2021/03/gs-tut/bin-icon.png" >}} button
-  You can **highlight a dataset** by clicking on the {{< img "/img/2021/03/gs-tut/highlight-s-off.png" >}} button. The highlight color is defined by the color selector right on top of it. Additionally, we can map an attribute to the highlight color using a color map. Let's try it out:
  
    1.  Click on the color box in the Hipparcos dataset we have just loaded from Topcat via SAMP
    2.  Select the radio button "Color map"
    3.  Select the *rainbow* color map
    4.  Choose your attriubte. In this case, we will use the number of transits, *ntr*
    5.  Click <kbd>Ok</kbd>
    6.  Click on the highlight dataset {{< img "/img/2021/03/gs-tut/highlight-s-off.png" >}} icon to apply the color map

-  You can **define basic filters** on the objects of the dataset using their attributes from the dataset preferences window <i class="fa fa-gear"></i>. For example, we can filter out all stars with \\(\delta > 50^{\circ}\\):

    1.  Click on the dataset preferences button <i class="fa fa-gear"></i>
    2.  Click on <kbd>Add filter</kbd>
    3.  Select your attribute (declination \\(\delta\\))
    4.  Select your comparator (\\(>\\))
    5.  Enter your value, in this case 50
    6.  Click <kbd>Ok</kbd>
    7.  The stars with a declination greater than 50 degrees should be filtered out

Multiple filters can be combined with the **AND** and **OR** operators

## External information

Gaia Sky offers three ways to display external information on the current focus object: **Wikipedia**, **Gaia archive** and **Simbad**.

{{< fig src="/img/2021/03/gs-tut/external-info.jpg" link="/img/2021/03/gs-tut/external-info.jpg" title="Wikipedia, Gaia archive and Simbad connections." class="fig-center" width="60%" loading="lazy" >}}

-  When the <kbd>+Info</kbd> button appears in the focus info pane, it means that there is a Wikipedia article on this object ready to be pulled and displayed in Gaia Sky
-  When the <kbd>Archive</kbd> button appears in the focus info pane, it means that the full table information of selected star can be pulled from the Gaia archive
-  When the ``Simbad`` link appears in the focus info pane, it means that the objects has been found on Simbad, and you can click the link to open it in your web browser

## Camera paths

Gaia Sky includes a feature to record and play back camera paths. This comes in handy if you want to showcase a certain itinerary through a dataset, for example.

**Recording a camera path** -- The system will capture the camera state at every frame and save it into a ``.gsc`` (for Gaia Sky camera) file. You can start a recording by clicking on the {{< img "/img/2021/03/gs-tut/rec-icon-gray.png" >}} icon in the camera pane of the control panel. Once the recording mode is active, the icon will turn red {{< img "/img/2021/03/gs-tut/rec-icon-red.png" >}}. Click on it again in order to stop recording and save the camera file to disk with an auto-generated file name (default location is ``$GS_DATA/camera`` (see the [folders section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Folders.html#folders) in the Gaia Sky documentation).

**Playing a camera path** -- In order to playback a previously recorded ``.gsc`` camera file, click on the {{< img "/img/2021/03/gs-tut/play-icon.png" >}} icon and select the desired camera path. The recording will start immediately.

{{< hint >}}
**Mind the FPS!** The camera recording system stores the position of the camera for every frame! It is important that recording and playback are done with the same (stable) frame rate. To set the target recording frame rate, edit the "Target FPS" field in the camrecorder settings of the preferences window. That will make sure the camera path is using the right frame rate. In order to play back the camera file at the right frame rate, you can edit the "Maximum frame rate" input in the graphics settings of the preferences window.
{{</ hint >}}

{{< fig src="/img/2021/03/gs-tut/camerapaths.jpg" link="/img/2021/03/gs-tut/camerapaths.jpg" title="Location of the controls of the camcorder in Gaia Sky." class="fig-center" width="60%" loading="lazy" >}}

More information on camera paths in Gaia Sky can be found in [the camera paths section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Camera-paths.html#camera-paths) of the Gaia Sky user manual.

### Keyframe system

The camera path system offers an additional way to define camera paths based on keyframes. Essentially, the user defines the position and orientation of the camera at certain times and the system generates the camera path from these definitions. Gaia Sky incorporates a whole keyframe definition system which is outside the scope of this tutorial.

As a very short preview, in order to bring up the keyframes window to start defining a camera path, click on the icon {{< img "/img/2021/03/gs-tut/rec-key-icon-gray.png" >}}. 

More information on the keyframe system can be found in the [keyframe system subsection](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Camera-paths.html#keyframe-system) of the Gaia Sky user manual.

## Frame output system

In order to create high-quality videos, Gaia Sky offers the possibility to export every single still frame to an image file. The resolution of these still frames can be set independently of the current screen resolution.

You can start the frame output system by pressing <kbd>F6</kbd>. Once active, the frame rate will go down (each frame is being saved to disk). The save location of the still frame images is, by default, ``$GS_DATA/frames/[prefix]_[num].jpg``, where ``[prefix]`` is an arbitrary string that can be defined in the preferences. The save location, mode (simple or advanced), and the resolution can also be defined in the preferences.

{{< fig src="/img/2021/03/gs-tut/frameoutput.jpg" link="/img/2021/03/gs-tut/frameoutput.jpg" title="The configuration screen for the frame output system." class="fig-center" width="60%" loading="lazy" >}}

Once we have the still frame images, we can convert them to a video using ``ffmpeg`` or any other encoding software. Additional information on how to convert the still frames to a video can be found in the [capturing videos section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Capturing-videos.html#capture-videos) of the Gaia Sky user manual.

## Scripting

This section includes a **hands-on session** inspecting pre-existing scripts and writing new ones to later run them on Gaia Sky.

More information on the scripting system can be found in the [scripting section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/Scripting-with-python.html#scripting) of the Gaia Sky user manual.

- Scripting **API specification**:

    - [API Gaia Sky master (development branch)](https://gitlab.com/langurmonkey/gaiasky/blob/master/core/src/gaiasky/script/IScriptingInterface.java)
    - [API Gaia Sky 3.0.2](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/javadoc/3.0.2/gaiasky/script/IScriptingInterface.html)

- Interesting **showcase scripts** can be found [here](https://gitlab.com/langurmonkey/gaiasky/tree/master/assets/scripts/showcases).
- Basic **testing scripts** can be found [here](https://gitlab.com/langurmonkey/gaiasky/tree/master/assets/scripts/tests).


# Conclusion

In this tutorial we have walked through the basic usage and options of Gaia Sky. We have learned about the controls, the camera modes, the user interface, the time operation, the different render modes, the visibility of components, external datasets and filters, camera paths and keyframes, and the scripting subsystem. 

There is much much more to Gaia Sky, so if you are interested to continue learning, I'd suggest to have a look at these additional resources:

-  [Video tutorials](https://odysee.com/$/search?q=Gaia%20Sky%20-%20Tutorial)
-  [Official documentation](https://gaia.ari.uni-heidelberg.de/gaiasky/docs) 
-  [Source code repository](https://gitlab.com/langurmonkey/gaiasky).
