+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "linux", "i3wm", "sway", "wayland", "open source", "english"]
date = 2022-01-25
linktitle = ""
title = "Trying out Sway and Wayland"
description = "Is Wayland ready for prime time yet? Find out here."
featuredpath = "date"
type = "post"
+++

**Wayland** is a modern display server protocol that will eventually replace X11. It is still not quite a 100% there, but it has been improving steadily and gaining ground over the past years. It is expected to become the new default display server on Linux systems at some point in the near future.

This past weekend I had some time to play around with **Sway**, a window manager and Wayland compositor that mimics i3. How did it go?

<!--more-->

Why even care
-------------

Well, Wayland brings some advantages over X11:

- Sane and clean code base, especially when compared to XOrg's convoluted hack pile.
- Simpler and more constrained.
- In Wayland the compositor is the display server, so compositing (use of off-screen buffers for rendering) is a given. No screen tearing.
- Better security, so that clients can't know about each other by default. Keylogging is not possible.
- Better performance and battery life.
- Native support for Freesync and the like.

It also has some drawbacks, which are especially important because they are what's actively preventing more distros and users to adopt it by default:

- Still somewhat immature (see [here](https://arewewaylandyet.com)).
- Many applications are not yet Wayland-ready (and some will never be).
- Lack of support for proprietary driver stacks (NVIDIA).

I don't want to try it yet in my various desktop computers until NVIDIA support is there. Unfortunately, I use NVIDIA in all my desktops because CUDA. However, my laptop does not have a discrete GPU, and the Intel iGPU (mesa) should be very well supported.

So I installed [Sway](https://swaywm.org), which is close to a drop-in replacement for i3. I then copied my i3 configuration from `~/.config/i3/config` to `~/.config/sway/config` and started it.

Starting Sway
-------------

I do not use a [display manager](/blog/2021/dont-need-dm), so I need to start my graphical sessions manually from the `tty`. For i3/X11, it is as easy as running the following (provided your `.xinitrc` is handsome enough):

```shell
 $  startx
```

In the case of Sway, we can just run the command directly:

```shell
 $  sway
```

Configuration
-------------

Sway is supposed to be a drop-in replacement where the same configuration file can be used with either, and in my experience, it is *mostly* true. However, some adjustments had to be made.

{{< fig src="/img/2022/01/screen-i3-x11_s.jpg" link="/img/2022/01/screen-i3-x11.jpg" title="My setup running i3 on X11." class="fig-center" width="50%" loading="lazy" >}}

The i3 configuration did not work out-of-the-box for me, but it didn't take long to fix. Some utilities worked straight away, and I had to replace others with Wayland-ready counterparts. What did work and what did not? Let's have a look.

{{< fig src="/img/2022/01/screen-sway-wayland_s.jpg" link="/img/2022/01/screen-sway-wayland.jpg" title="My setup running Sway on Wayland. Note the missing systray." class="fig-center" width="50%" loading="lazy" >}}

What works
----------

- **Rofi** as a launcher menu worked without any tweaks. I was a bit surprised, as I had read that a patch or fork was needed for it to be Wayland-ready.
- **i3blocks** is my status bar of choice, and it also worked out-of-the-box. I had to adapt some of the module scripts though.
- **Alacritty** is my terminal, and it is Wayland-ready. No surprises.
- **Gaps** are supported by default.
- **Key mapping** is supported by default. I'm using this snippet to use <kbd>CapsLock</kbd> as <kbd>Esc</kbd> and vice-versa, to use <kbd>Alt</kbd>+<kbd>Space</kbd> to cycle through keyboard layouts, and to set the repeat delay and rate.

```sway/config
input * {
    xkb_layout "us,es"
    xkb_options "grp:alt_space_toggle,caps:swapescape,eurosign:e"
    xkb_model "pc104"
    repeat_delay 200
    repeat_rate 35
}
```

Many other stuff works via translation layers (``xwayland``) and I didn't even realize.

What doesn't work
-----------------

- **System tray**---for the life of me I could not get ``i3blocks`` or ``waybar`` to display the system tray with the tray icons, and it wasn't for lack of trying.
- **Scrot** for screenshots. Using `grim` and `slurp` (with the [`grimshot`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/grimshot) script).
- **Opacity** was previously defined in the picom configuration file. Sway also acts as a compositor and does not support transparency. I am only interested in transparency for the terminal, so I just added it to the configuration of Alacritty. It's a shame that I lost the ability to blur the background provided by picom though.
- I needed a new **exit script**. It is [here](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/sway-exit) (i3 version [here](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/i3exit)).
- No need for external utilities to **turn off** the monitor, as `swayidle`, `swaylock` and `swaymsg` can manage that.
- I had to replace [`xcwd`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/xcwd) with [`wcwd`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/wcwd) to open new terminal windows at the current location.
- I had to change the syntax of **mode** names in the Sway configuration file, but this is really a minor thing.
- Of course, `sxiv` (simple X image viewer) does not run on Wayland. No problem, as `imv` is super similar and does work on both.
- Image previews on Alacritty do not work, as Uberzug is for X11. Kitty has its own way of displaying images on the terminal, so that is something to explore.
- Also, no need of external tools to set the **wallpaper**. This just works:
```sway/config
output "*" bg /path/to/image.jpg fill
```

Conclusion
----------

All in all, I think Sway works very well. I had to do some tweaking, but the experience was overall quite painless. However, the lack of a system tray is a bit of a deal breaker for me, as I tend to find myself looking for it more often than not. 
I think I'll keep logging into Sway for now and see if the benefits outweigh the possible drawbacks.
