FROM ubuntu:latest

RUN useradd -ms /bin/bash newuser
RUN apt-get update -y 
RUN apt-get upgrade -y 
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-venv -y
     
RUN cd /home/newuser
RUN python3 -m venv venv
SHELL ["/bin/bash", "-c"] 
RUN source venv/bin/activate
RUN pip install python-gvm
