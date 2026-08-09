"""Validate that implementation, public contract, manifest, and prose describe one v4 API."""

from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path
from typing import Any, get_type_hints

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import ig_trading_lib  # noqa: E402
from ig_trading_lib._protocol.manifest import (  # noqa: E402
    OPERATION_MANIFEST,
    PUBLIC_OPERATION_MANIFEST,
    SOURCE_EXCLUSIONS,
)
from ig_trading_lib.api import (  # noqa: E402
    IG,
    AsyncIG,
    AsyncOperations,
    AsyncWorkflows,
    Operations,
    Workflows,
)
from ig_trading_lib.core import OAuthCredentials, SessionCredentials  # noqa: E402
from ig_trading_lib.models import IGModel  # noqa: E402

CONTRACT = ROOT / "docs/contracts/public-api.yml"
LEGACY_MODULES = (
    "client.py",
    "services.py",
    "async_services.py",
    "versions.py",
    "endpoint_catalog.py",
)
REQUIRED_VALUE_LANGUAGE = (
    "typed operations",
    "safe workflows",
    "operations",
    "workflows",
    "AmbiguousExecutionError",
)


def _contract() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


def _public_method_names(instance_type: type[object]) -> set[str]:
    return {
        name
        for name, value in inspect.getmembers(instance_type, inspect.isfunction)
        if not name.startswith("_")
    }


def _validate_roots(contract: dict[str, Any]) -> None:
    assert set(ig_trading_lib.__all__) == set(contract["root_exports"]), (
        "Root exports must be exactly enumerated in public-api.yml"
    )
    assert set(Operations.__dataclass_fields__) == set(contract["operations"])
    assert set(AsyncOperations.__dataclass_fields__) == set(contract["operations"])
    assert set(Workflows.__dataclass_fields__) == set(contract["workflows"])
    assert set(AsyncWorkflows.__dataclass_fields__) == set(contract["workflows"])
    assert tuple(inspect.signature(IG).parameters) == tuple(inspect.signature(AsyncIG).parameters)
    assert "version" not in inspect.signature(SessionCredentials).parameters
    assert "version" not in inspect.signature(OAuthCredentials).parameters


def _validate_modules(contract: dict[str, Any]) -> None:
    for module_name in contract["public_modules"]:
        importlib.import_module(module_name)
    source = ROOT / "src/ig_trading_lib"
    for module_name in LEGACY_MODULES:
        assert not (source / module_name).exists(), (
            f"Competing legacy module remains: {module_name}"
        )


def _validate_operation_surface(contract: dict[str, Any]) -> None:
    manifest_ids: set[str] = set()
    for namespace, methods in contract["operations"].items():
        sync_type = get_type_hints(Operations)[namespace]
        async_type = get_type_hints(AsyncOperations)[namespace]
        expected = set(methods)
        assert _public_method_names(sync_type) == expected
        assert _public_method_names(async_type) == expected
        for method_name, operation_id in methods.items():
            sync_method = getattr(sync_type, method_name)
            async_method = getattr(async_type, method_name)
            assert (
                inspect.signature(sync_method).parameters
                == inspect.signature(async_method).parameters
            )
            if operation_id.startswith("streaming."):
                continue
            assert operation_id in PUBLIC_OPERATION_MANIFEST
            manifest_ids.add(operation_id)
            return_type = get_type_hints(sync_method).get("return")
            assert inspect.isclass(return_type) and issubclass(return_type, IGModel), (
                f"{namespace}.{method_name} must return an operation-specific IGModel"
            )
            signature_text = str(inspect.signature(sync_method))
            assert "Mapping" not in signature_text
            assert "Any" not in signature_text
            assert "version" not in inspect.signature(sync_method).parameters
    assert manifest_ids == set(PUBLIC_OPERATION_MANIFEST)


def _validate_workflows(contract: dict[str, Any]) -> None:
    for namespace, methods in contract["workflows"].items():
        sync_type = get_type_hints(Workflows)[namespace]
        async_type = get_type_hints(AsyncWorkflows)[namespace]
        assert _public_method_names(sync_type) == set(methods)
        assert _public_method_names(async_type) == set(methods)
        for method_name in methods:
            assert inspect.signature(getattr(sync_type, method_name)).parameters == (
                inspect.signature(getattr(async_type, method_name)).parameters
            )


def _validate_evidence() -> None:
    assert SOURCE_EXCLUSIONS
    for operation_id, spec in OPERATION_MANIFEST.items():
        assert spec.operation_id == operation_id
        assert spec.evidence.url.startswith("https://labs.ig.com/")
        assert spec.evidence.retrieved_on
        assert len(spec.evidence.sha256) == 64
        assert spec.schema_provenance


def _validate_prose() -> None:
    prose_paths = [ROOT / "README.md", ROOT / "docs/index.md", ROOT / "docs/getting-started.md"]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in prose_paths)
    lowered = combined.lower()
    for phrase in REQUIRED_VALUE_LANGUAGE:
        assert phrase.lower() in lowered, f"Documentation must explain {phrase}"
    for legacy_name in ("IGClient", "AsyncIGClient", "ResourceClient", ".v1", ".v2", ".v3"):
        assert legacy_name not in combined, f"Legacy guidance remains: {legacy_name}"
    for compatibility_promise in (
        "same names, inputs, and results",
        "same operation and workflow names, parameters, and result models",
    ):
        assert compatibility_promise not in combined, (
            f"New compatibility promise remains: {compatibility_promise}"
        )
    assert "library v4" in lowered
    assert "ig api version 4" not in lowered


def main() -> int:
    contract = _contract()
    assert contract["schema_version"] == 2
    assert set(contract["mental_model"]) == {"operations", "workflows"}
    _validate_roots(contract)
    _validate_modules(contract)
    _validate_operation_surface(contract)
    _validate_workflows(contract)
    _validate_evidence()
    _validate_prose()
    print("Documentation contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
