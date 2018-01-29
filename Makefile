.PHONY: env

all: env

env: requirements.txt
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt && pip install -e .

dev-env: requirements.txt requirements-dev.txt
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && pip install -e .

lint:
	. ./env/bin/activate && flake8 --ignore=E501 bin/*

clean:
	rm -rf env
