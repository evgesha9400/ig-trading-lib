"""Typed market operations shared by synchronous and asynchronous roots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from pydantic import Field

from ig_trading_lib.models import IGModel
from ig_trading_lib.transport import AsyncTransport, SyncTransport


class MarketSearchRequest(IGModel):
    """Validated input for a market search."""

    search_term: str = Field(min_length=1)


class MarketSummary(IGModel):
    """Known fields returned for one market search result."""

    epic: str
    instrument_name: str | None = None
    market_status: str | None = None


class MarketSearchResponse(IGModel):
    """Typed response from the market search operation."""

    markets: tuple[MarketSummary, ...]


class MarketGetRequest(IGModel):
    """Validated input for retrieving one market."""

    epic: str = Field(min_length=1)


class MarketInstrument(IGModel):
    """Known instrument fields returned by market details."""

    epic: str
    name: str | None = None


class MarketSnapshot(IGModel):
    """Known price snapshot fields returned by market details."""

    market_status: str | None = None
    bid: float | None = None
    offer: float | None = None


class MarketDealingRules(IGModel):
    """Known dealing-rule fields returned by market details."""

    market_order_preference: str | None = None


class MarketGetResponse(IGModel):
    """Typed response from the market details operation."""

    instrument: MarketInstrument
    snapshot: MarketSnapshot | None = None
    dealing_rules: MarketDealingRules | None = None


@dataclass(frozen=True, slots=True)
class _ReadOperation:
    path: str
    version: int


@dataclass(frozen=True, slots=True)
class _MarketOperationSpecification:
    search: _ReadOperation
    get: _ReadOperation


_MARKET_OPERATIONS = _MarketOperationSpecification(
    search=_ReadOperation(path="/markets", version=1),
    get=_ReadOperation(path="/markets/{epic}", version=4),
)


class MarketOperations:
    """Synchronous typed market operations."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def search(self, search_term: str) -> MarketSearchResponse:
        """Search markets by a human-readable term."""
        operation = _MARKET_OPERATIONS.search
        response = self._transport.request(
            "GET",
            operation.path,
            version=operation.version,
            params=_search_params(search_term),
        )
        return _parse_search_response(response.json())

    def get(self, epic: str) -> MarketGetResponse:
        """Retrieve one market by exact epic."""
        operation = _MARKET_OPERATIONS.get
        response = self._transport.request(
            "GET",
            _market_path(operation, epic),
            version=operation.version,
        )
        return _parse_get_response(response.json())


class AsyncMarketOperations:
    """Asynchronous typed market operations."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def search(self, search_term: str) -> MarketSearchResponse:
        """Search markets by a human-readable term."""
        operation = _MARKET_OPERATIONS.search
        response = await self._transport.request(
            "GET",
            operation.path,
            version=operation.version,
            params=_search_params(search_term),
        )
        return _parse_search_response(response.json())

    async def get(self, epic: str) -> MarketGetResponse:
        """Retrieve one market by exact epic."""
        operation = _MARKET_OPERATIONS.get
        response = await self._transport.request(
            "GET",
            _market_path(operation, epic),
            version=operation.version,
        )
        return _parse_get_response(response.json())


def _search_params(search_term: str) -> dict[str, str]:
    request = MarketSearchRequest(search_term=search_term)
    return {"searchTerm": request.search_term}


def _market_path(operation: _ReadOperation, epic: str) -> str:
    request = MarketGetRequest(epic=epic)
    return operation.path.format(epic=quote(request.epic, safe=""))


def _parse_search_response(payload: Any) -> MarketSearchResponse:
    return MarketSearchResponse.model_validate(payload)


def _parse_get_response(payload: Any) -> MarketGetResponse:
    return MarketGetResponse.model_validate(payload)
