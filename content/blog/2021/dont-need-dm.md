+++
author = "Toni Sagrista Selles"
categories = []
tags = []
date = 2021-09-14
linktitle = ""
title = "You (probably) don't need a display manager"
description = "How to log in directly with startx and .xinitrc"
featuredpath = "date"
type = "post"
+++

In the Linux world, a display manager is a little GUI program that presents the user with a login screen right after boot, allows her to enter her login credentials and choose the desired desktop environment or window manager. The most common ones are `gdm` (the default in Gnome), `kdm` (same for KDE), `lightdm` (originally written for Ubuntu's Unity DE) and `lxdm` (for LXDE). There also exist a bunch of arguably simpler terminal-based display managers like `ly`, `cdm` or `nodm`.

But for most users a fully featured display manager may be a bit too much bloat. You can achieve the exact same functionality by simply using the default shell login and a single command. Everything in this post applies only to **X11** (sorry Wayland users).

<!--more-->

If you are the only user of your computer, you may not need a display manager at all. Not using one has the advantages of removing complexity, sparing a few MB from your drive, getting rid of an `init` or `systemd` task, and being in control of what exactly happens when X starts.

If you have no display manager configured in your init system, after boot you will be presented with the default login shell. Use it to log in normally and access a terminal `tty` with your default shell.

Now you need to start the X window system, and your desktop environment or window manager of choice with it. To do so, look at the `~/.xinitrc` file.

## The `~/.xinitrc` script

There are a couple of utilities that can launch the X server for you. The first is `xinit`, the second is `startx`. In reality, `startx` is nothing but a wrapper script around `xinit` that adds a few bells and whistles, so I suggest you use only `startx` and leave `xinit` alone. You can inspect the `startx` script easily:

```bash
less $(where startx)
```

The login sequence goes like this:

1. Login using the default shell
2. run `startx`

As we mentioned above, `startx` calls `xinit`, which reads the `~/.xinitrc` file to know what to execute.

`~/.xinitrc` is a regular script that contains the commands to run when starting X. The final command should run the DE or WM. An example of `~/.xinitrc` that starts `i3wm` file follows:


{{< highlight bash "linenos=table" >}}
# This is an ~/.xinitrc example file

# Start compositor
# picom blah blah ...

# Start applets, daemons, etc.
# diskie
# nm-applet
# ...

# Apply .Xresources settings (dpi)
[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

# Start i3wm
exec i3
{{</ highlight >}}

In the listing above, we start `i3wm` with the line `exec i3`. The rest of the file can be as complex as you want it to be.

## Set your DPI in `~/.Xresources`

If you use a special display density (DPI) setting, you should make sure to include a call to `xrdb` with your `~/.Xresources` file. In my case, I use a 4K display, so I set a DPI of 192 in my `~/.Xresources` file:

```
!--------------------------------------------
! Custom DPI
!--------------------------------------------
Xft.dpi: 192
Xft.autohint: 0
Xft.lcdfilter: lcddefault
Xft.hintstyle: hintfull
Xft.hinting: 1
Xft.antialias: 1
Xft.rgba: rgb
```

You can check that this configuration file is sourced correctly by querying the dots per inch setting of your system:

```bash
$ xdpyinfo | grep dots
  resolution:    192x192 dots per inch
```

## Conclusion

In this post we have seen how to configure our system to login without a display manager. I would argue this is a good practice, especially if you are the only user, as it removes unnecessary complexity and failure points.


