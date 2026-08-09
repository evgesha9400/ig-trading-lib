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


class OpenIndicativeCostResponse(IGModel):
    borrowing_charge: Decimal | None = None
    closing_commission: Decimal | None = None
    closing_fx_fee: Decimal | None = None
    closing_iftt: Decimal | None = None
    closing_spread: Decimal | None = None
    currency_code_iso: str | None = None
    daily_running_fx_fee: Decimal | None = None
    etp_entry_cost: Decimal | None = None
    etp_exit_cost: Decimal | None = None
    etp_ongoing_cost: Decimal | None = None
    guaranteed_stop_deposit: Decimal | None = None
    guaranteed_stop_return: Decimal | None = None
    indicative_quote_reference: str | None = None
    inducements: Decimal | None = None
    knockout_premium_deposit: Decimal | None = None
    knockout_premium_return: Decimal | None = None
    notional_value: Decimal | None = None
    notional_value_in_user_currency: Decimal | None = None
    opening_commission: Decimal | None = None
    opening_fx_fee: Decimal | None = None
    opening_iftt: Decimal | None = None
    opening_spread: Decimal | None = None
    overnight_funding_fee: Decimal | None = None


class ClosingIndicativeCost(IGModel):
    closing_commission: Decimal | None = None
    closing_fx_fee: Decimal | None = None
    closing_iftt: Decimal | None = None
    closing_spread: Decimal | None = None
    etp_exit_cost: Decimal | None = None
    guaranteed_stop_return: Decimal | None = None
    indicative_quote_reference: str | None = None
    knockout_premium_return: Decimal | None = None
    notional_value: Decimal | None = None
    notional_value_in_user_currency: Decimal | None = None


class CloseIndicativeCostResponse(IGModel):
    close: ClosingIndicativeCost | None = None
    currency_code_iso: str | None = None


class EditIndicativeCostResponse(IGModel):
    currency_code_iso: str | None = None
    limit: ClosingIndicativeCost | None = None
    stop: ClosingIndicativeCost | None = None


class IndicativeCostHistoryEntry(IGModel):
    created_timestamp: str | None = None
    direction: str | None = None
    indicative_quote_reference: str | None = None
    instrument_name: str | None = None
    type: str | None = None


class IndicativeCostHistoryPagination(IGModel):
    page_number: int | None = None
    page_size: int | None = None
    total_elements: int | None = None
    total_pages: int | None = None


class IndicativeCostHistoryQuery(IGRequest):
    page_size: int | None = Field(default=None, ge=0)
    page_number: int | None = Field(default=None, ge=0)
    type: str | None = Field(default=None, min_length=1)


class IndicativeCostHistoryResponse(IGModel):
    costs_and_charges_history: tuple[IndicativeCostHistoryEntry, ...] = ()
    pagination: IndicativeCostHistoryPagination | None = None


class DurableMediumResponse(IGModel):
    content: bytes
    content_type: str | None = None


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

    def get_durable_medium(self, quote_reference: str) -> DurableMediumResponse:
        return self._executor.execute(
            "indicative_costs.get_durable_medium",
            DurableMediumResponse,
            path={"quote_reference": quote_reference},
        )

    def history(
        self,
        from_date: datetime | str,
        to_date: datetime | str,
        query: IndicativeCostHistoryQuery | None = None,
    ) -> IndicativeCostHistoryResponse:
        return self._executor.execute(
            "indicative_costs.history",
            IndicativeCostHistoryResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
            query=query.to_wire() if query else None,
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

    async def get_durable_medium(self, quote_reference: str) -> DurableMediumResponse:
        return await self._executor.execute(
            "indicative_costs.get_durable_medium",
            DurableMediumResponse,
            path={"quote_reference": quote_reference},
        )

    async def history(
        self,
        from_date: datetime | str,
        to_date: datetime | str,
        query: IndicativeCostHistoryQuery | None = None,
    ) -> IndicativeCostHistoryResponse:
        return await self._executor.execute(
            "indicative_costs.history",
            IndicativeCostHistoryResponse,
            path={"from_date": _time(from_date), "to_date": _time(to_date)},
            query=query.to_wire() if query else None,
        )


def _time(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else value
