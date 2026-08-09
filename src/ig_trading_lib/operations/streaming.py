"""Streaming as an IG protocol operation namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from ig_trading_lib.streaming import (
    AsyncStreamingClient,
    StreamingClient,
    StreamSubscription,
    StreamUpdate,
)


class StreamingOperations:
    def __init__(self, client: StreamingClient) -> None:
        self._client = client

    def subscribe(self, subscription: StreamSubscription) -> Iterator[StreamUpdate]:
        return self._client.iter_updates(subscription)

    def close(self) -> None:
        self._client.close()


class AsyncStreamingOperations:
    def __init__(self, client: AsyncStreamingClient) -> None:
        self._client = client

    def subscribe(self, subscription: StreamSubscription) -> AsyncIterator[StreamUpdate]:
        return self._client.aiter_updates(subscription)

    async def close(self) -> None:
        await self._client.close()
