# Self Hosting

These are my notes from an experiment with running a bunch of self-hosted
cloud services, and to see how well Android works in 2018 without Google
services.

My device is a Nexus 7 (2013) w/ LTE (Project Fi) running Lineage OS 14.1
(Android 7) without Google Play Services installed. My server is running
Debian 9 (Stretch).

Later on when my Nexus 7's screen took some physical damage and stopped working,
I re-ran this experiment on a Pixel (1st gen) with Lineage OS 16 (Android 9),
again **without** Google Play Services installed.

* [Summary of Solutions](#summary-of-solutions)
* [Play Store Apps](#play-store-apps)
* [Server Software](#server-software)
	* [Email: IMAP &amp; SMTP](#email-imap-smtp)
	* [Webmail](#webmail)
	* [Calendars and Contacts](#calendars-and-contacts)
* [File Sync](#file-sync)
* [Messaging](#messaging)

---

# Summary of Solutions

My Android without Google tablet has the following features now:

* Self-hosted e-mail account.
* Contacts and Calendar sync from self-hosted WebDAV.
* File sync for photo backups, password vault, etc.
* Fennec browser which is just rebranded _Firefox for Android_ with Firefox
  Sync, uBlock Origin and other familiar features.

Links to software used:

* E-mail Hosting:
	* Webmail: [Roundcube](https://roundcube.net/)
	* Android: [K-9 Mail](https://f-droid.org/en/packages/com.fsck.k9/) or any standard mail client (I used <acronym title="Android Open Source Project">AOSP</acronym> Email).
	* Desktop: [Mozilla Thunderbird](https://www.thunderbird.net/) (cross platform)
	* Server: [postfix](http://www.postfix.org/) for SMTP and [dovecot](https://www.dovecot.org/) for IMAP.
* Calendar and Contact Sync:
	* Run standard WebDAV services (CalDAV and CardDAV)!
	* Android: [DAVdroid](https://f-droid.org/en/packages/at.bitfire.davdroid/) from F-Droid.
	* Desktop (Thunderbird): `CardBook` for Contacts and `Lightning` for Calendar, then just add remote CalDAV sources to each.
	* Server: [Radicale](https://radicale.org/)
* Password Manager:
	* KeePass for a complete self-hosted solution.
	* Desktop: [KeePass XC](https://keepassxc.org/) for Windows, Mac and Linux.
	* Android: [KeePass DX](https://f-droid.org/en/packages/com.kunzisoft.keepass.libre/)
	* I sync my password vault with Syncthing.
* Files and Password Vault Sync:
	* [Syncthing](https://syncthing.net/) - runs everywhere, works very well, no web access! My preferred pick.
		* Android (F-Droid): [Syncthing](https://f-droid.org/en/packages/com.nutomic.syncthingandroid/)
	* [Nextcloud](https://nextcloud.com/) - PHP, if you want web access like Dropbox, but that's not for me.
		* Android (F-Droid): [Nextcloud](https://f-droid.org/en/packages/com.nextcloud.client/)
* Open Source Android Apps (Without Google):
	* App Stores
		* [F-Droid](https://f-droid.org/) - my preferred pick, only fully open source software.
		* [Amazon App Store](https://www.amazon.com/gp/mas/blp/install/) - for a market that competes with the Play Store but without Google apps.
	* [Fennec F-Droid](https://f-droid.org/en/packages/org.mozilla.fennec_fdroid/) is upstream `Firefox for Android` under a different brand. Supports Firefox Sync.
  * Chromium: [Auto Updater for Chromium](https://f-droid.org/en/packages/com.dosse.chromiumautoupdater)
	* Calendar and Contact Sync: [DAVdroid](https://f-droid.org/en/packages/at.bitfire.davdroid/) from F-Droid.
	* KeePass: [KeePass DX](https://f-droid.org/en/packages/com.kunzisoft.keepass.libre/) from F-Droid.
	* File sync: [Syncthing](https://f-droid.org/en/packages/com.nutomic.syncthingandroid/) or [Nextcloud](https://f-droid.org/en/packages/com.nextcloud.client/) from F-Droid.
	* Maps &amp; Navigation: [OsmAnd+](https://f-droid.org/en/packages/net.osmand.plus/) seems to be the best contender but is a very clunky app. Will take my tablet on adventures just to see how it does.
	* Messaging:
		* [Signal](https://signal.org/android/apk/) is not available on F-Droid but you can download the `.apk` directly from their site, and it will self-update.
		* [Riot.im](https://f-droid.org/en/packages/im.vector.alpha/) on F-Droid is a client for any [Matrix](https://matrix.org/) server.

---

# Play Store Apps

Most of this page talks about using only open-source software (F-Droid) with no
Google Play Services or Play Store apps involved. Some things can be found on
Amazon's App Store but most of the popular apps (Netflix, Hulu, etc) are only on
Play Store.

A lot of Play Store apps rely on Google Play Services at runtime and might not
work on a device without Google services installed.

**To install apps from the Play Store,** I used [Aurora Store](https://f-droid.org/en/packages/com.dragons.aurora/)
from F-Droid. [Yalp Store](https://f-droid.org/en/packages/com.github.yeriomin.yalpstore/)
is another open source client for the Play Store.

Some notes on testing how well certain apps work once installed (with no Google
services on the phone):

* **Netflix**
  * Works well for local playback! I was able to log in and stream shows on my
    Google-free phone.
  * The Chromecast button identified my SHARP ROKU TV with built-in Netflix app,
    but it did not see any Google Chromecast devices on my network.
* **Hulu**
  * I was able to log in to the app, but after that it crashes often. My guess
    is it crashes trying to look for Chromecast devices. If I'm fast I can get
    it to play back content but haven't tested for extended periods.
* **Venmo:** was usable, crashes randomly though.

Other apps I use that worked fine on my Google-free device:

* Sync for Reddit
* Firefox
* Slack
* Twitter
* Snapchat? (didn't log in as I forgot my password but the app didn't crash)
* Fly Delta? (doesn't crash but I wasn't flying anywhere so haven't fully tested
              all the app functionality)

Apps that strongly required the Google Play Services and pop up an error message
right away and won't work:

* YouTube
* Postmates

# Server Software

## Email: IMAP &amp; SMTP

I used postfix for the SMTP server and Dovecot for the IMAP server.

Using a tutorial like: <https://www.tecmint.com/install-postfix-mail-server-with-webmail-in-debian/>

> I highly recommend this being the **FIRST** thing you set up and verify working.
> E-mail is so easy to fuck up.

## Webmail

I installed Roundcube from the official Debian apt repo (`apt install roundcube`)
and configured it in nginx.

Install MariaDB-server first and get it up and running; Debian's roundcube asks
questions about the database immediately. Use `dpkg-reconfigure roundcube` to
reconfigure it later.

I used nginx instead of Apache to host Roundcube. I needed to `apt install php7-fpm`
and use this config:

```nginx
# /etc/nginx/sites-enabled/mail.caskir.net
server {
	server_name mail.caskir.net;
	listen 443 ssl;
	listen [::]:443 ssl;

	index index.cgi index.php index.html index.htm;

	access_log /var/log/nginx/mail-access.log;
	error_log /var/log/nginx/mail-error.log;

	ssl on;
	ssl_certificate /etc/letsencrypt/live/caskir.net/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/caskir.net/privkey.pem;
	include ssl_params;

	root /var/lib/roundcube;

	# legacy CGI scripts
	# https://wiki.debian.org/nginx/FastCGI
	location ~ \.php$ {
		try_files $uri =404;
		fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
		fastcgi_index index.php;
		fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
		include fastcgi_params;
	}
}

server {
	server_name mail.caskir.net;
	listen 80;
	listen [::]:80;
	return 301 https://mail.caskir.net$request_uri;
}
```

## Calendars and Contacts

I installed [Radicale](https://radicale.org) into a Python3 virtual environment
as my normal user account.

```bash
% export WORKON_HOME=~/.virtualenvs
% mkvirtualenv -p /usr/bin/python3 radicale
Installing into ~/.virtualenvs/radicale/bin/python...
(radicale)% pip install radicale
(radicale)% which radicale
/home/kirsle/.virtualenvs/radicale/bin/radicale
```

I put my Radicale config at `~/radicale/config` with these contents:

```ini
# /home/kirsle/radicale/config
[server]
hosts = 127.0.0.1:5232

[auth]
type = http_x_remote_user

[storage]
filesystem_folder = ~/.var/lib/radicale/collections
```

The Radicale service is managed by supervisor which runs it as a low-privileged
account:

```ini
# /etc/supervisor/conf.d/radicale.conf
[program:radicale]
command = /home/kirsle/.virtualenvs/radicale/bin/radicale --config /home/kirsle/radicale/config
user = kirsle
directory = /home/kirsle/radicale
```

And I put an nginx proxy in front so I can terminate SSL there (using
[Let's Encrypt](https://letsencrypt.org/) for free automated SSL certs).

```nginx
# /etc/nginx/sites-enabled/caskir.net
server {
	server_name www.caskir.net;
	listen 443 ssl;
	listen [::]:443 ssl;

	index index.html index.htm;

	access_log /var/log/nginx/caskir-access.log;
	error_log /var/log/nginx/caskir-error.log;

	ssl on;
	ssl_certificate /etc/letsencrypt/live/caskir.net/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/caskir.net/privkey.pem;
	include ssl_params;

	root /home/kirsle/www;

	location /dav/ { # The trailing / is important!
		proxy_pass http://localhost:5232/; # The / is important!
		proxy_set_header     X-Script-Name /dav;
		proxy_set_header     X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header     X-Remote-User $remote_user;
		auth_basic           "Radicale - Password Required";
		auth_basic_user_file /etc/nginx/htpasswd;
	}
}

server {
	server_name caskir.net;
	listen 443 ssl;
	listen [::]:443 ssl;

	ssl on;
	ssl_certificate /etc/letsencrypt/live/caskir.net/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/caskir.net/privkey.pem;
	include ssl_params;

	return 301 https://www.caskir.net$request_uri;
}

server {
	server_name www.caskir.net caskir.net;
	listen 80;
	listen [::]:80;
	return 301 https://www.caskir.net$request_uri;
}
```

HTTP Basic Auth refresher:

```bash
# To get the htpasswd commands.
$ apt install apache2-utils

# Create the password database.
$ htpasswd -c /etc/nginx/htpasswd kirsle
Password:
Verify:

# Add another user.
$ htpasswd /etc/nginx/htpasswd alice
```

Radicale has a very minimal web interface so you'll need a WebDAV client to
actually import your data. I used CardBook in Thunderbird and just imported
my contacts file from [Google Takeout](https://takeout.google.com/settings/takeout).

Thunderbird has CardBook and Lightning add-ons that can sync with the WebDAV
service. GNOME Calendar works, too, but depends on a full GNOME desktop environment
(installing it by itself on Xfce leaves it in a broken state as it can't interact
with GNOME's Online Accounts system).

For Android, [DAVdroid](https://f-droid.org/en/packages/at.bitfire.davdroid/) is
available on F-Droid and will sync contacts and calendars to your device.

---

# File Sync

I chose Syncthing over Nextcloud because it fit my needs better. Nextcloud is a
PHP application that has a web interface, like Dropbox, to log in and access your
files. Nextcloud also syncs contacts and address books (so you don't need Radicale).

I don't require web access to my files, as I'll always have either my phone or
one of my computers with me, and I really only use Syncthing to sync my password
database. Having a complicated web app written in PHP would present quite a
surface area for random drive-by attacks.

I sync between my desktop PC, offsite web server, two laptops and two Android
devices.

Download Linux packages at [Syncthing.net](https://syncthing.net/); they
have Debian/Ubuntu APT repositories to keep it updated.

To access its web interface _securely_, tunnel it through SSH like:

```bash
% ssh -L 8384:localhost:8384 user@hostname
```

And then accessing <http://localhost:8384/> on your desktop should access the
web interface on the server.

For Android, [Syncthing](https://f-droid.org/en/packages/com.nutomic.syncthingandroid/)
is available on F-Droid.

# Messaging

I found out you're not allowed to sync [Signal](https://signal.org/android/apk/)
between two different mobile devices (like my phone and my Nexus 7 tablet), only
between my phone and desktop PCs. However, it does seem Signal can be downloaded
directly from their website and would _probably_ work on a normal phone. I couldn't
activate it with my tablet's "phone number" because it doesn't receive SMS.

[Riot.im](https://f-droid.org/en/packages/im.vector.alpha/) is available on F-Droid
and can get you on to the Matrix federated protocol.
