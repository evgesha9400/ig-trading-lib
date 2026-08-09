"""Generate agent-facing indexes from the checked public API contract."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

API_INDEX_PATH = Path("docs/reference/public-api-index.json")
CLIENT_ENTRY_POINTS_PATH = Path("docs/reference/.client-entry-points.md")
CONTRACT_PATH = Path("docs/contracts/public-api.yml")
ENDPOINT_CATALOG_PATH = Path("src/ig_trading_lib/endpoint_catalog.py")
CLIENT_SOURCE_PATH = Path("src/ig_trading_lib/api.py")
LLMS_PATH = Path("docs/llms.txt")
REST_REFERENCE_DIRECTORY = Path("docs/rest-api-reference")
ROOT_LLMS_PATH = Path("llms.txt")
AGENT_INDEX_SCHEMA_VERSION = 4
CLIENT_ENTRY_POINT_NAMES = ("IG", "AsyncIG")
CLIENT_MODULE_NAME = "ig_trading_lib.api"


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


def load_endpoint_reference(
    project_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Project the maintained endpoint catalog and official section order into JSON-safe data."""
    source_path = str(project_root / "src")
    sys.path.insert(0, source_path)
    try:
        from ig_trading_lib.endpoint_catalog import DOCUMENTED_ENDPOINTS, REST_REFERENCE_SECTIONS

        return (
            [
                {
                    "name": endpoint.name,
                    "path_template": endpoint.path_template,
                    "method": endpoint.method,
                    "category": endpoint.category,
                }
                for endpoint in DOCUMENTED_ENDPOINTS
            ],
            [{"slug": section.slug, "title": section.title} for section in REST_REFERENCE_SECTIONS],
        )
    finally:
        sys.path.remove(source_path)


def build_api_index(
    project_root: Path,
    contract: Mapping[str, Any],
    endpoints: list[dict[str, Any]],
    rest_reference_sections: list[dict[str, str]],
) -> dict[str, Any]:
    """Return the machine-readable projection without hand-maintained signatures."""
    entry_points = load_client_entry_points(project_root, contract)
    return {
        "schema_version": AGENT_INDEX_SCHEMA_VERSION,
        "contract_schema_version": contract["schema_version"],
        "generated_from": {
            "contract": str(CONTRACT_PATH),
            "endpoint_catalog": str(ENDPOINT_CATALOG_PATH),
            "client_source": str(CLIENT_SOURCE_PATH),
        },
        "root_exports": contract["root_exports"],
        "entry_points": entry_points,
        "complete_reference": {
            "classes": contract["classes"],
            "functions": contract["functions"],
            "exceptions": contract["exceptions"],
            "pydantic_fields": contract["pydantic_fields"],
        },
        "examples": contract["examples"],
        "mutation_safety_rules": contract["mutation_safety_rules"],
        "rest_reference": {
            "directory": contract["endpoint_reference"],
            "sections": rest_reference_sections,
        },
        "endpoints": endpoints,
    }


def load_client_entry_points(project_root: Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    """Project the source-owned client entry points and their service namespaces."""
    client_module = _load_client_module(project_root)
    class_contracts = _class_contracts(contract)
    class_references = _class_references_by_short_name(class_contracts)
    return {
        entry_point_name: _build_client_entry_point(
            client_module,
            entry_point_name,
            class_contracts,
            class_references,
        )
        for entry_point_name in CLIENT_ENTRY_POINT_NAMES
    }


def _load_client_module(project_root: Path) -> ast.Module:
    """Load the client source as syntax data without importing application code."""
    source_path = project_root / CLIENT_SOURCE_PATH
    if not source_path.is_file():
        raise DocumentationIndexError(f"Client source is missing: {CLIENT_SOURCE_PATH}")
    return ast.parse(source_path.read_text(encoding="utf-8"))


def _class_contracts(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the checked class contract or fail before producing partial documentation."""
    class_contracts = contract.get("classes")
    if not isinstance(class_contracts, Mapping):
        raise DocumentationIndexError("Public API contract must contain class declarations.")
    return class_contracts


def _class_references_by_short_name(class_contracts: Mapping[str, Any]) -> dict[str, str]:
    """Resolve source class names to their unambiguous checked contract entries."""
    references: dict[str, str] = {}
    for qualified_name in class_contracts:
        if not isinstance(qualified_name, str):
            raise DocumentationIndexError("Class contract names must be strings.")
        short_name = qualified_name.rsplit(".", maxsplit=1)[-1]
        if short_name in references:
            raise DocumentationIndexError(f"Class contract name is ambiguous: {short_name}")
        references[short_name] = qualified_name
    return references


def _build_client_entry_point(
    client_module: ast.Module,
    entry_point_name: str,
    class_contracts: Mapping[str, Any],
    class_references: Mapping[str, str],
) -> dict[str, Any]:
    """Build one constructible client and its source-owned service access paths."""
    client_class = _find_class(client_module, entry_point_name)
    constructor = _find_constructor(client_class)
    qualified_name = f"{CLIENT_MODULE_NAME}.{entry_point_name}"
    contract_entry = class_contracts.get(qualified_name)
    if not isinstance(contract_entry, Mapping):
        raise DocumentationIndexError(f"Client contract is missing: {qualified_name}")
    contract_constructor = contract_entry.get("constructor")
    if not isinstance(contract_constructor, Mapping):
        raise DocumentationIndexError(f"Client constructor contract is missing: {qualified_name}")
    return {
        "import": f"from ig_trading_lib import {entry_point_name}",
        "reference": qualified_name,
        "signature": _format_constructor_signature(entry_point_name, constructor),
        "constructor": contract_constructor,
        "namespaces": _client_namespaces(
            client_module,
            constructor,
            class_contracts,
            class_references,
        ),
    }


def _find_class(module: ast.Module, class_name: str) -> ast.ClassDef:
    """Find one declared client class in its source module."""
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise DocumentationIndexError(f"Client class is missing: {class_name}")


def _find_constructor(class_node: ast.ClassDef) -> ast.FunctionDef:
    """Find the explicit constructor that defines client-owned namespaces."""
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and node.name == "__init__":
            return node
    raise DocumentationIndexError(f"Client constructor is missing: {class_node.name}")


def _format_constructor_signature(class_name: str, constructor: ast.FunctionDef) -> str:
    """Render the exact source-level constructor signature for a generated docs block."""
    arguments = constructor.args
    positional = [*arguments.posonlyargs, *arguments.args]
    positional_defaults = [None] * (len(positional) - len(arguments.defaults)) + list(
        arguments.defaults
    )
    rendered = [
        _format_parameter(argument, default)
        for argument, default in zip(positional, positional_defaults, strict=True)
        if argument.arg != "self"
    ]
    if arguments.posonlyargs:
        rendered.insert(len(arguments.posonlyargs), "/")
    if arguments.vararg is not None:
        rendered.append(f"*{_format_parameter(arguments.vararg, None)}")
    elif arguments.kwonlyargs:
        rendered.append("*")
    rendered.extend(
        _format_parameter(argument, default)
        for argument, default in zip(arguments.kwonlyargs, arguments.kw_defaults, strict=True)
    )
    if arguments.kwarg is not None:
        rendered.append(f"**{_format_parameter(arguments.kwarg, None)}")
    return f"{class_name}({', '.join(rendered)})"


def _format_parameter(argument: ast.arg, default: ast.expr | None) -> str:
    """Render one typed parameter from a parsed source signature."""
    annotation = f": {ast.unparse(argument.annotation)}" if argument.annotation else ""
    default_value = f" = {ast.unparse(default)}" if default is not None else ""
    return f"{argument.arg}{annotation}{default_value}"


def _client_namespaces(
    client_module: ast.Module,
    constructor: ast.FunctionDef,
    class_contracts: Mapping[str, Any],
    class_references: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Return every public client attribute assigned a checked service object."""
    namespaces = [
        _namespace_from_assignment(
            client_module,
            statement,
            class_contracts,
            class_references,
        )
        for statement in constructor.body
        if _is_client_namespace_assignment(statement)
    ]
    names = [namespace["name"] for namespace in namespaces]
    if len(names) != len(set(names)):
        raise DocumentationIndexError("Client namespaces must have unique names.")
    return namespaces


def _is_client_namespace_assignment(statement: ast.stmt) -> bool:
    """Identify a public self attribute initialised from a service-class call."""
    return (
        isinstance(statement, ast.Assign)
        and len(statement.targets) == 1
        and isinstance(statement.targets[0], ast.Attribute)
        and isinstance(statement.targets[0].value, ast.Name)
        and statement.targets[0].value.id == "self"
        and not statement.targets[0].attr.startswith("_")
        and isinstance(statement.value, ast.Call)
        and isinstance(statement.value.func, ast.Name)
    )


def _namespace_from_assignment(
    client_module: ast.Module,
    assignment: ast.Assign,
    class_contracts: Mapping[str, Any],
    class_references: Mapping[str, str],
) -> dict[str, Any]:
    """Project one client namespace to its contract-derived operation descriptions."""
    target = assignment.targets[0]
    call = assignment.value
    if not isinstance(target, ast.Attribute) or not isinstance(call, ast.Call):
        raise DocumentationIndexError("Invalid client namespace assignment.")
    if not isinstance(call.func, ast.Name):
        raise DocumentationIndexError("Client namespace must use a named service class.")
    reference = class_references.get(call.func.id)
    if reference is None:
        raise DocumentationIndexError(
            f"Client namespace has no checked class contract: {call.func.id}"
        )
    namespace_class = _find_class(client_module, call.func.id)
    return {
        "name": target.attr,
        "reference": reference,
        "groups": _namespace_groups(namespace_class, class_contracts, class_references),
    }


def _namespace_groups(
    namespace_class: ast.ClassDef,
    class_contracts: Mapping[str, Any],
    class_references: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Project one two-layer namespace into its typed operation or workflow groups."""
    groups: list[dict[str, Any]] = []
    for statement in namespace_class.body:
        if not isinstance(statement, ast.AnnAssign) or not isinstance(statement.target, ast.Name):
            continue
        group_type = ast.unparse(statement.annotation).split("[", maxsplit=1)[0]
        reference = class_references.get(group_type)
        if reference is None:
            raise DocumentationIndexError(
                f"Namespace group has no checked class contract: {group_type}"
            )
        declaration = class_contracts[reference]
        if not isinstance(declaration, Mapping) or not isinstance(
            declaration.get("methods"), Mapping
        ):
            raise DocumentationIndexError(f"Namespace group contract is incomplete: {reference}")
        groups.append(
            {
                "name": statement.target.id,
                "reference": reference,
                "operations": declaration["methods"],
            }
        )
    return groups


def build_llms_document(api_index: Mapping[str, Any], *, site_root: bool) -> str:
    """Create a compact discovery document pointing agents to canonical artifacts."""
    exports = "\n".join(f"- `{name}`" for name in api_index["root_exports"])
    entry_points = "\n".join(
        f"- `{entry_point['import']}` — `{entry_point['signature']}`"
        for entry_point in api_index["entry_points"].values()
    )
    rules = "\n".join(f"- {rule['text']}" for rule in api_index["mutation_safety_rules"])
    link_prefix = "" if site_root else "docs/"
    documentation_suffix = "/" if site_root else ".md"
    recipes_path = "recipes/" if site_root else "docs/recipes/index.md"
    return f"""# IG Trading Library

> Safe, typed synchronous and asynchronous clients for IG REST and streaming APIs.

## Start here

- [Overview]({link_prefix}index{documentation_suffix})
- [Getting started]({link_prefix}getting-started{documentation_suffix})
- [Trading safety]({link_prefix}api-guide/trading-safety{documentation_suffix})
- [API guide]({link_prefix}api-guide/authentication-and-authorisation{documentation_suffix})
- [REST API reference]({link_prefix}rest-api-reference/account{documentation_suffix})
- [Sync and async recipes]({recipes_path})
- [Machine-readable API index]({link_prefix}reference/public-api-index.json)
- [Human API reference]({link_prefix}reference/public-api{documentation_suffix})

## Agent rules

- Read `docs/contracts/public-api.yml` when exact signatures, return types, or parameters matter.
- Treat `docs/reference/public-api-index.json` as generated discovery data,
  not an independent authority.
- The endpoint catalog records the library's maintained compatibility matrix;
  it is not a live verification of IG availability.
- Construct `IG` or `AsyncIG` only through the package root.
- Use `ig.operations` for one provider operation and `ig.workflows` for composition.
- A `TradingPermit` protects live mutations before any provider request is sent.
- A mutation that raises `AmbiguousExecutionError` needs confirmation or
  deal-reference verification before another mutation.

## Supported root exports

{exports}

## Service entry points

{entry_points}

## Safety rules

{rules}
"""


def build_client_entry_points_document(api_index: Mapping[str, Any]) -> str:
    """Render compact human construction guidance from the generated agent index."""
    entry_points = api_index["entry_points"]
    synchronous = entry_points["IG"]
    asynchronous = entry_points["AsyncIG"]
    sections = [
        "<!-- Generated from docs/contracts/public-api.yml and src/ig_trading_lib/api.py. -->",
        (
            "Construct one composition root from the package. Use `operations` for faithful IG "
            "calls and `workflows` for composed journeys."
        ),
        _render_entry_point(synchronous),
        _render_entry_point(asynchronous),
        _render_client_namespaces(synchronous, asynchronous),
    ]
    return "\n\n".join(sections) + "\n"


def _render_client_namespaces(
    synchronous: Mapping[str, Any], asynchronous: Mapping[str, Any]
) -> str:
    """Render the matching sync and async client-owned service namespaces as one table."""
    rows = [
        "### Two-layer public paths",
        "",
        "| Path | `IG` type | `AsyncIG` type |",
        "| --- | --- | --- |",
    ]
    asynchronous_namespaces = {
        namespace["name"]: namespace for namespace in asynchronous["namespaces"]
    }
    for namespace in synchronous["namespaces"]:
        namespace_name = namespace["name"]
        asynchronous_namespace = asynchronous_namespaces.get(namespace_name)
        if asynchronous_namespace is None:
            raise DocumentationIndexError(
                f"Async client is missing public namespace: {namespace_name}"
            )
        asynchronous_groups = {group["name"]: group for group in asynchronous_namespace["groups"]}
        for group in namespace["groups"]:
            group_name = group["name"]
            asynchronous_group = asynchronous_groups.get(group_name)
            if asynchronous_group is None:
                raise DocumentationIndexError(
                    f"Async namespace is missing group: {namespace_name}.{group_name}"
                )
            rows.append(
                f"| `ig.{namespace_name}.{group_name}` | "
                f"`{_short_reference(group['reference'])}` | "
                f"`{_short_reference(asynchronous_group['reference'])}` |"
            )
    return "\n".join(rows)


def _render_entry_point(entry_point: Mapping[str, Any]) -> str:
    """Render one application-client signature and its checked parameter descriptions."""
    constructor = entry_point["constructor"]
    parameters = constructor["parameters"]
    if not isinstance(parameters, list):
        raise DocumentationIndexError("Client constructor parameters must be a list.")
    rows = ["| Parameter | Type | Description |", "| --- | --- | --- |"]
    for parameter in parameters:
        if not isinstance(parameter, Mapping):
            raise DocumentationIndexError("Client constructor parameter is invalid.")
        rows.append(
            f"| `{parameter['name']}` | `{parameter['type']}` | {parameter['description']} |"
        )
    return "\n\n".join(
        [
            f"### `{entry_point['signature']}`",
            f"`{entry_point['import']}`",
            "\n".join(rows),
        ]
    )


def _short_reference(reference: object) -> str:
    """Format a fully-qualified contract reference for compact human documentation."""
    if not isinstance(reference, str):
        raise DocumentationIndexError("Contract reference must be a string.")
    return reference.rsplit(".", maxsplit=1)[-1]


def render_api_index(api_index: Mapping[str, Any]) -> str:
    """Render stable JSON for a reviewable checked-in artifact."""
    return f"{json.dumps(api_index, indent=2, sort_keys=True)}\n"


def generate_documentation_indexes(project_root: Path) -> None:
    """Write all agent-facing indexes from the public contract and endpoint catalog."""
    contract = load_public_contract(project_root)
    endpoints, sections = load_endpoint_reference(project_root)
    api_index = build_api_index(project_root, contract, endpoints, sections)
    _write_text(project_root / API_INDEX_PATH, render_api_index(api_index))
    _write_text(
        project_root / CLIENT_ENTRY_POINTS_PATH,
        build_client_entry_points_document(api_index),
    )
    _write_text(project_root / LLMS_PATH, build_llms_document(api_index, site_root=True))
    _write_text(project_root / ROOT_LLMS_PATH, build_llms_document(api_index, site_root=False))
    for section in sections:
        _write_text(
            project_root / _rest_reference_table_path(section["slug"]),
            build_rest_reference_table(section, endpoints),
        )


def check_documentation_indexes(project_root: Path) -> None:
    """Fail when checked-in generated documentation is absent or out of date."""
    contract = load_public_contract(project_root)
    endpoints, sections = load_endpoint_reference(project_root)
    api_index = build_api_index(project_root, contract, endpoints, sections)
    expected_outputs = {
        API_INDEX_PATH: render_api_index(api_index),
        CLIENT_ENTRY_POINTS_PATH: build_client_entry_points_document(api_index),
        LLMS_PATH: build_llms_document(api_index, site_root=True),
        ROOT_LLMS_PATH: build_llms_document(api_index, site_root=False),
        **{
            _rest_reference_table_path(section["slug"]): build_rest_reference_table(
                section, endpoints
            )
            for section in sections
        },
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


def build_rest_reference_table(section: Mapping[str, str], endpoints: list[dict[str, Any]]) -> str:
    """Render one official IG REST category from the maintained endpoint catalog."""
    rows = [
        "<!-- Generated from src/ig_trading_lib/endpoint_catalog.py. -->",
        "## Endpoint compatibility",
        "",
        "| Operation | Method | Path |",
        "| --- | --- | --- |",
    ]
    for endpoint in endpoints:
        if endpoint["category"] != section["slug"]:
            continue
        rows.append(
            f"| {endpoint['name']} | {endpoint['method']} | `{endpoint['path_template']}` |"
        )
    return "\n".join(rows) + "\n"


def _rest_reference_table_path(section_slug: str) -> Path:
    """Return the generated hidden endpoint table path for one reference section."""
    return REST_REFERENCE_DIRECTORY / f".{section_slug}-endpoints.md"


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
