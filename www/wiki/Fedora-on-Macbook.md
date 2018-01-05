# Fedora on Macbook

Notes on running Fedora Linux on a Macbook (Air 2015).

# What Doesn't Work

Most functionality works out of the box: media keys on the keyboard (keyboard backlight brightness, playback keys, volume control).

Things that don't work: monitor backlight brightness keys (the keyboard brightness DOES work, though) and the Facetime HD camera, which identifies itself as a PCI device rather than USB and there are no generic webcam drivers for Linux that can work with a PCI webcam.

# Installation/Boot

Make a Fedora USB stick like usual. Hold Option when booting the Macbook and choose the Fedora Media from USB to boot.

I found that rEFIt/rEFInd are no longer necessary when installing Fedora. Just free up some partition space and allow Fedora to automatically create a partition layout, and it sets up a /boot/efi HFS+ partition automatically to make the OS bootable. Manual instructions for this are available for Debian and Arch, etc.

GRUB installs itself and things work just like any other PC. In Fedora (as of v22), the GRUB menu lists a couple entries for Mac OS X (32-bit and 64-bit) but neither one works. Booting Fedora works though.

To boot OS X, hold down the Option key during boot and pick OS X from the firmware bootloader. If you want OS X to be the default OS you can pick it as the System Disk from within OS X's settings. In this case, to boot Linux you'd hold Option on boot and choose Fedora, which takes you to GRUB and then you boot Fedora from there.

# Backlight Brightness

See <http://sh.kirsle.net/mb-brightness> for this. The keyboard brightness keys (in Xfce at least) don't work; they show a brightness graph but the actual brightness doesn't change. This script uses root to write brightness values to files in /sys.

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
echo 0 | sudo tee /sys/module/hid_apple/parameters/iso_layout
echo 1 | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd
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