.PHONY: env

all: env

env:
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt
