+++
author = "Toni Sagrista Selles"
categories = ["Linux", "Privacy"]
tags = [ "security", "anonymity", "archlinux", "encryption", "luks", "dm-crypt", "lvm" ]
date = 2020-06-08
description = "Arch Linux installation with LUKS on LVM encryption"
linktitle = ""
title = "Arch with LUKS on LVM"
featuredpath = "date"
type = "post"
+++

It is well known that Arch Linux does not have the easiest install process of all Linux distributions. In my opinion, for technical users this is a big plus, as you get to know your system better simply by having to set it up from scratch. This comes with the perk that you only install the packages you need, leading to a smaller and arguably snappier system.

In this guide, I'm documenting my latest Arch Linux installation on my laptop, where I used full disk encryption with LUKS over LVM. BTW, you should **always** encrypt your disks on your mobile devices, either laptops or phones.It comes virtually for free, and it provides countless benefits. 

<!--more-->

There is a video version of a very similar installation process by LearnLinuxTV [here](https://invidio.us/watch?v=Lq4cbp5AOZM). You may want to use that instead if you'd rather follow a video tutorial.

Please note that this may become obsolete quickly, as the install process may change over time.
When we are done, we will have a system with a LUKS-encrypted physical volume with two logical partitions, `/` and `/home`. We will use `grub2` as a bootloader.

So, assuming you have the archiso USB ready, just plug it in, select it in your boot menu and start it.

## Network configuration

If you are using wired ethernet, you probably already have a connection. If you are using wifi, use the following to configure it.

```bash
# show interfaces
ip addr
wifi-menu
```
Select your wifi, enter your password and select 'connect'.

*The archiso I used (downloaded some time during the half part of May 2020) was broken and did not manage to connect to my wifi with `wifi-menu`. To solve that, I switched down the interface. Not sure why this worked, but keep it in mind in case you can't get a connection either.*

```bash
ip link set wlan0 down
```

## Setting up pacman mirrors

Update the repository index and edit the mirror list if the connection is slow:

```bash
pacman -Syyy
# uncomment desired mirrors
vim /etc/pacman.d/mirrorlist
# re-update repository index
pacman -Syyy
```

## Disk setup

Check your drives:

```bash
fdisk -l
```

We'll be installing Arch on the SSD `/dev/nvme0n1`. This will probably be different for you. et's now prepare the dist. We'll be creating two 500 MB partitions (for EFI and `/boot`), and another `ext4` partition for the logical volume.

```bash
fdisk /dev/nvme0n1
---------------------
#  below is the fdisk command line
#  let's start with listing the partitions
:  p
#  let's create a new 500 MB partition for EFI
:  n, enter, enter, +500M
#  and let's set the type to EFI
:  t, 1
#  now, let's create the /boot partition
:  n, enter, enter, +500M
#  let's set its type to 'Linux Filesystem'
:  t, 20
#  finally, let's create the LVM partition
:  n, enter, enter, enter
#  and let's set the type to 'Linux LVM'
:  t, 30
#  check everything is fine
:  p
#  write changes and exit
:  w
```

Our partitions are ready and we can start creating the LVM and files systems. At this point we have three partitions:

1.  `/dev/nvme0n1p1` for EFI. We'll format it with FAT.
2.  `/dev/nvme0n1p2` for `/boot`. We'll format it with EXT4.
3.  `/dev/nvme0n1p3` for LVM. We'll set up LUKS in this disk.

So, let's create the file systems:

```bash
mkfs.fat -F32 /dev/nvme0n1p1
mkfs.ext4 /dev/nvme0n1p2
```

## Set up LUKS on LVM

Now we need to set up encryption in the third disk. 

```bash
cryptsetup luksFormat /dev/nvme0n1p3
```

After that, you will need to type `YES` in capital letters and then enter your passphrase. Do not forget it ;)
Next, we need to open the encrypted device.

```bash
cryptsetup open --type luks /dev/nvme0n1p3 myvolume
```

You can give it any name (`myvolume` in my case), but remember it. Enter your passphrase.

Next, we need to configure LVM and create two partitions for the system and home. Let's first create the physical volume.

```bash
pvcreate --dataalignment 1m /dev/mapper/myvolume
```

Switch `myvolume` with whatever name you chose. Now, on to the volume group creation. I called my volume group `volumegroup`. My naming skills are over 9000.

```bash
vgcreate volumegroup /dev/mapper/myvolume
```

And finally, we are ready to create the logical volumes.

```bash
# first we create the system partition - I used 50 GB
lvcreate  -L 50GB volumegroup -n root
# then, we create the home partition with the rest of space
lvcreate -l 100%FREE volumegroup -n home
```

I create the root partition with the name `root` and the home partition with the name `home`. Also, I used all the space in the disk for my partitions, so I won't be able to use LVM snapshots. If you want this functionality, then reserve some free space to that purpose.

And now, let's create the file systems.

```bash
mkfs.ext4 /dev/volumegroup/root
mkfs.ext4 /dev/volumegroup/home
```

And mount them, along with the `/boot` partition.

```bash
mount /dev/volumegroup/root /mnt
mkdir /mnt/home
mount /dev/volumegroup/home /mnt/home
mkdir /mnt/boot
mount /dev/nvme0n1p2 /mnt/boot
mkdir /mnt/etc
```

## Proceed with the Arch Linux installation

Now our disk and partitions are set up an mounted, so let's generate the fstab file.

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

Now we are ready to actually starting the [regular installation of Arch](wiki.archlinux.org/index.php/Installation_guide). First use pacstrap to install the base package, the linux kernel and firmware. Then, chroot into the newly installed system.

```bash
pacstrap -i /mnt base linux linux-firmware
# switch to the installation disk
arch-chroot /mnt
```

We are now already operating from our installed system. We need to install some additionaly goodies. I've listed here some essentials. Particularly, you need the `lvm2` package.

```bash
pacman -S linux-headers intel-ucode base-devel neovim networkmanager wpa_supplicant wireless-tools netctl dialog lvm2
```

Install as many shit as your heart desires. You can feel guilty later when `neofetch` lists the number of packages in the thousands.
Now we enable the network manager so that systemd starts it automatically.

```bash
systemctl enable NetworkManager
```

Edit your hostname.

```
/etc/hostname # contains a single line with the host name.
----------------------------------------------------------
myhostname
```

And create the `etc/hosts` file with the following contents.

```
/etc/hosts
----------
127.0.0.1	localhost
::1		    localhost
127.0.1.1	myhostname.localdomain	myhostname
```
Remember to modify substitute `myhostname` with your host name.

**This step is important**. We need to enable encryption in the hooks of `mkinitcpio.conf`. To do so, edit the line which starts with `HOOKS=` in `/etc/mkinitcpio.conf` and add `encrypt` and `lvm2`. It should look like this:

```
/etc/mkinitcpio.conf
--------------------
[...]
HOOKS=(base udev autodetect modconf block encrypt lvm2 filesystems keyboard fsck)
[...]
```

And then run mkinitcpio.

```bash
mkinitcpio -p linux
```
If you installed another kernel, just substitute it in the command.

Now, uncomment your locale (remove the leading `#`) and generate it.

```
/etc/locale.gen
---------------
[...]
en_GB.UTF-8
[...]
```

```bash
locale-gen
```

## Set up user and passwords

Now, we set up the root password and create a user with superuser permissions. To do so, we add it to the `wheel` group, which we will add as superusers.

```bash
# change root password
passwd
# add user 'username'
useradd -m -g users -G wheel username
# change 'username' password
passwd username
```

Now, make users in the `wheel` group superusers by uncommenting a line in visudo.

```bash
# edit the visudo file
EDITOR=nvim visudo
```
```
visudo
------
[...]
%wheel ALL=(ALL) ALL
[...]
```

## Set up grub2

First install GRUB2 and some utilities

```bash
pacman -S grub efibootmgr dosfstools mtools os-prober
```

And edit `/etc/default/grub` and edit it so that the following lines are present.

```
/etc/default/grub
-----------------
[...]
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 cryptodevice=/dev/nvme0n1p3:volumegroup:allow-discards quiet"
[...]
GRUB_ENABLE_CRYPTODISK=y
[...]
```

Make sure that the name of the volume group is correct, as well as the partition it is located.
Mount the first partition we created as the EFI partition.

```bash
mkdir /boot/EFI
mount /dev/nvme0n1p1 /boot/EFI
```

And finally, install grub.

```bash
grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
```

Set up grub locale and generate the grub configuration file.

```bash
mkdir /boot/grub/locale
cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo
grub-mkconfig -o /boot/grub/grub.cfg
```

## Set up swap file

This is optional, but I usually like to use a swap file. To do so, run the following.

```bash
fallocate -l 8G /myswap
chmod 600 /myswap
mkswap /myswap
echo '/myswap none swap sw 0 0' | tee -a /etc/fstab
```

That is it, you can now install whatever display server you need, if any. Just follow the Arch Linux wiki for instructions on how to proceed from here.
I would usually install `xorg-server`, `ly-git`, `mesa` or `nvidia` and `i3-gaps`. Then I would deploy my [.dotfiles](/blog/2019/my-dotfiles), but that is another story.

I hope this guide helped!
