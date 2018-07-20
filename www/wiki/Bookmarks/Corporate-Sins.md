# Corporate Sins

Bookmarks to articles about **egregious** crimes against humanity committed by
corporations over the years.

* [Chick-fil-A](#chick-fil-a)
* [Cisco](#cisco)
* [Symantec](#symantec)

---

# Chick-fil-A

[Chick-fil-A](https://www.chick-fil-a.com/) continually donates millions of
dollars to groups that oppose same-sex marriage and other homophobic agendas.

Most famously they supported [Proposition 8](https://en.wikipedia.org/wiki/California_Proposition_8_\(2008\))
to take away equal rights from LGBT people in California in 2008.

* [Chick-fil-A same-sex marriage controversy](https://en.wikipedia.org/wiki/Chick-fil-A_same-sex_marriage_controversy)
* [Snopes: FACT CHECK: Chick-fil-A and Same-Sex Marriage](https://www.snopes.com/fact-check/chick-fil-a-gay-marriage/)

# Cisco

[Cisco](https://www.cisco.com/) is supposedly a trusted technology company
that sells corporate network infrastructure (routers, switches and things).
Your company probably has Cisco gear in their server closet and ISP's all
over the world run Cisco hardware.

With their position and level of trust they should know better, but Cisco has
implemented some of the most blatant backdoors that I have ever seen in my
entire career in tech.

> **Cisco Architecture for Lawful Intercept**
>
> Attackers could exploit these backdoors and not leave any audit trail. That’s
> how the lawful intercept protocol was designed so that ISP employees can’t tell
> when a law enforcement agent logs to the ISP’s routers (even though law
> enforcement is supposed to gain this access with a court order or other legal
> access request).
>
> Furthermore, this protocol could be abused by ISP employees because no one
> else working for the ISP could then tell when someone gained access to the
> routers via Cisco’s Architecture for Lawful Intercept.
>
> — [Tom's Hardware](https://www.tomshardware.com/news/cisco-backdoor-hardcoded-accounts-software,37480.html)

* [Backdoors Keep Appearing in Cisco's Routers](https://www.tomshardware.com/news/cisco-backdoor-hardcoded-accounts-software,37480.html) (July 2018) —
  five backdoors discovered in five months in 2018.
* [Cisco Removes Backdoor Account, Fourth in the Last Four Months](https://www.bleepingcomputer.com/news/security/cisco-removes-backdoor-account-fourth-in-the-last-four-months/) (June 2018)
* [Cisco fixes hard-coded password 'backdoor' flaw in Wi-Fi access points](https://www.zdnet.com/article/cisco-fixes-wi-fi-access-points-with-hard-coded-backdoor-access/) (2016)
* [Malicious Cisco router backdoor found on 79 more devices, 25 in the US](https://arstechnica.com/information-technology/2015/09/malicious-cisco-router-backdoor-found-on-79-more-devices-25-in-the-us/) (2015) — Security researchers discovered a hidden "knock sequence" that allowed remote access to the Cisco routers. When confronted, Cisco "fixed" the problem by shuffling the knock sequence around. The security researches discovered the new sequence again because *of course they did.*

# Symantec

[Symantec](https://www.symantec.com/) is a security company most known for
creating Norton Antivirus. Their response to a security incident is *apparently*
to **shut the fuck up** and pray that nobody ever finds out about it.

* [Top Voting Machine Vendor Admits It Installed Remote-Access Software on Systems Sold to States](https://motherboard.vice.com/en_us/article/mb4ezy/top-voting-machine-vendor-admits-it-installed-remote-access-software-on-systems-sold-to-states) — In 2006 hackers stole the source code to **pcAnywhere** and the public did not learn of this until 2012, when hackers posted the source code online. Only then did Symantec admit that *they knew about it the entire time.* Not only did this play a role in hacked voting machines but it compromised the security **of all customers of the pcAnywhere software.**
* [Google takes Symantec to the woodshed for mis-issuing 30,000 HTTPS certs](https://arstechnica.com/information-technology/2017/03/google-takes-symantec-to-the-woodshed-for-mis-issuing-30000-https-certs/) — Symantec has **repeatedly** had problems with this; the result is that Symantec has lost all trust by browser vendors and has been revoked from the trusted Certificate Authority Store on Chrome and Firefox. SSL providers are supposed to be among the **most trusted** companies because the security of the Internet rests in their hands. If hackers can trick Symantec into giving them an SSL cert for `google.com` then countries like Iran can [intercept private communications putting lives in real danger](https://en.wikipedia.org/wiki/DigiNotar).
