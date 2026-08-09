from __future__ import annotations

import ast
import dataclasses
import inspect
import json
import re
import tomllib
import types
from pathlib import Path
from typing import Union, get_args, get_origin, get_type_hints

import yaml
from pydantic import BaseModel

from ig_trading_lib.api import Operations, Workflows

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


def test_generated_market_search_reference_is_a_complete_method_contract() -> None:
    reference = (PROJECT_ROOT / "docs" / "reference" / "operations" / "markets.md").read_text(
        encoding="utf-8"
    )

    assert "## `ig.operations.markets.search()`" in reference
    assert "### Parameters" in reference
    assert "| `search_term` | `str` | required |" in reference
    assert "### Sync example" in reference
    assert 'ig.operations.markets.search(search_term="EUR/USD")' in reference
    assert "### Async example" in reference
    assert 'await ig.operations.markets.search(search_term="EUR/USD")' in reference
    assert "### Response shape: `MarketSearchResponse`" in reference
    assert "| `markets[].epic` | `str` | required |" in reference
    assert "### Response example" in reference
    assert '"epic": "CS.D.EURUSD.CFD.IP"' in reference
    assert "### Limitations" in reference
    assert "### Exceptions" in reference
    assert "| `AuthenticationError` |" in reference
    assert "| `ValueError` | `search_term` is empty" in reference
    assert "https://labs.ig.com/reference/markets-searchterm.html" in reference


def test_library_reference_hierarchy_matches_the_public_mental_model() -> None:
    reference = PROJECT_ROOT / "docs" / "reference"

    assert not (reference / "methods").exists()
    assert (reference / "index.md").exists()
    assert {path.stem for path in (reference / "operations").glob("*.md")} == {
        "accounts",
        "activity",
        "applications",
        "categories",
        "client_sentiment",
        "confirmations",
        "index",
        "indicative_costs",
        "markets",
        "positions",
        "prices",
        "repeat_dealing_window",
        "session",
        "streaming",
        "transactions",
        "watchlists",
        "working_orders",
    }
    assert {path.stem for path in (reference / "workflows").glob("*.md")} == {
        "discovery",
        "index",
        "portfolio",
        "positions",
        "working_orders",
    }

    navigation = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "- Operations:" in navigation
    assert "- Workflows:" in navigation
    assert "reference/operations/index.md" in navigation
    assert "reference/workflows/index.md" in navigation


def test_every_operation_and_workflow_has_complete_generated_documentation() -> None:
    public_contract = yaml.safe_load(
        (PROJECT_ROOT / "docs" / "contracts" / "public-api.yml").read_text(encoding="utf-8")
    )
    method_contract = yaml.safe_load(
        (PROJECT_ROOT / "docs" / "contracts" / "method-documentation.yml").read_text(
            encoding="utf-8"
        )
    )
    expected_methods = _public_methods(public_contract)

    assert len(expected_methods) == 59
    assert set(method_contract["methods"]) == set(expected_methods)
    for method_id, method in expected_methods.items():
        documented = method_contract["methods"][method_id]
        parameters = tuple(inspect.signature(method).parameters.values())[1:]
        assert documented["summary"]
        assert documented["official_reference"].startswith("https://labs.ig.com/")
        assert set(documented["arguments"]) == {parameter.name for parameter in parameters}
        assert documented["limitations"] or documented.get("limitation_profile")
        assert documented["exceptions"] or documented.get("exception_profile")
        assert all(
            name in method_contract["parameter_descriptions"]
            for name in _documented_parameter_names(method)
        )

        layer, namespace, method_name = method_id.split(".")
        page = (PROJECT_ROOT / "docs" / "reference" / layer / f"{namespace}.md").read_text(
            encoding="utf-8"
        )
        assert f"## `ig.{layer}.{namespace}.{method_name}()`" in page
        assert "### Parameters" in page
        assert "### Sync example" in page
        assert "### Async example" in page
        assert "### Response shape" in page
        assert "### Response example" in page
        assert "### Limitations" in page
        assert "### Exceptions" in page
        assert f"ig.{layer}.{namespace}.{method_name}(" in page
        for parameter_path in _documented_parameter_paths(method):
            assert f"| `{parameter_path}` |" in page
        for response_path in _response_paths(get_type_hints(method)["return"]):
            assert f"| `{response_path}` |" in page
        for exception_name in _method_exception_names(documented, method_contract):
            assert exception_name in method_contract["exceptions"]
            assert f"| `{exception_name}` |" in page


def test_every_generated_method_example_is_valid_python_and_json() -> None:
    pages = [
        path.read_text(encoding="utf-8")
        for layer in ("operations", "workflows")
        for path in (PROJECT_ROOT / "docs" / "reference" / layer).glob("*.md")
        if path.name != "index.md"
    ]
    python_examples = re.findall(r"```python\n(.*?)\n```", "\n".join(pages), re.DOTALL)
    response_examples = re.findall(r"```json\n(.*?)\n```", "\n".join(pages), re.DOTALL)

    assert len(python_examples) == 59 * 2
    assert len(response_examples) == 59
    for example in python_examples:
        ast.parse(example)
    for example in response_examples:
        json.loads(example)


def _public_methods(contract: dict[str, object]) -> dict[str, object]:
    methods = {}
    for layer, root in (("operations", Operations), ("workflows", Workflows)):
        namespaces = contract[layer]
        assert isinstance(namespaces, dict)
        for namespace, configured_methods in namespaces.items():
            namespace_type = get_type_hints(root)[namespace]
            names = (
                configured_methods
                if isinstance(configured_methods, list)
                else configured_methods.keys()
            )
            for name in names:
                methods[f"{layer}.{namespace}.{name}"] = getattr(namespace_type, name)
    return methods


def _documented_parameter_names(method: object) -> set[str]:
    names = set()
    hints = get_type_hints(method)
    for parameter in tuple(inspect.signature(method).parameters.values())[1:]:
        names.add(parameter.name)
        for candidate in (hints[parameter.name], *get_args(hints[parameter.name])):
            if inspect.isclass(candidate) and issubclass(candidate, BaseModel):
                names.update(candidate.model_fields)
    return names


def _documented_parameter_paths(method: object) -> set[str]:
    paths = set()
    hints = get_type_hints(method)
    for parameter in tuple(inspect.signature(method).parameters.values())[1:]:
        paths.add(parameter.name)
        for candidate in _structured_types(hints[parameter.name]):
            fields = (
                candidate.model_fields
                if inspect.isclass(candidate) and issubclass(candidate, BaseModel)
                else {field.name: field for field in dataclasses.fields(candidate)}
            )
            paths.update(f"{parameter.name}.{name}" for name in fields)
    return paths


def _structured_types(annotation: object) -> tuple[type[object], ...]:
    if inspect.isclass(annotation) and (
        issubclass(annotation, BaseModel) or dataclasses.is_dataclass(annotation)
    ):
        return (annotation,)
    return tuple(
        candidate for argument in get_args(annotation) for candidate in _structured_types(argument)
    )


def _response_paths(
    annotation: object,
    *,
    prefix: str = "",
    seen: frozenset[type[object]] = frozenset(),
) -> set[str]:
    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin in (Union, types.UnionType):
        annotation = next((item for item in arguments if item is not type(None)), annotation)
        origin = get_origin(annotation)
        arguments = get_args(annotation)
    if origin is not None and arguments:
        annotation = arguments[0]
    if not inspect.isclass(annotation) or annotation in seen:
        return set()
    if issubclass(annotation, BaseModel):
        fields = {name: field.annotation for name, field in annotation.model_fields.items()}
    elif dataclasses.is_dataclass(annotation):
        hints = get_type_hints(annotation)
        fields = {field.name: hints[field.name] for field in dataclasses.fields(annotation)}
    else:
        return set()
    paths = set()
    for name, field_annotation in fields.items():
        field_origin = get_origin(field_annotation)
        suffix = "[]" if field_origin in (tuple, list) else ""
        path = f"{prefix}.{name}{suffix}" if prefix else f"{name}{suffix}"
        paths.add(path)
        paths.update(_response_paths(field_annotation, prefix=path, seen=seen | {annotation}))
    return paths


def _method_exception_names(method: dict[str, object], contract: dict[str, object]) -> set[str]:
    profiles = contract["exception_profiles"]
    assert isinstance(profiles, dict)
    names = set(profiles[method["exception_profile"]])
    configured = method["exceptions"]
    assert isinstance(configured, list)
    names.update(item if isinstance(item, str) else next(iter(item)) for item in configured)
    return names
