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

Wayland is a modern display server protocol that defines the communication between a display server and the clients. It is still very much in the development phase, with some features not completely fleshed out, but it has been improving steadily over the past years. It is supposed to be the new default display server on Linux systems to the point that it will supposedly take over the X11 and its canonical implementation X.Org at some point in the near future.

This past weekend I had some time to play around with it in my laptop. How did it go?

<!--more-->

Wayland brings some improvements over X:

- Sane and clean code base, especially when compared to X11's convoluted one.
- Better security, so that clients can't know about each other by default.
- Better battery life.
- Compositing by default.
- Native support for Freesync and the like.

It also has some drawbacks, which are especially important because they are what's actively preventing more distros and users to adopt it by default:

- Still somewhat immature.
- Many applications are not yet Wayland-ready.
- Lack of support for non-open driver stacks (NVIDIA).

I don't want to try it yet in my various desktop computers until NVIDIA support is there. Unfortunately, I use NVIDIA in all my desktops due to my need of CUDA. However, my laptop does not have a discrete GPU, and the Intel iGPU (mesa) should be very well supported.

So I installed [Sway](https://swaywm.org), which is close to a drop-in replacement for i3wm. I then copied my i3 configuration from `~/.config/i3/config` to `~/.config/sway/config` and started `sway`.

Starting Sway
-------------

I do not use a login manager, so I need to star my graphical sessions manually. For i3/X11, it is as easy as running

```shell
 $  startx
```

In the case of Sway, we can just run the command.

```shell
 $  sway
```

Configuration
-------------

Sway is supposed to be a drop-in replacement, but of course some things are different and some syntax varies a little bit.

{{< fig src="/img/2022/01/screen-i3-x11_s.jpg" link="/img/2022/01/screen-i3-x11.jpg" title="My setup running i3 on X11." class="fig-center" width="50%" loading="lazy" >}}

The i3 configuration did not work for me out-of-the-box, but it did not take long to fix it. Some utils worked straight away, and I had to replace others with Wayland counterparts. What did work and what did not?

{{< fig src="/img/2022/01/screen-sway-wayland_s.jpg" link="/img/2022/01/screen-sway-wayland.jpg" title="My setup Sway on Wayland." class="fig-center" width="50%" loading="lazy" >}}

What worked
-----------

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

What did not work
-----------------

- **System tray**---For the life of me I could not get ``i3blocks`` or ``waybar`` to display the system tray with the tray icons.
- **Scrot** for screenshots. Using `grim` and `slurp` (with the [`grimshot`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/grimshot) script).
- **Opacity** was previously defined in the picom configuration file. Sway also acts as a compositor and does not support transparency. I am only interested in transparency for the terminal, so I just added it to the configuration of Alacritty. It's a shame that I lost the ability to blur the background provided by picom though.
- I needed a new **exit script**. It is [here](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/sway-exit) (i3 version [here](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/i3exit)).
- No need for external utilities to **turn off** the monitor, as `swayidle`, `swaylock` and `swaymsg` can manage that.
- I had to replace [`xcwd`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/xcwd) with [`wcwd`](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/bin/wcwd) to open new terminal windows at the current location.
- I had to change the syntax of **mode** names in the Sway configuration file, but this is really a minor thing.
- Also, no need of external tools to set the **wallpaper**. This just works:
```sway/config
output "*" bg /path/to/image.jpg fill
```

Conclusion
----------

All in all, I think Sway works very well. I had to do some tweaking, but the experience was quite painless. However, the lack of a system tray is kind of a deal breaker for me, as I tend to find myself looking for it more often than not. I'm not sure whether I'll stick to Sway in my laptop or return to i3, but the future is looking good for Wayland.

