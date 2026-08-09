"""Typed market discovery, category, and price operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class MarketSummary(IGModel):
    bid: Decimal | None = None
    delay_time: int | None = None
    epic: str
    expiry: str | None = None
    high: Decimal | None = None
    instrument_name: str | None = None
    instrument_type: str | None = None
    low: Decimal | None = None
    market_status: str | None = None
    net_change: Decimal | None = None
    offer: Decimal | None = None
    percentage_change: Decimal | None = None
    scaling_factor: Decimal | None = None
    streaming_prices_available: bool | None = None
    update_time: str | None = None
    update_time_utc: str | None = None


class MarketSearchResponse(IGModel):
    markets: tuple[MarketSummary, ...]


DistanceUnit = Literal["PERCENTAGE", "POINTS"]


class MarketDistanceRule(IGModel):
    unit: DistanceUnit
    value: Decimal


class MarketCurrency(IGModel):
    base_exchange_rate: Decimal | None = None
    code: str
    exchange_rate: Decimal | None = None
    is_default: bool | None = None
    symbol: str | None = None


class MarketInstrument(IGModel):
    chart_code: str | None = None
    contract_size: str | None = None
    country: str | None = None
    currencies: tuple[MarketCurrency, ...] = ()
    epic: str
    expiry: str | None = None
    limited_risk_premium: MarketDistanceRule | None = None
    lot_size: Decimal | None = None
    market_id: str | None = None
    name: str | None = None
    news_code: str | None = None
    streaming_prices_available: bool | None = None
    limit_allowed: bool | None = None
    stop_allowed: bool | None = None
    type: str | None = None
    unit: str | None = None
    value_of_one_pip: str | None = None


class MarketPriceLadderEntry(IGModel):
    bid: Decimal
    ask: Decimal


class MarketCurrencyLadder(IGModel):
    currency: str
    bid_sizes: tuple[Decimal, ...] = ()
    ask_sizes: tuple[Decimal, ...] = ()


class MarketSnapshot(IGModel):
    decimal_places_factor: int | None = None
    delay_time: int | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    market_status: str | None = None
    net_change: Decimal | None = None
    percentage_change: Decimal | None = None
    scaling_factor: Decimal | None = None
    update_timestamp_utc: int | None = None
    price_ladder: tuple[MarketPriceLadderEntry, ...] = ()
    currency_ladders: tuple[MarketCurrencyLadder, ...] = ()


class MarketDealingRules(IGModel):
    controlled_risk_spacing: MarketDistanceRule | None = None
    max_stop_or_limit_distance: MarketDistanceRule | None = None
    min_controlled_risk_stop_distance: MarketDistanceRule | None = None
    min_deal_size: MarketDistanceRule | None = None
    min_normal_stop_or_limit_distance: MarketDistanceRule | None = None
    min_step_distance: MarketDistanceRule | None = None
    trailing_stops_preference: str | None = None


class MarketGetResponse(IGModel):
    instrument: MarketInstrument
    snapshot: MarketSnapshot | None = None
    dealing_rules: MarketDealingRules | None = None


class MarketExpiryDetails(IGModel):
    last_dealing_date: str | None = None
    settlement_info: str | None = None


class MarketMarginDepositBand(IGModel):
    currency: str | None = None
    margin: Decimal | None = None
    max: Decimal | None = None
    min: Decimal | None = None


class MarketTime(IGModel):
    close_time: str | None = None
    open_time: str | None = None


class MarketOpeningHours(IGModel):
    market_times: tuple[MarketTime, ...] = ()


class MarketRolloverDetails(IGModel):
    last_rollover_time: str | None = None
    rollover_info: str | None = None


class DetailedMarketInstrument(MarketInstrument):
    controlled_risk_allowed: bool | None = None
    expiry_details: MarketExpiryDetails | None = None
    force_open_allowed: bool | None = None
    margin_deposit_bands: tuple[MarketMarginDepositBand, ...] = ()
    margin_factor: Decimal | None = None
    margin_factor_unit: DistanceUnit | None = None
    one_pip_means: str | None = None
    opening_hours: MarketOpeningHours | None = None
    rollover_details: MarketRolloverDetails | None = None
    slippage_factor: MarketDistanceRule | None = None
    special_info: tuple[str, ...] = ()
    sprint_markets_maximum_expiry_time: int | None = None
    sprint_markets_minimum_expiry_time: int | None = None
    stops_limits_allowed: bool | None = None


class DetailedMarketDealingRules(MarketDealingRules):
    market_order_preference: str | None = None


class DetailedMarketSnapshot(MarketSnapshot):
    bid: Decimal | None = None
    binary_odds: Decimal | None = None
    controlled_risk_extra_spread: Decimal | None = None
    offer: Decimal | None = None
    update_time: str | None = None


class MarketDetails(IGModel):
    dealing_rules: DetailedMarketDealingRules
    instrument: DetailedMarketInstrument
    snapshot: DetailedMarketSnapshot


class MarketsResponse(IGModel):
    market_details: tuple[MarketDetails, ...] = ()


class Category(IGModel):
    code: str
    non_tradeable: bool


class CategoriesResponse(IGModel):
    categories: tuple[Category, ...] = ()


class CategoryInstrument(IGModel):
    epic: str
    instrument_name: str | None = None
    expiry: str | None = None
    instrument_type: str | None = None
    lot_size: Decimal | None = None
    otc_tradeable: bool | None = None
    market_status: str | None = None
    delay_time: int | None = None
    bid: Decimal | None = None
    offer: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    net_change: Decimal | None = None
    percentage_change: Decimal | None = None
    update_time: str | None = None
    scaling_factor: Decimal | None = None


class PagingMetadata(IGModel):
    page_number: int
    page_size: int


class CategoryInstrumentsQuery(IGRequest):
    page_number: int = Field(default=0, ge=0)
    page_size: int = Field(default=150, ge=1, le=1000)
    reference_epic: str | None = None
    maturity_type: str | None = None


class CategoryInstrumentsResponse(IGModel):
    instruments: tuple[CategoryInstrument, ...] = ()
    metadata: PagingMetadata


class PriceValue(IGModel):
    bid: Decimal | None = None
    ask: Decimal | None = None
    last_traded: Decimal | None = None


class PricePoint(IGModel):
    snapshot_time: datetime | str | None = None
    snapshot_time_utc: str | None = None
    open_price: PriceValue | None = None
    close_price: PriceValue | None = None
    high_price: PriceValue | None = None
    low_price: PriceValue | None = None
    last_traded_volume: float | None = None


class PricePageData(IGModel):
    page_number: int
    page_size: int
    total_pages: int


class PriceAllowance(IGModel):
    allowance_expiry: int
    remaining_allowance: int
    total_allowance: int


class PriceMetadata(IGModel):
    page_data: PricePageData | None = None
    allowance: PriceAllowance | None = None
    size: int | None = None


class PricesResponse(IGModel):
    prices: tuple[PricePoint, ...] = ()
    instrument_type: str | None = None
    metadata: PriceMetadata | None = None


PriceResolution = Literal[
    "DAY",
    "HOUR",
    "HOUR_2",
    "HOUR_3",
    "HOUR_4",
    "MINUTE",
    "MINUTE_2",
    "MINUTE_3",
    "MINUTE_5",
    "MINUTE_10",
    "MINUTE_15",
    "MINUTE_30",
    "MONTH",
    "SECOND",
    "WEEK",
]


class PricesQuery(IGRequest):
    resolution: PriceResolution = "MINUTE"
    from_date: datetime | str | None = Field(default=None, alias="from")
    to_date: datetime | str | None = Field(default=None, alias="to")
    max_points: int | None = Field(default=None, alias="max", ge=1)
    page_size: int | None = Field(default=None, ge=0)
    page_number: int | None = Field(default=None, ge=1)


class MarketOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(
        self,
        epics: tuple[str, ...],
        *,
        filter: Literal["ALL", "SNAPSHOT_ONLY"] = "ALL",
    ) -> MarketsResponse:
        _validate_epics(epics)
        return self._executor.execute(
            "markets.list",
            MarketsResponse,
            query={"epics": ",".join(epics), "filter": filter},
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

    async def list(
        self,
        epics: tuple[str, ...],
        *,
        filter: Literal["ALL", "SNAPSHOT_ONLY"] = "ALL",
    ) -> MarketsResponse:
        _validate_epics(epics)
        return await self._executor.execute(
            "markets.list",
            MarketsResponse,
            query={"epics": ",".join(epics), "filter": filter},
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

    def list_instruments(
        self,
        category_id: str,
        query: CategoryInstrumentsQuery | None = None,
    ) -> CategoryInstrumentsResponse:
        return self._executor.execute(
            "categories.list_instruments",
            CategoryInstrumentsResponse,
            path={"category_id": category_id},
            query=query.to_wire() if query else None,
        )


class AsyncCategoriesOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> CategoriesResponse:
        return await self._executor.execute("categories.list", CategoriesResponse)

    async def list_instruments(
        self,
        category_id: str,
        query: CategoryInstrumentsQuery | None = None,
    ) -> CategoryInstrumentsResponse:
        return await self._executor.execute(
            "categories.list_instruments",
            CategoryInstrumentsResponse,
            path={"category_id": category_id},
            query=query.to_wire() if query else None,
        )


class PricesOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self, epic: str, query: PricesQuery | None = None) -> PricesResponse:
        return self._executor.execute(
            "prices.list",
            PricesResponse,
            path={"epic": epic},
            query=query.to_wire() if query else None,
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

    async def list(self, epic: str, query: PricesQuery | None = None) -> PricesResponse:
        return await self._executor.execute(
            "prices.list",
            PricesResponse,
            path={"epic": epic},
            query=query.to_wire() if query else None,
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


def _validate_epics(epics: tuple[str, ...]) -> None:
    if not 1 <= len(epics) <= 50:
        raise ValueError("epics must contain between 1 and 50 identifiers")
    if any(not epic for epic in epics):
        raise ValueError("epics must not contain empty identifiers")


def _date_time(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else value
