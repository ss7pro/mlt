FROM python:3.6

RUN apt-get update && apt-get install -y netcat
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl && cp ./kubectl /usr/local/bin/kubectl

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
RUN pip install virtualenv
RUN pip install -r requirements.txt
RUN pip install -e .