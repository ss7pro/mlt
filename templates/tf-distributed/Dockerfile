FROM python:3

ADD requirements.txt /src/deps/requirements.txt
RUN pip install -r /src/deps/requirements.txt

WORKDIR /src/app
ADD . /src/app

RUN pycodestyle -v .

ENTRYPOINT [ "python", "main.py" ]
