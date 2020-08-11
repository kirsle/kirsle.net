# Degoogle

My personal checklist and research to de-google my stuff.

## Motivations

* The Cambridge Analytica revelations ([blog post](/withdrawing-from-social-media))
* The [Purism Librem 5](https://puri.sm/products/librem-5/) phone is on my watch
  list. If released, it will be a GNU/Linux phone (not Android) so might as well
  prepare to leave the Android ecosystem while I wait.

Main things that have been keeping me on the stock Google Pixel 3 Android OS:

* Google Fi as cell carrier, and potential loss of features running an open source
  Android like LineageOS (mainly, ability to switch towers between T-Mobile, Sprint,
  US Cellular at will; WiFi Assistant I can care less about).
* Unlimited photo storage with Google Photos for a couple years with the Pixel phone
  purchase. But if I self-host my own photo cloud this is really a moot point.

## Progress

<table class="table table-striped">
  <thead class="thead-dark">
    <tr>
      <th>Google Service</th>
      <th>% Migrated</th>
      <th>Replacement Service</th>
      <th>Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Photos</th>
      <td>100%</td>
      <td>Nextcloud (self)</td>
      <td>All Google Photos migrated, Camera Backup enabled</td>
    </tr>
    <tr>
      <td>Contacts</td>
      <td>100%</td>
      <td>Nextcloud (self)</td>
      <td>Automatic sync between Android and Thunderbird (desktop)</td>
    </tr>
    <tr>
      <td>Calendar</td>
      <td>100%</td>
      <td>Nextcloud (self)</td>
      <td>Automatic sync between Android and Thunderbird (Lightning Calendar add-on)</td>
    </tr>
    <tr>
      <td>Drive</td>
      <td>100%</td>
      <td>Nextcloud (self)</td>
    </tr>
    <tr>
      <td>Gmail</td>
      <td>80%</td>
      <td>Rackspace Mail</td>
      <td>Moved kirsle.net from GSuite to Rackspace; minimizing use of Gmail.com account WIP</td>
    </tr>
    <tr>
      <td>Search</td>
      <td>100%</td>
      <td><a href="https://duckduckgo.com" target="_blank">DuckDuckGo</a></td>
      <td>Switched to DDG a long time ago as default search provider in Firefox.</td>
    </tr>
    <tr>
      <td>Maps</td>
      <td>0%</td>
      <td>n/a</td>
      <td>No real competitor to Maps</td>
    </tr>
    <tr>
      <td>YouTube</td>
      <td>0%</td>
      <td>n/a</td>
      <td>No real competitor to YouTube</td>
    </tr>
  </tbody>
</table>

## Checklist

* [x] Experiment first with old Pixel on LineageOS without Google Play Services
  nor microG. Install microG only as a last resort to test the crucial apps that
  didn't work otherwise.
* [x] Leave Google Fi for a normal carrier (T-Mobile or Sprint)
* [ ] Install/configure a home server to provide crucial services:
  * [x] Nextcloud for Contacts, Calendar, Camera Backup and File/Photo Storage
  * [ ] Personal OpenVPN Server
* [ ] ~~Install LineageOS on primary Android phone~~ I can't do without Chromecast
  support for Netflix/Hulu, so second best option is to remove Google accounts from
  my phone but keep the Google Play Services for Chromecast support.
  * [x] Change 2FA methods to TOTP app instead of Google push notification.
  * [x] Google Voice: forward text messages to email.
  * [x] Add Gmail address to a standard email app (Librem Mail on F-Droid)
  * Chromecast from apps still works fine.
  * Google Home app can still manage Chromecasts on the local network w/o account.
  * **Google WiFi:** requires a Google account to manage the WiFi routers. For this
    I installed [Android-x86](https://android-x86.org/) in VirtualBox on my laptop,
    if I need to manage my WiFi I can boot that up and use the app.
* [ ] Migrate out of Google's ecosystem
  * [x] Download latest export from Google Takeout
  * [x] Upload contacts to Nextcloud server
  * [x] Purge all photos from Google Photos (move all photos to Nextcloud)
  * [x] Clear out my Google Drive of all files (move important ones to Nextcloud)
  * [x] Clear all data from Google Assistant and other places
  * [x] Opt-out of all data services and ad personalization from Google.
  * [x] Move kirsle.net email from Google to an external provider
  * [ ] Migrate accounts linked to my Gmail address to Kirsle.net address
  * [ ] Wind down usage of Gmail account (unsubscribe from any mailing lists,
        get down to Inbox Zero where only Google themselves will ever send me
        mail to my Gmail account)

## Google-free Android

See [Self Hosting](/wiki/Self-Hosting) for my experiments running LineageOS
_without_ Google Services and the options for self-hosting crucial web services.

### App Compatibility w/o Play Services

Without Google Play Services some apps won't function correctly. I need to make
sure the apps that are important _to me_ work or have workable solutions.

**See also:** my [App Compatibility Table](/wiki/Degoogle/Apps)

