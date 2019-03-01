+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "programming", "scripts", "i3wm", "polybar", "rice" ]
date = 2019-03-01
description = "Modified version of memory, CPU and temperature applets"
linktitle = ""
title = "Polybar modules for memory, CPU and temperature"
featured = "polybar-cpu-mem.jpg"
featuredalt = "Polybar modules"
featuredpath = "date"
type = "post"
+++

A couple of days ago I sumbled upon [this video](https://www.youtube.com/watch?v=MNwpdqD_I8Y) from Luke Smith where he presented a couple of scripts to get CPU, memory and temperature information in [i3blocks](https://github.com/vivien/i3blocks). I use [polybar](https://github.com/jaagr/polybar) (it works better with my multiple monitors with different DPI), so I decided I'd adapt and change the scripts so that I can use them with polybar. You can find all these files in my [dotfiles repo](https://gitlab.com/langurmonkey/dotfiles).

## `memory.sh`

This script prints the amount of used memory with respect to the total available memory (uG/tG). If invoked with `--popup`, it brings up a notify-send popup with the top 10 memory intensive processes in the system.

```
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

```
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
