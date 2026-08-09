"""Typed client-sentiment operations."""

from __future__ import annotations

import re

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel


class ClientSentiment(IGModel):
    market_id: str | None = None
    long_position_percentage: float | None = None
    short_position_percentage: float | None = None


class ClientSentimentsResponse(IGModel):
    client_sentiments: tuple[ClientSentiment, ...] = ()


class ClientSentimentResponse(ClientSentiment):
    pass


class ClientSentimentOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, market_ids: tuple[str, ...] | None = None) -> ClientSentimentsResponse:
        return self._executor.execute(
            "client_sentiment.list",
            ClientSentimentsResponse,
            query=_market_ids_query(market_ids),
        )

    def get(self, market_id: str) -> ClientSentimentResponse:
        return self._executor.execute(
            "client_sentiment.get",
            ClientSentimentResponse,
            path={"market_id": market_id},
        )

    def related(self, market_id: str) -> ClientSentimentsResponse:
        return self._executor.execute(
            "client_sentiment.related",
            ClientSentimentsResponse,
            path={"market_id": market_id},
        )


class AsyncClientSentimentOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self, market_ids: tuple[str, ...] | None = None) -> ClientSentimentsResponse:
        return await self._executor.execute(
            "client_sentiment.list",
            ClientSentimentsResponse,
            query=_market_ids_query(market_ids),
        )

    async def get(self, market_id: str) -> ClientSentimentResponse:
        return await self._executor.execute(
            "client_sentiment.get",
            ClientSentimentResponse,
            path={"market_id": market_id},
        )

    async def related(self, market_id: str) -> ClientSentimentsResponse:
        return await self._executor.execute(
            "client_sentiment.related",
            ClientSentimentsResponse,
            path={"market_id": market_id},
        )


_MARKET_ID = re.compile(r"[A-Za-z0-9_\- ]{1,30}")


def _market_ids_query(market_ids: tuple[str, ...] | None) -> dict[str, str] | None:
    if market_ids is None:
        return None
    if not 1 <= len(market_ids) <= 500:
        raise ValueError("market_ids must contain between 1 and 500 identifiers")
    if any(_MARKET_ID.fullmatch(market_id) is None for market_id in market_ids):
        raise ValueError("market_ids must match the provider identifier format")
    return {"marketIds": ",".join(market_ids)}
