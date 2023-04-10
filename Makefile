SHELL=/bin/bash

all: install test publish

install:
	pip install .[dev]

publish:
	flit publish

test: test-model test-db

test-%:
	@echo "Testing $@"
	./test/main.sh test $@
