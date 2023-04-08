SHELL=/bin/bash

all: test

test: test-model test-db

test-%:
	@echo "Testing $@"
	./test/main.sh test $@
