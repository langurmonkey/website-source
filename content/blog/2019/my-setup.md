+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "programming", "scripts", "i3wm", "polybar", "rice", "qutebrowser", "pass", "neovim" ]
date = 2019-03-02
description = "Description of my daily Linux setup as of October 2019"
linktitle = ""
title = "My Linux setup (as of 10/2020)"
featuredpath = "date"
type = "post"
+++

{{< sp orange >}}Edit (2020-10-02):{{</ sp >}} change termite to kitty due to font ligatures support.\
{{< sp orange >}}Edit (2020-06-01):{{</ sp >}} change urxvt to termite, update info on qutebrowser with tor.*

---

## Overview

In this post I'm documenting the current (March 2019) system setup I use in my development machines. This has been converging for a long time already, and It will surely evolve in the future. However, right now, it works well for me.
I use the machines mostly for development work ([Gaia Sky](https://zah.uni-heidelberg.de/institutes/ari/gaia/outreach/gaiasky/), Gaia First Look, Ph.D., etc.). I also use my personal computers for the occasional light gaming session (Terraria, C&C remastered, or whatever I feel like at the moment) and as all-around computing devices to manage stuff.

The setup is based around the keyboard and command-line tools (CLI), that run in the terminal. Of course, I use also plenty of GUI applications, but the basic workflow is just optimized to minimal mouse use. It is just faster to get around and get things done quickly.

I use this configuration in the following machines:

- **ARI desktop** - *hidalgo*, i7-7700, 16 Gb RAM, GTX 1070, Ubuntu 18.04
- **IWR desktop** - *herschel*, i7-4790K, 16 Gb RAM, GTX 970, Manjaro Linux
- **Home laptop** - *simian*, Dell XPS 13 9370 13", i7-8550U, 16 Gb RAM, Intel UHD 620, Arch Linux
- **Home desktop** - *bonobo*, i5-4460, 16 Gb RAM, GTX 970, Antergos Linux

{{< fig src="/img/2019/03/ari-rice_s.jpg" link="/img/2019/03/ari-rice.jpg" title="This is what my work PC looks like. On the left is a 4K monitor, on the right is a FHD monitor in portrait orientation and with an xrandr scale of x1.5" width="75%" class="fig-center" loading="lazy" >}}

## Dotfiles project

All of the configuration files are hosted in my [dotfiles repository](https://gitlab.com/langurmonkey/dotfiles). I try to keep things clean, simple and generic. For more information see this [post](/blog/2019/my-dotfiles) where I originally shared the repo.

## Bootstrapping and deploying

I have a couple of scripts to painlessly and automatically bootstrap and deploy the configuration. Please, see the [README](https://gitlab.com/langurmonkey/dotfiles/blob/master/README.md) file for more details.
Basically, run:

```bash
bash <(curl -s https://gitlab.com/langurmonkey/dotfiles/raw/master/bootstrap.sh)
```

To check out the repository to `~/.dotfiles` and install the required software. Then, do:

```bash
~/.dotfiles/deploy
```

To deploy the configuration. You are done.


## Window manager

I use [`i3wm`](https://i3wm.org/), and in particular, Airblader's fork [`i3-gaps`](https://github.com/Airblader/i3) in every computer I have to do work with. Additionally, Gnome Shell is installed to my home desktop *bonobo* for convenience, since it is connected to the TV in my living room. It is not very convenient to operate i3 with one of [these](/img/2019/03/remote.jpg).

## Shell

I use [`zsh`](www.zsh.org) (actually, [`oh-my-zsh`](https://github.com/robbyrussell/oh-my-zsh)) because I'm used to lots of its features that I otherwise miss when using `bash`.

## Terminal emulator

My terminal emulator of choice is [`kitty`](https://sw.kovidgoyal.net/kitty/) because it is simple and easy to configure. It is not the fastest terminal emulator in the west, but it supports font ligatures. Ligatures are important to developers, and not many terminal emulators support them. I use the `FiraCode Nerd Font` font. It looks crisp and is just a beautiful monospace font for code, with ligatures. Other than that, I have bindings to modify the font size automatically, scroll up and down using `k` and `j` and little else.

I've played around with [`st`](https://st.suclkess.org) but I'm a fan of having to apply patches for even the most basic of functionalities. It is just not too convenient for me, even though I keep it installed in my systems.

## Bar

I tried a few bars: `i3bar`, `i3blocks`, `bumblebee-status`, you name it. The only one which worked with very little quirks and easy config with my two-monitor setup with different DPI is [`polybar`](https://github.com/jaagr/polybar). Also, it looks gorgeous, and it is very easy to write modules for. Check out this [post](/blog/2019/polybar-cpu-memory) for an example of a script which shows CPU and memory usage. 

{{< fig src="/img/2019/03/polybar.jpg" link="/img/2019/03/polybar.jpg" title="The Polybar in my main monitor" width="70%" class="fig-center" loading="lazy" >}}
<p style="text-align: center">

My polybar displays the workspaces, the current keyboard layout, available updates, memory usage, CPU and temperature, the current wireless network, the screen brightness, the battery, the volume,  date and time and the systray.

## Text editor

When it comes to text editors, my opinion is that there is no other than [`vim`](https://www.vim.org) (or [`neovim`](https://neovim.io) - sorry emacs folks. I only use just a couple of plugins: [`Ctrl-P`](https://github.com/kien/ctrlp.vim) for fuzzy searches and [`vim-surround`](https://github.com/tpope/vim-surround). Other that that, I don't have much else to add. If you don't use `vim`, try it. The first few days (or weeks) are hard, but once you build up the muscle memory you'll become dependent on it and you will find yourself trying to use the same paradigm in your browser, your terminal and your mail client.

## File manager

[`ranger`](https://github.com/ranger/ranger) is amazing. It has all the features I ever want, and tweaking and configuring it is so easy it is a pleasure. I have defined a couple of bindings that allow me to move directly to the wallpapers folder, change the current wallpaper with feh and change the current wallpaper and generate a new theme with pywal. For example, the following moves me directly to the wallpapers folder when I press gw:

```
map gw cd ~/.dotfiles/assets/wallpaper
```

Then, I can select a wallpaper and I can either use `bg` to set as background or `bw` to set as background, generate a new palette and apply the theme.

```
map bg shell cp %f ~/Pictures/wallpaper.jpg \
&& feh --bg-fil ~/Pictures/wallpaper.jpg

map bw shell cp %f ~/Pictures/wallpaper.jpg \
&& ~/.local/bin/wal -c && ~/.local/bin/wal -a 85 -i ~/Pictures/wallpaper.jpg
```

Additionally, I use this wee script to launch a new instance of ranger inside a terminal with a specific working directory:

```bash
#!/bin/bash
kitty -cd "$1" -e ranger --cmd="shell ~/.local/bin/wal -R"
```

Whenever I need a new instance of ranger, I use the script. For example, I bind $sup+f to a new ranger-in-term starting at the working directory of the currently focused window in my i3 configuration:

```
bindsym $sup+f exec ~/.dotfiles/bin/ranger-term "\`$HOME/.dotfiles/bin/xcwd\`"
```

Or I use ranger for displaying the mounted volumes from the udiskie tray icon, starting udiskie in this manner:

```
exec --no-startup-id udiskie -f "/home/tsagrista/.dotfiles/bin/ranger-term" --tray 
```

Finally, I use the following line to open the highlighted file instead of the selected file when pressing `l` or `arrow_right`.

```
map l move right=1 selection=False
```

## Browser

[`qutebrowser`](https://qutebrowser.org) all the way. It is light and snappy. Only thing I'm missing right now is some sort of advanced ad blocking (current ad blocking system is host-based). This does not always work with youtube videos, but most of the time I use `mpv` to watch them anyway, for I have `V` mapped to 'open video with mpv'. Additionally, the way it integrates with `pass` is very neat.
You can use qutebrowser easily with the tor network. Check it out [here](/blog/2020/tor-qutebrowser). It has a built-in ad-blocker and, if that is not enough, I also use a custom `/etc/hosts` file.

## Password manager

I used KeePassX for many years until I discovered [`pass`](https://www.passwordstore.org). It is a simple CLI password manager where the passwords are stored in text files encrypted with your PGP key. Then you can version control the `pass` folder to sync it across all your devices. Simple to set up and simpler to use, the passwords can even be decrypted directly with `gpg`, so you are always in control.

## Mail client

Right now I'm using [Thunderbird](https://thunderbird.net) with [Enigmail](https://enigmail.net). I need to research [`mutt`](http://mutt.org) and try it out when I have some time.

## Music player

I have used [`cmus`](https://cmus.github.io) with [`vis`](https://github.com/dpayne/cli-visualizer) for a long time, coupled with [`beets`](http://beets.io) to keep my library organised and my tags up to date. However, lately I've turned to the [`mdp`](https://musicpd.org) + [`ncmpcpp`](https://github.com/arybczak/ncmpcpp) tandem. The MPD service is running in the background and maintains the libary, playlists and player state. NCMPCPP connects to it and offers a terminal-based clean interface. Every day I like it more and more.

## RAW photo editing

I've been mostly using [RawTherapee](https://rawtherapee.com) (please, disregard the name) for years, but lately I've been playing around more and more with [darktable](https://www.darktable.org). Both have their strong points. I think I prefer RawTherapee's user interface, but darktable has more options and is better at memory management. One of the killer features that might end up tipping the balance for me in darktable's favour is the GPU acceleration support via OpenCL which makes editing operations lightning fast. Also, darktable supports masks, which RawTherapee does not.


{{< fig src="/img/2019/03/darktable-rawtherapee.jpg" link="/img/2019/03/darktable-rawtherapee.jpg" title="Darktable (left) and RawTherapee (rigtht)" width="70%" class="fig-center" loading="lazy" >}}

At the end of the day, both are very capable and produce good results. Also, both support `.CR2` and `.RW2` from my Canon 40D and my Panasonic Lumix LX10/15 respectively.

## Scripting

Most of my scripts are written in `bash`, even though for more complex things I also use `python` from time to time.

## Additional utilities

Here is a list of utilities I have installed and use regularly.

-  [`cava`](karlstav.github.io/cava) - Audio visualizer and equalizer
-  [`fd`](github.com/sharkdp/fd) - Amazing replacement for `find`
-  [`fzf`](github.com/junegunn/fzf) - Terminal fuzzy finder and vim plugin
-  [`sshfs`](github.com/libfuse/sshfs) - Mount file systems over SSH/SFTP
-  `apropos` - Search the man pages
-  [`units`](www.gnu.org/software/units) - Convert units on the terminal
-  [`translate-shell`](github.com/soimort/translate-shell) - Google translate terminal wrapper
-  [`rtv`](github.com/michael-lazar/rtv) - Reddit Terminal Viewer
-  [`tealdeer`](github.com/dbrgn/tealdeer) - Access [`tldr-pages`](github.com/tldr-pages/tldr) with style
-  [`pdfpc`](github.com/phillipberndt/pdfpc) - Presenter console for for PDF files
-  [`tig`](github.com/jonas/tig) - Text interface for `git`
-  `bc` - Best calculator ;)

## Closing Notes

I think this post sums up my basic setup pretty accurately. It will, of course, become obsolete at some point, but for the time being, I will try to keep it up to date whenever I implement major changes.
