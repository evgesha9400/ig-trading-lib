PYTEST := poetry run pytest
UNIT_DIR := tests/unit/v4

.PHONY: install test lint format type docs-check docs-serve workflow-check audit build verify

install:
	poetry sync --with dev

test:
	$(PYTEST) $(UNIT_DIR)

lint:
	poetry run ruff check src tests scripts examples

format:
	poetry run ruff format --check src tests scripts examples

type:
	poetry run pyright

docs-check:
	poetry run python scripts/generate_documentation_indexes.py --check
	poetry run python scripts/check_documentation_contract.py
	poetry run mkdocs build --strict --site-dir /tmp/ig-trading-lib-site

docs-serve:
	poetry run mkdocs serve

workflow-check:
	poetry run python scripts/check_release_workflow.py

audit:
	poetry export --only main --without-hashes --output /tmp/ig-trading-lib-requirements.txt
	poetry run pip-audit --strict --requirement /tmp/ig-trading-lib-requirements.txt

build:
	poetry build
	poetry run python scripts/check_built_distributions.py

verify: format lint type docs-check workflow-check test audit build
