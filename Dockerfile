FROM immauss/openvas

RUN cd /opt; mkdir reports
RUN mkdir app; cd ./app; mkdir config
RUN apt-get update -y; apt-get install cron -y;
RUN python3 -m pip install python-gvm --break-system-packages
RUN python3 -m pip install scapy --break-system-packages
COPY ./src /opt/app
COPY ./config /opt/app/config
CMD [ "bash", "/opt/app/config/setup_cron.sh" ]