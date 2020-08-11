# Linux Phones

This is a collection of notes about running GNU/Linux operating systems on
smartphones, specifically the [Pine64 Pinephone](https://www.pine64.org/pinephone/)
but also probably applicable to the [Purism Librem 5](https://puri.sm/products/librem-5/)
and similar devices.

The focus of this page is on standard GNU/Linux distros such as postmarketOS,
Debian/Phosh, Fedora and so on. Ubuntu Touch UBports is a different kind of
creature altogether and many notes on this page may not apply there.

Table of Contents:

* [See Also](#see-also)
* [Web Browsers](#web-browsers)
    * [GNOME Web (Epiphany)](#gnome-web-epiphany)
    * [Firefox](#firefox)
* [Productivity Apps](#productivity-apps)
    * [Nextcloud](#nextcloud)
    * [KeePass](#keepass)
* [Security](#security)
* [Default Software by OS](#default-software-by-os)
    * [GNU Coreutils on postmarketOS](#gnu-coreutils-on-postmarketos)

# See Also

Listings of potential mobile-friendly Linux apps:

* [postmarketOS: Potential apps](https://wiki.postmarketos.org/wiki/Potential_apps)
* [Mobile GNU/Linux Apps](https://mglapps.frama.io/)
* [apps (Mobian Wiki)](https://wiki.mobian-project.org/doku.php?id=apps)

[Librem5](https://source.puri.sm/Librem5) gitlab has patches for some Linux
apps for mobile friendliness:

* [Geary mail client](https://source.puri.sm/Librem5/geary)

# Web Browsers

## GNOME Web (Epiphany)

postmarketOS, Mobian/Phosh and probably others ship with GNOME Web as the
default browser. It's currently the best optimized mobile web browser for
Linux and has built-in support to "Install Site as Web Application" to add
an app launcher for web apps.

Installed web apps run in a mode where the URL bar is replaced by just a
title bar and seems to have a sandboxed profile (no cookie sharing with the
normal GNOME Web sessions).

### User-Agent String

You may want to customize the User Agent to look like mobile Firefox so
that sites like `mobile.twitter.com` will give a more modern front-end UI
instead of one that looks themed after Android 2.x

Run this command to set the User-Agent to appear like Firefox:

```bash
gsettings set org.gnome.Epiphany.web:/org/gnome/epiphany/web/ user-agent "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Safari/537.361"
```

## Firefox

> See also [Firefox on postmarketOS Wiki](https://wiki.postmarketos.org/wiki/Firefox)

Firefox is another _decent_ web browser for mobile Linux. With a few `about:config`
tweaks you can enable better touch controls. Some parts of Firefox UI is not very
mobile friendly and you probably only want to open one tab per window, as the tab
bar doesn't fit on screen very well when you have 2+ tabs open.

To set the necessary about:config tweaks, easiest is to use your prefs.js.
From the postmarketOS wiki:

> Go in your profile directory (.mozilla/firefox/xxxxxxxx.default/) then exec:

```bash
echo 'user_pref("dom.w3c.touch_events.enabled", true);' >> prefs.js
echo 'user_pref("browser.gesture.pinch.in", "cmd_fullZoomReduce");' >> prefs.js
echo 'user_pref("browser.gesture.pinch.out", "cmd_fullZoomEnlarge");' >> prefs.js
echo 'user_pref("general.useragent.site_specific_overrides", false );' >> prefs.js
echo 'user_pref("general.useragent.override", "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Safari/537.361");' >> prefs.js
```

> And restart the browser.

# Productivity Apps

## Nextcloud

I use [Nextcloud](https://nextcloud.com/) as a self-hosted replacement for many
Google services (see my [Degoogle](/wiki/Degoogle) page).

GNOME Online Accounts already has built-in support to use Nextcloud and syncs
your Contacts and Calendar with the respective GNOME apps. You can also browse
your Nextcloud filesystem using the File Browser (Nautilus) app.

The desktop app for Linux is _probably_ not mobile friendly but it has a
command-line program called `nextcloudcmd` which may be usable to set up a
traditional sync to local filesystem. I haven't tested it yet.

## KeePass

I use the [KeePass password manager](https://keepass.info/) and so need to find a
good app for this that I can use from my smartphone.

Currently I haven't found a native app that is mobile-friendly and fits on the
small display of the phone.

As a workaround I found that [KeeWeb](https://keeweb.info/) has a usable enough
mobile interface in the form of a web application. I installed it as a plugin on
my Nextcloud server. For best security you might install it directly onto the
local host of your phone, e.g. with nginx and access it at http://localhost.
Otherwise self-host it on a web server you control.

# Security

At time of writing, GNU/Linux distros don't have a security model as good as what's
available on Android. Linux security mainly boils down to filesystem-level access
controls, but there's very little in the way to prevent two user-space apps from
messing with each other's data.

Like on a desktop Linux system, common sense applies, don't install random dodgy
software from unknown sources, don't `wget | bash` to run unknown scripts without
reading them first and verify what they're doing, etc.

On distros running Phosh your user password is required to be a numeric PIN code
that you unlock the screen with. These sorts of passwords are _very_ weak and
you may want to disable `sudo` access to your account and instead set a very
strong `root` user password.

Some misc tips relevant to Linux on smartphones:

* Use full disk encryption is available. Currently only postmarketOS seems to
  support this but is marked as "experimental." The idea being if your phone is
  lost or stolen you don't wanna make it easy for somebody to access the
  filesystem and steal secrets from Firefox's cookies or saved password store etc.
* Use the GNOME Keyring or similar whenever possible. You can use any complex
  password you want for this, the stronger the better.
* If your password is a numeric PIN code, disable sudo access to your account and
  either create a secondary sudoer user or configure a root password. Use strong
  passwords either way.
* If your phone listens on an SSH server, set up [SSH key-based authentication](https://www.ssh.com/ssh/key/)
  and disable login using password. Especially if your password is a numeric PIN
  code! Also disable root login over SSH.
* If you generate SSH _client_ keys on your phone, password protect those! In
  case your phone is lost/stolen it will buy you time to remove the phone's SSH
  keys from your servers' `authorized_keys` files.

# Default Software by OS

Just some notes on what each GNU/Linux distro comes with out of box and some
notes.

* postmarketOS/Phosh:
  * Phone, SMS
  * GNOME Web
  * Cheese photo booth
  * Extensions (GNOME)
  * Settings
  * GNOME Software (not mobile friendly)
  * King's Cross (terminal emulator)

* Fedora
  * Phone, SMS
  * GNOME Web
  * GNOME Contacts
  * Evolution mail client (not mobile friendly)
  * GNOME Software (not mobile friendly)

* Mobian/Phosh
  * Phone, SMS
  * GNOME Web
  * GNOME Contacts
  * GNOME Calendar (not mobile friendly)
  * GNOME Software (patches to make it mobile friendly)
  * Geary (mail client, mobile-friendly patches)
  * King's Cross (terminal emulator)

## GNU Coreutils on postmarketOS

postmarketOS is based on Alpine Linux which is a very minimalist distro and
ships with [Busybox](https://www.busybox.net/) by default, meaning standard
CLI tools like `grep`, `less` and `du` are Busybox versions and not the standard
GNU coreutils found on most Linux distros.

So some CLI options to these programs aren't supported in Busybox, like
`grep --exclude` or `du --max-depth` or `less -r` and several of my bash shell
aliases relied on these options.

To install GNU versions (see also [How to get regular stuff working](https://wiki.alpinelinux.org/wiki/How_to_get_regular_stuff_working)
from Alpine Linux wiki):

```bash
apk add coreutils grep less
```
