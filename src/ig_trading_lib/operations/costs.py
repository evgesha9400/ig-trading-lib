"""Typed indicative-cost operations."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import Field

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest


class IndicativeCostRequest(IGRequest):
    ask: Decimal
    bid: Decimal
    deal_currency_code: str = Field(min_length=3, max_length=3)
    deal_reference: str = Field(min_length=1)
    size: Decimal = Field(gt=0)
    direction: Literal["BUY", "SELL"] | None = None
    epic: str | None = None
    guaranteed_stop: bool | None = None
    instrument_id: str | None = None
    knockout_premium: Decimal | None = None
    price_level: Decimal | None = None
    stop_level: Decimal | None = None


class OpenIndicativeCostRequest(IndicativeCostRequest):
    pass


class CloseIndicativeCostRequest(IndicativeCostRequest):
    opening_level: Decimal


class EditIndicativeCostRequest(IndicativeCostRequest):
    opening_level: Decimal
    edit_type: str | None = None
    limit_level: Decimal | None = None


class IndicativeCostResponse(IGModel):
    indicative_quote_reference: str | None = None
    total_cost: Decimal | None = None
    currency_code: str | None = None


class OpenIndicativeCostResponse(IndicativeCostResponse):
    pass


class CloseIndicativeCostResponse(IndicativeCostResponse):
    pass


class EditIndicativeCostResponse(IndicativeCostResponse):
    pass


class IndicativeCostHistoryResponse(IGModel):
    costs: tuple[IndicativeCostResponse, ...] = ()


class IndicativeCostsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def quote_open(self, request: OpenIndicativeCostRequest) -> OpenIndicativeCostResponse:
        return self._executor.execute(
            "indicative_costs.quote_open",
            OpenIndicativeCostResponse,
            body=request.to_wire(),
        )

    def quote_close(self, request: CloseIndicativeCostRequest) -> CloseIndicativeCostResponse:
        return self._executor.execute(
            "indicative_costs.quote_close",
            CloseIndicativeCostResponse,
            body=request.to_wire(),
        )

    def quote_edit(self, request: EditIndicativeCostRequest) -> EditIndicativeCostResponse:
        return self._executor.execute(
            "indicative_costs.quote_edit",
            EditIndicativeCostResponse,
            body=request.to_wire(),
        )

    def get_durable_medium(self, quote_reference: str) -> IndicativeCostResponse:
        return self._executor.execute(
            "indicative_costs.get_durable_medium",
            IndicativeCostResponse,
            path={"quote_reference": quote_reference},
        )

    def history(
        self, from_date: datetime | str, to_date: datetime | str
    ) -> IndicativeCostHistoryResponse:
        return self._executor.execute(
            "indicative_costs.history",
            IndicativeCostHistoryResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
        )


class AsyncIndicativeCostsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def quote_open(self, request: OpenIndicativeCostRequest) -> OpenIndicativeCostResponse:
        return await self._executor.execute(
            "indicative_costs.quote_open",
            OpenIndicativeCostResponse,
            body=request.to_wire(),
        )

    async def quote_close(self, request: CloseIndicativeCostRequest) -> CloseIndicativeCostResponse:
        return await self._executor.execute(
            "indicative_costs.quote_close",
            CloseIndicativeCostResponse,
            body=request.to_wire(),
        )

    async def quote_edit(self, request: EditIndicativeCostRequest) -> EditIndicativeCostResponse:
        return await self._executor.execute(
            "indicative_costs.quote_edit",
            EditIndicativeCostResponse,
            body=request.to_wire(),
        )

    async def get_durable_medium(self, quote_reference: str) -> IndicativeCostResponse:
        return await self._executor.execute(
            "indicative_costs.get_durable_medium",
            IndicativeCostResponse,
            path={"quote_reference": quote_reference},
        )

    async def history(
        self, from_date: datetime | str, to_date: datetime | str
    ) -> IndicativeCostHistoryResponse:
        return await self._executor.execute(
            "indicative_costs.history",
            IndicativeCostHistoryResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
        )


def _time(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else value
