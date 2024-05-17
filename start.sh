#!/bin/bash


if ! command -v docker &> /dev/null; then
    echo "[!] Docker is not installed."
    echo "[!] Warning: Script supports installing Docker on Ubuntu and Debian systems only!"
    echo "[*] Updating package lists..."
    sudo apt-get update -y
    echo "[*] Installing Docker..."
    sudo apt install docker.io -y
    echo "[+] Docker has been installed and started successfully."
else
    echo "[*] Docker is installed."
fi

sudo service docker start

if [ -z "$FREQUENCY" ]; then
    echo "[!] FREQUENCY is not set."
    echo "[!] Please set the FREQUENCY environment variable."
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo "[!] EMAIL is not set."
    echo "[!] Please set the EMAIL environment variable."
    exit 1
fi

if [ -z "$IP" ]; then
    echo "[!] IP is not set."
    echo "[!] Please set the IP environment variable."
    exit 1
fi

if [ -z "$SENDER_PASS" ]; then
    echo "[!] SENDER_PASS is not set."
    echo "[!] Please set the SENDER_PASS environment variable."
    exit 1
fi

if [ -z "$USERNAME" ]; then
    echo "[!] USERNAME is not set. Switching to default username: admin."
    USERNAME="admin"
fi

if [ -z "$PASSWORD" ]; then
    echo "[!] PASSWORD is not set. Switching to default password: admin."
    PASSWORD="admin"
fi

echo "[*] Pulling ghcr.io/adi7312/vuln-scan:latest..."
sudo docker pull ghcr.io/adi7312/vuln-scan:latest
echo "[*] Running the container in detached mode..."
sudo docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=$IP -e FREQUENCY=$FREQUENCY -e SENDER_PASS="$SENDER_PASS" -e EMAIL=$EMAIL -e USERNAME=$USERNAME -e PASSWORD=$PASSWORD --name avs ghcr.io/adi7312/vuln-scan:latest
sudo docker exec avs /bin/bash /opt/app/config/setup_cron.sh
sudo docker exec -it avs python3 /opt/app/gvm_handler.py


