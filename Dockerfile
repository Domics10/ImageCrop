FROM python:3.8-slim

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
    python3-dev \
    python3-setuptools \
    build-essential 

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 --version

COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV TF_ENABLE_ONEDNN_OPTS 0
ENV TORCH_HOME home/patch
WORKDIR $TORCH_HOME
COPY . .