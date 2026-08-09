"""Canonical snake_case models for IG wire payloads."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")
Item = TypeVar("Item")


def to_snake_case(value: str) -> str:
    """Convert an IG camelCase key to the canonical public snake_case key."""
    return _CAMEL_BOUNDARY.sub("_", value).lower().replace("-", "_")


def to_camel_case(value: str) -> str:
    """Convert a public snake_case field to an IG camelCase wire key."""
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


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


class IGRequest(BaseModel):
    """Strict operation input that serialises to IG wire field names."""

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )

    def to_wire(self) -> dict[str, Any]:
        """Return the validated provider request body without absent optional fields."""
        return _wire_value(self.model_dump(by_alias=True, exclude_none=True))


def _wire_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, date | datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _wire_value(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_wire_value(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class Page(Generic[Item]):
    """A typed IG result page with an optional provider continuation path."""

    items: tuple[Item, ...]
    next_path: str | None = None
