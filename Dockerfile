FROM ubuntu:16.04

# separately install software properties for adding apt-repo; then 1 update is needed rather than 2
RUN apt-get update && apt-get install -yq --no-install-recommends --fix-missing \
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    jq \
    make \
    netcat \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    python-wheel \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -yq --no-install-recommends --fix-missing \
    docker-ce && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
# need to clean so as to not get conftest importmismatch error
RUN make clean

RUN git config --global user.email "test@example.com"
RUN git config --global user.name "Test Docker User"
