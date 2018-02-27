PY_VERSION := 2
# if py_version is 2, use virtualenv, else python3 venv
VIRTUALENV_EXE=$(if $(subst 2,,$(PY_VERSION)),python3 -m venv,virtualenv)
VIRTUALENV_DIR=$(if $(subst 2,,$(PY_VERSION)),.venv3,.venv)
ACTIVATE="$(VIRTUALENV_DIR)/bin/activate"

.PHONY: venv

all: venv


# we need to update pip and setuptools because venv versions aren't latest
# need to prepend $(ACTIVATE) everywhere because all make calls are in subshells
# otherwise we won't be installing anything in the venv itself
$(ACTIVATE): requirements.txt requirements-dev.txt
	@echo "Updating virtualenv dependencies in: $(VIRTUALENV_DIR)..."
	@test -d $(VIRTUALENV_DIR) || $(VIRTUALENV_EXE) $(VIRTUALENV_DIR)
	@. $(ACTIVATE) && python$(PY_VERSION) -m pip install -U pip setuptools
	@. $(ACTIVATE) && python$(PY_VERSION) -m pip install -r requirements.txt -r requirements-dev.txt
	@. $(ACTIVATE) && python$(PY_VERSION) -m pip install -e .
	@touch $(ACTIVATE)

venv: $(ACTIVATE)
	@echo -n "Using "
	@. $(ACTIVATE) && python --version

venv2: venv

venv3: PY_VERSION=3
venv3: $(ACTIVATE)
	@echo -n "Using "
	@. $(ACTIVATE) && python3 --version

lint: venv
	. $(ACTIVATE) && flake8 bin/mlt mlt

lint3: PY_VERSION=3
lint3: lint

unit_test: venv
	@echo "Running unit tests..."
	@. $(ACTIVATE) && pytest -v $(TESTOPTS) tests/unit

unit_test3: PY_VERSION=3
unit_test3: unit_test

test: lint unit_test

test3: PY_VERSION=3
test3: test

docker:
	docker build -t mlt .

env-up: docker
	docker-compose up -d

end-down:
	docker-compose down

test-e2e: env-up
	docker-compose exec test pip install -r requirements-dev.txt
	docker-compose exec test ./resources/wait-port kubernetes 8080
	docker-compose exec test kubectl cluster-info
	docker-compose exec test py.test -v tests/e2e

clean:
	rm -rf .venv .venv3
