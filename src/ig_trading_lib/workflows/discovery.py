"""Market discovery workflows composed from typed operations."""

from __future__ import annotations

from ig_trading_lib.errors import ResourceNotFoundError
from ig_trading_lib.operations.markets import (
    AsyncMarketOperations,
    MarketGetResponse,
    MarketOperations,
)


class MarketDiscoveryWorkflow:
    """Synchronous search and exact-market selection."""

    def __init__(self, markets: MarketOperations) -> None:
        self._markets = markets

    def find_market(self, search_term: str, epic: str) -> MarketGetResponse:
        """Search, select an exact epic, and retrieve its details."""
        search = self._markets.search(search_term)
        selected = next((market for market in search.markets if market.epic == epic), None)
        if selected is None:
            raise _market_not_found(search_term, epic)
        return self._markets.get(selected.epic)


class AsyncMarketDiscoveryWorkflow:
    """Asynchronous search and exact-market selection."""

    def __init__(self, markets: AsyncMarketOperations) -> None:
        self._markets = markets

    async def find_market(self, search_term: str, epic: str) -> MarketGetResponse:
        """Search, select an exact epic, and retrieve its details."""
        search = await self._markets.search(search_term)
        selected = next((market for market in search.markets if market.epic == epic), None)
        if selected is None:
            raise _market_not_found(search_term, epic)
        return await self._markets.get(selected.epic)


def _market_not_found(search_term: str, epic: str) -> ResourceNotFoundError:
    return ResourceNotFoundError(
        f"Market search did not return the exact epic {epic!r}.",
        details={"epic": epic, "search_term": search_term},
    )
