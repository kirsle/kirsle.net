# PowerTOP and USB Autosuspend

Some of this was touched on at [Fedora on Macbook](/wiki/Fedora-on-Macbook).

PowerTOP is a useful tool to get more battery life out of a laptop. It makes the difference of several hours of battery life, so it's a useful thing to install.

## PowerTOP

Install and enable it:

```bash
sudo dnf install powertop
sudo systemctl enable powertop.service
sudo systemctl start powertop.service
```

The service runs `powertop --auto-tune` which automatically sets most tunables to their "Good" state, for maximum battery life.

But sometimes it doesn't work well, especially with USB mice.

## USB Autosuspend

It perplexed me for a while why my USB mouse on a laptop would deactivate itself randomly (its LED turns off, and the mouse doesn't work until you click one of the buttons, and then it will power itself off again after a couple minutes...). Unplugging the USB mouse and plugging it back in would fix the problem and it would no longer auto-suspend itself. I was checking `/var/log/messages` and all the usual suspects until I realized it was PowerTOP that was the problem.

When `powertop --auto-tune` gets run, every USB device attached at the time gets the `auto` power management profile set, meaning they deactivate themselves to save power. On a keyboard or most other devices that's probably fine, but a mouse isn't. My workarounds have been to either *not* connect my USB devices until after my laptop boots into my desktop environment, or to unplug and replug the USB mouse after the fact.

I can't find a good "official" way to work around the problem. Google suggests editing things in `/etc/laptop-mode` but that isn't a thing in Fedora, and others have suggested setting up udev rules for your USB device, but that doesn't work either. I even found this [Power Management Guide][1] for Fedora 19 which pointed me to `powertop2tuned` to override powertop rules, but that didn't help me either.

My hacky work-around: make a shell script that starts on user log-in, that undoes PowerTOP's change to the USB device.

1. Run `sudo powertop` and go to the Tunables tab.
2. Find the entry like "Autosuspend for USB device Microsoft 3-Button Mouse with IntelliEye(TM) [Microsoft]", and toggle it into a "Bad" state (meaning it doesn't auto-suspend now).
3. When toggling it, PowerTOP shows a message of what it did to toggle it, which looks like:

    `echo 'on' > '/sys/bus/usb/devices/2-3.2.3.1/power/control'`

4. Create a shell script that does that job. I made mine at `~/bin/powertop-fix`:

```bash
#!/bin/sh

# Disable USB auto-suspend for my mouse on startup
sleep 5;
MOUSE="/sys/bus/usb/devices/2-3.2.3.1/power/control";
if [ -f "$MOUSE" ]; then
	echo 'on' > $MOUSE;
fi
```

5. Edit your sudoers file to allow running that script with no password:

```bash
kirsle  ALL=(ALL) NOPASSWD: /home/kirsle/bin/powertop-fix
```

6. Make `sudo /home/kirsle/bin/powertop-fix` start automatically using your desktop's session management settings (e.g. Xfce Sessions and Startup -> Application Autostart).

[1]: https://docs.fedoraproject.org/en-US/Fedora/19/pdf/Power_Management_Guide/Fedora-19-Power_Management_Guide-en-US.pdf