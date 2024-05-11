FROM immauss/openvas

RUN cd /opt
RUN mkdir reports;
RUN mkdir app; cd ./app; mkdir config
RUN python3 -m pip install python-gvm --break-system-packages
RUN python3 -m pip install scapy --break-system-packages
COPY ./src /opt/app
COPY ./config /opt/app/config
