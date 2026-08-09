from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_every_unit_contract_runs_by_default_and_in_ci() -> None:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    makefile = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "publish-to-pypi.yml").read_text(
        encoding="utf-8"
    )

    assert pyproject["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests/unit/v4"]
    assert "UNIT_DIR := tests/unit/v4\n" in makefile
    assert "poetry run pytest tests/unit/v4\n" in workflow
    assert "tests/unit\n" not in workflow


def test_v4_modules_are_exhaustively_checked_and_generated() -> None:
    contract = yaml.safe_load(
        (PROJECT_ROOT / "docs" / "contracts" / "public-api.yml").read_text(encoding="utf-8")
    )
    public_modules = set(contract["public_modules"])
    index = json.loads(
        (PROJECT_ROOT / "docs" / "reference" / "public-api-index.json").read_text(encoding="utf-8")
    )

    assert {
        "ig_trading_lib.api",
        "ig_trading_lib.operations.markets",
        "ig_trading_lib.workflows.discovery",
    } <= public_modules
    assert {entry["name"] for entry in index["entry_points"]} == {"IG", "AsyncIG"}
    assert {tuple(entry["layers"]) for entry in index["entry_points"]} == {
        ("operations", "workflows")
    }
    assert {entry["namespace"] for entry in index["operations"]} == set(contract["operations"])
    assert {entry["namespace"] for entry in index["workflows"]} == set(contract["workflows"])
    assert all(entry["path"].startswith("ig.operations.") for entry in index["operations"])
    assert index["root_exports"] == contract["root_exports"]
    assert index["public_modules"] == contract["public_modules"]
    assert all(
        operation["sync_signature"] and operation["return_type"]
        for namespace in index["operations"]
        for operation in namespace["operations"]
    )


def test_documentation_does_not_create_an_async_compatibility_promise() -> None:
    prose = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "docs" / "getting-started.md",
            PROJECT_ROOT / "src" / "ig_trading_lib" / "api.py",
        )
    )

    assert "same names, inputs, and results" not in prose
    assert "same operation and workflow names, parameters, and result models" not in prose
