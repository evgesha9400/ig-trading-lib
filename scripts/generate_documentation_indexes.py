"""Generate human and machine discovery artifacts from the v4 contract and manifest."""

from __future__ import annotations

import argparse
import dataclasses
import inspect
import json
import sys
import types
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
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
    if annotation is type(None):
        return "None"
    if annotation is Ellipsis:
        return "..."
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
) -> list[tuple[str, str, str, str, str]]:
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
                "-",
                descriptions[parameter.name],
            )
        )
        rows.extend(
            _nested_parameter_rows(
                hints[parameter.name],
                prefix=parameter.name,
                descriptions=descriptions,
            )
        )
    return rows


def _nested_parameter_rows(
    annotation: object,
    *,
    prefix: str,
    descriptions: dict[str, str],
) -> list[tuple[str, str, str, str, str]]:
    rows = []
    for model in _structured_types(annotation):
        if inspect.isclass(model) and issubclass(model, BaseModel):
            for name, field in model.model_fields.items():
                rows.append(
                    (
                        f"{prefix}.{name}",
                        _short_type_name(field.annotation),
                        _field_required(field),
                        _field_constraints(field),
                        descriptions[name],
                    )
                )
        elif dataclasses.is_dataclass(model):
            hints = get_type_hints(model)
            for field in dataclasses.fields(model):
                required = (
                    "required"
                    if field.default is dataclasses.MISSING
                    and field.default_factory is dataclasses.MISSING
                    else f"default: `{field.default!r}`"
                )
                rows.append(
                    (
                        f"{prefix}.{field.name}",
                        _short_type_name(hints[field.name]),
                        required,
                        "-",
                        descriptions[field.name],
                    )
                )
    return rows


def _structured_types(annotation: object) -> tuple[type[Any], ...]:
    if inspect.isclass(annotation) and (
        issubclass(annotation, BaseModel) or dataclasses.is_dataclass(annotation)
    ):
        return (annotation,)
    return tuple(
        candidate for argument in get_args(annotation) for candidate in _structured_types(argument)
    )


def _field_required(field: Any) -> str:
    if field.is_required():
        return "required"
    return f"default: `{field.default!r}`"


def _field_constraints(field: Any) -> str:
    labels = {
        "gt": ">",
        "ge": ">=",
        "lt": "<",
        "le": "<=",
        "min_length": "minimum length",
        "max_length": "maximum length",
        "pattern": "pattern",
    }
    constraints = []
    for metadata in field.metadata:
        for attribute, label in labels.items():
            if (value := getattr(metadata, attribute, None)) is not None:
                constraints.append(f"{label} `{value}`")
    return "; ".join(constraints) or "-"


def _response_rows(
    annotation: object,
    *,
    prefix: str = "",
    seen: frozenset[type[Any]] = frozenset(),
) -> list[tuple[str, str, str]]:
    annotation = _response_item_type(annotation)
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return _pydantic_response_rows(annotation, prefix=prefix, seen=seen)
    if dataclasses.is_dataclass(annotation):
        return _dataclass_response_rows(annotation, prefix=prefix, seen=seen)
    return []


def _pydantic_response_rows(
    model: type[BaseModel], *, prefix: str, seen: frozenset[type[Any]]
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
        rows.extend(
            _response_rows(
                nested_annotation,
                prefix=path,
                seen=seen | {model},
            )
        )
    return rows


def _dataclass_response_rows(
    model: type[Any], *, prefix: str, seen: frozenset[type[Any]]
) -> list[tuple[str, str, str]]:
    if model in seen:
        return []
    rows = []
    hints = get_type_hints(model)
    for field in dataclasses.fields(model):
        annotation = hints[field.name]
        path = f"{prefix}.{field.name}" if prefix else field.name
        required = "required" if field.default is dataclasses.MISSING else repr(field.default)
        rows.append((path, _short_type_name(annotation), required))
        rows.extend(_response_rows(annotation, prefix=path, seen=seen | {model}))
    return rows


def _response_item_type(annotation: object) -> object:
    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin in (Union, types.UnionType):
        return next((item for item in arguments if item is not type(None)), annotation)
    if origin is not None and arguments:
        return arguments[0]
    return annotation


_EXAMPLE_VALUES = {
    "account_id": "ABC123",
    "currency": "GBP",
    "currency_code": "GBP",
    "deal_id": "DIAAAABBBCCC",
    "deal_reference": "ABC123",
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "instrument_name": "EUR/USD",
    "market_id": "EURUSD",
    "market_status": "TRADEABLE",
    "name": "Example",
    "status": "ENABLED",
    "update_time": "12:34:56",
}


def _response_example(annotation: object, *, field_name: str = "value") -> object:
    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin in (Union, types.UnionType):
        return _response_example(
            next((item for item in arguments if item is not type(None)), type(None)),
            field_name=field_name,
        )
    if origin in (tuple, list, set, frozenset):
        return [_response_example(arguments[0], field_name=field_name)] if arguments else []
    if origin is not None and origin is not Literal:
        if origin is Mapping or issubclass(origin, Mapping):
            return {"BID": "1.0812"}
        return _response_example(arguments[0], field_name=field_name) if arguments else None
    if origin is Literal:
        return arguments[0]
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return {
            field.alias or name: _response_example(field.annotation, field_name=name)
            for name, field in annotation.model_fields.items()
        }
    if dataclasses.is_dataclass(annotation):
        hints = get_type_hints(annotation)
        return {
            field.name: _response_example(hints[field.name], field_name=field.name)
            for field in dataclasses.fields(annotation)
        }
    if inspect.isclass(annotation) and issubclass(annotation, Enum):
        return next(iter(annotation)).value
    if annotation in (datetime, date):
        return "2026-08-08T12:34:56Z"
    if annotation is Decimal:
        return "1.0"
    if annotation is bytes:
        return "<binary data>"
    if annotation is str:
        return _EXAMPLE_VALUES.get(field_name, "example")
    if annotation is bool:
        return True
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is type(None):
        return None
    return "example"


def _configured_items(
    contract: dict[str, Any], documentation: dict[str, Any], kind: str
) -> list[Any]:
    profile = contract.get(f"{kind[:-1]}_profile")
    items = list(documentation.get(f"{kind[:-1]}_profiles", {}).get(profile, []))
    if kind == "limitations":
        return [*items, *contract[kind]]
    configured_by_name = {
        item if isinstance(item, str) else next(iter(item)): item for item in items
    }
    for item in contract[kind]:
        name = item if isinstance(item, str) else next(iter(item))
        configured_by_name[name] = item
    return list(configured_by_name.values())


def _request_imports(method: object) -> list[str]:
    hints = get_type_hints(method)
    imports = []
    for parameter in tuple(inspect.signature(method).parameters.values())[1:]:
        for model in _structured_types(hints[parameter.name]):
            imports.append(f"from {model.__module__} import {model.__name__}")
    return sorted(set(imports))


def _example_call_lines(method: object, call: str, *, asynchronous: bool) -> list[str]:
    response = get_type_hints(method)["return"]
    origin_name = getattr(get_origin(response), "__name__", "")
    if origin_name == "Iterator":
        return [f"for update in {call}:", "    print(update)"]
    if origin_name == "AsyncIterator":
        return [f"async for update in {call}:", "    print(update)"]
    prefix = "await " if asynchronous and inspect.iscoroutinefunction(method) else ""
    if response is type(None):
        return [f"{prefix}{call}"]
    return [f"result = {prefix}{call}"]


def _method_reference(
    layer: str,
    namespace: str,
    method_name: str,
    sync_method: object,
    async_method: object,
    documentation: dict[str, Any],
) -> str:
    method_id = f"{layer}.{namespace}.{method_name}"
    contract = documentation["methods"][method_id]
    hints = get_type_hints(sync_method)
    response_type = hints["return"]
    call_arguments = ", ".join(f"{name}={value}" for name, value in contract["arguments"].items())
    call = f"ig.{layer}.{namespace}.{method_name}({call_arguments})"
    response_name = _short_type_name(response_type)
    imports = _request_imports(sync_method)
    lines = [
        f"## `ig.{layer}.{namespace}.{method_name}()`",
        "",
        contract["summary"],
        "",
        "Official IG reference: "
        f"[{contract['official_reference']}]({contract['official_reference']})",
        "",
        "### Signatures",
        "",
        f"- Sync: `{_public_signature(sync_method)}`",
        f"- Async: `{_public_signature(async_method)}`",
        "",
        "### Parameters",
        "",
        "| Name | Type | Required/default | Constraints | Description |",
        "| --- | --- | --- | --- | --- |",
    ]
    parameter_rows = _parameter_rows(sync_method, documentation["parameter_descriptions"])
    if parameter_rows:
        for name, type_name, required, constraints, description in parameter_rows:
            lines.append(
                f"| `{name}` | `{type_name}` | {required} | {constraints} | {description} |"
            )
    else:
        lines.append("| None | - | - | - | This method accepts no parameters. |")
    sync_example = [
        *imports,
        "" if imports else None,
        *_example_call_lines(sync_method, call, asynchronous=False),
    ]
    async_example = [
        *imports,
        "" if imports else None,
        *_example_call_lines(async_method, call, asynchronous=True),
    ]
    lines.extend(
        [
            "",
            "### Sync example",
            "",
            "```python",
            *(line for line in sync_example if line is not None),
            "```",
            "",
            "### Async example",
            "",
            "```python",
            *(line for line in async_example if line is not None),
            "```",
            "",
            f"### Response shape: `{response_name}`",
            "",
            "| Field | Type | Required/default |",
            "| --- | --- | --- |",
        ]
    )
    response_rows = _response_rows(response_type)
    if response_rows:
        for path, type_name, required in response_rows:
            lines.append(f"| `{path}` | `{type_name}` | {required} |")
    else:
        lines.append("| None | - | This method returns no structured response fields. |")
    response_example = contract.get("response_example", _response_example(response_type))
    limitations = _configured_items(contract, documentation, "limitations")
    exceptions = _configured_items(contract, documentation, "exceptions")
    lines.extend(
        [
            "",
            "### Response example",
            "",
            "```json",
            json.dumps(response_example, indent=2),
            "```",
            "",
            "### Limitations",
            "",
            *(f"- {limitation}" for limitation in limitations),
            "",
            "### Exceptions",
            "",
            "| Exception | Trigger | Recovery |",
            "| --- | --- | --- |",
        ]
    )
    exception_definitions = documentation["exceptions"]
    if not exceptions:
        lines.append("| None | No library-specific exception is expected. | No action required. |")
    for configured_exception in exceptions:
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
    pages: dict[str, dict[str, list[str]]] = {"operations": {}, "workflows": {}}
    for method_id in documentation["methods"]:
        layer, namespace, method_name = method_id.split(".")
        sync_root = Operations if layer == "operations" else Workflows
        async_root = AsyncOperations if layer == "operations" else AsyncWorkflows
        sync_type = get_type_hints(sync_root)[namespace]
        async_type = get_type_hints(async_root)[namespace]
        pages[layer].setdefault(namespace, []).append(
            _method_reference(
                layer,
                namespace,
                method_name,
                getattr(sync_type, method_name),
                getattr(async_type, method_name),
                documentation,
            )
        )
    artifacts = {}
    for layer, namespaces in pages.items():
        for namespace, methods in namespaces.items():
            artifacts[ROOT / f"docs/reference/{layer}/{namespace}.md"] = (
                "<!-- Generated from docs/contracts/method-documentation.yml "
                "and live Python types. -->\n\n"
                f"# {namespace.replace('_', ' ').title()} {layer}\n\n"
                "Examples assume an initialized synchronous or asynchronous client named `ig`.\n\n"
                + "\n".join(methods)
            )
        artifacts[ROOT / f"docs/reference/{layer}/index.md"] = _layer_reference_index(
            layer, namespaces
        )
    artifacts[ROOT / "docs/reference/index.md"] = _library_reference_index(pages)
    return artifacts


def _library_reference_index(pages: dict[str, dict[str, list[str]]]) -> str:
    return (
        "\n".join(
            [
                "<!-- Generated from docs/contracts/method-documentation.yml "
                "and live Python types. -->",
                "",
                "# Library reference",
                "",
                "The reference hierarchy mirrors the library interface. Choose the layer that "
                "matches "
                "your intent before choosing a namespace.",
                "",
                "| Layer | Mental model | Namespaces | Methods |",
                "| --- | --- | ---: | ---: |",
                f"| [Operations](operations/index.md) | One faithful typed IG call. | "
                f"{len(pages['operations'])} | {_method_count(pages['operations'])} |",
                f"| [Workflows](workflows/index.md) | A multi-operation journey composed from "
                f"operations. | {len(pages['workflows'])} | {_method_count(pages['workflows'])} |",
                "| [Types and exceptions](types-and-exceptions/index.md) | Objects constructed, "
                "returned, streamed, or raised by those two layers. | 4 categories | - |",
                "",
                "Every method documents its parameters, sync and async examples, recursive "
                "response "
                "shape, response example, limitations, and exceptions.",
                "",
                "- Parameter and response tables use public Python field names.",
                "- Nested request fields include Pydantic defaults and declared constraints.",
                "- `ValidationError` is `pydantic.ValidationError`; all other named failures are "
                "exported by `ig_trading_lib`.",
                "- Mutation workflows retain `DealConfirmationError.deal_reference`; reconcile it "
                "instead of replaying the mutation.",
            ]
        )
        + "\n"
    )


def _layer_reference_index(layer: str, pages: dict[str, list[str]]) -> str:
    mental_model = {
        "operations": (
            "Each operation is one faithful typed IG call with protocol details kept private."
        ),
        "workflows": "Each workflow is a multi-operation journey composed only from operations.",
    }
    index_lines = [
        "<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->",
        "",
        f"# {layer.title()}",
        "",
        mental_model[layer],
        "",
        "| Namespace | Methods |",
        "| --- | ---: |",
    ]
    for namespace, methods in pages.items():
        index_lines.append(
            f"| [{namespace.replace('_', ' ').title()}]({namespace}.md) | {len(methods)} |"
        )
    return "\n".join(index_lines) + "\n"


def _method_count(pages: dict[str, list[str]]) -> int:
    return sum(len(methods) for methods in pages.values())


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
