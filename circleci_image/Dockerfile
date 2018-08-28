FROM ubuntu:16.04

MAINTAINER philophilo
RUN apt-get update -y && \
        apt-get install -y libssl-dev && \
        apt-get install -y software-properties-common && \
        add-apt-repository ppa:jonathonf/python-3.6 && \
        apt-get install -y python3-pip python3-dev && \
        apt-get install -y --no-install-recommends apt-utils && \
        pip3 install virtualenv && \
        apt-get install -y nginx
COPY yummy /etc/nginx/sites-available/
RUN rm -rf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
        ln -s /etc/nginx/sites-available/yummy /etc/nginx/sites-enabled/ && \
        mkdir -p yummy_api
RUN virtualenv venv && \
    . venv/bin/activate
RUN apt-get install -y awscli
RUN apt-get install curl && \
        curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.8.7/bin/linux/amd64/kubectl && \
        chmod +x ./kubectl && \
        mv ./kubectl /usr/local/bin/kubectl
RUN apt-get install wget && \
        wget https://github.com/kubernetes/kops/releases/download/1.8.0/kops-linux-amd64 && \
        chmod +x kops-linux-amd64 && \
        mv kops-linux-amd64 /usr/local/bin/kops
WORKDIR /yummy_api
ENV PATH=$PATH:/bin/bash
