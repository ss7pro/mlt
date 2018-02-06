FROM python:3.6

RUN apt-get update && apt-get install -y netcat
# Need to install kubectl, but the current link seems broken.

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
RUN pip install virtualenv
RUN pip install -r requirements.txt
RUN pip install -e .

RUN git config --global user.email "test@docker"
RUN git config --global user.name "Test Docker User"