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

The idea of `mpd` is elegant and simple. A server that runs as a daemon and serves music to different clients. It is always on in the background, ready to be requested anything from its library. It is powerful and extensible through plugins, and supports multiple audio interfaces. Several client applications can be used to talk to it. My client of choice is `ncmpcpp`, a C++ version of `ncmpc` with some improvements, but there are countless others for all needs and tastes. The awesome thing is that the library is handled by `mpd`, so that switching clients doesn't mean reimporting everything. In this post I document how to set up `mpd` in Arch Linux as a user service, and how to configure it. It is so simple that this introduction is longer than the actual setup. Bear with me.

First, we need to install `mpd`:

```bash
yay -S mpd
```

Once that's done, we need a configuration file. The default location is `~/.config/mpd/mpd.conf`. My configuration file contains the paths to the music directory, as well as the database, log files, and others. Then, a few lines to define the audio interfaces and the visualizer (if you need that).

{{< highlight bash "linenos=table" >}}
music_directory	        "~/Music"
playlist_directory		"~/.local/share/mpd/playlists"
db_file			        "~/.local/share/mpd/database"
log_file			    "~/.local/share/mpd/log"
pid_file			    "~/.local/share/mpd/pid"
state_file			    "~/.local/share/mpd/state"
sticker_file			"~/.local/share/mpd/sticker.sql"
log_level			    "default"
auto_update	            "yes"

input {
    plugin              "curl"
}

audio_output {
	type	        	"pulse"
	name		        "Pulse output"
    mixer_type          "software"
}

# FIFO visualizer in ncmpcpp
audio_output {
    type                "fifo"
    name                "mpd_fifo"
    path                "/tmp/mpd.fifo"
    format              "44100:16:2"
}
{{< /highlight >}}

Then, enable and start the service in user mode:

```bash
systemctl --user enable mpd.service
systemctl --user start mpd.service
```
`mpd` should now be ready to serve music. To test it, open `ncmpcpp` and press `u` to initialize/update your music library. A few seconds later --or minutes, depending on the size of your library-- all your music will be perfectly organised and available in the player, ready to be listened to, a few keyboard strokes away. Pair it with a `polybar` module and a few `i3wm` bindings, and it's over 9000.

```bash
bindsym $mod+period exec mpc next
bindsym $mod+comma exec mpc prev
```

The two lines above bind `$mod`+`.` and `$mod`+`,` to play the next and previous song respectively. So easy.


<p style="text-align: center; width: 70%; margin: 0 auto;">
<img src="/img/2020/10/ncmpcpp.jpg"
     alt="Ncmpcpp in all its glory"
     style="width: 100%" />
<em style="color: gray;">Glorious ncmpcpp is glorious</em>
</p>

My `~/.config/ncmpcpp/config` file is pretty basic. I mostly go with the defaults, but here it is in case you need it:


{{< highlight bash "linenos=table" >}}
ncmpcpp_directory = ~/.local/share/ncmpcpp
lyrics_directory = ~/.local/share/ncmpcpp/lyrics

[mdp]
mpd_host = localhost
mpd_port = 6600
mpd_music_dir = ~/Music
mpd_crossfade_time = 2

[visualizer]
visualizer_fifo_path = /tmp/mpd.fifo
visualizer_output_name = mpd_fifo
visualizer_in_stereo = no
visualizer_sync_interval = 15
visualizer_type = wave
visualizer_look = ●▮
visualizer_color = default

[global]
colors_enabled = yes
main_window_color = default
centered_cursor = yes
enable_window_title = yes
external_editor = nvim
{{< /highlight >}}

And that's it. Nowadays it is quite straightforward to configure a fully-featured audio server in your Linux box and pair it with a no-nonsense, CLI player that is lightweight and feels amazing to use.
