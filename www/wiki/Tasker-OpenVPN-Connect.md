# Tasker OpenVPN Connect

Source: <https://forums.openvpn.net/topic13122.html#p33893>

VPN profile name, as shown in OpenVPN Connect: **example.com/autologin**
In the steps below, replace this with your own profile name.
For fields with no listed value here, leave the Tasker field blank (shows as "Optional").
In the first Extra field in the "To Connect" procedure below, the colon and everything in bold is written as intended.

To Connect:

* Misc > **Send Intent**
    * Action: **android.intent.action.VIEW**
    * Cat: **None**
    * Mime Type:
    * Data:
    * Extra: **net.openvpn.openvpn.AUTOSTART_PROFILE_NAME: example.com/autologin**
    * Extra:
    * Package: **net.openvpn.openvpn**
    * Class: **net.openvpn.openvpn.OpenVPNClient**
    * Target: **Activity**

To Disconnect:

* Misc > Send Intent
    * Action: **android.intent.action.VIEW**
    * Cat: **None**
    * Mime Type:
    * Data:
    * Extra:
    * Extra:
    * Package: **net.openvpn.openvpn**
    * Class: **net.openvpn.openvpn.OpenVPNDisconnect**
    * Target: **Activity**