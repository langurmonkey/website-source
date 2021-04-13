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

A while back I changed my bar from Polybar to `i3bar` with `i3blocks`. One of the things I missed about Polybar is its internal CPU module, which can produce a core load graph directly in your bar by adding the right `ramp` characters. In this post I'm sharing a simple POSIX shell script I've written that does the same and can be used with any text-based bar. Here is what it looks like:

{{< figure src="/img/2021/04/cpu-levels.gif" title="CPU core load graph in my bar" width="35%" class="fig-center" >}}

<!--more-->

This is the script.

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

We use the `sar` command to get the CPU readings for one second, and then select the relevant lines with `grep`. The result of `sar -P ALL 1 1` is a data point taken over one second, plus the average at the end. This can be modified by changing the parameters. Below is the output with my *i7-7700*.

{{< highlight sh >}}
$  sar -P ALL 1 1
Linux 5.11.11-arch1-1 (hidalgo) 	13/04/21 	_x86_64_	(8 CPU)

09:26:25        CPU     %user     %nice   %system   %iowait    %steal     %idle
09:26:26        all     27.04      0.00     10.48      0.00      0.00     62.48
09:26:26          0     32.35      0.00      7.84      0.00      0.00     59.80
09:26:26          1     26.17      0.00     12.15      0.00      0.00     61.68
09:26:26          2     33.01      0.00     11.65      0.00      0.00     55.34
09:26:26          3     26.73      0.00      7.92      0.00      0.00     65.35
09:26:26          4     24.51      0.00      8.82      0.00      0.00     66.67
09:26:26          5     26.73      0.00      9.90      0.00      0.00     63.37
09:26:26          6     23.00      0.00     12.00      0.00      0.00     65.00
09:26:26          7     23.81      0.00     13.33      0.00      0.00     62.86

Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
Average:        all     27.04      0.00     10.48      0.00      0.00     62.48
Average:          0     32.35      0.00      7.84      0.00      0.00     59.80
Average:          1     26.17      0.00     12.15      0.00      0.00     61.68
Average:          2     33.01      0.00     11.65      0.00      0.00     55.34
Average:          3     26.73      0.00      7.92      0.00      0.00     65.35
Average:          4     24.51      0.00      8.82      0.00      0.00     66.67
Average:          5     26.73      0.00      9.90      0.00      0.00     63.37
Average:          6     23.00      0.00     12.00      0.00      0.00     65.00
Average:          7     23.81      0.00     13.33      0.00      0.00     62.86
{{</ highlight >}}

We need the average lines for each of the 8 cores, from 0 to 7. We select the relevant lines with `grep -E 'Average:\s+[0-9]+'`. This selects as many lines as cores. If you have more or less than 8, it should also work.

After that, we process each of these lines by taking the column number 3 (`%user` column, which contains the percentage of CPU utilization that occurred while executing at the user level) with `awk`, and we convert it to the ramp array (`$ramp_arr`) index with some math using `bc`. Finally, the ramp character is printed and we go on to the next core.

Here is the block as it appears in my `i3blocks` configuration file.

{{< highlight txt >}}
[cpulevels]
command=$LOCAL_DIR/cpu-levels
interval=repeat
color=#ffffff
border=#62ef3b
border_right=0
border_left=0
border_top=0
kborder_bottom=1
markup=pango
{{</ highlight >}}

