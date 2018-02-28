SHELL=bash

.PHONY: venv

all: venv

# we need to do it this way, because prerequisites get expanded *before*
# lazy evaluation
define pyversion_targets
# we need to update pip and setuptools because venv versions aren't latest
# need to prepend $$(ACTIVATE) everywhere because all make calls are in subshells
# otherwise we won't be installing anything in the venv itself
$(4): requirements.txt requirements-dev.txt
	@echo "Updating virtualenv dependencies in: $(3)..."
	@test -d $(3) || $(2) $(3)
	@. $(4) && python$(1) -m pip install -U pip setuptools
	@. $(4) && python$(1) -m pip install -r requirements.txt -r requirements-dev.txt
	@. $(4) && python$(1) -m pip install -e .

venv$(1): $(4)
	@echo -n "Using "
	@. $(4) && python --version

lint$(1): venv$(1)
	@. $(4) && flake8 bin/mlt mlt

unit_test$(1): venv$(1)
	@echo "Running unit tests..."
	@. $(4) && pytest -v $$(TESTOPTS) tests/unit

endef

$(eval $(call pyversion_targets,2,virtualenv,.venv,.venv/bin/activate))
$(eval $(call pyversion_targets,3,python3 -m venv,.venv3,.venv3/bin/activate))

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
	docker-compose exec test pip install -r requirements-dev.txt
	docker-compose exec test ./resources/wait-port kubernetes 8080
	docker-compose exec test kubectl cluster-info
	# conftest + docker have issues because of runtime path differences
	# https://stackoverflow.com/questions/44067609/getting-error-importmismatcherror-while-running-py-test
	docker-compose exec test find . -name \*.pyc -delete
	docker-compose exec test py.test -v tests/e2e

clean:
	rm -rf .venv .venv3
	find . -name '*.pyc' -delete
