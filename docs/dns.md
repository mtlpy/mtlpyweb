# DNS

As of 2023-03-05, this info is obsolete. See the mp-docs repo for more up to date information on the Montréal-Python infrastructure.

## Setup

Domains:
- montrealpython.org (primary 2007-11-04)
- montrealpython.com (legacy 2007-11-04)
- mtlpy.org (new cool stuff 2010-09-17)

Registrar: Gandi
Nameserver: Cloudflare

## Archive from Gandi

### montrealpython.org
```
@ 300 IN A 184.107.196.98
@ 10800 IN MX 10 aspmx.l.google.com.
@ 10800 IN MX 20 ALT1.ASPMX.L.GOOGLE.COM.
@ 10800 IN MX 20 ALT2.ASPMX.L.GOOGLE.COM.
@ 10800 IN MX 30 ASPMX2.GOOGLEMAIL.COM.
@ 10800 IN MX 30 ASPMX3.GOOGLEMAIL.COM.
@ 10800 IN SOA ns1.gandi.net. hostmaster.gandi.net. 1489338287 10800 3600 604800 10800
@ 10800 IN TXT "google-site-verification=E5uBpMqV35gPMxiMCBPSBGJgSNFtSMoCzok5EKeSfBA"
admwiki 3600 IN A 184.107.196.98
beta 3600 IN A 184.107.196.98
docs 3600 IN CNAME ghs.l.google.com.
i18n 3600 IN A 174.120.139.144
lists 10800 IN A 184.107.196.99
lists 28800 IN MX 1 ASPMX.L.GOOGLE.COM.
lists 28800 IN MX 3 ALT1.ASPMX.L.GOOGLE.COM.
lists 28800 IN MX 3 ALT2.ASPMX.L.GOOGLE.COM.
lists 28800 IN MX 5 ASPMX2.GOOGLEMAIL.COM.
lists 28800 IN MX 5 ASPMX3.GOOGLEMAIL.COM.
lists 10800 IN TXT "google-site-verification=NVuZjji-SA2MQkrRPykwVKslx6h6ICuzEGKZVeG51g8"
mail 3600 IN CNAME ghs.google.com.
new 3600 IN A 184.107.196.98
pycon 3600 IN A 184.107.196.98
redmine 300 IN A 184.107.196.98
stage 3600 IN A 184.107.196.98
test 10800 IN CNAME webredir.vip.gandi.net.
wiki 3600 IN A 184.107.196.98
www 300 IN A 184.107.196.98
youtube 10800 IN TXT "google-site-verification=3csPjQzJ_bnPGneQxZF0QNcxjiS4g7QnCD3s37FecPM"
```

### mtlpy.org
```
@ 300 IN A 184.107.196.98
@ 28800 IN MX 1 ASPMX.L.GOOGLE.COM.
@ 28800 IN MX 3 ALT1.ASPMX.L.GOOGLE.COM.
@ 28800 IN MX 3 ALT2.ASPMX.L.GOOGLE.COM.
@ 28800 IN MX 5 ASPMX2.GOOGLEMAIL.COM.
@ 28800 IN MX 5 ASPMX3.GOOGLEMAIL.COM.
@ 10800 IN SOA ns1.gandi.net. hostmaster.gandi.net. 1489338595 10800 3600 604800 10800
@ 10800 IN TXT "google-site-verification=SJunyDGgVZPVZihC8i5CL02Hqnuf6CzM2tBSB25OEAg"
beta 10800 IN A 184.107.196.98
cal 3600 IN CNAME ghs.l.google.com.
demo 1800 IN A 184.107.196.98
docs 3600 IN CNAME ghs.l.google.com.
mail 3600 IN CNAME ghs.google.com.
new 3600 IN A 184.107.196.98
pycon 1800 IN A 184.107.196.98
pycon 1800 IN A 184.107.196.98
s 3600 IN A 184.107.196.98
slack 3600 IN CNAME mtlpy-slackin.herokuapp.com.
stage 3600 IN A 184.107.196.98
status 3600 IN CNAME stats.uptimerobot.com.
wiki 3600 IN A 184.107.196.98
www 300 IN A 184.107.196.98
```
