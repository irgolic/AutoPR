format:
	black autopr

type:
	pyright 

test:
	pytest autopr/tests

schema:
	python -m autopr.models.config.entrypoints

all: format type test schema
