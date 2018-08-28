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
COPY yummy_api /yummy_api/
COPY script.sh /yummy_api/
RUN virtualenv venv && \
    . venv/bin/activate && \
    pip3 install -r /yummy_api/requirements.txt
WORKDIR /yummy_api
ENV PATH=$PATH:/bin/bash

CMD /bin/sh script.sh
