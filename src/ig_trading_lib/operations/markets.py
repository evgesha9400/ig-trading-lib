"""Typed market discovery, category, and price operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel


class MarketSummary(IGModel):
    epic: str
    instrument_name: str | None = None
    market_status: str | None = None


class MarketSearchResponse(IGModel):
    markets: tuple[MarketSummary, ...]


class MarketsResponse(MarketSearchResponse):
    pass


class MarketInstrument(IGModel):
    epic: str
    name: str | None = None


class MarketSnapshot(IGModel):
    market_status: str | None = None
    bid: float | None = None
    offer: float | None = None


class MarketDealingRules(IGModel):
    market_order_preference: str | None = None


class MarketGetResponse(IGModel):
    instrument: MarketInstrument
    snapshot: MarketSnapshot | None = None
    dealing_rules: MarketDealingRules | None = None


class Category(IGModel):
    id: str
    name: str | None = None


class CategoriesResponse(IGModel):
    nodes: tuple[Category, ...] = ()


class CategoryInstrumentsResponse(IGModel):
    markets: tuple[MarketSummary, ...] = ()


class PriceValue(IGModel):
    bid: Decimal | None = None
    ask: Decimal | None = None
    last_traded: Decimal | None = None


class PricePoint(IGModel):
    snapshot_time: datetime | str | None = None
    open_price: PriceValue | None = None
    close_price: PriceValue | None = None
    high_price: PriceValue | None = None
    low_price: PriceValue | None = None
    last_traded_volume: float | None = None


class PricesResponse(IGModel):
    prices: tuple[PricePoint, ...] = ()
    instrument_type: str | None = None


class MarketOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, epics: tuple[str, ...]) -> MarketsResponse:
        return self._executor.execute(
            "markets.list", MarketsResponse, query={"epics": ",".join(epics)}
        )

    def search(self, search_term: str) -> MarketSearchResponse:
        search_term = _required(search_term, "search_term")
        return self._executor.execute(
            "markets.search", MarketSearchResponse, query={"searchTerm": search_term}
        )

    def get(self, epic: str) -> MarketGetResponse:
        return self._executor.execute(
            "markets.get", MarketGetResponse, path={"epic": _required(epic, "epic")}
        )


class AsyncMarketOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self, epics: tuple[str, ...]) -> MarketsResponse:
        return await self._executor.execute(
            "markets.list", MarketsResponse, query={"epics": ",".join(epics)}
        )

    async def search(self, search_term: str) -> MarketSearchResponse:
        search_term = _required(search_term, "search_term")
        return await self._executor.execute(
            "markets.search", MarketSearchResponse, query={"searchTerm": search_term}
        )

    async def get(self, epic: str) -> MarketGetResponse:
        return await self._executor.execute(
            "markets.get", MarketGetResponse, path={"epic": _required(epic, "epic")}
        )


class CategoriesOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> CategoriesResponse:
        return self._executor.execute("categories.list", CategoriesResponse)

    def list_instruments(self, category_id: str) -> CategoryInstrumentsResponse:
        return self._executor.execute(
            "categories.list_instruments",
            CategoryInstrumentsResponse,
            path={"category_id": category_id},
        )


class AsyncCategoriesOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> CategoriesResponse:
        return await self._executor.execute("categories.list", CategoriesResponse)

    async def list_instruments(self, category_id: str) -> CategoryInstrumentsResponse:
        return await self._executor.execute(
            "categories.list_instruments",
            CategoryInstrumentsResponse,
            path={"category_id": category_id},
        )


class PricesOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, epic: str, *, resolution: str | None = None) -> PricesResponse:
        query = {"resolution": resolution} if resolution else None
        return self._executor.execute(
            "prices.list", PricesResponse, path={"epic": epic}, query=query
        )

    def list_points(self, epic: str, resolution: str, num_points: int) -> PricesResponse:
        return self._executor.execute(
            "prices.list_points",
            PricesResponse,
            path={"epic": epic, "resolution": resolution, "num_points": str(num_points)},
        )

    def list_date_range(
        self, epic: str, resolution: str, start_date: datetime | str, end_date: datetime | str
    ) -> PricesResponse:
        return self._executor.execute(
            "prices.list_date_range",
            PricesResponse,
            path={
                "epic": epic,
                "resolution": resolution,
                "start_date": _date_time(start_date),
                "end_date": _date_time(end_date),
            },
        )


class AsyncPricesOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self, epic: str, *, resolution: str | None = None) -> PricesResponse:
        query = {"resolution": resolution} if resolution else None
        return await self._executor.execute(
            "prices.list", PricesResponse, path={"epic": epic}, query=query
        )

    async def list_points(self, epic: str, resolution: str, num_points: int) -> PricesResponse:
        return await self._executor.execute(
            "prices.list_points",
            PricesResponse,
            path={"epic": epic, "resolution": resolution, "num_points": str(num_points)},
        )

    async def list_date_range(
        self, epic: str, resolution: str, start_date: datetime | str, end_date: datetime | str
    ) -> PricesResponse:
        return await self._executor.execute(
            "prices.list_date_range",
            PricesResponse,
            path={
                "epic": epic,
                "resolution": resolution,
                "start_date": _date_time(start_date),
                "end_date": _date_time(end_date),
            },
        )


def _required(value: str, name: str) -> str:
    if not value:
        raise ValueError(f"{name} must not be empty")
    return value


def _date_time(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else value
