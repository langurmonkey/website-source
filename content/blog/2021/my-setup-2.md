+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "programming", "scripts", "i3wm", "i3blocks", "rice", "qutebrowser", "pass", "neovim" ]
date = 2021-10-30
description = "Description of my daily Linux setup as of November 2021"
linktitle = ""
title = "My Linux setup (as of 11/2021)"
featuredpath = "date"
type = "post"
+++

A couple of years ago I wrote a [blog post](/blog/2019/my-setup/) about my Linux setup at the time. Well, understandably a lot of things have changed since then, and instead of updating a two year old post, I think writing a new one from scratch with the same principle and using the same template makes more sense. It is always fun to go back and read these old posts, and I fully expect that this one post will be as enjoyable for me in a few years time.

## Overview

In this post I'm documenting the current (November 2021) system setup I use in my development machines. This is a snapshot of the current state of things, and needless to say, it will evolve, meander and transform in unexpected ways.

The setup is still based around the keyboard and the foundation are some crazy useful command-line tools (CLI). Of course, I also use plenty of GUI applications, but the basic workflow is just optimized to minimize mouse usage.

I use this configuration in the following machines. Before, I had my main work machine running Ubuntu, another one running Antergos and some other with Manjaro. Note that hey have all moved to Arch Linux by now. Feels good man, so much simpler.

- **Work desktop** - *hidalgo*, i7-7700, 32 Gb RAM, GTX 1070, Arch Linux
- **Work laptop** - *chimp*, i7-8750H, 16 Gb RAM, GTX 1060, Arch Linux
- **Home laptop** - *simian*, Dell XPS 13 9370 13", i7-8550U, 16 Gb RAM, Intel UHD 620, Arch Linux
- **Home desktop** - *bonobo*, i5-4460, 16 Gb RAM, GTX 970, Arch Linux

{{< fig src="/img/2021/10/simian-config_s.jpg" link="/img/2021/10/simian-config.jpg" title="That is what my laptop looks like as of now. Nothing particularly interesting with it, really." width="60%" class="fig-center" loading="lazy" >}}

## Dotfiles project

All of the configuration files are still hosted in my [dotfiles repository](https://gitlab.com/langurmonkey/dotfiles). I try to keep things clean, simple and generic. For more information see this [post](/blog/2019/my-dotfiles) where I originally shared the repository back in 2019.
Please, see the [README](https://gitlab.com/langurmonkey/dotfiles/blob/master/README.md) file for more details.

## Window manager

I use [`i3wm`](https://i3wm.org/), and in particular, Airblader's fork [`i3-gaps`](https://github.com/Airblader/i3) in every computer I have to do work with. I genearally do not keep other window managers or desktop environments installed anymore, as i3 does everything I need it to do.

## Display manager

None. I use [`startx` with `.xinitrc`](/blog/2021/dont-need-dm/), and that's enough.

## Shell

I use [`zsh`](www.zsh.org) (no longer with `oh-my-zsh`, as I just have the few scripts I used directly cloned into my dotfiles repository) because I'm used to lots of its features that I otherwise miss when using `bash`.

## Terminal emulator

My terminal emulator of choice is currently [`alacritty`](https://alacritty.org). I used to use `kitty` for its font ligatures support, but at some point along the road I realized I didn't really care for ligatures and disabled them. Then I tried `alacritty`, and saw that it was good and simple, so I switched. My current font of choice is **JetBrainsMono Nerd Font**, which I use for pretty much everything.

I've played around with [`st`](https://st.suclkess.org) but I'm a fan of having to apply patches for even the most basic of functionalities. It is just not too convenient for me, even though I keep it installed in my systems.

## Bar

I am back to square one with the bar. After deeming `polybar` overkill for my purposes, I went back to `i3blocks`. I had to write some [scripts myself](https://gitlab.com/langurmonkey/dotfiles/-/tree/master/i3blocks/scripts) and took some others from the interwebs, but pretty much everything that I found useful in my `polybar` configuration is still here in `i3blocks`. 

{{< fig src="/img/2021/10/i3blocks.jpg" link="/img/2021/10/i3blocks.jpg" title="Look at that sexy bar!" width="100%" class="fig-center" loading="lazy" >}}

My bar now displays the workspaces all the way to the left, the current audio track via `playerctl`, a CPU bar per core, the used and total RAM, the keyboard layout, the available pacman updates, the screen brightness, the volume level, the battery level, the time and date and the systray.

## Text editor

When it comes to text editors, my opinion is that there is no other than [`neovim`](https://neovim.io)---sorry emacs folks. I use now a handful of plugins, as I find myself using vim more and more for development work:

``` vim
" Plugins with vim-plug
call plug#begin('~/.config/nvim/plugged')
    Plug 'alvan/vim-closetag'
    Plug 'mcchrish/nnn.vim' " nnn file manager
    Plug 'sheerun/vim-polyglot'
    Plug 'raimondi/delimitmate'
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim' " fuzzy search with fzf
    Plug 'ervandew/supertab' " tabs on steroids
    Plug 'vim-airline/vim-airline' " the bottom line
    Plug 'vim-airline/vim-airline-themes'
    Plug 'rust-lang/rust.vim' " rust goodies
    Plug 'neoclide/coc.nvim', { 'branch': 'release'} " conquer of completion
    Plug 'ojroques/vim-scrollstatus' " scrollbar in airline
    Plug 'lervag/vimtex'
    Plug 'tpope/vim-commentary' " easily comment code
    Plug 'sainnhe/sonokai'
    Plug 'uiiaoo/java-syntax.vim'
    Plug 'EdenEast/nightfox.nvim' " a cool theme
call plug#end()

```

You can find more about each plugin by visiting the corresponding github page if you're really interested.
Also, I wrote about my [mouseless Rust development environment](/blog/2021/rust-devenv/) based on vim a few months ago, in case that is the kind of thing that turns you on.

## File manager

I used to use [`ranger`](https://github.com/ranger/ranger) a lot, but now I tend to gravitate towards [`lf`](https://github.com/gokcehan/lf) much more, especially for navigating around and doing simple file manager things like copying and moving things around. I use via an `lfcd` bash function which `cd`s into the current directory on exit. Very handy to quickly move around:

``` bash
lf () {
    tmp="$(mktemp)"

    # use lfi if found
    if ! command -v lfi &> /dev/null
    then
        lf -last-dir-path="$tmp" "$@"
    else
        lfi -last-dir-path="$tmp" "$@"
    fi

    if [ -f "$tmp" ]; then
        dir="$(cat "$tmp")"
        rm -f "$tmp"
        if [ -d "$dir" ]; then
            if [ "$dir" != "$(pwd)" ]; then
                cd "$dir"
            fi
        fi
    fi
}
```

## Browser

Still [`qutebrowser`](https://qutebrowser.org) all the way. It is light and snappy. Since 2019 an awesome ad blocker has been added, so it does everything perfectly for me now. It hits all the right keys, which is an odd thing in a browser.
If you value your online anonymity, you can use `qutebrowser` easily with the tor network. Check it out [here](/blog/2020/tor-qutebrowser).

## Password manager

Still sporting [`pass`](https://www.passwordstore.org) like a champ. It is a simple CLI password manager where the passwords are stored in text files encrypted with a PGP key. Then you can version control the `pass` folder to sync it across all your devices. Simple to set up and simpler to use, the passwords can even be decrypted directly with `gpg`, so you are always in control.
There is a [qutebrowser script](https://github.com/qutebrowser/qutebrowser/blob/master/misc/userscripts/qute-pass) which does the integration very well.

## Mail client

Right now I'm using [Thunderbird](https://thunderbird.net) and `mutt`, even though I'm not as comfortable with `mutt` as I would like. I need to invest some more time to really consolidate a workflow, as I have it fully configured and ready to go with my work and personal mail accounts already. It just need some more love I reckon.

## Music player

I just use `ncmpcpp` with `mpd`. Read more about them [here](/blog/2020/mpd/).

## RAW photo editing

By now I've ditched [RawTherapee](https://rawtherapee.com) and use [darktable](https://www.darktable.org) exclusively. I've grown more and more fond of this amazing piece of software and how well thought out it is. Granted, it hits you hard at start, but it is worth investing some time to learn its ins and outs.

At the end of the day, both are very capable and produce good results. Also, both support `.CR2` and `.RW2` from my Canon 40D and my Panasonic Lumix LX10 respectively (see the [photo section](/photography)).

## Scripting

Most of my scripts are written in POSIX shell, even though for more complex things or when I get lazy and don't remember some of the weird POSIX syntax I also use Python from time to time.

## Weather in terminal

[wttr.in](https://wttr.in) serves weather information directly to the terminal. You can query it via curl. I have a shell function:

```sh
weather () {
	curl https://wttr.in/$1\?1Fn
}
```

Which I call with a location to check the weather:

```bash
$ weather Ottawa
Weather report: Ottawa

                Mist
   _ - _ - _ -  +9(7) °C
    _ - _ - _   ↙ 19 km/h
   _ - _ - _ -  8 km
                0.1 mm
                        ┌─────────────┐
┌───────────────────────┤  Sun 31 Oct ├───────────────────────┐
│             Noon      └──────┬──────┘      Night            │
├──────────────────────────────┼──────────────────────────────┤
│      .-.      Light drizzle  │               Overcast       │
│     (   ).    +10(8) °C      │      .--.     +10(8) °C      │
│    (___(__)   → 14-19 km/h   │   .-(    ).   → 17-24 km/h   │
│     ‘ ‘ ‘ ‘   2 km           │  (___.__)__)  10 km          │
│    ‘ ‘ ‘ ‘    0.2 mm | 86%   │               0.0 mm | 0%    │
└──────────────────────────────┴──────────────────────────────┘
Location: Ottawa, Ontario, Canada [45.4210328,-75.6900218]
```

## Additional utilities

Here is a list of utilities I have installed and use regularly.

-  [`fd`](https://github.com/sharkdp/fd) -- Amazing replacement for `find`
-  [`fzf`](https://github.com/junegunn/fzf) -- Terminal fuzzy finder and vim plugin
-  [`mons`](https://github.com/Ventto/mons) -- Handy script to manage external displays
-  [`sshfs`](https://github.com/libfuse/sshfs) -- Mount file systems over SSH/SFTP
-  `apropos` -- Search the man pages
-  [`units`](https://gnu.org/software/units) -- Convert units on the terminal
-  [`tealdeer`](https://github.com/dbrgn/tealdeer) -- Access [`tldr-pages`](github.com/tldr-pages/tldr) with style
-  [`pdfpc`](https://github.com/phillipberndt/pdfpc) -- Presenter console for for PDF files
-  [`tig`](https://github.com/jonas/tig) -- Text interface for `git`
-  `bc` -- Best calculator ;)
-  [`screen`](/blog/2021/gnu-screen-cheatsheet/) -- GNU terminal multiplexer

