PYTEST := poetry run pytest
UNIT_DIR := tests/unit/v3

.PHONY: install test lint format type audit build verify

install:
	poetry sync --with dev

test:
	$(PYTEST) $(UNIT_DIR)

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format --check src tests

type:
	poetry run pyright

audit:
	poetry export --only main --without-hashes --output /tmp/ig-trading-lib-requirements.txt
	poetry run pip-audit --strict --requirement /tmp/ig-trading-lib-requirements.txt

build:
	poetry build

verify: format lint type test audit build
