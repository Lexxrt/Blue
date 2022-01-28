if [ "$EUID" -ne 0 ]
  then echo "[-] Please run as root"
  exit
fi

echo "\n[+] Installing Dependencies...\n"
sudo apt install curl
sudo apt install nmap
sudo apt install whois
sudo apt install python3
sudo apt install python3-pip

echo "\n[+] Installing Python Modules...\n"
pip3 install -r requirements.txt