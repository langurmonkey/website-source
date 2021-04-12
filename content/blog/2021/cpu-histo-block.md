+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = ["i3wm", "linux", "i3blocks"]
date = 2021-04-12
linktitle = ""
title = "CPU core load graph script for your bar"
description = "Simple script to add a CPU core load to your favorite bar"
featuredpath = "date"
type = "post"
+++

A while back I changed my bar from Polybar to `i3blocks`. One of the things I missed of Polybar is its internal CPU module, which can produce a core load graph directly in your bar by adding the right `ramp` characters. In this post I'm sharing a simple POSIX shell script I've written that does the same and can be used with any text-based bar. Here is what it looks like:

{{< figure src="/img/2021/04/cpu-levels.gif" title="CPU core load graph in my bar" width="50%" class="fig-center" >}}

<!--more-->

The script is the following:

{{< highlight sh "linenos=table" >}}
#!/bin/sh

# Define array
ramp_arr=(▁ ▂ ▃ ▄ ▅ ▆ ▇ █)

sar -P ALL 1 1 | grep -E 'Average:\s+[0-9]+' | while read -r line ; do
    val=$(echo $line | awk '{cpu_usage=$3} END {printf "%0.2f", cpu_usage}')
    idx=`echo "scale=4; $val/14.3" | bc`
    intidx=$( printf "%.0f" $idx )
    printf "${ramp_arr[$intidx]}"
done
echo
{{</ highlight >}}

It uses the `sar` command to get the CPU readings for one second, and then it selects the relevant lines with `grep`. The lines are then processed with `awk` to extract the CPU usage for each core. The usage is then converted to an index in the array `$ramp_arr`, which contains the characters to output depending on the load level.

Here is the block code in the configuration file of `i3blocks`.

{{< highlight txt >}}
[cpulevels]
command=$LOCAL_DIR/cpu-levels
interval=repeat
color=#ffffff
border=#62ef3b
border_right=0
border_left=0
border_top=0
border_bottom=1
markup=pango
{{</ highlight >}}

