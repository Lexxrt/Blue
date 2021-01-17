from bs4 import BeautifulSoup
from collections import deque
import json
import nmap
import os
import re
import requests
import requests.exceptions
import time
from time import gmtime, strftime
from urllib.error import URLError
from urllib.parse import urlsplit
import urllib3
import urllib.request
from urllib.request import urlopen


def banner():
    print('''
 _______   __                     
/       \ /  |                    
$$$$$$$  |$$ | __    __   ______  
$$ |__$$ |$$ |/  |  /  | /      \ 
$$    $$  $$ |$$ |  $$ |/$$$$$$  |
$$$$$$$  |$$ |$$ |  $$ |$$    $$ |
$$ |__$$ |$$ |$$ \__$$ |$$$$$$$$/ 
$$    $$/ $$ |$$    $$/ $$       |
$$$$$$$/  $$/  $$$$$$/   $$$$$$$/           


        Blue - Information Gathering Tool
        Author: Lexxrt | https://github.com/Lexxrt
 ''')


def menu():
    print("[+] 1.   Whois Lookup")
    print("[+] 2.   DNS Lookup")
    print("[+] 3.   Nmap Port Scan")
    print("[+] 4.   HTTP Header Grabber")
    print("[+] 5.   Clickjacking Test - X-Frame-Options Header")
    print("[+] 6.   Robots.txt Scanner")
    print("[+] 7.   Link Grabber")
    print("[+] 8.   IP GeoLocation Finder")
    print("[+] 9.   Traceroute")
    print("[+] 10.  Have I been pwned")
    print("[+] 11.  Exit\n")


def main():
    choice = ("1")
    banner()

    while choice != ("11"):
        menu()
        choice = input("[+] Enter your choice: ")

        if choice == ("1"):
            try:
                target = input("[+] Enter Domain or IP Address: ").lower()
                os.system("reset")
                print(f"[+] Searching for... Whois Lookup: ".format(target) + target)
                time.sleep(1.5)
                command = ("whois " + target)
                proces = os.popen(command)
                results = str(proces.read())
                print("" + results + command + "")

            except Exception:
                pass

        elif choice == ("2"):
            try:
                target = input("[+] Enter Domain or IP Address: ").lower()
                os.system("reset")
                print(f"[+] Searching for... DNS Lookup: ".format(target) + target)
                time.sleep(1.5)
                command = ("dig " + target + " +trace ANY")
                proces = os.popen(command)
                results = str(proces.read())
                print("" + results + command + "")

            except Exception:
                pass

        elif choice == ("3"):
            try:
                target = input("Enter Domain or IP Address: ").lower()
                os.system("reset")
                print("[+] Scanning.... Nmap Port Scan: " + target)
                print("[+] This will take a moment.\n")
                time.sleep(1.5)

                scanner = nmap.PortScanner()
                command = ("nmap -Pn " + target)
                process = os.popen(command)
                results = str(process.read())
                logPath = "logs/nmap-" + strftime("%Y-%m-%d_%H:%M:%S", gmtime())

                print("" + results + command + logPath + "")
                print("[+] Nmap Version: ", scanner.nmap_version())

            except KeyboardInterrupt:
                    print("\n")
                    print("[-] User Interruption Detected..!")
                    time.sleep(1)

        elif choice == ("4"):
            try:
                target = input("[+] Enter Domain or IP Address: ").lower()
                os.system("reset")
                print("[+] Scanning.... HTTP Header Grabber: \n" + target)
                time.sleep(1.5)
                command = ("http -v " + target)
                proces = os.popen(command)
                results = str(proces.read())
                print("" + results + command + "")

            except Exception:
                pass

        elif choice == ("5"):
            target = input("[+] Enter the Domain to test: ").lower()
            os.system("reset")

            if not (target.startswith("http://") or target.startswith("https://")):
                target = "http://" + target
            print("[+] Testing...  Clickjacking Test: " + target)
            time.sleep(2)
            try:
                resp = requests.get(target)
                headers = resp.headers
                print("\nHeader set are: \n")
                for item, xfr in headers.items():
                    print("" + item + ":" + xfr + "")

                if "X-Frame-Options" in headers.keys():
                    print("\n[+] Click Jacking Header is present")
                    print("[+] You can't clickjack this site !\n")
                else:
                    print("\n[*] X-Frame-Options-Header is missing ! ")
                    print("[!] Clickjacking is possible, this site is vulnerable to Clickjacking\n")

            except Exception as ex:
                print("[+] Exception caught: " + str(ex))

        elif choice == ("6"):
            try:
                target = input("Enter Domain: ").lower()
                os.system("reset")
                print("[+] Scanning.... Robots.txt Scanner: \n" + target)
                time.sleep(1.5)

                if not (target.startswith("http://") or target.startswith("https://")):
                    target = "http://" + target
                robot = target + "/robots.txt"

                try:
                    bots = urlopen(robot).read().decode("utf-8")
                    print("" + (bots) + "")
                except URLError:
                    print("[-] Can\'t access to {page}!".format(page=robot))

            except Exception as ex:
                print("[+] Exception caught: " + str(ex))

        elif choice == ("7"):
            try:
                target = input("Enter Domain: ").lower()
                os.system("reset")
                print("[+] Scanning.... Link Grabber: \n" + target)
                time.sleep(2)
                if not (target.startswith("http://") or target.startswith("https://")):
                    target = "http://" + target
                deq = deque([target])
                pro = set()

                try:
                    while len(deq):
                        url = deq.popleft()
                        pro.add(url)
                        parts = urlsplit(url)
                        base = "{0.scheme}://{0.netloc}".format(parts)

                        print("[+] Crawling URL " + "" + url + "")
                        try:
                            response = requests.get(url)
                        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                            continue

                        soup = BeautifulSoup(response.text, "lxml")
                        for anchor in soup.find_all("a"):
                            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                            if link.startswith("/"):
                                link = base + link
                            if not link in deq and not link in pro:
                                deq.append(link)
                            continue

                except KeyboardInterrupt:
                        print("\n")
                        print("[-] User Interruption Detected..!")
                        time.sleep(1)
                        print("\n[+] Exiting...\n")

            except Exception:
                pass

        elif choice == ("8"):
            try:
                target = input("[+] Enter Domain or IP Address: ").lower()
                url = ("http://ip-api.com/json/")
                response = urllib.request.urlopen(url + target)
                data = response.read()
                jso = json.loads(data)
                os.system("reset")
                print(f"[+] Searching.... IP Location Finder: ".format(url) + target)
                time.sleep(1.5)

                print("\n [+] Url: " + target + "")
                print(" [+] " + "" + "IP: " + jso["query"] + "")
                print(" [+] " + "" + "Status: " + jso["status"] + "")
                print(" [+] " + "" + "Region: " + jso["regionName"] + "")
                print(" [+] " + "" + "Country: " + jso["country"] + "")
                print(" [+] " + "" + "City: " + jso["city"] + "")
                print(" [+] " + "" + "ISP: " + jso["isp"] + "")
                print(" [+] " + "" + "Lat & Lon: " + str(jso['lat']) + " & " + str(jso['lon']) + "")
                print(" [+] " + "" + "Zipcode: " + jso["zip"] + "")
                print(" [+] " + "" + "TimeZone: " + jso["timezone"] + "")
                print(" [+] " + "" + "AS: " + jso["as"] + "" + "\n")

            except URLError:
                print("[-] Please provide a valid IP address!")

        elif choice == ("9"):
            try:
                target = input("[+] Enter Domain or IP Address: ").lower()
                os.system("reset")
                print(f"[+] Searching for: Traceroute: ".format(target) + target)
                print("[+] This will take a moment... Get some coffee :)\n")
                time.sleep(5)
                command = ("mtr " + "-4 -rwc 1 " + target)
                proces = os.popen(command)
                results = str(proces.read())
                print("" + results + command + "")

            except Exception:
                pass

        elif choice == ("10"):
            try:
                target = input("[+] Enter email: ")
                os.system("reset")
                print("[+] Scanning....Have I been pwned: \n" + target)
                time.sleep(1.5)
                url = ("https://haveibeenpwned.com/api/v2/breachedaccount/%s" % target)
                response = requests.get(url)

                if response.status_code == 200:
                    response = response.json()
                    le = len(response)

                    for item in range(le):
                        clas = str(response[item]["DataClasses"])
                        clas = re.sub("\[(?:[^\]|]*\|)?([^\]|]*)\]", r"\1", clas)
                        clas = clas.replace("'", "")

                        print("\n")
                        print("[+] Name:     " + "" + str(response[item]["Title"]) + "")
                        print("[+] Domain:   " + "" + str(response[item]["Domain"]) + "")
                        print("[+] Breached: " + "" + str(response[item]["BreachDate"]) + "")
                        print("[+] Details:  " + "" + str(clas) + "")
                        print("[+] Verified: " + "" + str(response[item]["IsVerified"]) + "")
                else:
                    print("[+] Email NOT Found in Database")

            except Exception:
                print("[+] Unable to reach HaveIBeenPwned")

        elif choice == ("11"):
            time.sleep(1)
            print("\n[+] Exiting...")

        else:
            print("[-] Invalid option!")


# =====# Main #===== #

if __name__ == "__main__":
    main()
