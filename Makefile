SHELL := bash
ifeq ($(OS),Windows_NT)
	EXITCODE = %ERRORLEVEL%
else
	EXITCODE = $$?
endif

.PHONY: install
install:
	poetry install --no-interaction --only main

.PHONY: install-dev-tools
install-dev-tools:
	poetry install --no-interaction

.PHONY: lint
lint: install-dev-tools
	poetry run flake8 .
	poetry run pylint ./scripts/*.py ./plexanisync || poetry run pylint-exit --error-fail --warn-fail $(EXITCODE)

.PHONY: test
test: install-dev-tools
	poetry run pytest -v

.PHONY: update-requirements
update-requirements:
	poetry export --without-hashes --format=requirements.txt -o requirements.txt