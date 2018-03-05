SHELL=bash

.PHONY: venv venv2 venv3 lint lint2 lint3 unit_test unit_test2 unit_test3 clean test

VENV2_BIN := virtualenv
VENV3_BIN := python3 -m venv
VENV2_DIR := .venv
VENV3_DIR := .venv3
ACTIVATE2 := .venv/bin/activate
ACTIVATE3 := .venv3/bin/activate

all: venv

# we need to update pip and setuptools because venv versions aren't latest
# need to prepend `activate` everywhere because all make calls are in subshells
# otherwise we won't be installing anything in the venv itself
$(ACTIVATE2): requirements.txt requirements-dev.txt
	@echo "Updating virtualenv dependencies in: $(VENV2_DIR)..."
	@test -d $(VENV2_DIR) || $(VENV2_BIN) $(VENV2_DIR)
	@. $(ACTIVATE2) && python -m pip install -U pip setuptools
	@. $(ACTIVATE2) && python -m pip install -r requirements.txt -r requirements-dev.txt
	@. $(ACTIVATE2) && python -m pip install -e .

venv2: $(ACTIVATE2)
	@echo -n "Using "
	@. $(ACTIVATE2) && python --version

lint2: venv2
	@. $(ACTIVATE2) && flake8 bin/mlt mlt

unit_test2: venv2
	@echo "Running unit tests..."
	@. $(ACTIVATE2) && pytest -v $(TESTOPTS) tests/unit

$(ACTIVATE3): requirements.txt requirements-dev.txt
	@echo "Updating virtualenv dependencies in: $(VENV3_DIR)..."
	@test -d $(VENV3_DIR) || $(VENV3_BIN) $(VENV3_DIR)
	@. $(ACTIVATE3) && python$(1) -m pip install -U pip setuptools
	@. $(ACTIVATE3) && python$(1) -m pip install -r requirements.txt -r requirements-dev.txt
	@. $(ACTIVATE3) && python$(1) -m pip install -e .

venv3: $(ACTIVATE3)
	@echo -n "Using "
	@. $(ACTIVATE3) && python --version

lint3: venv3
	@. $(ACTIVATE3) && flake8 bin/mlt mlt

unit_test3: venv3
	@echo "Running unit tests..."
	@. $(ACTIVATE3) && pytest -v $(TESTOPTS) tests/unit

# defaults/shortcuts for python 2
venv: venv2
lint: lint2
unit_test: unit_test2

test: lint unit_test

docker:
	docker build -t mlt .

env-up: docker
	docker-compose up -d

end-down:
	docker-compose down

test-e2e: env-up
	docker-compose exec test pip install -r requirements-dev.txt -r requirements.txt
	docker-compose exec test pip install -e .
	docker-compose exec test ./resources/wait-port kubernetes 8080
	docker-compose exec test kubectl cluster-info
	# conftest + docker have issues because of runtime path differences
	# https://stackoverflow.com/questions/44067609/getting-error-importmismatcherror-while-running-py-test
	docker-compose exec test py.test -v tests/e2e

clean:
	rm -rf .venv .venv3
	find . -name '*.pyc' -delete
