"""Typed dealing operations and requests."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import Field, model_validator

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest

Direction = Literal["BUY", "SELL"]
OrderType = Literal["LIMIT", "MARKET", "QUOTE"]
TimeInForce = Literal["EXECUTE_AND_ELIMINATE", "FILL_OR_KILL"]


class DealReferenceResponse(IGModel):
    deal_reference: str


class DealConfirmationResponse(IGModel):
    deal_reference: str
    deal_id: str | None = None
    deal_status: str | None = None
    reason: str | None = None
    status: str | None = None


class Position(IGModel):
    deal_id: str
    deal_reference: str | None = None
    direction: Direction | None = None
    size: Decimal | None = None
    level: Decimal | None = None
    limit_level: Decimal | None = None
    stop_level: Decimal | None = None


class DealingMarket(IGModel):
    epic: str
    instrument_name: str | None = None
    market_status: str | None = None
    bid: Decimal | None = None
    offer: Decimal | None = None


class PositionSummary(IGModel):
    position: Position
    market: DealingMarket


class PositionsResponse(IGModel):
    positions: tuple[PositionSummary, ...] = ()


class PositionResponse(PositionSummary):
    pass


class CreatePositionRequest(IGRequest):
    epic: str = Field(min_length=1)
    direction: Direction
    size: Decimal = Field(gt=0)
    order_type: OrderType
    currency_code: str = Field(min_length=3, max_length=3)
    expiry: str = "-"
    force_open: bool = True
    guaranteed_stop: bool = False
    level: Decimal | None = None
    quote_id: str | None = None
    time_in_force: TimeInForce | None = None
    limit_distance: Decimal | None = None
    limit_level: Decimal | None = None
    stop_distance: Decimal | None = None
    stop_level: Decimal | None = None
    trailing_stop: bool | None = None
    trailing_stop_increment: Decimal | None = None
    deal_reference: str | None = None

    @model_validator(mode="after")
    def validate_provider_constraints(self) -> CreatePositionRequest:
        _validate_order_level(self.order_type, self.level, self.quote_id)
        _require_force_open_for_limits_and_stops(self)
        _require_one_of(self.limit_level, self.limit_distance, "limit_level", "limit_distance")
        _require_one_of(self.stop_level, self.stop_distance, "stop_level", "stop_distance")
        _validate_guaranteed_stop(self)
        _validate_trailing_stop(self)
        return self


def _validate_order_level(
    order_type: OrderType,
    level: Decimal | None,
    quote_id: str | None,
) -> None:
    if order_type == "LIMIT" and level is None:
        raise ValueError("LIMIT orders require level")
    if order_type == "LIMIT" and quote_id is not None:
        raise ValueError("LIMIT orders do not accept quote_id")
    if order_type == "MARKET" and (level is not None or quote_id is not None):
        raise ValueError("MARKET orders do not accept level or quote_id")
    if order_type == "QUOTE" and (level is None or quote_id is None):
        raise ValueError("QUOTE orders require level and quote_id")


def _require_force_open_for_limits_and_stops(request: CreatePositionRequest) -> None:
    has_limit_or_stop = any(
        value is not None
        for value in (
            request.limit_distance,
            request.limit_level,
            request.stop_distance,
            request.stop_level,
        )
    )
    if has_limit_or_stop and not request.force_open:
        raise ValueError("force_open must be true when a limit or stop is set")


def _require_one_of(
    first: Decimal | None,
    second: Decimal | None,
    first_name: str,
    second_name: str,
) -> None:
    if first is not None and second is not None:
        raise ValueError(f"Set only one of {first_name} and {second_name}")


def _validate_guaranteed_stop(request: CreatePositionRequest) -> None:
    if not request.guaranteed_stop:
        return
    has_exactly_one_stop = (request.stop_level is None) != (request.stop_distance is None)
    if not has_exactly_one_stop:
        raise ValueError("A guaranteed stop requires exactly one stop_level or stop_distance")


def _validate_trailing_stop(request: CreatePositionRequest) -> None:
    if request.trailing_stop is False and request.trailing_stop_increment is not None:
        raise ValueError("trailing_stop_increment requires trailing_stop")
    if request.trailing_stop is not True:
        return
    if request.stop_level is not None:
        raise ValueError("A trailing stop does not accept stop_level")
    if request.guaranteed_stop:
        raise ValueError("A trailing stop cannot be guaranteed")
    if request.stop_distance is None or request.trailing_stop_increment is None:
        raise ValueError("A trailing stop requires stop_distance and trailing_stop_increment")


class AmendPositionRequest(IGRequest):
    limit_level: Decimal | None = None
    stop_level: Decimal | None = None
    guaranteed_stop: bool | None = None
    trailing_stop: bool | None = None
    trailing_stop_distance: Decimal | None = None
    trailing_stop_increment: Decimal | None = None


class ClosePositionRequest(IGRequest):
    direction: Direction
    size: Decimal = Field(gt=0)
    order_type: OrderType = "MARKET"
    deal_id: str | None = None
    epic: str | None = None
    expiry: str | None = None
    level: Decimal | None = None
    quote_id: str | None = None
    time_in_force: TimeInForce | None = None

    @model_validator(mode="after")
    def identify_position(self) -> ClosePositionRequest:
        if self.deal_id is None and self.epic is None:
            raise ValueError("Either deal_id or epic is required")
        return self


class WorkingOrderData(IGModel):
    deal_id: str
    epic: str
    direction: Direction | None = None
    order_size: Decimal | None = None
    order_level: Decimal | None = None
    order_type: str | None = None


class WorkingOrderSummary(IGModel):
    working_order_data: WorkingOrderData
    market_data: DealingMarket


class WorkingOrdersResponse(IGModel):
    working_orders: tuple[WorkingOrderSummary, ...] = ()


class CreateWorkingOrderRequest(IGRequest):
    epic: str = Field(min_length=1)
    direction: Direction
    size: Decimal = Field(gt=0)
    level: Decimal
    order_type: Literal["LIMIT", "STOP"]
    currency_code: str = Field(min_length=3, max_length=3)
    expiry: str = "-"
    force_open: bool = True
    guaranteed_stop: bool = False
    good_till_date: str | None = None
    limit_distance: Decimal | None = None
    limit_level: Decimal | None = None
    stop_distance: Decimal | None = None
    stop_level: Decimal | None = None
    time_in_force: Literal["GOOD_TILL_CANCELLED", "GOOD_TILL_DATE"] = "GOOD_TILL_CANCELLED"


class AmendWorkingOrderRequest(IGRequest):
    level: Decimal
    order_type: Literal["LIMIT", "STOP"]
    time_in_force: Literal["GOOD_TILL_CANCELLED", "GOOD_TILL_DATE"]
    good_till_date: str | None = None
    limit_distance: Decimal | None = None
    limit_level: Decimal | None = None
    stop_distance: Decimal | None = None
    stop_level: Decimal | None = None


class RepeatDealingWindowResponse(IGModel):
    remaining_seconds: int | None = None


class ConfirmationsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def get(self, deal_reference: str) -> DealConfirmationResponse:
        return self._executor.execute(
            "confirmations.get",
            DealConfirmationResponse,
            path={"deal_reference": deal_reference},
        )


class AsyncConfirmationsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def get(self, deal_reference: str) -> DealConfirmationResponse:
        return await self._executor.execute(
            "confirmations.get",
            DealConfirmationResponse,
            path={"deal_reference": deal_reference},
        )


class PositionsOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> PositionsResponse:
        return self._executor.execute("positions.list", PositionsResponse)

    def get(self, deal_id: str) -> PositionResponse:
        return self._executor.execute("positions.get", PositionResponse, path={"deal_id": deal_id})

    def create(self, request: CreatePositionRequest) -> DealReferenceResponse:
        return self._executor.execute(
            "positions.create", DealReferenceResponse, body=request.to_wire()
        )

    def amend(self, deal_id: str, request: AmendPositionRequest) -> DealReferenceResponse:
        return self._executor.execute(
            "positions.amend",
            DealReferenceResponse,
            path={"deal_id": deal_id},
            body=request.to_wire(),
        )

    def close(self, request: ClosePositionRequest) -> DealReferenceResponse:
        return self._executor.execute(
            "positions.close", DealReferenceResponse, body=request.to_wire()
        )


class AsyncPositionsOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> PositionsResponse:
        return await self._executor.execute("positions.list", PositionsResponse)

    async def get(self, deal_id: str) -> PositionResponse:
        return await self._executor.execute(
            "positions.get", PositionResponse, path={"deal_id": deal_id}
        )

    async def create(self, request: CreatePositionRequest) -> DealReferenceResponse:
        return await self._executor.execute(
            "positions.create", DealReferenceResponse, body=request.to_wire()
        )

    async def amend(self, deal_id: str, request: AmendPositionRequest) -> DealReferenceResponse:
        return await self._executor.execute(
            "positions.amend",
            DealReferenceResponse,
            path={"deal_id": deal_id},
            body=request.to_wire(),
        )

    async def close(self, request: ClosePositionRequest) -> DealReferenceResponse:
        return await self._executor.execute(
            "positions.close", DealReferenceResponse, body=request.to_wire()
        )


class WorkingOrdersOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def list(self) -> WorkingOrdersResponse:
        return self._executor.execute("working_orders.list", WorkingOrdersResponse)

    def create(self, request: CreateWorkingOrderRequest) -> DealReferenceResponse:
        return self._executor.execute(
            "working_orders.create", DealReferenceResponse, body=request.to_wire()
        )

    def amend(self, deal_id: str, request: AmendWorkingOrderRequest) -> DealReferenceResponse:
        return self._executor.execute(
            "working_orders.amend",
            DealReferenceResponse,
            path={"deal_id": deal_id},
            body=request.to_wire(),
        )

    def delete(self, deal_id: str) -> DealReferenceResponse:
        return self._executor.execute(
            "working_orders.delete", DealReferenceResponse, path={"deal_id": deal_id}
        )


class AsyncWorkingOrdersOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def list(self) -> WorkingOrdersResponse:
        return await self._executor.execute("working_orders.list", WorkingOrdersResponse)

    async def create(self, request: CreateWorkingOrderRequest) -> DealReferenceResponse:
        return await self._executor.execute(
            "working_orders.create", DealReferenceResponse, body=request.to_wire()
        )

    async def amend(self, deal_id: str, request: AmendWorkingOrderRequest) -> DealReferenceResponse:
        return await self._executor.execute(
            "working_orders.amend",
            DealReferenceResponse,
            path={"deal_id": deal_id},
            body=request.to_wire(),
        )

    async def delete(self, deal_id: str) -> DealReferenceResponse:
        return await self._executor.execute(
            "working_orders.delete", DealReferenceResponse, path={"deal_id": deal_id}
        )


class RepeatDealingWindowOperations:
    def __init__(self, executor: SyncExecutor) -> None:
        self._executor = executor

    def get(self) -> RepeatDealingWindowResponse:
        return self._executor.execute("repeat_dealing_window.get", RepeatDealingWindowResponse)


class AsyncRepeatDealingWindowOperations:
    def __init__(self, executor: AsyncExecutor) -> None:
        self._executor = executor

    async def get(self) -> RepeatDealingWindowResponse:
        return await self._executor.execute(
            "repeat_dealing_window.get", RepeatDealingWindowResponse
        )
