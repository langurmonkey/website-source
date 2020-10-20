+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "linux", "open source", "fun", "music" ]
date = 2020-10-20
description = "Run mpd as a user service for maximum fun"
linktitle = ""
title = "Music player daemon"
featuredpath = "date"
type = "post"
+++

I remember many years ago, when I was a Windows user, and even later after I made the switch to Linux, I always struggled to find the perfect music player that would fit my needs perfectly. From time to time I would fantasize about programming my own little, perfect, shiny music player program that would fit my needs perfectly like Cinderella's shoe. But I was nowhere near naïve enough to actually start the project, let alone finish it. I know how much time and effort it would take. Then I discovered [`mpd`](https://www.musicpd.org), the music player daemon.

<!--more-->

The idea of `mpd` is elegant and simple. A server that runs on the background and serves music to different clients. It is always on in the background (if needed), ready to be requested anything from its library. It is powerful and extensible through plugins. Multiple client applications can be used to talk to it. My client of choice is `ncmpcpp`, a C++ version of `ncmpc`, but there are countless others for all needs and tastes. The awesome thing is that the library is handled by `mpd`, so that switching clients is much easier:. In this post I document how to set up `mpd` in Arch Linux as a user service, and how to configure it.

First, we need to install `mpd`:

```bash
yay -S mpd
```

Then, enable and start the service in user mode:

```bash
systemctl --user enable mpd.service
systemctl --user start mpd.service
```
Once that's done, `mpd` will look for configuration files in `~/.config/mpd/mpd.conf`. In my case, my config file, as well as my playlists, are stored in [the `mpd` folder of my dotfiles project](https://gitlab.com/langurmonkey/dotfiles/-/tree/master/mpd). The [configuration file](https://gitlab.com/langurmonkey/dotfiles/-/blob/master/mpd/config/mpd.conf) is pretty straightforward. It contains the paths to the music directory, as well as the database, log files, and others. Then, a few lines to define the audio interfaces and the visualizer (if you need that).

<p style="text-align: center; width: 70%; margin: 0 auto;">
<img src="/img/2020/10/ncmpcpp.jpg"
     alt="Ncmpcpp in all its glory"
     style="width: 100%" />
<em style="color: gray;">Glorious ncmpcpp is glorious</em>
</p>

And that's it. Just open `ncmpcpp` and press `u` to initialize/update your music library. A few seconds later --or minutes, depending on the size of your library-- all your music will be perfectly organised and available in the player, ready to be listened to, a few keyboard strokes away. Pair it with a `polybar` module and a few `i3wm` bindings, and it's over 9000.


