.PHONY: env

all: env

env: requirements.txt
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt && pip install -e .

dev-env: requirements.txt requirements-dev.txt
	virtualenv env && . ./env/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && pip install -e .

lint:
	. ./env/bin/activate && flake8 --ignore=E501 mlt mltlib

docker:
	docker build -t mlt .

env-up: docker
	docker-compose up -d

end-down:
	docker-compose down

test: env-up
	docker-compose exec test ./resources/wait-port kubernetes 8080
	docker-compose exec test kubectl cluster-info

clean:
	rm -rf env
