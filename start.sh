#!/bin/bash


if ! command -v docker &> /dev/null; then
    echo -e "\e[0;31m[!]\e[m Docker is not installed."
    echo -e "\e[0;31m[!]\e[m Warning: Script supports installing Docker on Ubuntu and Debian systems only!"
    echo -e "\e[0;36m[*]\e[m Updating package lists..."
    sudo apt-get update -y
    echo -e "\e[0;36m[*]\e[m Installing Docker..."
    sudo apt install docker.io -y
    echo -e "\e[0;31m\e[0;32m[*]\e[m\e[m Docker has been installed and started successfully."
else
    echo -e "\e[0;36m[*]\e[m Docker is installed."
fi

sudo service docker start

if [ -z "$FREQUENCY" ]; then
    echo -e "\e[0;31m[!]\e[m FREQUENCY is not set."
    echo -e "\e[0;31m[!]\e[m Please set the FREQUENCY environment variable."
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo -e "\e[0;31m[!]\e[m EMAIL is not set."
    echo -e "\e[0;31m[!]\e[m Please set the EMAIL environment variable."
    exit 1
fi

if [ -z "$IP" ]; then
    echo -e "\e[0;31m[!]\e[m IP is not set."
    echo -e "\e[0;31m[!]\e[m Please set the IP environment variable."
    exit 1
fi

if [ -z "$SENDER_PASS" ]; then
    echo -e "\e[0;31m[!]\e[m SENDER_PASS is not set."
    echo -e "\e[0;31m[!]\e[m Please set the SENDER_PASS environment variable."
    exit 1
fi

if [ -z "$USERNAME" ]; then
    echo -e "\e[0;31m[!]\e[m USERNAME is not set. Switching to default username: admin."
    USERNAME="admin"
fi

if [ -z "$PASSWORD" ]; then
    echo -e "\e[0;31m[!]\e[m PASSWORD is not set. Switching to default password: admin."
    PASSWORD="admin"
fi

echo -e "\e[0;36m[*]\e[m Pulling ghcr.io/adi7312/vuln-scan:latest..."
sudo docker pull ghcr.io/adi7312/vuln-scan:latest
# if --audit flag is passed perform below operation
if [ "$1" = "--audit-enable" ]; then
    echo -e "\e[0;36m[*]\e[m Running the audit script..."
    sudo bash audit/audit.sh
fi
echo -e "\e[0;36m[*]\e[m Running the container in detached mode..."
sudo docker run --detach --publish 8090:9392 -e SKIPSYNC=true -e IP=$IP -e FREQUENCY=$FREQUENCY -e SENDER_PASS="$SENDER_PASS" -e EMAIL=$EMAIL -e USERNAME=$USERNAME -e PASSWORD=$PASSWORD --name avs ghcr.io/adi7312/vuln-scan:latest
sudo docker exec avs /bin/bash /opt/app/config/setup_cron.sh
sudo docker exec -it avs python3 /opt/app/gvm_handler.py


