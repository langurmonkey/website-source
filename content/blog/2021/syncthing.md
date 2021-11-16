+++
author = "Toni Sagrista Selles"
categories = ["Syncthing"]
tags = ["cloud", "drive", "dropbox", "privacy", "linux", "english"]
date = 2021-11-15
linktitle = ""
title = "Use Syncthing to synchronize your files"
description = "Forget about third-party cloud solutions that invade your privacy"
featuredpath = "date"
type = "post"
+++

These days almost everyone uses services like Dropbox or mega.nz to store their important files and have them accessible wherever and whenever they need them. I'm told it is not uncommon to use these external services to back up *all* one's files, from photos to sensitive and private documents. Well, good news. If you actually care about your files and feel uneasy to have them all in other people's servers, you may want to have a look at [Syncthing](https://syncthing.net), an open source and free (as in free beer) continuous file synchronization program that synchronizes your files between your computers without being stored or ever going through third parties. In this post I'll talk about how it works and how to set it up to sync directories between your computers, laptops and phones.

<!--more-->

## Why use it

Why would you give up the convenience of having someone else storing your files for you? First and foremost, privacy. When you give away your private files to someone else you are giving away part of your privacy. It does not matter that they promise not to look at your data, or swear that even they can't look at the files because they are encrypted. These companies have been caught [time](https://www.infoworld.com/article/2621901/dropbox-caught-with-its-finger-in-the-cloud-cookie-jar.html) after time doing bad stuff, and the amount of power they have by holding millions of people's files is too large. You can't trust them, and you've got alternatives. Alternatives that do not require external parties' services, and that put you in control. Enter Syncthing.

Syncthing runs on your devices and syncs file over the network by establishing direct communications between them. This makes sense. In order to sync data between two or more devices without the intervention of a third party, these need to be online. Syncthing runs in a **distributed manner**, meaning that essentially all clients are at the same level and run the same software. They all talk to everyone. If you run a home server, a [NAS](/blog/2021/ts-351-review) or even a [Raspberry Pi](/blog/2021/raspberry-pi-4-first-impressions) you already have the means to easily set up your Syncthing and have your files always available.

{{< hint >}}
If you prefer a more centralized approach that uses a server-client scheme you might want to look at the also open source project [Nextcloud](https://nextcloud.com).
{{</ hint >}}

## Installing Syncthing

You need to install Syncthing in every computer that you want to sync.

Most distros have Syncthing packages available in their repository, so installing it is probably as easy as entering a single command in your terminal. In Arch Linux, you can do:

```bash
pacman -S syncthing
```

On Debian and derivatives, do:

```bash
apt install syncthing
```

And so on.

## Android?

If you have an android phone, you can find the [official Syncthing app in F-Droid](https://f-droid.org/en/packages/com.nutomic.syncthingandroid/). There is also [Syncthing-fork](https://f-droid.org/en/packages/com.github.catfriend1.syncthingandroid/), which is a fork of the former and the one I personally use. It brings some additional enhancements like individual sync conditions per device and directory.

## Using Syncthing

You can start Syncthing by running the `syncthing` binary. However, if you do it like this you need to start it every time you want it to run. In Linux it is usually better to enable the `systemd` *user* or *system* service so that it runs at startup. The *user* service only starts when the user is logged into the system, whereas the *system* service runs at startup even if there is no active user session.

Enabling and starting the user service is easy:

```bash
systemctl enable synchting@[USERNAME].service
systemctl start synchting@[USERNAME].service
```

The system service can be accessed with the name `synchting.service`.

Once Syncthing is running, it exposes its default interface via HTTP at the local port 8384. Fire up your browser and point it to `http://localhost:8384`. You will be greeted with the default web UI of Syncthing. From here, you can administer the shared directories and add additional 'partners', other devices to share files with.

{{< fig src="/img/2021/11/syncthing-webui_s.jpg" link="/img/2021/11/syncthing-webui.jpg" title="The default web UI of Syncthing with the dark theme and some folders." width="60%" class="fig-center" loading="lazy" >}}

You can find more information on the UI in the [official documentation of the project](https://docs.syncthing.net/intro/gui.html).

Keep in mind that after adding additional devices some time might be required for them to actually start synchronizing files. Just give it some time. 

Syncthing is very flexible. In each device, you can define what folders to share with whom. For instance, I run Synchting-fork on my phone and share only one directory (the `DCIM` directory that contains the photos made with the phone camera). This directory is only shared with my NAS. My desktop and laptop computers don't even see it. Additionally, for each shared folder you can choose whether you want versioning (keeping old versions of files when they are modified) and the share type. The share type specifies whether the folder is **share** (data is sent to others, but if the directory changes elsewhere the files are not updated) or **share and receive** (the changes to files in the directory are shared regardless of where they happen).

## Conclusion

If you want to get away from traditional cloud-based sync systems you've got options. A centralized approach for those who run their own server is Nextcloud. Syncthing, on the other hand, does a peer-to-peer synchronization that might appeal more to the layman. The project is mature and works very well.
