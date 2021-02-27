+++
author = "Toni Sagrista Selles"
categories = ["Hardware"]
tags = [ "nas", "qnap", "storage", "linux"]
date = "2021-02-18"
description = "I got myself a QNAP TS-351-2G NAS a year ago, here is my review"
linktitle = ""
title = "NAS review: QNAP TS-351-2G"
type = "post"
+++


A little over a year ago, in January 2020, I got myself a QNAP TS-351-2G 3-bay NAS in order to store all of my and my family's data in a failsafe RAID configuration. I opted for the somewhat unconventional 3-bay setup in an attempt to trade off limited physical space at home with storage capacity. I don't have much space in my living room for a big NAS, and the 2-bay options, albeit being very compact, are limited to RAID-1, where half of the space is used for storage and the other half is used for redundancy protection (data is basically mirrored on the second drive). In QNAP's website there are three 3-bay *Home* options: the entry-level TS-332X, the middle-range TS-328 and the high-end TS-351. So I thought to myself, "*I'm getting the high-end unit, how bad can it be?*". Well, now that I have been using this NAS for a year I think I can answer this question.

<!--more-->

<p style="float: right; width: 40%; margin: 0 0 1em 1em;">
<img src="/img/2021/02/qnap-ts351.jpg"
     alt="QNAP TS-351"
     style="width: 100%" ></img>
</p>

### The good

The device has some redeeming properties. It is compact and well built. It is quiet to the point that it's actually hard to hear it is doing anything at all. The android apps generally work well and get the work done. The QTS software has many options and there's tons of apps you can install. Sometimes it looks a little bloated, but I guess that's just me.

### The bad

The list of bad things is longer. Let's see...

#### CLI

It is clear that a terminal emulator is a second or third-class citizen for QNAP. You can `ssh` into your NAS, but the environment you find is quite bare, and installing stuff is cumbersome. The overall CLI experience is lacking and that is a big downside for me.

#### LVM incompatibility

This is a problem with all QNAP devices. In the eventual case of a NAS hardware fail, **you can't recover the data by removing the disks and plugging them in elsewhere**. You absolutely need a QNAP device, as they ship their own implementation of LVM which renders it incompatible with non-QNAP hardware. This kind of vendor lock-in is an utter shame, it's *bullshit*, and had I made my homework and researched this properly before buying, I would have never bought QNAP in the first place. Synology, for example, uses plain LVM, and their RAID is [readable from any Linux](https://www.synology.com/en-global/knowledgebase/DSM/tutorial/Storage/How_can_I_recover_data_from_my_DiskStation_using_a_PC).

#### The hardware

With that show-stopping nonsense out of the way, let's continue. Together with the NAS, I bought three Seagate ST1000DMZ10 BarraCuda compute 3 TB hard drives, plus a 256 GB Silicon Power NVMe SSD to use as cache. I installed everything easily. The hardware is generally well built. No complains there. I turned it on and configured it in a RAID-5 setting, where I would have 6 TB of usable space, and 3 TB would be used for data protection. So far so good. Let's look at the hardware closely.


##### Running out of memory

From a distance, the TS-351-2G looks like agood machine overall. The 2 GB of RAM are a bit on the scrawny side, but it should be enough to run an embedded Linux, right? Well, nope. Not enough. Is it due to their software being bloated? Maybe, but they must have also realized that 2 GB is far too low nowadays for a NAS with an HDMI port that is supposed to connect to the TV and perform the functions of an HTPC, as the 2 GB option is now listed as EOL on their website. I noticed that too, and less than a week after the purchase I got myself a HyperX Impact 4 GB 1866 RAM stick and installed it. Most QNAP NASes are quite picky as to what memory sticks can be expected to work with them. They even have compatibility lists on their website for each model, so I made sure this one works with the TS-351. I installed it and the system works a bit better now.

##### Processor

Now the CPU. It comes with a 2013 Celeron J1800, and God, it is slow. In my opinion, the processor breaks the package. It works well enough for the lesser demanding tasks like moving data around and browsing through QTS, the web interface used to interact with the NAS, but once it needs to do any serious task like video transcoding or streaming it just falls flat. One would have thought that a NAS with an HDMI port would be at least capable of decently playing back video. Frack me, right?

##### HTPC?

So here is my recommendation. **DO NOT GET THIS NAS** if you plan on plugging it directly to your TV and use it as an HTPC. If it isn't clear enough yet: This is not an HTPC and it does not work well as an HTPC. Why this has an HDMI connection at all, I will never know. The software that is supposed to enable direct rendering through HDMI, called [HybridDesk Station](https://www.qnap.com/en/how-to/tutorial/article/installing-hybriddesk-station), is just unusable most of the time. Wait times are loooong. Any action you take is followed by long seconds  of "*Please wait, loading...*". Video playback only works well in sub-HD resolutions (720p and below). Full HD (1080) is not fluid at all. Depending on your video's encoding, It won't work at all--forget about HEVC/H.265. If you are a masochist and still want to try, bad luck. You need to buy an additional license for a bullshit product that implements HEVC transcoding and other mundane features. Not nice, QNAP.

### Conclusion

The list of problems goes on, but I will stop here.
In short, I do not recommend getting the TS-351 if you plan to use it for anything other than just storing your data and mounting it remotely in your other devices (and if so, just get a 3-bay NAS without the HDMI interface), or if you expect the data to be recoverable when your NAS crashes. Video playback, transcoding, streaming, or anything similar won't work. I reckon the old, slow CPU is to blame here. I will probably never buy a QNAP device again due to the LVM issue.
