.PHONY = all
all: install test

.PHONY = install
install: env
	env/bin/pip install -r requirements.txt

env:
	pyvenv-3.5 env

.PHONY = test
test: env
	env/bin/nosetests test.py
