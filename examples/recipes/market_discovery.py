"""Discover markets through the faithful operation layer."""

from ig_trading_lib import IG, AsyncIG


def discover_markets(ig: IG, search_term: str) -> tuple[str, ...]:
    return tuple(market.epic for market in ig.operations.markets.search(search_term).markets)


async def discover_markets_async(ig: AsyncIG, search_term: str) -> tuple[str, ...]:
    response = await ig.operations.markets.search(search_term)
    return tuple(market.epic for market in response.markets)
