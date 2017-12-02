# Fedora NetworkManager OpenVPN

I set up an OpenVPN server on my Raspberry Pi using the instructions [here](http://readwrite.com/2014/04/10/raspberry-pi-vpn-tutorial-server-secure-web-browsing).

Setting it up in Fedora via the NetworkManager Applet wasn't extremely straightforward.

## Install OpenVPN Support

```bash
sudo dnf -y install NetworkManager-openvpn NetworkManager-openvpn-gnome \
    openvpn
```

## NetworkManager Logs

The log is the most useful place to look when the OpenVPN connection fails, as the only thing the applet tells you is that it failed but it doesn't elaborate.

Check the logs with `journalctl`:

```bash
sudo journalctl -u NetworkManager
# -or-
sudo journalctl -t nm-openvpn
```

## SELinux: Where to place your certificates

SELinux will prevent access for nm-applet to read your certificates unless you put them in the right location.

Put your OpenVPN cert/key files in `~/.cert/`

## Make the .ovpn file importable

The Raspberry Pi OpenVPN tutorial above ends with creating a `.ovpn` file for the client certificate. This file is importable and works just fine in OpenVPN Connect for Android (and presumably other apps), but the NetworkManager Applet doesn't import it correctly: you'd still have to browse and pick all your cert/key files/etc.

If you open the ovpn file in a text editor you see it has all the certificates and keys included in-line in the file, like:

```
<ca>
-----BEGIN CERTIFICATE-----
...base64 encoded junk...
-----END CERTIFICATE-----
</ca>
```

To make it compatible with the NetworkManager Applet, keep all these certs in separate files (example, `ca.crt`) and edit the config file to refer to them by name.

Full file example:

```bash
client
dev tun
proto udp
remote ${YOUR_VPN_SERVER} 1194
resolv-retry infinite
nobind
persist-key
persist-tun
mute-replay-warnings
ns-cert-type server
key-direction 1
cipher AES-128-CBC
comp-lzo
verb 1
mute 20
ca ca.crt
cert ${Your_User.crt}
key ${Your_User.key}
tls-auth ta.key
```