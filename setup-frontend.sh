#!/bin/bash

if [ -z ${PORT} ]; then
	PORT=5000
fi

echo -n "[*] Checking if docker exists: "
(docker -v) &>/dev/null

if [[ $? == 0 ]]; then
	docker -v | cut -d ' ' -f 3
else
	echo "Not Found!"
	exit 1
fi

echo "[*] Building the docker container!"
docker build -t raidware-front ./Frontend

echo "[+] Running the docker container on Port $PORT."
_=$(docker run -d -p $PORT:3000 raidware-frontend)

if [[ $? == 0 ]]; then
	echo "[*] Container successfully running. ID: $_"
fi
