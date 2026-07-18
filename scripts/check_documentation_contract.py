"""Fail documentation builds when the declared public contract drifts from source."""

from __future__ import annotations

import ast
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "library_id",
        "title",
        "pitch",
        "repository",
        "repository_url",
        "package",
        "status",
        "categories",
    }
)
MANIFEST_VALUES = {
    "schema_version": 1,
    "library_id": "ig-trading-lib",
    "title": "IG Trading Library",
    "pitch": "Safe, typed synchronous and asynchronous IG REST and streaming clients.",
    "repository": "evgesha9400/ig-trading-lib",
    "repository_url": "https://github.com/evgesha9400/ig-trading-lib",
    "package": {"name": "ig-trading-lib"},
    "status": "published",
    "categories": ["brokerage", "trading"],
}
SOURCE_MODULES = (
    "ig_trading_lib.client",
    "ig_trading_lib.core",
    "ig_trading_lib.endpoint_catalog",
    "ig_trading_lib.errors",
    "ig_trading_lib.models",
    "ig_trading_lib.services",
    "ig_trading_lib.async_services",
    "ig_trading_lib.streaming",
    "ig_trading_lib.versions",
)
PUBLIC_API_REFERENCE_PATH = Path("docs/reference/public-api.md")
KNOWN_EXCEPTIONS = frozenset(
    {
        "AmbiguousExecutionError",
        "AuthenticationError",
        "AuthorizationError",
        "IGError",
        "LiveTradingPermissionError",
        "ProviderRejectionError",
        "RateLimitError",
        "ResourceNotFoundError",
        "StreamingDataLossError",
        "StreamingSubscriptionError",
        "TransportError",
    }
)


class DocumentationContractError(ValueError):
    """Raised when release documentation does not cover the supported API."""


@dataclass(frozen=True)
class DocumentationPaths:
    """The documentation files validated as one release contract."""

    project_root: Path
    manifest: Path
    contract: Path
    endpoint_matrix: Path

    @classmethod
    def from_project_root(cls, project_root: Path) -> DocumentationPaths:
        docs_root = project_root / "docs"
        return cls(
            project_root=project_root,
            manifest=docs_root / "library.yml",
            contract=docs_root / "contracts" / "public-api.yml",
            endpoint_matrix=docs_root / "reference" / "endpoint-matrix.md",
        )


def validate_documentation_contract(project_root: Path) -> None:
    """Validate durable metadata, declared API details, examples, and endpoint coverage."""
    paths = DocumentationPaths.from_project_root(project_root)
    manifest = _load_yaml_mapping(paths.manifest)
    contract = _load_yaml_mapping(paths.contract)
    _validate_manifest(manifest)
    _validate_contract_shape(contract)
    source_modules = _load_source_modules(paths.project_root, contract)
    _validate_public_reference(paths.project_root, contract)
    _validate_root_exports(paths.project_root, contract)
    _validate_declared_classes(source_modules, contract)
    _validate_declared_functions(source_modules, contract)
    _validate_exception_hierarchy(source_modules, contract)
    _validate_pydantic_fields(source_modules, contract)
    _validate_documented_examples(paths.project_root, contract)
    _validate_mutation_safety_rules(paths.project_root, contract)
    _validate_endpoint_matrix(paths, contract)


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise DocumentationContractError(f"Missing required documentation file: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise DocumentationContractError(f"Invalid YAML in {path}: {error}") from error
    if not isinstance(loaded, dict):
        raise DocumentationContractError(f"Documentation mapping expected in {path}")
    return loaded


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise DocumentationContractError(
            "docs/library.yml must contain exactly the portal's durable manifest fields."
        )
    if manifest != MANIFEST_VALUES:
        raise DocumentationContractError(
            "docs/library.yml must match the portal allowlisted identity and durable metadata."
        )


def _validate_contract_shape(contract: Mapping[str, Any]) -> None:
    required_fields = {
        "schema_version",
        "public_modules",
        "root_exports",
        "classes",
        "functions",
        "exceptions",
        "pydantic_fields",
        "examples",
        "mutation_safety_rules",
        "endpoint_matrix",
    }
    if set(contract) != required_fields or contract["schema_version"] != 1:
        raise DocumentationContractError(
            "Public API contract must use the complete schema version 1 shape."
        )
    documented_modules = contract["public_modules"]
    if not isinstance(documented_modules, list) or set(documented_modules) != set(SOURCE_MODULES):
        raise DocumentationContractError(
            "Public API contract must enumerate every documented source module."
        )


def _load_source_modules(project_root: Path, contract: Mapping[str, Any]) -> dict[str, ast.Module]:
    source_modules: dict[str, ast.Module] = {}
    for module_name in contract["public_modules"]:
        module_path = project_root / "src" / Path(*module_name.split(".")).with_suffix(".py")
        if not module_path.is_file():
            raise DocumentationContractError(f"Public module source is missing: {module_name}")
        source_modules[module_name] = ast.parse(module_path.read_text(encoding="utf-8"))
    return source_modules


def _validate_public_reference(project_root: Path, contract: Mapping[str, Any]) -> None:
    reference_path = project_root / PUBLIC_API_REFERENCE_PATH
    if not reference_path.is_file():
        raise DocumentationContractError(f"Missing public API reference: {reference_path}")
    reference_content = reference_path.read_text(encoding="utf-8")
    missing_modules = [
        module_name
        for module_name in contract["public_modules"]
        if f"::: {module_name}" not in reference_content
    ]
    if missing_modules:
        raise DocumentationContractError(
            f"Public API reference is missing module documentation: {', '.join(missing_modules)}"
        )


def _validate_root_exports(project_root: Path, contract: Mapping[str, Any]) -> None:
    root_module = ast.parse(
        (project_root / "src" / "ig_trading_lib" / "__init__.py").read_text(encoding="utf-8")
    )
    source_exports = _extract_all_exports(root_module)
    documented_exports = contract["root_exports"]
    if source_exports != documented_exports:
        raise DocumentationContractError(
            "Root exports must be exactly enumerated in public-api.yml."
        )


def _extract_all_exports(module: ast.Module) -> list[str]:
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets
        ):
            continue
        if not isinstance(node.value, ast.List | ast.Tuple):
            break
        values = [element.value for element in node.value.elts if isinstance(element, ast.Constant)]
        if all(isinstance(value, str) for value in values):
            return values
    raise DocumentationContractError("ig_trading_lib.__all__ must be a literal string sequence.")


def _validate_declared_classes(
    source_modules: Mapping[str, ast.Module], contract: Mapping[str, Any]
) -> None:
    source_classes = _public_classes(source_modules)
    documented_classes = contract["classes"]
    if not isinstance(documented_classes, dict) or set(documented_classes) != set(source_classes):
        raise DocumentationContractError(
            "Public API contract must enumerate every public class exactly once."
        )
    for qualified_name, class_node in source_classes.items():
        declaration = documented_classes[qualified_name]
        if not isinstance(declaration, dict):
            raise DocumentationContractError(
                f"Class declaration must be a mapping: {qualified_name}"
            )
        _validate_class_fields(qualified_name, class_node, declaration)
        _validate_constructor(qualified_name, class_node, declaration)
        _validate_methods(qualified_name, class_node, declaration)


def _public_classes(source_modules: Mapping[str, ast.Module]) -> dict[str, ast.ClassDef]:
    return {
        f"{module_name}.{node.name}": node
        for module_name, module in source_modules.items()
        for node in module.body
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
    }


def _validate_class_fields(
    qualified_name: str, class_node: ast.ClassDef, declaration: Mapping[str, Any]
) -> None:
    documented_fields = declaration.get("fields")
    source_fields = _source_class_fields(class_node)
    if documented_fields != source_fields:
        raise DocumentationContractError(
            f"Class fields must be exactly documented for {qualified_name}."
        )


def _source_class_fields(class_node: ast.ClassDef) -> list[str]:
    fields: list[str] = []
    for node in class_node.body:
        if not isinstance(node, ast.AnnAssign) or not isinstance(node.target, ast.Name):
            continue
        fields.append(node.target.id)
    return fields


def _validate_constructor(
    qualified_name: str, class_node: ast.ClassDef, declaration: Mapping[str, Any]
) -> None:
    constructor = _method_named(class_node, "__init__")
    documented_constructor = declaration.get("constructor")
    if constructor is None:
        if documented_constructor is not None:
            raise DocumentationContractError(
                f"Generated constructor must not be declared for {qualified_name}."
            )
        return
    _validate_callable(qualified_name, "constructor", constructor, documented_constructor)


def _validate_methods(
    qualified_name: str, class_node: ast.ClassDef, declaration: Mapping[str, Any]
) -> None:
    source_methods = {
        node.name: node
        for node in class_node.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("_")
    }
    documented_methods = declaration.get("methods")
    if not isinstance(documented_methods, dict) or set(documented_methods) != set(source_methods):
        raise DocumentationContractError(
            f"Public methods must be exactly documented for {qualified_name}."
        )
    for method_name, method_node in source_methods.items():
        _validate_callable(
            qualified_name, method_name, method_node, documented_methods[method_name]
        )


def _method_named(
    class_node: ast.ClassDef, name: str
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == name:
            return node
    return None


def _validate_callable(
    qualified_class: str,
    callable_name: str,
    source_callable: ast.FunctionDef | ast.AsyncFunctionDef,
    declaration: object,
) -> None:
    if not isinstance(declaration, dict):
        raise DocumentationContractError(
            f"Callable declaration is missing for {qualified_class}.{callable_name}."
        )
    required_fields = {"parameters", "returns", "exceptions"}
    if set(declaration) != required_fields:
        raise DocumentationContractError(
            f"Callable contract must enumerate parameters, returns, and exceptions: "
            f"{qualified_class}.{callable_name}."
        )
    _validate_parameter_contract(
        qualified_class,
        callable_name,
        _source_parameters(source_callable),
        declaration["parameters"],
    )
    source_return = ast.unparse(source_callable.returns) if source_callable.returns else "None"
    if declaration["returns"] != source_return:
        raise DocumentationContractError(
            f"Return value must be exactly documented for {qualified_class}.{callable_name}."
        )
    exceptions = declaration["exceptions"]
    if not isinstance(exceptions, list) or not set(exceptions).issubset(KNOWN_EXCEPTIONS):
        raise DocumentationContractError(
            f"Exceptions must use known public exception names: {qualified_class}.{callable_name}."
        )


def _validate_parameter_contract(
    qualified_class: str,
    callable_name: str,
    source_parameters: list[dict[str, str]],
    documented_parameters: object,
) -> None:
    if not isinstance(documented_parameters, list):
        raise DocumentationContractError(
            f"Parameters must be a list for {qualified_class}.{callable_name}."
        )
    expected_parameters = [
        {"name": parameter["name"], "type": parameter["type"]}
        for parameter in documented_parameters
        if isinstance(parameter, dict)
    ]
    if expected_parameters != source_parameters:
        raise DocumentationContractError(
            f"Parameter names and types must be exactly documented for "
            f"{qualified_class}.{callable_name}."
        )
    if any(
        set(parameter) != {"name", "type", "description"}
        or not isinstance(parameter["description"], str)
        or not parameter["description"].strip()
        for parameter in documented_parameters
        if isinstance(parameter, dict)
    ):
        raise DocumentationContractError(
            f"Parameter descriptions must be non-empty for {qualified_class}.{callable_name}."
        )


def _source_parameters(
    source_callable: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[dict[str, str]]:
    arguments = [
        *source_callable.args.posonlyargs,
        *source_callable.args.args,
        *source_callable.args.kwonlyargs,
    ]
    return [
        {
            "name": argument.arg,
            "type": ast.unparse(argument.annotation) if argument.annotation else "Any",
        }
        for argument in arguments
        if argument.arg not in {"self", "cls"}
    ]


def _validate_declared_functions(
    source_modules: Mapping[str, ast.Module], contract: Mapping[str, Any]
) -> None:
    source_functions = {
        f"{module_name}.{node.name}": node
        for module_name, module in source_modules.items()
        for node in module.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("_")
    }
    documented_functions = contract["functions"]
    if not isinstance(documented_functions, dict) or set(documented_functions) != set(
        source_functions
    ):
        raise DocumentationContractError(
            "Public API contract must enumerate every public function exactly once."
        )
    for qualified_name, function_node in source_functions.items():
        class_name, function_name = qualified_name.rsplit(".", maxsplit=1)
        _validate_callable(
            class_name, function_name, function_node, documented_functions[qualified_name]
        )


def _validate_exception_hierarchy(
    source_modules: Mapping[str, ast.Module], contract: Mapping[str, Any]
) -> None:
    source_classes = _public_classes(source_modules)
    expected_exceptions = _public_exception_bases(source_classes)
    documented_exceptions = contract["exceptions"]
    if documented_exceptions != expected_exceptions:
        raise DocumentationContractError("Public exception hierarchy must be exactly documented.")


def _public_exception_bases(source_classes: Mapping[str, ast.ClassDef]) -> dict[str, str]:
    classes_by_name = {
        qualified_name.rsplit(".", maxsplit=1)[-1]: (qualified_name, class_node)
        for qualified_name, class_node in source_classes.items()
    }
    exception_names = {"RuntimeError", "PermissionError"}
    exception_bases: dict[str, str] = {}
    while True:
        additions = {
            qualified_name: base_name
            for class_name, (qualified_name, class_node) in classes_by_name.items()
            if qualified_name not in exception_bases
            for base_name in (ast.unparse(base).split(".")[-1] for base in class_node.bases)
            if base_name in exception_names
        }
        if not additions:
            return exception_bases
        exception_bases.update(additions)
        exception_names.update(
            qualified_name.rsplit(".", maxsplit=1)[-1] for qualified_name in additions
        )


def _validate_pydantic_fields(
    source_modules: Mapping[str, ast.Module], contract: Mapping[str, Any]
) -> None:
    source_models = {
        qualified_name: _source_class_fields(class_node)
        for qualified_name, class_node in _public_classes(source_modules).items()
        if any(ast.unparse(base).split(".")[-1] == "BaseModel" for base in class_node.bases)
    }
    documented_models = contract["pydantic_fields"]
    if documented_models != source_models:
        raise DocumentationContractError("Pydantic fields must be exactly documented.")


def _validate_documented_examples(project_root: Path, contract: Mapping[str, Any]) -> None:
    examples = contract["examples"]
    if not isinstance(examples, list) or not examples:
        raise DocumentationContractError("Public API contract must include executable examples.")
    for example in examples:
        if not isinstance(example, dict) or set(example) != {"id", "path", "contains"}:
            raise DocumentationContractError(
                "Each example contract needs id, path, and contains fields."
            )
        path = project_root / example["path"]
        if not path.is_file():
            raise DocumentationContractError(f"Documented example is missing: {example['path']}")
        content = path.read_text(encoding="utf-8")
        if example["contains"] not in content:
            raise DocumentationContractError(f"Documented example is incomplete: {example['id']}")
        if path.suffix == ".py":
            compile(content, str(path), "exec")


def _validate_mutation_safety_rules(project_root: Path, contract: Mapping[str, Any]) -> None:
    rules = contract["mutation_safety_rules"]
    if not isinstance(rules, list) or not rules:
        raise DocumentationContractError(
            "Public API contract must enumerate mutation-safety rules."
        )
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != {"id", "path", "text"}:
            raise DocumentationContractError(
                "Each mutation-safety rule needs id, path, and text fields."
            )
        document_path = project_root / rule["path"]
        if not document_path.is_file() or rule["text"] not in document_path.read_text(
            encoding="utf-8"
        ):
            raise DocumentationContractError(f"Mutation-safety rule is undocumented: {rule['id']}")


def _validate_endpoint_matrix(paths: DocumentationPaths, contract: Mapping[str, Any]) -> None:
    if contract["endpoint_matrix"] != "docs/reference/endpoint-matrix.md":
        raise DocumentationContractError(
            "Endpoint matrix path must be part of the public API contract."
        )
    expected_rows = _source_endpoint_rows(paths.project_root)
    actual_rows = _documented_endpoint_rows(paths.endpoint_matrix)
    if actual_rows != expected_rows:
        raise DocumentationContractError("Endpoint matrix must exactly match DOCUMENTED_ENDPOINTS.")


def _source_endpoint_rows(project_root: Path) -> list[tuple[str, str, str, str]]:
    source_path = str(project_root / "src")
    sys.path.insert(0, source_path)
    try:
        from ig_trading_lib.endpoint_catalog import DOCUMENTED_ENDPOINTS

        return [
            (
                endpoint.name,
                endpoint.method,
                endpoint.path_template,
                _format_versions(endpoint.versions),
            )
            for endpoint in DOCUMENTED_ENDPOINTS
        ]
    finally:
        sys.path.remove(source_path)


def _documented_endpoint_rows(path: Path) -> list[tuple[str, str, str, str]]:
    if not path.is_file():
        raise DocumentationContractError(f"Missing endpoint matrix: {path}")
    rows: list[tuple[str, str, str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"Operation", "---"}:
            continue
        if all(cell and set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(tuple(cells))
    return rows


def _format_versions(versions: tuple[int, ...]) -> str:
    return ", ".join(f"v{version}" for version in versions)


if __name__ == "__main__":
    try:
        validate_documentation_contract(Path(__file__).resolve().parents[1])
    except DocumentationContractError as error:
        raise SystemExit(f"Documentation contract failed: {error}") from error
    print("Documentation contract passed.")
