"""Give an agent only generated, documented operations to choose from."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def load_agent_context(index_path: Path) -> dict[str, Any]:
    """Load the generated API index that points back to the public contract."""
    context = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(context, dict) or "endpoints" not in context:
        raise ValueError("Expected a generated IG Trading Library API index.")
    return context


def select_documented_operation(context: Mapping[str, Any], operation_name: str) -> dict[str, Any]:
    """Return one catalogued operation instead of letting an agent invent an endpoint."""
    endpoints = context.get("endpoints")
    if not isinstance(endpoints, list):
        raise ValueError("Generated API index has no endpoint list.")
    for operation in endpoints:
        if isinstance(operation, dict) and operation.get("name") == operation_name:
            return operation
    raise KeyError(f"No documented operation named {operation_name!r}.")
