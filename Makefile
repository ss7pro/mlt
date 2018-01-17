.PHONY: env

all: env

env: requirements.txt
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt && pip install -e .

clean:
	rm -rf env
