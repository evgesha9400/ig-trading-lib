"""Generate human and machine discovery artifacts from the v4 contract and manifest."""

from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path
from typing import Any, get_type_hints

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ig_trading_lib._protocol.manifest import OPERATION_MANIFEST  # noqa: E402
from ig_trading_lib.api import (  # noqa: E402
    AsyncOperations,
    AsyncWorkflows,
    Operations,
    Workflows,
)

CONTRACT_PATH = ROOT / "docs/contracts/public-api.yml"


def _contract() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT_PATH.read_text(encoding="utf-8"))


def _index(contract: dict[str, Any]) -> dict[str, Any]:
    operations = []
    for namespace, methods in contract["operations"].items():
        sync_type = get_type_hints(Operations)[namespace]
        async_type = get_type_hints(AsyncOperations)[namespace]
        operation_items = []
        for method, operation_id in methods.items():
            sync_method = getattr(sync_type, method)
            async_method = getattr(async_type, method)
            callable_contract = {
                "sync_signature": _public_signature(sync_method),
                "async_signature": _public_signature(async_method),
                "return_type": _type_name(get_type_hints(sync_method)["return"]),
            }
            if operation_id.startswith("streaming."):
                operation_items.append(
                    {"method": method, "operation_id": operation_id, **callable_contract}
                )
                continue
            spec = OPERATION_MANIFEST[operation_id]
            operation_items.append(
                {
                    "method": method,
                    "operation_id": operation_id,
                    **callable_contract,
                    "http_method": spec.method,
                    "path": spec.path,
                    "protocol_version": spec.version,
                    "mutation": spec.mutation,
                }
            )
        operations.append(
            {
                "namespace": namespace,
                "path": f"ig.operations.{namespace}",
                "operations": operation_items,
            }
        )
    workflows = []
    for namespace, methods in contract["workflows"].items():
        sync_type = get_type_hints(Workflows)[namespace]
        async_type = get_type_hints(AsyncWorkflows)[namespace]
        workflows.append(
            {
                "namespace": namespace,
                "path": f"ig.workflows.{namespace}",
                "methods": methods,
                "signatures": {
                    method: {
                        "sync": _public_signature(getattr(sync_type, method)),
                        "async": _public_signature(getattr(async_type, method)),
                        "return_type": _type_name(
                            get_type_hints(getattr(sync_type, method))["return"]
                        ),
                    }
                    for method in methods
                },
            }
        )
    return {
        "schema_version": 2,
        "canonical_sources": {
            "public_contract": "docs/contracts/public-api.yml",
            "operation_manifest": "src/ig_trading_lib/_protocol/manifest.py",
            "composition_root": "src/ig_trading_lib/api.py",
        },
        "entry_points": [
            {"name": "IG", "execution": "sync", "layers": ["operations", "workflows"]},
            {"name": "AsyncIG", "execution": "async", "layers": ["operations", "workflows"]},
        ],
        "mental_model": contract["mental_model"],
        "root_exports": contract["root_exports"],
        "public_modules": contract["public_modules"],
        "operations": operations,
        "workflows": workflows,
    }


def _public_signature(callable_object: object) -> str:
    signature = inspect.signature(callable_object)
    parameters = tuple(signature.parameters.values())[1:]
    return str(signature.replace(parameters=parameters))


def _type_name(annotation: object) -> str:
    if inspect.isclass(annotation):
        return f"{annotation.__module__}.{annotation.__qualname__}"
    return str(annotation).replace("typing.", "")


def _entry_points(index: dict[str, Any]) -> str:
    lines = [
        "<!-- Generated from docs/contracts/public-api.yml and src/ig_trading_lib/api.py. -->",
        "",
        "| Root | Execution | Faithful layer | Journey layer |",
        "| --- | --- | --- | --- |",
    ]
    for item in index["entry_points"]:
        lines.append(
            f"| `{item['name']}(config)` | {item['execution']} | `.operations` | `.workflows` |"
        )
    lines.extend(
        [
            "",
            "| Namespace | Purpose |",
            "| --- | --- |",
            "| `ig.operations.<resource>` | One typed IG provider operation. |",
            "| `ig.workflows.<journey>` | A safe sequence composed from operations. |",
        ]
    )
    return "\n".join(lines) + "\n"


def _llms(index: dict[str, Any]) -> str:
    lines = [
        "# IG Trading Library v4",
        "",
        "> Typed IG operations and safe trading workflows for Python.",
        "",
        "## Mental model",
        "",
        "- Construct `IG(config)` or `AsyncIG(config)`.",
        "- Use `.operations` for faithful typed IG calls.",
        "- Use `.workflows` for composed journeys.",
        "- Never select HTTP paths or provider protocol versions.",
        "- Pass `TradingPermit()` before live mutations.",
        "- Treat `AmbiguousExecutionError` as an unknown mutation outcome; "
        "reconcile before retrying.",
        "",
        "## Operation paths",
        "",
    ]
    for namespace in index["operations"]:
        methods = ", ".join(item["method"] for item in namespace["operations"])
        lines.append(f"- `{namespace['path']}`: {methods}")
    lines.extend(["", "## Workflow paths", ""])
    for namespace in index["workflows"]:
        lines.append(f"- `{namespace['path']}`: {', '.join(namespace['methods'])}")
    lines.extend(
        [
            "",
            "## Canonical machine index",
            "",
            "- `docs/reference/public-api-index.json`",
        ]
    )
    return "\n".join(lines) + "\n"


REFERENCE_GROUPS = {
    "login": {"session"},
    "account": {"accounts", "activity", "transactions"},
    "markets": {"categories", "markets", "prices"},
    "watchlists": {"watchlists"},
    "client-sentiment": {"client_sentiment"},
    "indicative-costs-and-charges": {"indicative_costs"},
    "dealing": {"confirmations", "positions", "working_orders", "repeat_dealing_window"},
    "general": {"applications"},
}


def _reference_fragment(index: dict[str, Any], group: str) -> str:
    allowed = REFERENCE_GROUPS[group]
    lines = [
        "<!-- Generated from src/ig_trading_lib/_protocol/manifest.py. -->",
        "",
        "| Python operation | IG request | Protocol version |",
        "| --- | --- | ---: |",
    ]
    for namespace in index["operations"]:
        if namespace["namespace"] not in allowed:
            continue
        for operation in namespace["operations"]:
            if "http_method" not in operation:
                continue
            lines.append(
                f"| `{namespace['path']}.{operation['method']}()` | "
                f"`{operation['http_method']} {operation['path']}` | "
                f"{operation['protocol_version']} |"
            )
    return "\n".join(lines) + "\n"


def _artifacts() -> dict[Path, str]:
    contract = _contract()
    index = _index(contract)
    index_text = json.dumps(index, indent=2, sort_keys=True) + "\n"
    llms = _llms(index)
    artifacts = {
        ROOT / "docs/reference/public-api-index.json": index_text,
        ROOT / "docs/reference/.client-entry-points.md": _entry_points(index),
        ROOT / "docs/llms.txt": llms,
        ROOT / "llms.txt": llms,
    }
    for group in REFERENCE_GROUPS:
        artifacts[ROOT / f"docs/rest-api-reference/.{group}-endpoints.md"] = _reference_fragment(
            index, group
        )
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale: list[str] = []
    for path, content in _artifacts().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if stale:
        print("Generated documentation artifacts are stale:")
        for path in stale:
            print(f"- {path}")
        return 1
    print("Generated documentation indexes are current." if args.check else "Generated docs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
