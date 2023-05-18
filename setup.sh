#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "[!] Please run the script as root!"
	exit 1
fi

echo "[+] Raidware Setup script."
echo "[+] Setting up mingw:"
(apt install mingw-w64-common mingw-w64-i686-dev mingw-w64-tools mingw-w64-x86-64-dev -y) &>/dev/null

echo "[+] Setting up CSC for dotnet: "
echo "[*] Downloading the microsoft prod package"
(wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb) &>/dev/null
(sudo dpkg -i /tmp/packages-microsoft-prod.deb) &>/dev/null
(rm /tmp/packages-microsoft-prod.deb) &>/dev/null

echo "[*] Updating the repositories"
(apt update) &>/dev/null
echo "[*] Install dotnet-sdk and dotnet-runtime"
(apt install -y dotnet-sdk-7.0 dotnet-runtime-7.0) &>/dev/null

echo "[*] Installing docker and mono-devel"
(apt install -y docker.io mono-devel) &>/dev/null

echo "[*] Checking if python3 exists"
(python3 --version) &>/dev/null

if [[ $? == 0 ]]; then
	echo -n "[*] Found! Version: "
	python3 --version | cut -d ' ' -f 2
else
	echo "[!] Python3 wasn't found. Installing"
	(apt install -y python3 python3-pip) &>/dev/null
fi

echo "[*] Installing the libraries required..."
pip3 install -r requirements.txt

echo "[+] Done!"
