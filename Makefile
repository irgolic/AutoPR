type:
	pyright 

test:
	pytest autopr/tests

schema:
	python -m autopr.models.config.entrypoints

all: type test schema
