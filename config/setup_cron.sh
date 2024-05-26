#!/bin/bash

service cron start
frequency=$FREQUENCY
unit="${frequency: -1}"
crontab -l > /tmp/mycron
env >> /etc/environment
if [[ "$unit" == "D" ]]; then
    echo "30 0 * * *  /usr/bin/python3 /opt/app/gvm_handler.py" >> /tmp/mycron
elif [[ "$unit" == "W" ]]; then
    echo "30 0 * * 0  /usr/bin/python3 /opt/app/gvm_handler.py" >> /tmp/mycron
elif [[ "$unit" == "M" ]]; then
    echo "30 0 1 * *  /usr/bin/python3 /opt/app/gvm_handler.py" >> /tmp/mycron
else
    echo "30 0 * * *  /usr/bin/python3 /opt/app/gvm_handler.py" >> /tmp/mycron
fi
crontab /tmp/mycron
