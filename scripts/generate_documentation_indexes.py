"""Generate agent-facing indexes from the checked public API contract."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

API_INDEX_PATH = Path("docs/reference/public-api-index.json")
CONTRACT_PATH = Path("docs/contracts/public-api.yml")
ENDPOINT_CATALOG_PATH = Path("src/ig_trading_lib/endpoint_catalog.py")
LLMS_PATH = Path("docs/llms.txt")
ROOT_LLMS_PATH = Path("llms.txt")


class DocumentationIndexError(RuntimeError):
    """Raised when generated documentation artifacts are missing or stale."""


def load_public_contract(project_root: Path) -> dict[str, Any]:
    """Load the canonical public-contract mapping without deriving signatures from prose."""
    path = project_root / CONTRACT_PATH
    if not path.is_file():
        raise DocumentationIndexError(f"Public API contract is missing: {CONTRACT_PATH}")
    contract = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(contract, dict):
        raise DocumentationIndexError("Public API contract must be a mapping.")
    return contract


def load_endpoint_index(project_root: Path) -> list[dict[str, Any]]:
    """Project the maintained endpoint catalog into JSON-safe entries."""
    source_path = str(project_root / "src")
    sys.path.insert(0, source_path)
    try:
        from ig_trading_lib.endpoint_catalog import DOCUMENTED_ENDPOINTS

        return [
            {
                "name": endpoint.name,
                "path_template": endpoint.path_template,
                "method": endpoint.method,
                "versions": list(endpoint.versions),
            }
            for endpoint in DOCUMENTED_ENDPOINTS
        ]
    finally:
        sys.path.remove(source_path)


def build_api_index(contract: Mapping[str, Any], endpoints: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the machine-readable projection without hand-maintained signatures."""
    return {
        "schema_version": contract["schema_version"],
        "generated_from": {
            "contract": str(CONTRACT_PATH),
            "endpoint_catalog": str(ENDPOINT_CATALOG_PATH),
        },
        "public_modules": contract["public_modules"],
        "root_exports": contract["root_exports"],
        "classes": contract["classes"],
        "functions": contract["functions"],
        "exceptions": contract["exceptions"],
        "pydantic_fields": contract["pydantic_fields"],
        "examples": contract["examples"],
        "mutation_safety_rules": contract["mutation_safety_rules"],
        "endpoint_matrix": contract["endpoint_matrix"],
        "endpoints": endpoints,
    }


def build_llms_document(api_index: Mapping[str, Any], *, site_root: bool) -> str:
    """Create a compact discovery document pointing agents to canonical artifacts."""
    exports = "\n".join(f"- `{name}`" for name in api_index["root_exports"])
    modules = "\n".join(f"- `{name}`" for name in api_index["public_modules"])
    rules = "\n".join(f"- {rule['text']}" for rule in api_index["mutation_safety_rules"])
    link_prefix = "" if site_root else "docs/"
    documentation_suffix = "/" if site_root else ".md"
    recipes_path = "recipes/" if site_root else "docs/recipes/index.md"
    return f"""# IG Trading Library

> Safe, typed synchronous and asynchronous clients for IG REST and streaming APIs.

## Start here

- [Overview]({link_prefix}index{documentation_suffix})
- [Getting started]({link_prefix}getting-started{documentation_suffix})
- [Safety boundary]({link_prefix}guides/safety{documentation_suffix})
- [Conceptual guides]({link_prefix}guides/credentials{documentation_suffix})
- [Sync and async recipes]({recipes_path})
- [Machine-readable API index]({link_prefix}reference/public-api-index.json)
- [Human API reference]({link_prefix}reference/public-api{documentation_suffix})
- [Endpoint matrix]({link_prefix}reference/endpoint-matrix{documentation_suffix})

## Agent rules

- Read `docs/contracts/public-api.yml` when exact signatures, return types, or parameters matter.
- Treat `docs/reference/public-api-index.json` as generated discovery data,
  not an independent authority.
- The endpoint catalog records the library's maintained compatibility matrix;
  it is not a live verification of IG availability.
- `v1` through `v4` are generic, raw-payload facades. Do not infer a dedicated
  helper or a provider payload schema from a resource name.
- A `TradingPermit` protects live mutations on guarded typed resources and all
  raw version-facade mutations. It does not guard every possible `ResourceClient` instance.
- A mutation that raises `AmbiguousExecutionError` needs confirmation or
  deal-reference verification before another mutation.

## Supported root exports

{exports}

## Public modules

{modules}

## Safety rules

{rules}
"""


def render_api_index(api_index: Mapping[str, Any]) -> str:
    """Render stable JSON for a reviewable checked-in artifact."""
    return f"{json.dumps(api_index, indent=2, sort_keys=True)}\n"


def generate_documentation_indexes(project_root: Path) -> None:
    """Write all agent-facing indexes from the public contract and endpoint catalog."""
    contract = load_public_contract(project_root)
    api_index = build_api_index(contract, load_endpoint_index(project_root))
    _write_text(project_root / API_INDEX_PATH, render_api_index(api_index))
    _write_text(project_root / LLMS_PATH, build_llms_document(api_index, site_root=True))
    _write_text(project_root / ROOT_LLMS_PATH, build_llms_document(api_index, site_root=False))


def check_documentation_indexes(project_root: Path) -> None:
    """Fail when checked-in generated documentation is absent or out of date."""
    contract = load_public_contract(project_root)
    api_index = build_api_index(contract, load_endpoint_index(project_root))
    expected_outputs = {
        API_INDEX_PATH: render_api_index(api_index),
        LLMS_PATH: build_llms_document(api_index, site_root=True),
        ROOT_LLMS_PATH: build_llms_document(api_index, site_root=False),
    }
    stale_paths = [
        str(path)
        for path, expected_content in expected_outputs.items()
        if not (project_root / path).is_file()
        or (project_root / path).read_text(encoding="utf-8") != expected_content
    ]
    if stale_paths:
        formatted_paths = ", ".join(stale_paths)
        raise DocumentationIndexError(
            f"Generated documentation is stale: {formatted_paths}. "
            "Run `poetry run python scripts/generate_documentation_indexes.py`."
        )


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail instead of rewriting stale files."
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = _parse_arguments()
    project_root = Path(__file__).resolve().parents[1]
    if arguments.check:
        check_documentation_indexes(project_root)
        print("Generated documentation indexes are current.")
    else:
        generate_documentation_indexes(project_root)
        print("Generated documentation indexes.")
