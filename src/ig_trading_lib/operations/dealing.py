"""Typed dealing operations and requests."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import Field, model_validator

from ig_trading_lib._protocol.executor import AsyncExecutor, SyncExecutor
from ig_trading_lib.models import IGModel, IGRequest

Direction = Literal["BUY", "SELL"]
OrderType = Literal["LIMIT", "MARKET", "QUOTE", "STOP"]
TimeInForce = Literal["EXECUTE_AND_ELIMINATE", "FILL_OR_KILL", "GOOD_TILL_CANCELLED"]


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
    limit_distance: Decimal | None = None
    limit_level: Decimal | None = None
    stop_distance: Decimal | None = None
    stop_level: Decimal | None = None
    trailing_stop: bool | None = None
    trailing_stop_increment: Decimal | None = None
    deal_reference: str | None = None


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
