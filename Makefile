all: lint test

lint:
	yamllint -s .
	flake8
	bandit -r .

test:
	PYTHONPATH=.:.. pytest
