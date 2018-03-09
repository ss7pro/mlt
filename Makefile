SHELL=bash

.PHONY: venv test lint clean

all: venv

venv:
	@echo "Creating python2 and 3 virtualenv in .venv and .venv3 dirs"
	@tox -e py27-venv -e py35-venv

dev-env:
	@echo "Creating python2 and 3 editable install in .venv and .venv3"
	@tox -e py27-dev -e py35-dev

test:
	@echo "Running unit tests across python platforms..."
	@tox -e py27-unit -e py35-unit

lint:
	@echo "Linting with flake8..."
	@tox -e py27-lint -e py35-lint

coverage:
	@echo "Running coverage report..."
	@tox -e py27-coverage -e py35-coverage

docker:
	docker build --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t mlt .

env-up: docker
	docker-compose up -d

end-down:
	docker-compose down

test-e2e: env-up
	docker-compose exec test ./resources/wait-port kubernetes 8080
	docker-compose exec test kubectl cluster-info
	docker-compose exec test pip install tox
	docker-compose exec test tox -e py27-e2e -e py35-e2e

clean:
	rm -rf .venv .venv3
	find . -name '*.pyc' -delete
