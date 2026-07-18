"""Canonical snake_case models for IG wire payloads."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")
Item = TypeVar("Item")


def to_snake_case(value: str) -> str:
    """Convert an IG camelCase key to the canonical public snake_case key."""
    return _CAMEL_BOUNDARY.sub("_", value).lower().replace("-", "_")


def normalize_wire_value(value: Any) -> Any:
    """Recursively normalise provider response keys without changing values."""
    if isinstance(value, dict):
        return {to_snake_case(key): normalize_wire_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_wire_value(item) for item in value]
    return value


class IGModel(BaseModel):
    """Flexible typed resource that preserves all documented provider fields."""

    model_config = ConfigDict(extra="allow", frozen=True)

    @model_validator(mode="before")
    @classmethod
    def normalize_wire_keys(cls, value: Any) -> Any:
        return normalize_wire_value(value)


@dataclass(frozen=True, slots=True)
class Page(Generic[Item]):
    """A typed IG result page with an optional provider continuation path."""

    items: tuple[Item, ...]
    next_path: str | None = None
