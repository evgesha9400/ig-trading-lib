"""Build a market-price subscription and delegate update iteration to the client."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from ig_trading_lib import AsyncIGClient, IGClient, StreamSubscription, StreamUpdate


def market_price_subscription(epic: str) -> StreamSubscription:
    """Create one reusable Lightstreamer market-price subscription definition."""
    return StreamSubscription(
        key="market-prices",
        mode="MERGE",
        items=(f"MARKET:{epic}",),
        fields=("BID", "OFFER", "UPDATE_TIME"),
    )


def iter_market_price_updates(client: IGClient, epic: str) -> Iterator[StreamUpdate]:
    """Yield synchronous market updates until the caller closes the iterator."""
    yield from client.streaming.iter_updates(market_price_subscription(epic))


async def aiter_market_price_updates(
    client: AsyncIGClient, epic: str
) -> AsyncIterator[StreamUpdate]:
    """Yield asynchronous market updates until the consumer closes the iterator."""
    async for update in client.streaming.aiter_updates(market_price_subscription(epic)):
        yield update
