+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "programming", "scripts", "i3wm", "polybar", "rice" ]
date = 2019-03-01
description = "Modified version of system monitor scripts"
linktitle = ""
title = "System monitoring polybar modules"
featured = "polybar-cpu-mem.jpg"
featuredalt = "Polybar modules"
featuredpath = "date"
type = "post"
+++

A couple of days ago I sumbled upon [this video](https://www.youtube.com/watch?v=MNwpdqD_I8Y) by Luke Smith where he presented a couple of scripts to display CPU, memory and temperature information in [i3blocks](https://github.com/vivien/i3blocks). Since I use [polybar](https://github.com/jaagr/polybar) due to it working much better in tandem with my dual-monitor setup with different DPIs, I decided I'd adapt and change the scripts to work in polybar. Polybar already comes with memory, CPU and temperature modules by default, but they don't include a popup showing the top-consuming processes, which is a nice feature to have.

You can find all these files in my [dotfiles repo](https://gitlab.com/langurmonkey/dotfiles).

For this setup we need two bash scripts, `memory.sh` and `cpu.sh`, and a few extra lines in the polybar config file `~/.config/polybar/config` to set up the modules. Let's see the details.

## `memory.sh`

This script prints the amount of used memory with respect to the total available memory (uG/tG). If invoked with `--popup`, it brings up a notify-send popup with the top 10 memory intensive processes in the system.

```bash
#!/bin/sh
case "$1" in
    --popup)
        notify-send "Memory (%)" "$(ps axch -o cmd:10,pmem k -pmem | head | awk '$0=$0"%"' )"
        ;;
    *)
        echo " $(free -h --si | awk '/^Mem:/ {print $3 "/" $2}')"
        ;;
esac
```

## `cpu.sh`

This is very similar to the memory script. It prints CPU usage and temperature, and a popup with a list of the top 10 CPU processes when invoked with `--popup`. 

```bash
#!/bin/sh
case "$1" in
    --popup)
        notify-send "CPU time (%)" "$(ps axch -o cmd:10,pcpu k -pcpu | head | awk '$0=$0"%"' )"
        ;;
    *)
        echo " $(grep 'cpu ' /proc/stat | awk '{cpu_usage=($2+$4)*100/($2+$4+$5)}
        END {printf "%0.2f%", cpu_usage}')
         $(sensors | grep temp1 | head -1 | awk '{print $2}')"
        ;;
esac
```

## Polybar configuration

Finally, in our polybar configuration file, we need to create the modules like this:

```
[bar/my-bar]
...
modules-right = [...] memory-info cpu-info [...]

[module/memory-info]
type = custom/script
exec = ~/.config/polybar/scripts/memory.sh
click-left = ~/.config/polybar/scripts/memory.sh --popup
format-underline = ${colors.primary}

[module/cpu-info]
type = custom/script
exec = ~/.config/polybar/scripts/cpu.sh
click-left = ~/.config/polybar/scripts/cpu.sh --popup
format-underline = ${colors.primary}
```

That is all, just remember to modify the path to the script files.
