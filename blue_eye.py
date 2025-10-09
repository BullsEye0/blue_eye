#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

# Author: Jolanda de Koff Bulls Eye
# GitHub: https://github.com/BullsEye0
# Website: https://hackingpassion.com
# linkedin: https://www.linkedin.com/in/jolandadekoff
# Facebook: https://www.facebook.com/profile.php?id=100069546190609
# Facebook Page: https://www.facebook.com/ethical.hack.group
# Facebook Group: https://www.facebook.com/groups/ethical.hack.group/
# YouTube: https://www.youtube.com/@HackingPassion

# Blue Eye Created June- August 2019
# Blue Eye v2 January 2020
# Blue Eye v2.1 Extended - October 2025
# Copyright (c) 2019 - 2025 Jolanda de Koff.

########################################################################

# A notice to all nerds and n00bs...
# If you will copy the developer's work it will not make you a hacker..!
# Respect all developers, we doing this because it's fun...

########################################################################

import dns.resolver
import json
import nmap
import os
import re
import requests
import socket
import time
import urllib.request
from datetime import datetime
from time import gmtime, strftime


# Global storage for report data
report_data = {
    'target': '',
    'scan_time': '',
    'ip_info': {},
    'dns_records': {},
    'subdomains': [],
    'technologies': [],
    'certificates': [],
    'github_users': [],
    'emails': []
}


banner = ("""
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
              ░                                   ░ ░   v2.1 Extended
            \033[1;m

        \033[34mBlue Eye\033[0m Recon Toolkit

        Author:  Jolanda de Koff Bulls Eye
        Github:  https://github.com/BullsEye0
        Website: https://HackingPassion.com

            \033[1;31mHi there, Shall we play a game..?\033[0m 😃
            """)

print (banner)
time.sleep(0.4)


target = input("[+] \033[34mWhat domain do you want to search: \033[0m").strip()
compname = input("[+] \033[34mEnter the company name: \033[0m").strip()
company = target.partition(".")
comp = company[0]
time.sleep(1)

# Initialize report data
report_data['target'] = target
report_data['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def jan():
    try:
        url = ("http://ip-api.com/json/")
        response = urllib.request.urlopen(url + target)
        data = response.read()
        jso = json.loads(data)
        time.sleep(1.5)

        print("\n [+] \033[34mUrl: " + target + "\033[0m")
        print(" [+] " + "\033[34m" + "IP: " + jso["query"] + "\033[0m")
        print(" [+] " + "\033[34m" + "Status: " + jso["status"] + "\033[0m")
        print(" [+] " + "\033[34m" + "Region: " + jso["regionName"] + "\033[0m")
        print(" [+] " + "\033[34m" + "Country: " + jso["country"] + "\033[0m")
        print(" [+] " + "\033[34m" + "City: " + jso["city"] + "\033[0m")
        print(" [+] " + "\033[34m" + "ISP: " + jso["isp"] + "\033[0m")
        print(" [+] " + "\033[34m" + "Lat & Lon: " + str(jso['lat']) + " & " + str(jso['lon']) + "\033[0m")
        print(" [+] " + "\033[34m" + "Zipcode: " + jso["zip"] + "\033[0m")
        print(" [+] " + "\033[34m" + "TimeZone: " + jso["timezone"] + "\033[0m")
        print(" [+] " + "\033[34m" + "AS: " + jso["as"] + "\033[0m" + "\n")
        print ("»"*60 + "\n")
        time.sleep(1)
        
        # Store for report
        report_data['ip_info'] = jso

    except Exception:
        pass

    except KeyboardInterrupt:
            print("\n")
            print("[-] User Interruption Detected..!")
            time.sleep(1)


def header():
    try:
        print("\033[34mScanning.... HTTP Header \033[0m" + target)
        time.sleep(1.5)
        command = ("http -v " + target)
        proces = os.popen(command)
        results = str(proces.read())
        print("\033[1;34m" + results + command + "\033[1;m")
        print ("»"*60 + "\n")

    except Exception:
        pass

    except KeyboardInterrupt:
            print("\n")
            print("[-] User Interruption Detected..!")
            time.sleep(1)


def nmaps():
    try:
        print("\033[34mScanning.... Nmap Port Scan: \033[0m" + target)
        print ("[+]\033[34m - --> \033[0mThis may take a moment \033[34mBlue Eye\033[0m gathers the data.....\n")
        time.sleep(1)

        scanner = nmap.PortScanner()
        command = ("nmap -Pn " + target)
        process = os.popen(command)
        results = str(process.read())
        logPath = "logs/nmap-" + strftime("%Y-%m-%d_%H:%M:%S", gmtime())

        print("\033[34m" + results + command + logPath + "\033[0m")
        print("\033[34mNmap Version: \033[0m", scanner.nmap_version())
        print ("»"*60 + "\n")

    except Exception:
        pass

    except KeyboardInterrupt:
            print("\n")
            print("[-] User Interruption Detected..!")
            time.sleep(1)


def aug():
    print ("[+] \033[34mMail Servers:\033[0m " + target + "\n")
    time.sleep(0.5)
    mx_records = []
    for sun in dns.resolver.query(target, "MX"):
        mx_records.append(sun.to_text())
        print ("\t\033[34m" + (sun.to_text()) + "\033[0m")
    
    print ("\n" + "»" * 60)
    print ("[+] \033[34mDNS Text Records:\033[0m " + target + "\n")
    time.sleep(0.2)
    txt_records = []
    for sun in dns.resolver.query(target, "TXT"):
        txt_records.append(sun.to_text())
        print ("\t\033[34m" + (sun.to_text()) + "\033[0m")
    
    print ("\n" + "»" * 60)
    print ("[+] \033[34mNameserver Records:\033[0m " + target + "\n")
    time.sleep(0.2)
    ns_records = []
    for sun in dns.resolver.query(target, "NS"):
        ns_records.append(sun.to_text())
        print ("\t\033[34m" + (sun.to_text()) + "\033[0m")
    
    print ("\n" + "»" * 60)
    
    # Store for report
    report_data['dns_records'] = {
        'mx': mx_records,
        'txt': txt_records,
        'ns': ns_records
    }
    
    okta = comp + ".okta.com"
    webmail = "webmail." + comp + ".com"
    email = "email." + comp + ".com"
    slack = "%s.slack.com" % comp

    try:
        if len(socket.gethostbyname(okta)) <= 15:
            print ("\n\t\033[34mHost of interest:\033[0m " + okta)
            time.sleep(0.3)
        if len(socket.gethostbyname(webmail)) <= 15:
            print ("\t\033[34mHost of interest:\033[0m " + webmail)
            time.sleep(0.3)
        if len(socket.gethostbyname(email)) <= 15:
            print ("\t\033[34mHost of interest:\033[0m " + email)
            time.sleep(0.3)
        if len(socket.gethostbyname(slack)) <= 15:
            print ("\t\033[34mHost of interest:\033[0m " + slack + "\n")
            time.sleep(0.3)

    except Exception:
        pass


def june():
    print ("»" * 60 + "\n")
    print ("[+] \033[34mSearch Results for: \033[0m%s " % target)
    # Updated to use crt.sh instead of broken Entrust API
    url = ("https://crt.sh/?q=%%.%s&output=json" % target)
    useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36")
    headers = {"User-Agent": useragent}
    try:
        print ("[+]\033[34m - --> \033[0mThis may take a moment \033[34mBlue Eye\033[0m gathers the data.....\n")
        time.sleep(1)
        response = requests.get(url, headers=headers, timeout=30)
        
        # Parse JSON response from crt.sh
        if response.status_code == 200:
            try:
                json_data = response.json()
                babs = []
                
                for item in json_data:
                    if 'name_value' in item:
                        # Split on newlines as crt.sh can return multiple domains per entry
                        domains = item['name_value'].split('\n')
                        for domain in domains:
                            # Clean up the domain
                            domain = domain.strip()
                            # Remove wildcard asterisks for DNS resolution
                            if domain.startswith('*.'):
                                domain = domain[2:]
                            if domain and domain not in babs:
                                babs.append(domain)
                
                dmset = sorted(set(babs))
                counter = 0
                print ("")

                for itemm in dmset:
                    counter = counter + 1
                    print ("%s. %s" % (str(counter), str(itemm)))

                    try:
                        ns = dns.resolver.query(str(itemm), "A")
                        if "dns.resolver" in str(ns):
                            for joo in ns.response.answer:
                                for aug in joo.items:
                                    ip = str(aug)
                                    print("\t[+]\033[34m %s resolves to: %s\033[0m" % (str(itemm), str(ip)))
                                    report_data['certificates'].append({'domain': str(itemm), 'ip': str(ip)})

                    except Exception:
                        pass

                print ("")
                print ("\033[34m[+] Total Domains: %s\033[0m" % str(counter))
            
            except json.JSONDecodeError:
                print("\033[1;91m[!] Error parsing response from crt.sh\033[0m")
        else:
            print("\033[1;91m[!] Error: crt.sh returned status code %s\033[0m" % response.status_code)

        print ("»"*60 + "\n")
        time.sleep(1)

    except requests.exceptions.Timeout:
        print("\033[1;91m[!] Request timed out. Please try again.\033[0m")
        print ("»"*60 + "\n")

    except KeyboardInterrupt:
            print ("\n\033[1;91m[!]\033[0m User Interruption Detected..!")
            time.sleep(1)

    except Exception as e:
        print("\033[1;91m[!] Error: %s\033[0m" % str(e))
        print ("»"*60 + "\n")


def sept():
    """Subdomain Brute-forcing Scanner"""
    print ("»" * 60 + "\n")
    print ("[+] \033[34mScanning subdomains for:\033[0m %s" % target)
    print ("[+]\033[34m - --> \033[0mThis may take a moment \033[34mBlue Eye\033[0m gathers the data.....\n")
    time.sleep(1)
    
    # Common subdomains to check
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'admin', 'api', 'dev',
        'staging', 'test', 'demo', 'm', 'mobile', 'blog', 'shop', 'forum', 'support',
        'portal', 'vpn', 'cdn', 'assets', 'static', 'media', 'images', 'img', 'video',
        'backup', 'secure', 'remote', 'cloud', 'git', 'svn', 'beta', 'alpha', 'v1',
        'v2', 'api1', 'api2', 'app', 'apps', 'dashboard', 'panel', 'status', 'monitor'
    ]
    
    found = 0
    found_subdomains = []
    
    for sub in subdomains:
        subdomain = sub + "." + target
        try:
            ip = socket.gethostbyname(subdomain)
            found += 1
            found_subdomains.append({'subdomain': subdomain, 'ip': ip})
            print ("\t[+] \033[34m" + subdomain + " → " + ip + "\033[0m")
            time.sleep(0.1)
        except:
            pass
    
    print ("\n\033[34m[+] Total Subdomains Found: %s\033[0m" % str(found))
    print ("»"*60 + "\n")
    time.sleep(1)
    
    # Store for report
    report_data['subdomains'] = found_subdomains


def okt():
    """Technology Stack Detection"""
    print ("»" * 60 + "\n")
    print ("[+] \033[34mDetecting technologies for:\033[0m %s" % target)
    print ("[+]\033[34m - --> \033[0mThis may take a moment \033[34mBlue Eye\033[0m gathers the data.....\n")
    time.sleep(1)
    
    try:
        url = "https://" + target if not target.startswith('http') else target
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        content = response.text.lower()
        
        technologies = []
        
        # Check Server header
        if 'server' in headers:
            server = headers['server']
            technologies.append({'type': 'Web Server', 'name': server})
            print ("\t[+] \033[34mWeb Server: " + server + "\033[0m")
            time.sleep(0.2)
        
        # Check X-Powered-By header
        if 'x-powered-by' in headers:
            powered = headers['x-powered-by']
            technologies.append({'type': 'Powered By', 'name': powered})
            print ("\t[+] \033[34mPowered By: " + powered + "\033[0m")
            time.sleep(0.2)
        
        # Check for common frameworks/CMS in HTML
        detections = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla', '/components/com_'],
            'Drupal': ['drupal', 'sites/all/'],
            'React': ['react', 'react-dom'],
            'Vue.js': ['vue.js', 'vue.min.js'],
            'Angular': ['angular', 'ng-app'],
            'jQuery': ['jquery'],
            'Bootstrap': ['bootstrap'],
            'Laravel': ['laravel'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Flask': ['flask'],
            'Express': ['express'],
            'Cloudflare': ['cloudflare']
        }
        
        for tech, signatures in detections.items():
            for sig in signatures:
                if sig in content:
                    technologies.append({'type': 'Framework/CMS', 'name': tech})
                    print ("\t[+] \033[34m" + tech + " detected\033[0m")
                    time.sleep(0.2)
                    break
        
        # Check for CDN
        if 'cf-ray' in headers:
            technologies.append({'type': 'CDN', 'name': 'Cloudflare'})
            print ("\t[+] \033[34mCDN: Cloudflare\033[0m")
            time.sleep(0.2)
        
        if not technologies:
            print ("\t\033[34m[!] No specific technologies detected from headers/content\033[0m")
        
        print ("\n\033[34m[+] Total Technologies Detected: %s\033[0m" % str(len(technologies)))
        print ("»"*60 + "\n")
        time.sleep(1)
        
        # Store for report
        report_data['technologies'] = technologies
        
    except Exception as e:
        print("\t\033[1;91m[!] Error detecting technologies: %s\033[0m" % str(e))
        print ("»"*60 + "\n")


mainhub = ("https://github.com/%s" % comp)
gitpeople = ("https://github.com/orgs/%s/people" % comp)
response = requests.get(mainhub)
response_text = response.text
resp = requests.get(gitpeople)
respon_text = resp.text
listusers = re.findall(r'self\" href=\"[a-zA-Z0-9\-/]{3,}', respon_text)
listuser = []


def list_users():
    try:
        for item in listusers:
            x = re.sub("self\" href=\"/", "", item)
            listuser.append(x)

        usersset = set(listuser)
        counter = 0

        if listusers != []:
            print ("\033[34m[+] List of %s github user pages:\033[0m" % target)
            print ("»"*60 + "\n")
            for user in usersset:
                try:
                    counter = counter + 1
                    userpage = ("https://github.com/%s" % user)
                    print (str(counter) + " \t[+] " + "\033[34m " + userpage + "\033[0m")
                    report_data['github_users'].append(userpage)
                except Exception as e:
                    print("Error: %s" % e)

        print ("")
        print ("\033[34m[+] Total Users Found: %s\033[0m" % str(counter))

        print ("»"*60 + "\n")
        time.sleep(1)

    except KeyboardInterrupt:
            print ("\n")
            print ("\033[1;91m[!]\033[0m User Interruption Detected..!")
            time.sleep(1)

    except Exception:
        pass


def mails():
    listofusers2 = set(listuser)
    try:
        print ("[+] \033[34mList of possible company email addresses harvested")
        print ("from %s github user pages & duckduckgo searches:\033[0m" % target)
        time.sleep(0.5)
        print ("»"*60 + "\n")
        for user in listofusers2:
            userpage = ("https://api.github.com/users/%s/events/public" % user)
            respon = requests.get(userpage)
            respons_text = respon.text
            findemail = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', respons_text)
            if findemail != []:
                emailset = set(findemail)
                for each in emailset:
                    if target in each:
                        print ("\t[+] \033[34m" + (each) + "\033[0m")
                        report_data['emails'].append(each)
                        time.sleep(0.1)

        searchurl = ("https://duckduckgo.com/html/?q=site%3Alinkedin.com+email+%40%22" + target + '%22')
        webresponse = requests.get(searchurl)
        webresp = webresponse.text
        findem = re.findall(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+', webresp)
        if findem != [1]:
            setmail = set(findem)
            for each in setmail:
                if target in each:
                    print ("\t[+] \033[34m" + (each) + "\033[0m\n\n")
                    if each not in report_data['emails']:
                        report_data['emails'].append(each)
                    time.sleep(1)

    except KeyboardInterrupt:
            print ("\n\033[1;91m[!] User Interruption Detected..!\033[0m")
            time.sleep(1)

    except Exception:
        pass


def nov():
    """Generate HTML Report"""
    print ("»" * 60 + "\n")
    print ("[+] \033[34mGenerating HTML report...\033[0m")
    time.sleep(1)
    
    try:
        filename = "blue_eye_report_" + target.replace(".", "_") + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blue Eye Recon Report - {report_data['target']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        .header {{
            text-align: center;
            padding: 20px 0;
            border-bottom: 3px solid #667eea;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .subtitle {{
            color: #a8b3ff;
            font-size: 1.2em;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .info-item {{
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 5px;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }}
        .info-label {{
            color: #a8b3ff;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #fff;
        }}
        ul {{
            list-style: none;
            padding-left: 0;
        }}
        li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        li:before {{
            content: "▸ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid rgba(102, 126, 234, 0.3);
            color: #a8b3ff;
        }}
        .emoji {{
            font-size: 1.2em;
        }}
        .highlight {{
            color: #667eea;
            font-weight: bold;
        }}
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Blue Eye Recon Report</h1>
            <div class="subtitle">Professional OSINT Reconnaissance Report</div>
            <div style="margin-top: 20px;">
                <span class="badge">Target: {report_data['target']}</span>
                <span class="badge">Scan Date: {report_data['scan_time']}</span>
            </div>
        </div>

        <!-- IP Information -->
        <div class="section">
            <h2>🌐 IP & Geolocation Information</h2>
            <div class="info-grid">
"""
        
        if report_data['ip_info']:
            ip_info = report_data['ip_info']
            html_content += f"""
                <div class="info-item">
                    <span class="info-label">IP Address</span>
                    <span class="info-value">{ip_info.get('query', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Country</span>
                    <span class="info-value">{ip_info.get('country', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Region</span>
                    <span class="info-value">{ip_info.get('regionName', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">City</span>
                    <span class="info-value">{ip_info.get('city', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">ISP</span>
                    <span class="info-value">{ip_info.get('isp', 'N/A')}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Timezone</span>
                    <span class="info-value">{ip_info.get('timezone', 'N/A')}</span>
                </div>
"""
        
        html_content += """
            </div>
        </div>

        <!-- Subdomains -->
        <div class="section">
            <h2>🔎 Discovered Subdomains</h2>
"""
        
        if report_data['subdomains']:
            html_content += f"<p>Total found: <span class='highlight'>{len(report_data['subdomains'])}</span></p><ul>"
            for sub in report_data['subdomains']:
                html_content += f"<li>{sub['subdomain']} → {sub['ip']}</li>"
            html_content += "</ul>"
        else:
            html_content += "<p>No subdomains discovered.</p>"
        
        html_content += """
        </div>

        <!-- Technologies -->
        <div class="section">
            <h2>🛠️ Detected Technologies</h2>
"""
        
        if report_data['technologies']:
            html_content += f"<p>Total detected: <span class='highlight'>{len(report_data['technologies'])}</span></p><ul>"
            for tech in report_data['technologies']:
                html_content += f"<li><strong>{tech['type']}:</strong> {tech['name']}</li>"
            html_content += "</ul>"
        else:
            html_content += "<p>No specific technologies detected.</p>"
        
        html_content += """
        </div>

        <!-- DNS Records -->
        <div class="section">
            <h2>📋 DNS Records</h2>
"""
        
        if report_data['dns_records']:
            if report_data['dns_records'].get('mx'):
                html_content += "<h3 style='color: #a8b3ff; margin-top: 15px;'>Mail Servers (MX)</h3><ul>"
                for mx in report_data['dns_records']['mx']:
                    html_content += f"<li>{mx}</li>"
                html_content += "</ul>"
            
            if report_data['dns_records'].get('ns'):
                html_content += "<h3 style='color: #a8b3ff; margin-top: 15px;'>Name Servers (NS)</h3><ul>"
                for ns in report_data['dns_records']['ns']:
                    html_content += f"<li>{ns}</li>"
                html_content += "</ul>"
        
        html_content += """
        </div>

        <!-- GitHub Users -->
"""
        
        if report_data['github_users']:
            html_content += f"""
        <div class="section">
            <h2>👥 GitHub Users</h2>
            <p>Total found: <span class='highlight'>{len(report_data['github_users'])}</span></p>
            <ul>
"""
            for user in report_data['github_users']:
                html_content += f"<li><a href='{user}' style='color: #667eea;'>{user}</a></li>"
            html_content += """
            </ul>
        </div>
"""
        
        # Emails
        if report_data['emails']:
            html_content += f"""
        <div class="section">
            <h2>📧 Discovered Email Addresses</h2>
            <p>Total found: <span class='highlight'>{len(report_data['emails'])}</span></p>
            <ul>
"""
            for email in report_data['emails']:
                html_content += f"<li>{email}</li>"
            html_content += """
            </ul>
        </div>
"""
        
        html_content += f"""
        <div class="footer">
            <p><strong>Blue Eye</strong> Recon Toolkit v2.1 Extended</p>
            <p>Created by <span class="highlight">Jolanda de Koff</span> | Bulls Eye</p>
            <p style="margin-top: 10px;">
                <a href="https://hackingpassion.com" style="color: #667eea;">HackingPassion.com</a> | 
                <a href="https://github.com/BullsEye0" style="color: #667eea;">GitHub</a>
            </p>
            <p style="margin-top: 15px; font-size: 0.9em;">
                <span class="emoji">🎯</span> Want to master OSINT & Reconnaissance? <br>
                <a href="https://www.udemy.com/course/ethical-hacking-complete-course-zero-to-expert/?couponCode=BULLSEYE" 
                   style="color: #667eea; font-weight: bold;">
                   Get the full Ethical Hacking Course – Zero to Expert
                </a>
            </p>
            <p style="margin-top: 20px; color: #a8b3ff;">
                <span class="emoji">😃</span> I like to See Ya, Hacking!
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print ("\t[+] \033[34mReport saved to: " + filename + "\033[0m")
        print ("\t[+] \033[34mOpen it in your browser to view! 🌐\033[0m")
        print ("»"*60 + "\n")
        time.sleep(1)
        
    except Exception as e:
        print("\t\033[1;91m[!] Error generating report: %s\033[0m" % str(e))
        print ("»"*60 + "\n")


print ("\n\t\033[34m I like to See Ya, Hacking\033[0m 😃\n")


# =====# Main #===== #
if __name__ == "__main__":
    jan()
    header()
    nmaps()
    aug()
    june()
    sept()      # NEW: Subdomain scanner
    okt()       # NEW: Technology detection
    list_users()
    mails()
    nov()       # NEW: HTML report generator
    
    print ("\n\n\t\033[34m[!] Scan complete! Check your HTML report! 📄\033[0m 😃\n\n")
