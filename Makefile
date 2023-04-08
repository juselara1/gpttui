SHELL=/bin/bash

all: test

test: test-model

test-%:
	@echo "Testing $@"
	./test/main.sh test $@
