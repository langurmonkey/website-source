+++
author = "Toni Sagristà Sellés"
title = "Upgrading the Steam Deck SSD"
description = "A step-by-step guide to upgrade the internal drive of Valve's Steam Deck"
date = "2023-07-10"
linktitle = ""
featured = ""
featuredpath = ""
featuredalt = ""
categories = ["Steam Deck"]
tags = ["technology", "graphics", "technical", "steam", "english"]
type = "post"
draft = false
+++

I got my Steam Deck almost [a year ago](https://mastodon.social/@jumpinglangur/109279233328548307). I got the cheapest 64 GB model fully expecting that I would need to upgrade its internal M.2 2230 NVMe SSD to something with more capacity down the road. Well, the day finally came. In this post I report the quick and painless process I followed to successfully upgrade the Steam Deck 64 GB SSD to a more than respectable 1 TB M.2 NVMe drive. Here are the steps involved in the process:

- [step 0: requirements](#step0)
- [step 1: open the deck](#step1)
- [step 2: clone the drives](#step2)
- [step 3: resize home partition](#step3)
- [step 4: wrap-up](#step4)

<!-- More -->

## Step 0: Requirements
<div id="step0"></div>

Obviously, you need to first get your new SSD. I got a Corsair MP600 Mini 1TB M.2 NVMe PCIe x4 offf Amazon for 112 euros ([here](https://www.amazon.de/dp/B0C28HLKNB)). Additionally, since I did not want to open my PC and always tend to choose the route of lower friction, I got [this](https://www.amazon.de/dp/B0BGS3NZ4C) M.2 NVMe USB case. You will also need a small Phillips screwdriver, and a plastic opening pick.

{{< fig src="/img/2023/07/deck-start.jpg" class="fig-center" width="65%" title="Everything ready: Steam Deck, SSD and screwdriver. SD card out of the slot!" loading="lazy" >}}

## Step 1: Open the Deck
<div id="step1"></div>

{{< notice "Important" >}}
Remember to remove the SD card from the SD card slot before proceeding. Otherwise you may damage it when opening the device!
{{</ notice >}}

The first step is simple. Use your Phillips screwdriver to remove the four 9.5 mm screws and the four 5.8 mm screws from the back of the Deck. Then use an opening pick to push on the small gap between the front and back covers. You should hear a few 'clicks' as the back cover comes loose. After that, remove the screws from the shield (including the hidden one under the shiny sticker) and you have direct access to the SSD. Remove the shielding and you are good to go.

{{< fig src="/img/2023/07/deck-openback.jpg" class="fig-center" width="65%" title="The back cover removed, ready to extract the shield. Under it is the 64 GB SSD." loading="lazy" >}}

A nice guide on how to open the deck for SSD replacement can be found [here](https://www.ifixit.com/Guide/Steam+Deck+SSD+Replacement/148989).

## Step 2: Clone the drive
<div id="step2"></div>

In this step we clone the partitions and data in old SSD to the new one. To that effect, we'll use a computer with Linux. If you don't have access to one, you may want to look into using [CloneZilla](https://clonezilla.org) or something similar. Since I only have one one M.2 USB case, I'm using a 2-step process: first, I clone the old 64 GB drive into an image file in my PC, and second, I restore this image to the new 1 TB drive.

First, we insert the old SSD and use `lsblk` find out the device name we need to create the image.

```bash
➜ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 232.9G  0 disk 
├─sda1   8:1    0   512M  0 part 
├─sda4   8:4    0 108.3G  0 part /
└─sda5   8:5    0 124.1G  0 part /home
sdb      8:16   0 931.5G  0 disk 
└─sdb1   8:17   0 931.5G  0 part /bigdata
sdc      8:32   1     0B  0 disk 
sdd      8:48   1     0B  0 disk 
sde      8:64   1     0B  0 disk 
sdf      8:80   1     0B  0 disk 
sdg      8:96   0  57.6G  0 disk 
├─sdg1   8:97   0    64M  0 part 
├─sdg2   8:98   0    32M  0 part /run/media/tsagrista/efi
├─sdg3   8:99   0    32M  0 part /run/media/tsagrista/efi1
├─sdg4   8:100  0     5G  0 part /run/media/tsagrista/rootfs
├─sdg5   8:101  0     5G  0 part /run/media/tsagrista/rootfs1
├─sdg6   8:102  0   256M  0 part /run/media/tsagrista/var1
├─sdg7   8:103  0   256M  0 part /run/media/tsagrista/var
└─sdg8   8:104  0    47G  0 part /run/media/tsagrista/home
sr0     11:0    1  1024M  0 rom  
```

In my case, the Steam Deck SSD is in `/dev/sdg`. It contains 8 partitions, form `/dev/sdg1` to `/dev/sdg8`. Then, we use `dd` (aka disk destroyer) to copy its contents to our PC. If we use the device name, `/dev/sdg`, the whole disk will be copied, including all partitions and the partition table. That is what we want, as the first 7 partitions are system partitions which contain the bootloader and root file system of the Deck. Note that you probably need to run the command with `sudo`.

```bash
dd if=/dev/sdg of=./steamdeck-2230-64gb.img status=progress
```

{{< fig src="/img/2023/07/deck-dding.jpg" class="fig-center" width="65%" title="Running the dd command." loading="lazy" >}}

Once this has finished, the file `steamdeck-2230-64gb.img` contains the full image of the disk. We now need to dump it to the new SSD, using a very similar command:

```bash
dd if=./steamdeck-2230-64gb.img of=/dev/sdg status=progress
```

{{< notice "Note" >}}
If you have two M.2 slots in your computer, you can clone the drives without an intermediate file. Just use `dd if=/dev/sdX of=/dev/sdY status=progress`, where `sdX` is the old drive and `sdY` is the new one.
{{</ notice >}}


Now our 1 TB SSD contains an exact clone of our 64 GB original Deck SSD. The problem is that the size of the home partition (`/home`) is only 47 GB. We need to resize it.

## Step 3: Resize home partition
<div id="step3"></div>

The easiest way to resize the home partition is to use a partition program like Gparted or similar. With Gparted, you need to select `/dev/sdg8` and just resize it to take up all the empty space at the back of the drive. In my case, this gives me a home partition of 920.89 GB.

{{< fig src="/img/2023/07/deck-gparted.jpg" class="fig-center" width="65%" title="I used Gparted to resize the home partition. This is the resulting layout of the 1 TB SSD before inserting it into the Steam Deck." loading="lazy" >}}

## Step 4: Wrap-up
<div id="step4"></div>

Finally, just insert the newly cloned SSD into the deck and close it. Start it to make sure that everything went smoothly. The Steam Deck should boot without problems with the new SSD.

{{< fig src="/img/2023/07/deck-done.jpg" class="fig-center" width="65%" title="Everything went fine. The new drive is now available!" loading="lazy" >}}

