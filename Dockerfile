FROM ubuntu:16.04

# fix-missing is needed to get `git` to work
RUN apt-get update && apt-get install -yq --no-install-recommends --fix-missing \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    jq \
    make \
    python-setuptools \
    python3-setuptools \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update

RUN apt-get install -yq --no-install-recommends --fix-missing netcat docker-ce python python-pip
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
RUN make clean

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "test@docker"
RUN git config --global user.name "Test Docker User"
