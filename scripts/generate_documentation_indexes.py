"""Generate human and machine discovery artifacts from the v4 contract and manifest."""

from __future__ import annotations

import argparse
import inspect
import json
import sys
import types
from pathlib import Path
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints

import yaml
from pydantic import BaseModel

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
METHOD_DOCUMENTATION_PATH = ROOT / "docs/contracts/method-documentation.yml"


def _contract() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT_PATH.read_text(encoding="utf-8"))


def _method_documentation() -> dict[str, Any]:
    return yaml.safe_load(METHOD_DOCUMENTATION_PATH.read_text(encoding="utf-8"))


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


def _short_type_name(annotation: object) -> str:
    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        return " | ".join(_short_type_name(item) for item in get_args(annotation))
    if origin is Literal:
        return "Literal[" + ", ".join(repr(item) for item in get_args(annotation)) + "]"
    if origin is not None:
        arguments = get_args(annotation)
        name = getattr(origin, "__name__", str(origin).replace("typing.", ""))
        return f"{name}[{', '.join(_short_type_name(item) for item in arguments)}]"
    return getattr(annotation, "__name__", str(annotation).replace("typing.", ""))


def _parameter_rows(
    method: object, descriptions: dict[str, str]
) -> list[tuple[str, str, str, str]]:
    signature = inspect.signature(method)
    hints = get_type_hints(method)
    rows = []
    for parameter in tuple(signature.parameters.values())[1:]:
        required = (
            "required" if parameter.default is inspect.Parameter.empty else repr(parameter.default)
        )
        rows.append(
            (
                parameter.name,
                _short_type_name(hints[parameter.name]),
                required,
                descriptions[parameter.name],
            )
        )
    return rows


def _field_required(field: Any) -> str:
    if field.is_required():
        return "required"
    return f"default: `{field.default!r}`"


def _response_rows(
    model: type[BaseModel],
    *,
    prefix: str = "",
    seen: frozenset[type[BaseModel]] = frozenset(),
) -> list[tuple[str, str, str]]:
    if model in seen:
        return []
    rows = []
    for name, field in model.model_fields.items():
        annotation = field.annotation
        origin = get_origin(annotation)
        arguments = get_args(annotation)
        nested_annotation = annotation
        suffix = ""
        if origin in (Union, types.UnionType):
            nested_annotation = next(
                (item for item in arguments if item is not type(None)), annotation
            )
            origin = get_origin(nested_annotation)
            arguments = get_args(nested_annotation)
        if origin in (tuple, list) and arguments:
            nested_annotation = arguments[0]
            suffix = "[]"
        path = f"{prefix}.{name}{suffix}" if prefix else f"{name}{suffix}"
        rows.append((path, _short_type_name(annotation), _field_required(field)))
        if inspect.isclass(nested_annotation) and issubclass(nested_annotation, BaseModel):
            rows.extend(
                _response_rows(
                    nested_annotation,
                    prefix=path,
                    seen=seen | {model},
                )
            )
    return rows


def _method_reference(
    namespace: str,
    method_name: str,
    method: object,
    documentation: dict[str, Any],
) -> str:
    method_id = f"operations.{namespace}.{method_name}"
    contract = documentation["methods"][method_id]
    hints = get_type_hints(method)
    response_type = hints["return"]
    call_arguments = ", ".join(f"{name}={value}" for name, value in contract["arguments"].items())
    call = f"ig.operations.{namespace}.{method_name}({call_arguments})"
    lines = [
        f"## `ig.operations.{namespace}.{method_name}()`",
        "",
        contract["summary"],
        "",
        "Official IG reference: "
        f"[{contract['official_reference']}]({contract['official_reference']})",
        "",
        "### Signatures",
        "",
        f"- Sync: `{_public_signature(method)}`",
        "- Async: use the same parameters and `await` the result.",
        "",
        "### Parameters",
        "",
        "| Name | Type | Required/default | Description |",
        "| --- | --- | --- | --- |",
    ]
    for name, type_name, required, description in _parameter_rows(
        method, documentation["parameter_descriptions"]
    ):
        lines.append(f"| `{name}` | `{type_name}` | {required} | {description} |")
    lines.extend(
        [
            "",
            "### Sync example",
            "",
            "```python",
            f"result = {call}",
            "```",
            "",
            "### Async example",
            "",
            "```python",
            f"result = await {call}",
            "```",
            "",
            f"### Response shape: `{response_type.__name__}`",
            "",
            "| Field | Type | Required/default |",
            "| --- | --- | --- |",
        ]
    )
    for path, type_name, required in _response_rows(response_type):
        lines.append(f"| `{path}` | `{type_name}` | {required} |")
    lines.extend(
        [
            "",
            "### Response example",
            "",
            "```json",
            json.dumps(contract["response_example"], indent=2),
            "```",
            "",
            "### Limitations",
            "",
            *(f"- {limitation}" for limitation in contract["limitations"]),
            "",
            "### Exceptions",
            "",
            "| Exception | Trigger | Recovery |",
            "| --- | --- | --- |",
        ]
    )
    exception_definitions = documentation["exceptions"]
    for configured_exception in contract["exceptions"]:
        if isinstance(configured_exception, str):
            name = configured_exception
            override = {}
        else:
            name, override = next(iter(configured_exception.items()))
        definition = {**exception_definitions[name], **override}
        lines.append(f"| `{name}` | {definition['trigger']} | {definition['recovery']} |")
    return "\n".join(lines) + "\n"


def _method_reference_artifacts(
    contract: dict[str, Any], documentation: dict[str, Any]
) -> dict[Path, str]:
    artifacts = {}
    for method_id in documentation["methods"]:
        layer, namespace, method_name = method_id.split(".")
        if layer != "operations":
            raise ValueError(f"Unsupported method documentation layer: {layer}")
        sync_type = get_type_hints(Operations)[namespace]
        content = "# Markets operations\n\n" if namespace == "markets" else ""
        content += _method_reference(
            namespace,
            method_name,
            getattr(sync_type, method_name),
            documentation,
        )
        artifacts[ROOT / f"docs/reference/methods/{namespace}.md"] = content
    return artifacts


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
    method_documentation = _method_documentation()
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
    artifacts.update(_method_reference_artifacts(contract, method_documentation))
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
