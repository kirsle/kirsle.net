# Fedora on Macbook

Notes on running Fedora Linux on a Macbook (Air 2015).

Updated September 19, 2018 on Fedora 28 (Xfce Desktop).

# What Works?

Most functionality works out of the box. The function keys to control the display
brightness, keyboard backlight brightness, and media playback control all work
fine. The keys for Mission Control and Dashboard are recognized by X11 as keys
named `XF86LaunchA` and `XF86LaunchB` respectively, and could be bound to custom
application shortcuts or whatever.

For example I bound the Dashboard key to `xfdashboard` which gives me a GNOME 3
like overview of my desktop that I'll probably never use.

* Function keys: all supported
* Suspend and Hibernate: works, but Xfce desktop gets confused if you use "suspend when the laptop lid is closed" and enters a suspend-wakeup-suspend cycle; but manual suspending is fine.
* Bluetooth: recognized but audio quality is flaky
* WiFi: with proprietary Broadcom `wl` driver
* Camera: doesn't work, but see below.
* SD Card Reader: works
* External Display: works

## WiFi

The WiFi chip in the Macbook Air is a Broadcom device that uses the `wl` driver.

It's easily available from RPMFusion via the `akmod-wl` package and then you
never need to worry about it again.

Use a USB to Ethernet adapter or use USB tethering from your mobile phone to
download the `wl` driver.

# What Doesn't Work?

## FaceTime HD Camera

The webcam on the Macbook is a strange device because it's registered on the
motherboard as a PCIe device rather than USB like what most laptop webcams are.

There are generic USB video drivers that work for all USB cameras but there
aren't generic PCIe drivers because PCIe cameras are rare.

I found [this project](https://github.com/patjak/bcwc_pcie) for a Linux driver
that gets the camera to work, but I haven't tested it.

## Bluetooth is flakey

The Bluetooth quality is pretty bad, with audio lagging and hanging and
disconnecting a lot. I haven't tried other kinds of Bluetooth functionality.

Inserting a USB Bluetooth adapter caused the system to prioritize that device
over the built-in which worked around any audio problems.

# Installation/Boot

Make a Fedora USB stick like usual. Hold Option when booting the Macbook and
choose the Fedora Media from USB to boot.

I found that rEFIt/rEFInd are no longer necessary when installing Fedora.
Just free up some partition space and allow Fedora to automatically create a
partition layout, and it sets up a /boot/efi HFS+ partition automatically to
make the OS bootable. Manual instructions for this are available for Debian
and Arch, etc.

GRUB installs itself and things work just like any other PC. In Fedora
(as of v22), the GRUB menu lists a couple entries for Mac OS X (32-bit
and 64-bit) but neither one works. Booting Fedora works though.

To boot OS X, hold down the Option key during boot and pick OS X from the
firmware bootloader. If you want OS X to be the default OS you can pick it
as the System Disk from within OS X's settings. In this case, to boot Linux
you'd hold Option on boot and choose Fedora, which takes you to GRUB and then
you boot Fedora from there.

# Backlight Brightness

When I first started running Fedora on my Macbook it was Fedora 22 and the
display backlight keys didn't work, so I wrote a script to do this the hard
way. The script may still be useful if this problem comes back again.

See <https://sh.kirsle.net/mb-brightness> for this. The keyboard brightness
keys (in Xfce at least) don't work; they show a brightness graph but the
actual brightness doesn't change. This script uses root to write brightness
values to files in /sys.

In case that link stops working, it basically manipulates values in these two
files (writable only to root):

```
BRIGHTNESS     = "/sys/class/backlight/intel_backlight/brightness"
MAX_BRIGHTNESS = "/sys/class/backlight/intel_backlight/max_brightness"
```

`MAX_BRIGHTNESS` has some arbitrary value like `2777` and you just write a
number between 0 and `MAX_BRIGHTNESS` into the other file.

```bash
# to set the display to 50% brightness, you get the max brightness
$ cat /sys/class/backlight/intel_backlight/max_brightness
2777

# divide it in half
$ perl -E 'say 2777 / 2'
1388.5

# write that into the brightness file
$ echo 1388 | sudo tee /sys/class/backlight/intel_backlight/brightness
```

# Battery Saving

Use `powertop` to tune the battery. The easiest thing is to just make it run `--auto-tune` automatically on boot via systemd.

The `powertop` package comes with a systemd service you can enable. If you don't have one for some reason, create `/etc/systemd/system/powertop.service` with these contents:

```ini
[Unit]
Description=Powertop tunings

[Service]
Type=oneshot
ExecStart=/sbin/powertop --auto-tune

[Install]
WantedBy=multi-user.target
```

And enable the service with `sudo systemctl enable powertop.service`

Other things to mess with are `powertop --calibrate` and `powertop --html`

With this you can typically squeeze 7+ hours of battery life out of the 13" Macbook Air 2015 (which gets about 12 hours battery life under OS X, but this is possibly the best you can do with non-Apple software on a Macbook).

# Keyboard Tweaks

This section provides some tips on changing keyboard settings. All of these are temporary (they don't persist across reboots), and making them permanent varies from distro to distro. [Arch Linux](https://wiki.archlinux.org/index.php/Apple_Keyboard) and [Ubuntu](https://help.ubuntu.com/community/AppleKeyboard) make them permanent by adding configs to `/etc/modprobe.d/hid_apple.conf` and maybe rebuilding the initramfs (Fedora uses `dracut` and this whole method *does not work*).

The way to make these changes permanent in Fedora is to use systemd's `rc.local` compatibility service. This works as of Fedora 22.

Create a shell script at `/etc/rc.d/rc.local` with the commands below for the features you want to enable. For example:

```bash
#!/bin/bash
echo 0 | tee /sys/module/hid_apple/parameters/iso_layout
echo 1 | tee /sys/module/hid_apple/parameters/swap_opt_cmd
```

Make the script executable (`sudo chmod 0755 /etc/rc.d/rc.local`) and reboot.

## Tilde/Backtick Key

The keyboard layout on the Macbook maps the tilde/backtick key to `<` and `>` under Linux. The fix that works for me is:

```
$ echo 0 | sudo tee /sys/module/hid_apple/parameters/iso_layout
```

## Swap the Command and Option Keys

By default the Option/Alt key is mapped as Alt in Linux, and the Command key is mapped to Super (equivalent to the Windows key on a PC). To swap these the other way around, so e.g. Command+Tab brings up the window switcher instead of Alt+Tab (as it does under Mac OS X), do this:

```
$ echo 1 | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd
```

## Function Keys

By default if you want to input a function key (F1-F12) you have to hold Fn and press the key you want. Otherwise those keys map to the media keys when pressed. You can swap this behavior backwards (sort of like a `Fn Lock` feature of some PCs), so that the keys will input their function key when pressed and you need to hold Fn down to input the media key.

```bash
# FnLock ON
$ echo 2 | sudo tee /sys/module/hid_apple/parameters/fnmode

# FnLock OFF
$ echo 1 | sudo tee /sys/module/hid_apple/parameters/fnmode
```

If you echo `0` into it, it effectively *disables* the `Fn` key. So pressing `Fn+F11` is the same as pressing `F11` and this renders the media functions inaccessible.