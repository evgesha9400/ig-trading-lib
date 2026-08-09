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

    assert pyproject["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests/unit"]
    assert "UNIT_DIR := tests/unit\n" in makefile
    assert "poetry run pytest tests/unit\n" in workflow
    assert "tests/unit/v3" not in workflow


def test_v4_modules_are_exhaustively_checked_and_generated() -> None:
    contract = yaml.safe_load(
        (PROJECT_ROOT / "docs" / "contracts" / "public-api.yml").read_text(encoding="utf-8")
    )
    public_modules = set(contract["public_modules"])
    classes = contract["classes"]
    index = json.loads(
        (PROJECT_ROOT / "docs" / "reference" / "public-api-index.json").read_text(encoding="utf-8")
    )

    assert {
        "ig_trading_lib.api",
        "ig_trading_lib.operations.markets",
        "ig_trading_lib.workflows.discovery",
    } <= public_modules
    assert {
        "ig_trading_lib.api.IG",
        "ig_trading_lib.api.AsyncIG",
        "ig_trading_lib.operations.markets.MarketOperations",
        "ig_trading_lib.operations.markets.AsyncMarketOperations",
        "ig_trading_lib.workflows.discovery.MarketDiscoveryWorkflow",
        "ig_trading_lib.workflows.discovery.AsyncMarketDiscoveryWorkflow",
    } <= set(classes)
    assert set(index["entry_points"]) == {"IG", "AsyncIG"}
    assert _public_paths(index["entry_points"]["IG"]) == {
        "operations.markets",
        "workflows.discovery",
    }
    assert _public_paths(index["entry_points"]["AsyncIG"]) == {
        "operations.markets",
        "workflows.discovery",
    }


def _public_paths(entry_point: dict[str, object]) -> set[str]:
    namespaces = entry_point["namespaces"]
    assert isinstance(namespaces, list)
    return {
        f"{namespace['name']}.{group['name']}"
        for namespace in namespaces
        for group in namespace["groups"]
    }
