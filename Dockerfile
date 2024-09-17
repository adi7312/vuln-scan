FROM immauss/openvas
RUN cd /opt; mkdir reports; mkdir log; touch ./log/app.log
RUN mkdir app; cd ./app; mkdir config;
RUN apt-get update -y; apt-get install cron -y; apt-get upgrade -y;
RUN python3 -m pip install python-gvm --break-system-packages
COPY ./src /opt/app
COPY ./config /opt/app/config
RUN chmod +x /opt/app/gvm_handler.py; chmod +x /opt/app/logger.py; chmod +x /opt/app/smtp_handler.py
RUN chmod +x /opt/app/config/setup_cron.sh; chmod +x /opt/app/config/update.sh
