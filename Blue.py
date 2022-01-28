import bs4
import json
import os
import requests
import time

class utils:
    def clearScreen():
        os.system('clear')
    def chkOS():
        if os.name == 'nt':
            print('[+] Blue is not supported for Windows yet.')
            exit()
        else:
            pass

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
    print('[+] 1. WhoIs Lookup')
    print('[+] 2. DNS Lookup')
    print('[+] 3. Nmap Port Scan')
    print('[+] 4. HTTP Header Grabber')
    print('[+] 5. Clickjacking Test - X-Frame-Options Header')
    print('[+] 6. Robots.txt Scanner')
    print('[+] 7. Link Grabber')
    print('[+] 8. IP GeoLocation Finder')
    print('[+] 9. Traceroute')

def main():
    banner()
    menu()

    choice = input('\n[+] Enter your choice: ')
    # WhoIs Lookup
    if choice == ('1'):
        try:
            target = input('[+] Enter Domain or IP Address: ').lower()
            utils.clearScreen()
            time.sleep(1.5)
            os.system(f'whois {target}')
        except Exception:
            pass
    # DNS Lookup
    elif choice == ('2'):
        try:
            target = input('[+] Enter Domain or IP Address: ').lower()
            utils.clearScreen()
            time.sleep(1.5)
            os.system(f'dig {target} +trace ANY')
        except Exception:
            pass
    # Nmap Port Scan
    elif choice == ('3'):
        try:
            target = input('Enter Domain or IP Address: ').lower()
            utils.clearScreen()
            print('[+] This will take a moment.\n')
            time.sleep(1.5)
            logPath = f'logs/nmap-scan'
            os.system(f'nmap -p- -oN {logPath} {target}')
        except KeyboardInterrupt:
                print('\n')
                print('[-] User Interruption Detected..!')
                time.sleep(1)
    # HTTP Header
    elif choice == ('4'):
        try:
            target = input('[+] Enter Domain or IP Address: ').lower()
            utils.clearScreen()
            time.sleep(1.5)
            os.system(f'curl -i {target}')
        except Exception:
            pass
    # Click-Jacking Scan
    elif choice == ('5'):
        target = input('[+] Enter the Domain to test: ').lower()
        utils.clearScreen()
        if not (target.startswith('http://') or target.startswith('https://')):
            target = 'http://',target
        
        time.sleep(2)
        try:
            resp = requests.get(target).headers
            print('\nHeader set are: \n')
            if 'X-Frame-Options' in resp.keys():
                print('\n[+] Click Jacking Header is present')
                print('[+] You can\'t clickjack this site !\n')
            else:
                print('\n[*] X-Frame-Options-Header is missing ! ')
                print('[!] Clickjacking is possible, this site is vulnerable to Clickjacking\n')
        except Exception as ex:
            print('[+] Exception caught: ',str(ex))
    # Robots.txt Scan
    elif choice == ('6'):
        try:
            target = input('Enter Domain: ').lower()
            utils.clearScreen()
            time.sleep(1.5)
            if not (target.startswith('http://') or target.startswith('https://')):
                target = 'http://',target
            try:
                requests.get(f'{target}/robots.txt')
            except:
                print(f'[-] Can\'t access {target}/robots.txt')
        except Exception as ex:
            print('[+] Exception caught: ',str(ex))
    # Link Grabber
    elif choice == ('7'):
        try:
            target = input('Enter Domain: ').lower()
            utils.clearScreen()
            time.sleep(2)
            if not (target.startswith('http://') or target.startswith('https://')):
                target = 'http://',target
            main_req = requests.get(target).text
            soup = bs4.BeautifulSoup(main_req, 'html.parser')
            href = soup.findAll('a')
            for i in href:
                print(str(i))
        except Exception:
            pass
        # GeoLocation Finder
    elif choice == ('8'):
        try:
            target = input('[+] Enter Domain or IP Address: ').lower()
            response = requests.get(f'http://ip-api.com/json/{target}').text
            jso = json.loads(response)
            utils.clearScreen()
            time.sleep(1.5)
            print('\n [+] Url:', target)
            print('[+] IP:', jso['query'])
            print('[+] Status:', jso['status'])
            print('[+] Region:', jso['regionName'])
            print('[+] Country:', jso['country'])
            print('[+] City:', jso['city'])
            print('[+] ISP:', jso['isp'])
            print('[+] Lat & Lon:', str(jso['lat']), '&', str(jso['lon']))
            print('[+] Zipcode:', jso['zip'])
            print('[+] TimeZone:', jso['timezone'])
            print('[+] AS:', jso['as'])
        except:
            print('[-] Please provide a valid IP address!')
    elif choice == ('9'):
        try:
            target = input('[+] Enter Domain or IP Address: ').lower()
            utils.clearScreen()
            print('[+] This will take a moment...\n')
      
            time.sleep(5)
            os.system(f'mtr -4 -rwc 1 {target}')
        except Exception:
            pass
    else:
        print('[-] Invalid option!')

if __name__ == '__main__':
    if os.path.exists('./logs'):
        pass
    else:
        os.mkdir('logs')
    
    try:
        utils.chkOS()
        main()
    except:
        pass
