#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "[!] Please run the script as root!"
	exit 1
fi

echo -e "[+] Raidware Setup script.\n\n"
echo "[+] Setting up required tools: "
(apt install mingw-w64-common mingw-w64-i686-dev mingw-w64-tools mingw-w64-x86-64-dev docker.io mono-complete -y) &>/dev/null

echo "[*] Checking if python3 exists"
(python3 --version) &>/dev/null

if [[ $? == 0 ]]; then
	echo -n "[*] Found! Version: "
	python3 --version | cut -d ' ' -f 2
else
	echo "[!] Python3 wasn't found. Installing"
	(apt install -y python3 python3-pip) &>/dev/null
fi

echo "[*] Checking if pip3 exists"
(pip3 --version) &>/dev/null

if [[ $? == 0 ]]; then
	echo -n "[*] Found! Version: "
	pip3 --version | cut -d ' ' -f 2
else
	echo "[!] Python3 wasn't found. Installing"
	(apt install -y python3-pip) &>/dev/null
fi

echo "[*] Installing the libraries required..."
pip3 install -r requirements.txt

echo "[+] Done!"
