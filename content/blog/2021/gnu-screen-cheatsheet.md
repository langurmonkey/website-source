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
|<kbd>ctrl</kbd> + <kbd>a</kbd>|escape key (used to access all other key bindings)|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>d</kbd>|detach and go back to original terminal session|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>D</kbd> <kbd>D</kbd>|detach and log out|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>\\</kbd>|exit all programs in screen|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>ctrl</kbd> + <kbd>\\</kbd>|force exit (not recommended)|
|<kbd>ctrl</kbd> + <kbd>a</kbd> `:quit`|close session and quit screen|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>?</kbd>|help|

Window management
-----------------

|Keys |Action  |
| --- | --- |
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>c</kbd>|create new window|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>A</kbd>|rename current window|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>"</kbd>|show window list and choose window|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>w</kbd>|display window bar|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>1</kbd>,<kbd>2</kbd>,...|switch to window number|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>n</kbd>|move to next window|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>p</kbd>|move to previous window|
|Close all processes (incl. shell)          |close window|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>k</kbd>|force close window|

Splits
------

|Keys |Action  |
|--- | --- |
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>S</kbd>|horizontal split|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>V</kbd> or <kbd>\|</kbd>|vertical split|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>tab</kbd>|jump to next region|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>X</kbd>|close current region|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>Q</kbd>|close all regions but current|

Clibpoard
---------

|Keys |Action  |
|--- | --- |
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>[</kbd>|enter copy mode|
|<kbd>space</kbd>|toggle selection and copy|
|<kbd>ctrl</kbd> + <kbd>a</kbd> <kbd>]</kbd>|paste|

Configuration
-------------

Finally, I just want to share my `.screenrc` configuration. It starts with 5 windows by default and adds a window bar at the bottom with the host, the window list and the time so that you never miss your appointments. Find it [here](https://gitlab.com/langurmonkey/dotfiles/-/tree/master/screen).

{{< figure src="/img/2021/05/gnu-screen-config.jpg" link="/img/2021/05/gnu-screen-config.jpg" title="GNU screen with the configuration above" class="fig-center" width="70%" >}}
