"""Shared protocol execution for all faithful operation namespaces."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from urllib.parse import quote

import httpx

from ig_trading_lib._protocol.manifest import OPERATION_MANIFEST, OperationSpec
from ig_trading_lib.core import TradingGuard
from ig_trading_lib.models import IGModel
from ig_trading_lib.transport import AsyncTransport, SyncTransport

Response = TypeVar("Response", bound=IGModel)


def _path(operation_id: str, values: Mapping[str, str]) -> str:
    path = OPERATION_MANIFEST[operation_id].path
    return path.format(**{name: quote(value, safe="") for name, value in values.items()})


class SyncExecutor:
    """Execute a manifest-bound operation synchronously."""

    def __init__(self, transport: SyncTransport, guard: TradingGuard) -> None:
        self._transport = transport
        self._guard = guard

    def execute(
        self,
        operation_id: str,
        response_type: type[Response],
        *,
        path: Mapping[str, str] | None = None,
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> Response:
        spec = OPERATION_MANIFEST[operation_id]
        if spec.mutation:
            self._guard.require_mutation_permission()
        response = self._transport.request(
            spec.method,
            _path(operation_id, path or {}),
            version=spec.version,
            params=query,
            json=body,
        )
        result = response_type.model_validate(_response_payload(spec, response))
        if spec.invalidates_session:
            self._transport.invalidate_session()
        return result


class AsyncExecutor:
    """Execute the same manifest-bound operation asynchronously."""

    def __init__(self, transport: AsyncTransport, guard: TradingGuard) -> None:
        self._transport = transport
        self._guard = guard

    async def execute(
        self,
        operation_id: str,
        response_type: type[Response],
        *,
        path: Mapping[str, str] | None = None,
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> Response:
        spec = OPERATION_MANIFEST[operation_id]
        if spec.mutation:
            self._guard.require_mutation_permission()
        response = await self._transport.request(
            spec.method,
            _path(operation_id, path or {}),
            version=spec.version,
            params=query,
            json=body,
        )
        result = response_type.model_validate(_response_payload(spec, response))
        if spec.invalidates_session:
            self._transport.invalidate_session()
        return result


def _payload(response: httpx.Response) -> object:
    try:
        return response.json()
    except ValueError:
        return {}


def _response_payload(spec: OperationSpec, response: httpx.Response) -> object:
    if spec.response_format == "binary":
        return {
            "content": response.content,
            "content_type": response.headers.get("content-type"),
        }
    payload = _payload(response)
    if not spec.response_headers or not isinstance(payload, Mapping):
        return payload
    enriched = dict(payload)
    for field_name, header_name in spec.response_headers:
        if value := response.headers.get(header_name):
            enriched[field_name] = value
    return enriched
