.PHONY: dependencies

all: main

main: main.py
	@echo "Should run linting and tests before submitting application"

build:
	docker build --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} -t ${CONTAINER_NAME} .
