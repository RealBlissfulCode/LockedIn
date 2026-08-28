# The Handbook. No dependencies beyond Python 3 and Node for the tests.
#
#   make            build the data file and stamp the cache version
#   make check      fail if anything checked in is stale or invalid
#   make test       run the browser-less smoke tests
#   make serve      preview the site on http://localhost:8080
#   make all        check + test, which is exactly what CI runs

PY ?= python3
NODE ?= node
PORT ?= 8080

.PHONY: all build check test serve clean

build:
	$(PY) src/build_data.py

check:
	$(PY) src/build_data.py --check

test:
	$(NODE) test/run.js

all: check test

serve:
	@echo "http://localhost:$(PORT)"
	$(PY) tools/serve.py $(PORT)

clean:
	rm -rf src/__pycache__
