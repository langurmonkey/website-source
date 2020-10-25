+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "linux", "open source", "torrent", "pirate" ]
date = 2020-10-25
title = "Transmission, a CLI torrent manager"
description = "How to use transmission from CLI and remotely"
linktitle = ""
featuredpath = "date"
type = "post"
+++

<p style="float: right; width: 25%; margin: 0 0 1em 1em;">
<img src="/img/2020/10/pirate.jpg"
     alt="Pirate"
     style="width: 100%" />
</p>
At home, I have a scrawny HTPC called `chimp` in my living room connected to the TV --as I don't own a Smart TV [for good reasons](https://www.tomsguide.com/news/new-studies-reveal-how-smart-tvs-spy-on-you)--. Even though I have a NAS in the network capable of serving media, I connected a dedicated external disk directly to `chimp` because my stock router is not the fastest around. Whenever I use the HTPC, I use it remotely from either my desktop, `bonobo`, or my laptop, `simian`. Sometimes I need to fetch torrents and download them to the disk connected to the HTPC.
Enter Transmission. [Transmission](https://transmissionbt.com/) is a somewhat popular BitTorrent client that includes a 'hidden' command line interface which is very, very useful and simple to use. Learn to use it and you will probably never want to open a GUI torrent client ever again.  
<!--more-->

This post describes how to set up an use transmission in a remote setup.


First, install it. You know how. Once installed, you will want to have a look at two CLI utilities, `transmission-daemon` and `transmission-remote`. The former starts transmission in the background as a daemon. The latter is used to control the daemon: add torrents, remove them, query the state, etc.

Usually, you will want to configure at least the default download location, as well as some speed limits, before starting adding torrents. Check `man` for the options at your disposal regarding `transmission-daemon`. At the very least, change the default download directory:

```bash
transmission-daemon --download-dir "/path/to/my/downloads"
```

You can output a JSON listing of all settings with the following command.

```sh
$  transmission-daemon --dump-settings
{
    "alt-speed-down": 50,
    "alt-speed-enabled": false,
    "alt-speed-time-begin": 540,
    "alt-speed-time-day": 127,
    "alt-speed-time-enabled": false,
    "alt-speed-time-end": 1020,
    "alt-speed-up": 50,
    "bind-address-ipv4": "0.0.0.0",
    "bind-address-ipv6": "::",
    [...]
    "start-added-torrents": true,
    "trash-original-torrent-files": false,
    "umask": 18,
    "upload-slots-per-torrent": 14,
    "utp-enabled": true
}
```

Start the daemon by just calling the program with no arguments. Then, you can start adding torrents:

```bash
transmission-remote -a "magnet-link"
```

You can either use magnet links, or the URL of the torrent file directly. Both work.

Then, check the status of your downloads list with:

```bash
$  transmission-remote -l 
    ID   Done       Have  ETA           Up    Down  Ratio  Status       Name
     1*  100%    2.26 GB  Done         0.0     0.0    0.0  Stopped      This is an open movie
     3*  100%    1.99 GB  Done         0.0     0.0    0.0  Stopped      Arch Linux x86_64 ISO
     4*  100%   996.9 MB  Done         0.0     0.0    0.0  Stopped      Virtual Box OpenSUSE image
     5*  100%    2.52 GB  Done         0.0     0.0    0.0  Stopped      Manjaro Architect x86_64
```

Use `watch` to update the listing automatically every x seconds.

```bash
watch -n 3 "transmission-remote -l"
```

As a final tip, I personally find typing `transmission-remote` every time far too long. I have aliased it to `tr`, with an extra `tra` and `trl` for adding an listing:

```bash
alias tr='transmission-remote'
alias tra='transmission-remote -a'
alias trl='transmission-remote -l'
```

