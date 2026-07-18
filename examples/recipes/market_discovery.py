"""Discover provider markets through the typed synchronous and asynchronous facades."""

from __future__ import annotations

from ig_trading_lib import AsyncIGClient, IGClient


def discover_markets(client: IGClient, search_term: str) -> tuple[str, ...]:
    """Return matching market epics from the typed market-search facade."""
    return tuple(market.epic for market in client.markets.search(search_term).items)


async def discover_markets_async(client: AsyncIGClient, search_term: str) -> tuple[str, ...]:
    """Return matching market epics through the asynchronous market-search facade."""
    markets = await client.markets.search(search_term)
    return tuple(market.epic for market in markets.items)
