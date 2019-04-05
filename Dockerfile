FROM ubuntu:16.04

MAINTAINER philophilo

# install update and install 
# - pythoon3.6, for development, pip3
# - virtualenv and nginx
RUN apt-get update -y && \
        apt-get install -y libssl-dev && \
        apt-get install -y software-properties-common && \
        add-apt-repository ppa:jonathonf/python-3.6 && \
        apt-get install -y python3-pip python3-dev && \
        apt-get install -y --no-install-recommends apt-utils && \
        pip3 install virtualenv && \
        apt-get install -y nginx

# copy nginx configuration to available sites
# create a symbolic link between the configuration  available sites and enabled sites
# this will allow the applicatin to receive traffic once the container is running
COPY yummy /etc/nginx/sites-available/
RUN rm -rf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default && \
        ln -s /etc/nginx/sites-available/yummy /etc/nginx/sites-enabled/ && \
        mkdir -p yummy_api

# copy the application folder into the container
COPY yummy_api /yummy_api/
# copy the script for starting the application
COPY script.sh /yummy_api/
# create a virtual environment, activate, install requirements
RUN virtualenv venv && \
    . venv/bin/activate && \
    pip3 install -r /yummy_api/requirements.txt
# set the working directory
WORKDIR /yummy_api
# set the path for bash
ENV PATH=$PATH:/bin/bash
# run start up script when the container is run
CMD ["/bin/sh", "script.sh"]
