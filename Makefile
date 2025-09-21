# -------- Config --------
PYTEST := poetry run pytest -q
UNIT_DIR := tests/unit
INTEG_DIR := tests/integration

.PHONY: help install venv clean \
        test test-unit test-integration test-all \
        test-failed

help:
	@echo "Targets:"
	@echo "  install          - poetry install (deps + package)"
	@echo "  venv             - show Poetry venv path"
	@echo "  clean            - remove .pytest_cache and __pycache__"
	@echo "  test             - run UNIT tests (default)"
	@echo "  test-unit        - run UNIT tests"
	@echo "  test-integration - run INTEGRATION tests"
	@echo "  test-all         - run ALL tests (unit + integration)"
	@echo "  test-file        - run a specific test file/class/case (TEST=...)"
	@echo "  test-failed      - rerun only tests that failed last run"

install:
	poetry install

clean:
	@find tests -name '__pycache__' -type d -exec rm -rf {} + || true
	@rm -rf .pytest_cache

# ----- Test Targets -----

# Default: fast feedback — unit only
test: test-unit

test-unit:
	$(PYTEST) $(UNIT_DIR)

test-integration:
	$(PYTEST) $(INTEG_DIR)

test-all:
	$(PYTEST) $(UNIT_DIR) $(INTEG_DIR)

test-failed:
	$(PYTEST) --last-failed
