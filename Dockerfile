FROM immauss/openvas

RUN cd /opt; mkdir reports; mkdir log; touch ./log/app.log
RUN mkdir app; cd ./app; mkdir config;
RUN apt-get update -y; apt-get install cron -y;
RUN python3 -m pip install python-gvm --break-system-packages
COPY ./src /opt/app
COPY ./config /opt/app/config