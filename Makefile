PYTHON = python3
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

# For PyPI publication (requires `twine` and `build`; configure `~/.pypirc`)
build:
	rm -rf dist
	$(PYTHON) -m build

publish-test: build
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish: build
	$(PYTHON) -m twine upload dist/*


.PHONY: install uninstall dev_install test coverage clean console build publish-test publish
