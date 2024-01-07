PYTHON = python
PROGRAM = twwanim
SRC_PY = src
TEST_PY = tests
COV_PY=coverage/lcov.info

PYTEST_OPTS = ""  # --full-trace
export PYTHONPATH=$(SRC_PY)

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

uninstall:
	pip uninstall $(PROGRAM)

dev-install:
	$(PYTHON) setup.py develop

dev-uninstall:
	$(PYTHON) setup.py develop -u

test:
	$(PYTHON) -m pytest -x --cov=$(SRC_PY) --cov-report=lcov:$(COV_PY) $(PYTEST_OPTS) $(TEST_PY)

coverage:
	coverage run --source=src setup.py test

clean:
	$(PYTHON) setup.py clean

console:
	cd src && $(PYTHON)

lab:
	export PYTHONPATH=$(PWD)/src
	cd notebooks && jupyter-lab

register:
	$(PYTHON) setup.py register

publish:
	$(PYTHON) setup.py sdist upload

.PHONY: build install uninstall dev_install dev_uninstall pep8 test coverage clean console register publish
