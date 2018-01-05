# IPv6 on Linux

Notes on setting up IPv6 support on Linux -- particularly for setting a static IP address (DHCP is usually pretty easy as long as your router is handing out v6 addresses!)

If you're a newbie to IPv6 I suggest you read up on it first. Some quick highlights:

* An IPv6 address is a 128-bit address split into 8 octets of 4 hexadecimal characters each. They look like e.g. `2606:1234:5678:dc00:c646:19ff:fe20:c4e1` but they can be truncated shorter if a sequence of octets evaluates to 0.
    * Example: `2606:1234:5678:dc00::ABCD` is equivalent to `2606:1234:5678:dc00:0000:0000:0000:ABCD`
* Your ISP assigns you a 64-bit prefix. This means the first 4 octets of your address space are out of your control. The latter 4 octets you can assign as you wish.
* To keep your addresses as short as possible you may want to only assign the final octet to your devices, example `2606:1234:5678:dc00::ABCD`

## Finding out your information on DHCP

It's easiest to get a DHCP lease for a v6 address first, gather information from it, and then set a static one.

First, to find your IPv6 address you can use either `ifconfig` or `ip -6 address show`, example:

```bash
$ ip -6 address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
3: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qlen 1000
    inet6 2606:1234:5678:dc00:c646:19ff:fe20:c4e1/64 scope global mngtmpaddr dynamic 
       valid_lft 3600sec preferred_lft 3600sec
    inet6 fe80::c646:19ff:fe20:c4e1/64 scope link 
       valid_lft forever preferred_lft forever
```

In this example `2606:1234:5678:dc00:c646:19ff:fe20:c4e1` is our DHCP IPv6 address. If you only have an address beginning with `fe80` or another link-local prefix, then **you do not have a public IPv6 address** and shouldn't bother with the rest of this page.

Then, you need to find your router's IPv6 address (the gateway address):

```bash
$ ip -6 route show default  
default via fe80::16cf:e2ff:fea6:2047 dev wlp3s0  proto ra  metric 1024  expires 1798sec hoplimit 64 pref medium
```

Here the router's address is the link-local `fe80::16cf:e2ff:fea6:2047` address. This one confused me for a second, because my router got *its own* public IPv6 address from the ISP, but that address is not the gateway address; the link-local one is!

## Setting a Static IPv6 Address

If you're using a graphical Linux desktop you can configure the static IP address in the Network Manager applet.

![Screenshot](/creativity/articles/ipv6-nm-applet.png)

Just pick the "Manual" method, Add an IP address, enter in the static IPv6 address you want, the prefix is usually going to be 64 (you control 64 bits of the 128-bit address), and paste the router's link-local address in the Gateway.

The DNS servers I use are Google's Public DNS, which have the IPv6 addresses of `2001:4860:4860::8888, 2001:4860:4860::8844`