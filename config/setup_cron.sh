#!/bin/bash

service cron start
frequency=$FREQUENCY
echo $FREQUENCY
unit="${frequency: -1}"
echo $unit
crontab -l > /tmp/mycron
if [[ "$unit" == "H" ]]; then
    echo "30 * * * * root python3 /opt/app/gvm_handler.py" >> /tmp/mycron
elif [[ "$unit" == "D" ]]; then
    echo "30 0 * * * root python3 /opt/app/gvm_handler.py" >> /tmp/mycron
elif [[ "$unit" == "W" ]]; then
    echo "30 0 * * 0 root python3 /opt/app/gvm_handler.py" >> /tmp/mycron
elif [[ "$unit" == "M" ]]; then
    echo "30 0 1 * * root python3 /opt/app/gvm_handler.py" >> /tmp/mycron
else
    echo "30 0 * * * root python3 /opt/app/gvm_handler.py" >> /tmp/mycron
fi

crontab /tmp/mycron
rm /tmp/mycron
