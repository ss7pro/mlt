.PHONY: dependencies

all: main

main: main.py
	@echo "Should run linting and tests before submitting application"

build:
	docker pull pytorch/pytorch:v0.2
	docker tag pytorch/pytorch:v0.2 ${CONTAINER_NAME}
