PYTHON = python
PROGRAM = twwanim
SRC_PY = src
TEST_PY = tests
COV_PY=coverage/lcov.info

PYTEST_OPTS = ""  # --full-trace

install:
	pip install .

uninstall:
	pip uninstall $(PROGRAM)

dev-install:
	pip install -e .

test:
	$(PYTHON) -m pytest -x --cov=$(SRC_PY) --cov-report=lcov:$(COV_PY) $(PYTEST_OPTS) $(TEST_PY)

coverage:
	coverage run --source=src setup.py test

clean:
	$(PYTHON) setup.py clean

console:
	cd src && $(PYTHON)

lab:
	cd notebooks && jupyter-lab

register:
	$(PYTHON) setup.py register

publish:
	$(PYTHON) setup.py sdist upload

.PHONY: install uninstall dev_install test coverage clean console register publish
