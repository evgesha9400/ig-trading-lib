"""Build a market-price subscription and use the streaming operation namespace."""

from collections.abc import AsyncIterator, Iterator

from ig_trading_lib import IG, AsyncIG, StreamSubscription, StreamUpdate


def market_price_subscription(epic: str) -> StreamSubscription:
    return StreamSubscription(
        key="market-prices",
        mode="MERGE",
        items=(f"MARKET:{epic}",),
        fields=("BID", "OFFER", "UPDATE_TIME"),
    )


def iter_market_price_updates(ig: IG, epic: str) -> Iterator[StreamUpdate]:
    yield from ig.operations.streaming.subscribe(market_price_subscription(epic))


async def aiter_market_price_updates(ig: AsyncIG, epic: str) -> AsyncIterator[StreamUpdate]:
    async for update in ig.operations.streaming.subscribe(market_price_subscription(epic)):
        yield update
