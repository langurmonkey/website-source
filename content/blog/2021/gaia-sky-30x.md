+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "programming", "opengl", "release", "version", "english" ]
date = 2021-03-07
description = "Dramatic performance improvements and lots of new features in Gaia Sky 3"
linktitle = ""
title = "Gaia Sky 3"
featuredpath = "date"
type = "post"
+++

It's been a while since I last talked about new Gaia Sky releases. Today I'm doing a recap of the last four releases, starting with ``3.0.0``. This very verison came out with [Gaia eDR3](https://www.cosmos.esa.int/web/gaia/early-data-release-3) on Dec 3, 2020. It was a big jump for Gaia Sky, as it introduced a plethora of new features and QOL improvements along with lots of bug fixes and little tweaks. This post goes over the latest versions from ``3.0.0`` to ``3.0.3``, and reflects on what they brought to the table. 

Jump to the analysis for each of the versions directly:

*  [3.0.0]({{< relref "gaia-sky-30x#300" >}})
*  [3.0.1]({{< relref "gaia-sky-30x#301" >}})
*  [3.0.2]({{< relref "gaia-sky-30x#302" >}})
*  [3.0.3]({{< relref "gaia-sky-30x#303" >}})

<!--more-->

<a name="300"></a>
# 3.0.0

This version came out the same day as eDR3, and it was released along with the catalogs based on this data release. With a development cycle of almost 5 months since ``2.3.1``, it contains by far the most new features and improvements, but it does not lag behind when it comes to bug fixes. Below is a list of features, fixes, build changes and refactorings.  This is a major version, so I made a flashy teaser trailer, as it is customary:

<div style="text-align: center;">
<iframe id="lbry-iframe" width="80%" height="500" src="https://odysee.com/$/embed/gaia-sky-3-0-0-teaser-trailer/65b1fd96c6c75bb86e701b129450c8917a4bf2b7?r=621u1MynW1hV1p9kTVvSiB3pZyjj9tJW" allowfullscreen></iframe>
</div>

Find here a [full commit list between 2.3.1 and 3.0.0](https://gitlab.com/langurmonkey/gaiasky/compare/2.3.1...3.0.0).

### 3.0.0 - Features
- new recursive grid object ([video here](https://odysee.com/@GaiaSky:8/gaia-sky-recursive-grid-preview:e))
- new welcome screen reorganizes dataset management
- new game controller UI with virtual keyboard
- UI adjustments and tweaks all around: new fonts and visual appearance
- add number of objects to download manager 
- velocity scaling allows approaching stars slowly 
- add optional arrow caps to polylines 
- add progress bar to dataset loading
- add brightness power and reload defaults to visual settings 
- improve loading tips subsystem with custom styles and arbitrary elements 
- download helper accepts local files (`file://`)
- API call to get parameters from stars given its name or id
- API call to set the maximum allowed time 
- 3D fonts can be limited in solid angle size
- catalog selection displayed when more than one Gaia catalog is selected
- add wavefront converter
- camera speed-from-distance function rescaling
- update eDR3 catalog descriptors
- add `--debug` flag to activate debug output to ``stdout``
- improve `--version` information 
- add ASCII Gaia image to text ouptut

### 3.0.0 - Bug Fixes
- adjust default area line width 
- star clusters visual appearance 
- min star size scaled by resolution 
- apply scale factor to milky way 
- camera group bottom buttons aligned to center 
- emulate 64-bit float with two 32-bit floats in shader to be able to extend time beyond +-5 Myr 
- controller mappings not found on first startup. Fixes [#341](https://gitlab.com/langurmonkey/gaiasky/issues/341). [#341](https://gitlab.com/langurmonkey/gaiasky/issues/341) 
- use Java2D instead of Toolkit to determine initial screen size 
- data description update 
- controller mappings looking for assets location if not found 
- manpage generation
- smooth game camera view 
- spacecraft mode fixes 
- GUI registry check 
- add timeout to sync behavior in dataset loading 
- new default startup window size to accommodate welcome screen 
- update default data desc pointers to version 3.0.0 
- default fps limit value, aux vectors in recursive grid 
- overwrite coordinate system matrix by recursive grid 
- start some units over `XZ` plane to avoid conflicting with recursive grid 
- gaiasky script defaults back to system java installation if nothing else is found 
- octreegen empty hip x-match crash 
- points in VertsObject with wrong uniform name - incorrect location 
- do not round dialog position values 
- blue, orange and red themes crashed 
- controls scroll box resizing 
- download data window sizings, update data desc 
- regular color picker does not show dialog 
- music player actually finds audio files 
- size of keyboard shortcuts table in controls pane 
- disable background models' depth test 
- focused widgets in scroll panes capture all keyboard events 
- actually send errors to `stderr` instead of `stdout` 
- fix VR properties data pointer 
- motion blur bug producing wrong results for models 
- `touchUp` event on Link and LinkButton objects not working 
- improve logging messages in case of index name conflicts 
- update URL pointers after ARI CMS update 
- graphics quality in log messages 

### 3.0.0 - Build System
- modify installer unpacking message 
- ignore release candidates in changelog, update some defaults 
- generate `sha256` in catalog-pack script 
- macOS does not query screen size due to exception 
- check OS when trying to use Linux commands 
- remove music files from release, don't use OS-dependent system for controller mappings 
- upgrade to Libgdx `1.9.12` 
- update STIL library jar 
- upgrade to Libgdx `1.9.11` 
- update version and data pointer 

### 3.0.0 - Code Refactoring
- run code inspections, cleanup. Improve particle effects 
- `begin()` and `end()` substituted with `bind()` 
- remove unused or derived uniform definitions 
- use `java.utils` collections whenever possible, Libgdx buggy since `1.9.11`
- complete font update to more modern, spacey choices 
- all regular UI fonts from Tahoma to Roboto regular 
- use `system.out` with UTF-8 encoding, improve gen scripts 
- remove ape, Gaia scan properties 
- move RenderGroup to render package for consistency 


<a name="301"></a>
# 3.0.1

This was released some 10 days after the previous release, and it contains fixes to some bugs that were introduced in ``3.0.0``, along a few small new features that address configuration issues and improved compatibility. The ``safemode`` flag was introduced in this version. This flag forces OpenGL 3.x instead of 4.x, avoiding the usage of advanced buffer formats which may cause performance issues on older devices. The full commit list can be found [here](https://gitlab.com/langurmonkey/gaiasky/compare/3.0.0...3.0.1).

### 3.0.1 - Features
- saner error reporting with new dialog 
- add error dialog that works with OpenGL 2.0 and informs the user of insufficient OpenGL or Java versions 
- add safe graphics mode CLI argument ``--safemode``
- dynamic resolution scaling - first implementation, deactivated 
- add safe graphics mode, which does not use float buffers at all. It is activated by default if the context creation for 4.1 fails. It uses OpenGL 3.1. 
- download manager is capable of resuming downloads 
- special flag to enable OpenGL debug output 
- enable GPU debug info with ``--debug`` flag 

### 3.0.1 - Bug Fixes
- show information dialog in case of OpenGL or Java version problems 
- disposing bookmarks manager without it being initialized 
- update default screen size 
- remove idle FPS and backbuffer config 
- file chooser allows selection when entering directories if in DIRECTORIES mode 
- update default max number of stars 
- increase max heap space from 4 to 8 GB in all configurations 
- 24-bit depth buffer, 8-bit stencil 
- JSON pointer from DR2 to eDR3 

### 3.0.1 - Build System
- update bundled JRE version to 11.0.9+11 

### 3.0.1 - Code Refactoring
- all startup messages to I18N bundle, fix swing themes 

### 3.0.1 - Documentation
- update pointers to documentation 

<a name="302"></a>
# 3.0.2

This version contains about a month worth of work. The highlight of this release is the addition of a new, more compact binary format for the level-of-detail catalogs, which enables faster loading and streaming. It also adds new color conversion algorithms, an improved interface with the Wikipedia API and fractional UI scaling. This last item allowed us to do away with the HiDPI (``-x2``) themes. In the bugfix department, I could finally knock down a weird issue that had been plaguing some users since the beginning. This issue produced micro-stutters when loading new data in rather large octrees.

See the full commit history [here](https://gitlab.com/langurmonkey/gaiasky/compare/3.0.1...3.0.2).

### 3.0.2 - Features
- add warning when selecting more than one star catalog 
- add white core to star shaders 
- add `T_eff` to STIL-loaded catalogs 
- add color conversion by Harre and Heller 
- add output format version argument to octree generator 
- support for  in catalog selector 
- add versioning to binary catalog format. Create new, more compact version 
- improve information of version line in welcome and loading screens 
- add GL info to welcome screen 
- new connection to wikipedia REST API to show content in a window 
- add unsharp mask post-processing filter 
- new checkbox textures, adjust window visuals 
- dataset selection dialog uses same structure as dataset manager 
- time warp slider instead of buttons 
- new fractional UI scaling
- add regexp to some column names for STIL loader, add invalid names array 
- case-insensitive columns in STIL loader, enable FITS loading 

### 3.0.2 - Bug Fixes
- stuttering updating counts top-down in large octrees, now the counts are updated locally, bottom-up, when octants are loaded/unloaded 
- RAM units in crash report, add indentation 
- default proper motion factor and length values 
- 'App not responding' message on win10 - fix by upgrading to `gdx-controllers:2.0.0`, plus some other goodies 
- remove useless network checker thread, fix thumbnail URL crash on Win10 
- minimizing screen crashes Gaia Sky on Win10. Fixes [#333](https://gitlab.com/langurmonkey/gaiasky/issues/333), [#345](https://gitlab.com/langurmonkey/gaiasky/issues/345) [#333](https://gitlab.com/langurmonkey/gaiasky/issues/333) 
- VR init failure actually prompts right error message 
- properties files' encodings set to UTF-8. Fixes [#344](https://gitlab.com/langurmonkey/gaiasky/issues/344) [#344](https://gitlab.com/langurmonkey/gaiasky/issues/344) 
- VR mode now accepts any window resize, backbuffer size used for everything internally 
- BREAKING CHANGE API `landOnObjectLocation()` -> `landAtObjectLocation()` 
- octreegen additional split accepts now coma and spaces 
- use different sprite batch for VR UI with backbuffer size 
- pan scaled with FOV factor 
- red-night theme disabled styles 
- proper 'disabled' textures for buttons 
- labels occlude objects behind, buffer writes disabled. 
- download speed moving cancel button in dataset manager 
- `safemode` flag used correctly, fix raymarching not being setup in safe mode 

### 3.0.2 - Performance Improvements
- arrays of size not dependent on `maxPart` for octreegen 
- remove boundingBox from octant, reduce memory token duplication 
- replace extra attributes hashmap with objectdoublemap for RAM compactness 
- do not write star name strings if they are the same as ID, velocity vectors represented with single-precision floats 
- reduce main memory usage of stars by adjusting data types 
- switch to unordered gdx Arrays when possible to minimize copy operations 
- replace `java.util.ArrayList`s with Libgdx's `Array`s to minimize allocations 
- index lists are of base types, use `dst2` for distance sorting 
- improve memory usage of extra star attributes and fix render system unnecessary `setUniform` calls 
- reduce memory usage in particle groups -> no metadata array 

### 3.0.2 - Build System
- auto-update offered through install4j, backup solution in-app still available when not launched using install4j 
- remove `sdl2gdx` in favor of `gdx-controllers:2.0.0`
- exclude old `gdx-controllers` library 
- add --parallelism parameter to 
- fix script so that geo-distances file is additional data instead of special argument 
- fix helper script arguments
- update release instructions with Flatpak, fix build script 

### 3.0.2 - Code Refactoring
- interface particle record to allow for multiple implementations 
- binary providers are versioned, fix binary version 0/1 loading 
- increase number of maps for octree gen 
- modify default bloom settings (default intensity, passes, amount) 

### 3.0.2 - Documentation
- fix javadocs for binary format

### 3.0.2 - Style
- fix missing coma in night-red theme JSON file 
- update thread names, fix monitor objects, increase scene graph update time interval 

<a name="303"></a>
# 3.0.3

This version was released only a few days ago. Amongst its most important features are the upgrade to Java 15 with the use by default of the Shenandonah GC or the improvement of VRAM memory usage for star groups. The full commit list is [here](https://gitlab.com/langurmonkey/gaiasky/compare/3.0.2...3.0.3).

### 3.0.3 - Features
- improvements to catalog generation (hashmap to treemap, rename params, accept multiple string ids per column, etc.) 
- add search suggestions to search dialog - fixes [#351](https://gitlab.com/langurmonkey/gaiasky/issues/351) [#351](https://gitlab.com/langurmonkey/gaiasky/issues/351) 
- remember 'show hidden' preference in file chooser 

### 3.0.3 - Bug Fixes
- controller image fetch crash 
- `getDistanceTo()` with star group object, `goToObject()` with no angle 
- `setSimulationTime()` crash 
- move wikiname to celestial body, remove unused parameters, prepare star to be loaded directly 
- use proper values for depth test 
- post-process bugs (sorting, etc.) 
- check the wrong catalog type `catalog-lod`
- use local descriptors when server descriptor fails to recognize a catalog 
- button sizes adapt to content (fixes [#353](https://gitlab.com/langurmonkey/gaiasky/issues/353)) [#353](https://gitlab.com/langurmonkey/gaiasky/issues/353) 
- bug introduced in [40b99a2](https://gitlab.com/langurmonkey/gaiasky/-/commit/40b99a2bdfe181a305b9bb23664b33c92d5af507) - star cores not applied alpha - fixes [#352](https://gitlab.com/langurmonkey/gaiasky/issues/352) [#352](https://gitlab.com/langurmonkey/gaiasky/issues/352) 
- move temp folder into data folder - partially fixes [#350](https://gitlab.com/langurmonkey/gaiasky/issues/350) [#350](https://gitlab.com/langurmonkey/gaiasky/issues/350) 
- local catalog numbers work when no internet connection available 
- update `jamepad` and `gdx-controllers` versions due to macOS crash 

### 3.0.3 - Build System
- remove branding from installer strings 
- move to ``gdx-controllers`` ``2.1.0`` 
- genearte `md5` and `sha256` of appimage package 
- add appimage build 
- update docs repository pointer 
- update bundled jre version to `15.0.2`
- complete move to Shenandonah GC 
- use Shenandonah GC instead of G1, minor fixes 
- upgrade to libgdx `1.9.14`

### 3.0.3 - Performance Improvements
- remove runtime limiting magnitude 

### 3.0.3 - Style
- cosmetic changes to octree generator 
- renamed some variables, add some extra code comments 
- tweak some parameters in star renderer


# Conclusion

This post recaps on the new features and bug fixes introduced since the first release of Gaia Sky 3. The next big version will be ``3.5``, which will most probably come along with the release of Gaia DR3. Until then, we'll release new minor bufgix versions if needed.
