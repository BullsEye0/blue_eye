#!/usr/bin/env/python
# This Python file uses the following encoding: utf-8

# Author: Jolanda de Koff
# Bulls Eye: https://github.com/BullsEye0
# linkedin: https://www.linkedin.com/in/jolandadekoff
# Facebook: facebook.com/jolandadekoff
# Facebook Group: https://www.facebook.com/groups/ethicalhacking.hacker
# Facebook Page: https://www.facebook.com/ethical.hack.group

# Created June- August 2019 | Copyright (c)2019 Jolanda de Koff.

# A notice to all nerds and n00bs...
# If you will copy developers work it will not make you a hacker..!
# Resepect all developers, we doing this because it's fun... :)

#######################################################################

import dns.resolver
import re
import requests
import shodan
import socket
import time

banner = """
            \033[1;34m
         ▄▄▄▄    ██▓     █    ██ ▓█████    ▓█████▓██   ██▓▓█████
        ▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀    ▓█   ▀ ▒██  ██▒▓█   ▀
        ▒██▒ ▄██▒██░    ▓██  ▒██░▒███      ▒███    ▒██ ██░▒███
        ▒██░█▀  ▒██░    ▓▓█  ░██░▒▓█  ▄    ▒▓█  ▄  ░ ▐██▓░▒▓█  ▄
        ░▓█  ▀█▓░██████▒▒▒█████▓ ░▒████▒   ░▒████▒ ░ ██▒▓░░▒████▒
        ░▒▓███▀▒░ ▒░▓  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░   ░░ ▒░ ░  ██▒▒▒ ░░ ▒░ ░
        ▒░▒   ░ ░ ░ ▒  ░░░▒░ ░ ░  ░ ░  ░    ░ ░  ░▓██ ░▒░  ░ ░  ░
         ░    ░   ░ ░    ░░░ ░ ░    ░         ░   ▒ ▒ ░░     ░
         ░          ░  ░   ░        ░  ░      ░  ░░ ░        ░  ░
              ░                                   ░ ░
            \033[1;m

        \033[34mBlue Eye\033[0m Recon Toolkit
        Author: Jolanda de Koff
        Bulls Eye | https://github.com/BullsEye0

              Hi there, Shall we play a game..?
            """
print (banner)
time.sleep(0.4)

target = raw_input("[+] \033[34mWhat domain do you want to search: \033[0m").strip()
compname = raw_input("[+] \033[34mEnter the company name: \033[0m").strip()
company = target.partition('.')
comp = company[0]
time.sleep(1)

print "\n"
havekey = raw_input("[+] \033[34mDo you have a Shodan API key \033[0m(Y/N) ").strip()


def showdam(key):
    try:
        print "[+]\033[34m - --> \033[0mThis may take a few seconds \033[34mBlue Eye\033[0m gathers the data.....\n"
        time.sleep(1)
        dnsResolve = "https://api.shodan.io/dns/resolve?hostnames=" + target + "&key=" + key
        resolved = requests.get(dnsResolve)
        hostIP = resolved.json()[target]
        api = shodan.Shodan(key)
        host = api.host(hostIP)

        if len(host) != 0:
            print "[+] \033[34mSearch Results for: \033[0m%s " % target
            print "[+] \033[34mIP: \033[0m%s" % host.get("ip_str")
            print "[+] \033[34mOrganization: \033[0m%s" % host.get("org")
            print "[+] \033[34mCountry: \033[0m%s" % host.get("country_name")
            print "[+] \033[34mCity: \033[0m%s" % host.get("city")
            print "[+] \033[34mLatitude: \033[0m%s" % host.get("latitude")
            print "[+] \033[34mLongitude: \033[0m%s" % host.get("longitude")
            print "[+] \033[34mHostnames: \033[0m%s" % host.get("hostnames"[:])
            print "[+] \033[34mO.S: \033[0m%s" % host.get("os")
            print "[+] \033[34mUpdated: \033[0m%s" % host.get("updated")
            print "[+] \033[34mASN: \033[0m%s" % host.get("asn")
            print "[+] \033[34mMSB: \033[0m%s" % host.get("msb")
            print "[+] \033[34mType: \033[0m%s" % host.get("type")
            print "[+] \033[34mUptime: \033[0m%s" % host.get("uptime")

            print "»" * 60 + "\n"
            print "[+] \033[34mOpen ports: \033[0m\n"
            for open_port in host["data"]:
                print "[+] \033[34mPort: %s" % open_port["port"] + "\033[0m"
            time.sleep(1)

        for item in host["data"]:
            print "»" * 60 + "\n"
            print "[+] \033[34mPort: \033[0m%s" % item["port"]
            print "[+] \033[34mHeader:\n%s" % item["data"] + "\033[0m"
            print "»" * 60
            time.sleep(1)

    except KeyboardInterrupt:
            print "\n"
            print "\033[1;91m[!]\033[0 User Interruption Detected."
            time.sleep(0.5)


def aug():
    print "[+] \033[34mMail Servers:\033[0m " + target + "\n"
    for sun in dns.resolver.query(target, "MX"):
        print "\t\033[34m" + (sun.to_text()) + "\033[0m"
    print "\n" + "»" * 60
    print "[+] \033[34mDNS Text Records:\033[0m " + target + "\n"
    for sun in dns.resolver.query(target, "TXT"):
        print "\t\033[34m" + (sun.to_text()) + "\033[0m"
    print "\n" + "»" * 60
    print "[+] \033[34mNameserver Records:\033[0m " + target + "\n"
    for sun in dns.resolver.query(target, "NS"):
        print "\t\033[34m" + (sun.to_text()) + "\033[0m"
    print "\n" + "»" * 60
    okta = comp + ".okta.com"
    webmail = "webmail." + comp + ".com"
    email = "email." + comp + ".com"
    slack = "%s.slack.com" % comp

    try:
        if len(socket.gethostbyname(okta)) <= 15:
            print "\n\t\033[34mHost of interest:\033[0m " + okta
        if len(socket.gethostbyname(webmail)) <= 15:
            print "\t\033[34mHost of interest:\033[0m " + webmail
        if len(socket.gethostbyname(email)) <= 15:
            print "\t\033[34mHost of interest:\033[0m " + email
        if len(socket.gethostbyname(slack)) <= 15:
            print "\t\033[34mHost of interest:\033[0m " + slack + "\n"

    except Exception:
        pass


def june():
    print "»" * 60 + "\n"
    print "[+] \033[34mSearch Results for: \033[0m%s " % target
    url = "https://ctsearch.entrust.com/api/v1/certificates?fields=subjectDN&domain=%s&includeExpired=false&exactMatch=false&limit=5000" % target
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    headers = {"User-Agent": useragent}
    try:
        print "\033[34mSearching\033[0m..... \n"
        time.sleep(2)
        response = requests.get(url, headers=headers)
        rain = re.findall(r'subjectDN": "cn\\u003d[a-zA-Z0-9.\-]{1,}', response.text)
        babs = []
        for item in rain:
            xtra = re.sub("subjectDN\": \"cn\\\\u003d", '', item)
            babs.append(xtra)

        dmset = set(babs)
        counter = 0
        print ""

        for itemm in dmset:
            counter = counter + 1
            print "%s. %s" % (str(counter), str(itemm))

            try:
                ns = dns.resolver.query(str(itemm), 'A')
                if "dns.resolver" in str(ns):
                    for joo in ns.response.answer:
                        for aug in joo.items:
                            ip = str(aug)
                            print("\t[+]\033[34m %s resolves to: %s\033[0m" % (str(itemm), str(ip)))
            except Exception:
                pass

        print ""
        print "\033[34m[+] Total Domains: %s\033[0m" % str(counter)

        print "»"*60 + "\n"
        time.sleep(1)

    except KeyboardInterrupt:
            print "\n"
            print "\033[1;91m[!]\033[0 User Interruption Detected..!"
            time.sleep(1)

    except Exception:
        pass


mainhub = "https://github.com/%s" % comp
gitpeople = "https://github.com/orgs/%s/people" % comp
response = requests.get(mainhub)
response_text = response.text
resp = requests.get(gitpeople)
respon_text = resp.text
listusers = re.findall(r'self\" href=\"[a-zA-Z0-9\-/]{3,}', respon_text)
listuser = []


def list_users():
    try:
        for item in listusers:
            x = re.sub("self\" href=\"/", '', item)
            listuser.append(x)

        usersset = set(listuser)
        counter = 0

        if listusers != []:
            print "\033[34m[+] List of %s github user pages:\033[0m" % target
            print "»"*60 + "\n"
            for user in usersset:
                try:
                    counter = counter + 1
                    userpage = "https://github.com/%s" % user
                    print str(counter) + " \t[+] " + "\033[34m " + (userpage) + "\033[0m"
                except Exception as e:
                    print('Error: %s' % e)

        print ""
        print "\033[34m[+] Total Users Found: %s\033[0m" % str(counter)

        print "»"*60 + "\n"
        time.sleep(1)

    except KeyboardInterrupt:
            print "\n"
            print "\033[1;91m[!]\033[0 User Interruption Detected..!"
            time.sleep(1)

    except Exception:
        pass


def mails():
    listofusers2 = set(listuser)
    try:
        print "[+] \033[34mList of possible company email addresses harvested from %s github user pages or from duckduckgo searches:\033[0m" % target
        print "»"*60 + "\n"
        for user in listofusers2:
            userpage = "https://api.github.com/users/%s/events/public" % user
            respon = requests.get(userpage)
            respons_text = respon.text
            findemail = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', respons_text)
            if findemail != []:
                emailset = set(findemail)
                for each in emailset:
                    if target in each:
                        print "\t[+] \033[34m" + (each) + "\033[0m"

        searchurl = 'https://duckduckgo.com/html/?q=site%3Alinkedin.com+email+%40%22' + target + '%22'
        webresponse = requests.get(searchurl)
        webresp = webresponse.text
        findem = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', webresp)
        if findem != [1]:
            setmail = set(findem)
            for each in setmail:
                if target in each:
                    print "\t[+] \033[34m" + (each) + "\033[0m\n\n"
            print "\n\n\t\033[34m[!] I like to See Ya, Hacking\033[0m\n\n"

    except KeyboardInterrupt:
            print "\n"
            print "\033[1;91m[!] User Interruption Detected..!\033[0"
            time.sleep(1)
            print "\n\n\t\033[34m[!] I like to See Ya, Hacking\033[0m\n\n"

    except Exception:
        pass


if (havekey == "Y" or havekey == "y"):
    key = raw_input("[+] \033[34mEnter Your Shodan API key: \033[0m").strip()
    print "\n"
    showdam(key)
else:
    print "[!] \033[34mShodan search skipped\033[0m\n"
    print "»" * 60

# =====# Main #===== #
if __name__ == "__main__":
    aug()
    june()
    list_users()
    mails()
