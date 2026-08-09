"""Give an agent only generated, documented operations to choose from."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def load_agent_context(index_path: Path) -> dict[str, Any]:
    """Load the generated API index that points back to the public contract."""
    context = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(context, dict) or "operations" not in context:
        raise ValueError("Expected a generated IG Trading Library API index.")
    return context


def select_documented_operation(context: Mapping[str, Any], operation_name: str) -> dict[str, Any]:
    """Return one catalogued operation instead of letting an agent invent an endpoint."""
    namespaces = context.get("operations")
    if not isinstance(namespaces, list):
        raise ValueError("Generated API index has no operation list.")
    for namespace in namespaces:
        if not isinstance(namespace, dict):
            continue
        for operation in namespace.get("operations", []):
            if isinstance(operation, dict) and operation.get("operation_id") == operation_name:
                return operation
    raise KeyError(f"No documented operation named {operation_name!r}.")
