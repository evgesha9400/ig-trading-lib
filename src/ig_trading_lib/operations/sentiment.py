"""Typed client-sentiment operations."""

from __future__ import annotations

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

    def list(self) -> ClientSentimentsResponse:
        return self._executor.execute("client_sentiment.list", ClientSentimentsResponse)

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

    async def list(self) -> ClientSentimentsResponse:
        return await self._executor.execute("client_sentiment.list", ClientSentimentsResponse)

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
