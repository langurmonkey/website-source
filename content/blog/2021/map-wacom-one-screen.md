+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "wacom", "drawing", "linux"]
date = "2021-03-01"
linktitle = ""
description = "How to map a graphics tablet to a single display in a multi-monitor setup in Linux"
title = "Map Wacom tablet to a single display"
type = "post"
+++

I have a Wacom Intuos graphics tablet for my occasional drawing and signing. By default, the tablet area is mapped to the whole screen area, making it almost unusable if you are using two or more monitors, as your drawing application of choice ([Krita](krita.org) in my case) usually resides in one display only. 

Well, turns out there's a very easy way to map the tablet to a single display in Linux with ``xinput``. But first, we need to find out the display we want to map the table to with ``xrandr``.

```bash
$ xrandr
Screen 0: minimum 8 x 8, current 7740 x 2160, maximum 32767 x 32767
DVI-D-0 connected 3840x2160+0+0 (normal left inverted right x axis y axis) 531mm x 299mm
   1920x1080     60.00*+
   1680x1050     59.95  
   1440x900      59.89  
   1280x1024     75.02    60.02  
   1280x720      60.00  
   1024x768      75.03    60.00  
   800x600       75.00    60.32  
   640x480       75.00    59.94  
HDMI-0 disconnected (normal left inverted right x axis y axis)
HDMI-1 disconnected (normal left inverted right x axis y axis)
DP-0 disconnected (normal left inverted right x axis y axis)
DP-1 disconnected (normal left inverted right x axis y axis)
DP-2 connected primary 3840x2160+3900+0 (normal left inverted right x axis y axis) 527mm x 296mm
   3840x2160     60.00*+  29.98  
   2560x1440     59.95  
   2048x1280     59.96  
   1920x1200     59.88  
   1920x1080     60.00    60.00    59.94    50.00    23.98  
   1600x1200     60.00  
   1600x900      60.00  
   1280x1024     75.02    60.02  
   1280x720      60.00    59.94    50.00  
   1152x864      75.00  
   1024x768      75.03    60.00  
   800x600       75.00    60.32  
   720x576       50.00  
   720x480       59.94  
   640x480       75.00    59.94    59.93  
DP-3 disconnected (normal left inverted right x axis y axis)
```

In my case, I have two displays. To the left, I use a 1080p Fujitsu connected via DVI (``DVI-D-0``). To the right, I have a 4K Dell connected via a display port (``DP-2``). Of course, I want to map the tablet to the 4K display to use the extra pixels.

Now, before actually doing the mapping with ``xinput``, we need to find the identifiers of our Wacom device:

```bash
$ xinput | grep Wacom
⎜   ↳ Wacom Intuos BT S Pad                   	id=11	[slave  pointer  (2)]
⎜   ↳ Wacom Intuos BT S Pen Pen (0x8880f16b)  	id=13	[slave  pointer  (2)]
    ↳ Wacom Intuos BT S Pen                   	id=12	[slave  keyboard (3)]
```

Here they are. The IDs are 11, 12 and 13, so let's map them to ``DP-2``:

```bash
$ xinput map-to-output 11 DP-2
$ xinput map-to-output 12 DP-2
$ xinput map-to-output 13 DP-2
```

And that's it. Easy-peasy!

