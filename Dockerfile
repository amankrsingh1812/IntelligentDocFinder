FROM ubuntu:20.04

ADD ./IntelligentDocFinder /home/IntelligentDocFinder

RUN apt-get update
RUN apt-get install -y build-essential

RUN apt-get install -y python3.8

RUN apt-get install -y curl

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN apt-get install -y python3.8-distutils
RUN python3.8 get-pip.py

RUN pip install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

WORKDIR  /home/IntelligentDocFinder
RUN apt-get install -y python3.8-dev
RUN pip install -r requirements.txt

RUN python3.8 setup.py


ENTRYPOINT nohup python3.8 index.py > server.logs 2>&1 & bash
