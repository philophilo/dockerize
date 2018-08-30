FROM circleci/python:3.6.2-stretch-browsers

RUN sudo apt-get update && \
        sudo apt-get install docker python-pip python-setuptools wget

RUN sudo wget -q https://storage.googleapis.com/kubernetes-release/release/v1.8.7/bin/linux/amd64/kubectl && \
        sudo chmod +x kubectl && \
        sudo mv kubectl /usr/bin

RUN sudo wget -q https://github.com/kubernetes/kops/releases/download/1.8.0/kops-linux-amd64 && \
        sudo chmod +x kops-linux-amd64 && \
        sudo mv kops-linux-amd64 /usr/bin/kops
