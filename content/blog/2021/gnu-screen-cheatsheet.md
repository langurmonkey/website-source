+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = ["linux", "english", "gnu screen", "cli", "terminal"]
date = 2021-05-31
linktitle = ""
title = "GNU screen cheatsheet"
description = "Quick reference to GNU screen essential bindings"
featuredpath = "date"
type = "post"
+++

[GNU screen](https://www.gnu.org/software/screen/) is a terminal multiplexer that allows for different virtual windows and panes running different processes within the same terminal session, being it local or remote. This post contains a quick reference to the most used **default** key bindings of GNU screen. In contrast to other terminal multiplexers like tmux, GNU screen is *probably* already installed in your server of choice.

<!--more-->

Commands
--------

|Command |Action  |
| --- | --- |
|`screen -S <session-name>`|create new session with name|
|`screen -r` or `screen -x`|attach to most recent session|
|`screen -r <session-name>`|attach to named session|
|`screen -ls`|list running sessions|

Basics
------

|Keys |Action  |
| --- | --- |
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}}|escape key (used to access all other key bindings)|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}d{{</ sp >}}|detach and go back to original terminal session|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}D{{</ sp >}} {{< sp guilabel >}}D{{</ sp >}}|detach and log out|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}\{{</ sp >}}|exit all programs in screen|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}\{{</ sp >}}|force exit (not recommended)|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} `:quit`|close session and quit screen|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}?{{</ sp >}}|help|

Window management
-----------------

|Keys |Action  |
| --- | --- |
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}c{{</ sp >}}|create new window|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}A{{</ sp >}}|rename current window|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}"{{</ sp >}}|show window list and choose window|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}w{{</ sp >}}|display window bar|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}1{{</ sp >}}\|{{< sp guilabel >}}2{{</ sp >}}\|...|switch to window number|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}n{{</ sp >}}|move to next window|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}p{{</ sp >}}|move to previous window|

Splits
------

|Keys |Action  |
|--- | --- |
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}S{{</ sp >}}|horizontal split|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}V{{</ sp >}} or {{< sp guilabel >}}\|{{</ sp >}}|vertical split|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}tab{{</ sp >}}|jump to next region|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}Xab{{</ sp >}}|close current region|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}Qab{{</ sp >}}|close all regions but current|

Clibpoard
---------

|Keys |Action  |
|--- | --- |
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}[{{</ sp >}}|enter copy mode|
|{{< sp guilabel >}}space{{</ sp >}}|toggle selection and copy|
|{{< sp guilabel >}}ctrl{{</ sp >}} + {{< sp guilabel >}}a{{</ sp >}} {{< sp guilabel >}}]{{</ sp >}}|paste|

Configuration
-------------

Finally, I just want to share my `.screenrc` configuration. It starts with 5 windows by default and adds a window bar at the bottom with the host, the window list and the time so that you never miss your appointments. Find it [here](https://gitlab.com/langurmonkey/dotfiles/-/tree/master/screen).

{{< figure src="/img/2021/05/gnu-screen-config.jpg" link="/img/2021/05/gnu-screen-config.jpg" title="GNU screen with the configuration above" class="fig-center" width="70%" >}}
