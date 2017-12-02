# Debian on Macbook

Debian is a bit trickier to install and set up on a Macbook than Fedora is ([Fedora on Macbook](/wiki/Fedora-on-Macbook)). Here's some information I found in comparison to Fedora.

All of this was done using Debian's graphical installer. YMMV if you use the text installer.

# Installation Notes

If you've never installed Debian on anything before, play around in VirtualBox for practice.

## EFI System Partition

In Fedora when you let it create its own partition layout, it would create its own EFI system partition for `/boot/efi` and install its boot code there. My disk looked like this:

1. `/dev/sda1`: Apple EFI System Partition
2. `/dev/sda2`: Mac OS X
3. `/dev/sda3`: Mac OS Recovery
4. `/dev/sda4`: Fedora EFI System Partition (`/boot/efi`)
5. `/dev/sda5`: Fedora boot partition (`/boot`)
6. `/dev/sda6`: Encrypted LUKS + LVM container
    * rootfs: `/`
    * home: `/home`
    * swap

With Debian on the other hand, if you're not careful it will just install its bootloader onto the same ESP partition as Apple's. If you don't want that and you'd prefer Debian to use your own ESP partition, these are the steps:

1. Create your ESP partition first. I made mine 200MB because that's what Fedora does, but it could be much smaller. 10MB, probably.
    * "Use as": "EFI System Partition"
2. Select the *existing* Apple EFI partition (/dev/sda1 in my case), and pick "Use as: do not use"
3. On the main screen of the (graphical) partition manager, there should be a letter "K" (for "keep") next to your *second* ESP partition and NOT next to the first one.

Keep your eye on it as you go and add partitions, because for example setting up an encrypted space or LVM will require writing the partition table and it will reset which partitions it wants to "keep" or not, and it will probably put the "K" next to the Apple ESP again!

## Aside: Encrypted LUKS + LVM

This isn't Mac specific, but Fedora makes it *so* easy to set up full disk encryption with LUKS (dm-crypt) and LVM and setting this up on Debian is a much more manual process.

The main thing to do is **make sure you create an encrypted volume first, THEN put the LVM on top of it.** If you do it the other way around you'll end up entering your encryption password once each for all the partitions inside the LVM!

So I set up my ESP and /boot partitions as normal (this part's easy), and then I picked the encrypted disk setup and chose the free space at the end of the disk for where to put the encrypted volume.

Once the encrypted volume was there I went into the Logical Volume Management and picked the `/dev/mapper/` crypto partition as the target. In the LVM you can add multiple logical volumes and this is done similarly to normal partitions, so I made one for rootfs (50GB), swap (4GB) and home (the remaining space).

# Apple Startup Manager

When I had Fedora on the Macbook: if I booted the computer while holding the Option key, the Apple Startup Manager would appear and list Mac OS X and Fedora as bootable targets, and any other bootable USB devices attached at the time. Also, under Mac OS X in the Startup Disk preferences, Fedora would have an entry and could be picked as the default operating system.

In Debian none of this got set up for me automatically.

I tried following directions [from here](http://glandium.org/blog/?p=2830) but just ended up with an unbootable system (or rather, it would simply boot into OS X; Debian was still missing from the Apple Startup Manager). YMMV.

I decided not to mess with it. What I found from researching is that:

* The Intel EFI spec says that EFI System Partitions (ESP) must be formatted as FAT filesystems.
* However, Apple has customized their EFI implementation to include a read-only HFS+ driver as well.
* For the Apple Startup Manager, the ESP is ignored entirely and it only cares about HFS+ partitions that were "blessed" (Fedora made and blessed an HFS+ partition, but Debian made the ESP as a FAT filesystem).
* When the system boots up, it:
    * First checks the Intel-compatible EFI for a bootable device, this is where Debian gets found.
    * If nothing is found, it goes to the Apple custom firmware system which finds the blessed HFS+ disks and ends up booting OS X.

Macbooks have an Intel FAT ESP partition but they don't use it to boot. It occasionally gets used as a staging area for firmware updates though.

In the event that the EFI boot gets messed up and prefers Mac OS instead (e.g. this happens when upgrading to a newer version of OS X), I'll just have to use a Linux LiveUSB and re-assign the preferred boot order via the `efibootmgr` command.

# Hardware Support

## Display Brightness

Unlike in Fedora, Debian fully supports all of the keyboard functions on the Macbook Air (mid 2015), including the display backlight keys. I now suspect this may have been an SELinux issue in Fedora, since Debian doesn't have SELinux and Fedora would try to adjust the brightness (showing a progress bar on-screen) but simply failing to.

## Broadcom Wireless

In Fedora you'd have needed to get RPMFusion and install `kmod-wl` or `akmod-wl` to get the wifi to work.

In Debian you can follow the [directions on the Debian wiki](https://wiki.debian.org/wl) to get the `wl` driver loaded. Briefly:

Enable the "non-free" repo in `/etc/apt/sources.list` and run these commands:

```bash
# Update and install linux headers and broadcom-sta-dkms
% apt-get update
% apt-get install linux-headers-$(uname -r|sed 's,[^-]*-[^-]*-,,') broadcom-sta-dkms

# Unload conflicting modules
% modprobe -r b44 b43 b43legacy ssb brcmsmac

# Load the wl driver
% modprobe wl
```