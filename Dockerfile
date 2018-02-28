FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update

RUN apt-get install -y netcat docker-ce python python-pip
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
RUN make clean

RUN git config --global user.email "test@docker"
RUN git config --global user.name "Test Docker User"
