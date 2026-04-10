FROM ubuntu:22.04

RUN dpkg --add-architecture i386
RUN apt update && apt -y upgrade
RUN apt install -y python3-dev python3-pip build-essential sudo gcc
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Upgrade pip first to help with dependency resolution
RUN python3 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /

RUN python3 -m pip install -r /requirements.txt
CMD ["/bin/bash"]
