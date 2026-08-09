"""Common dealing journeys composed only from faithful operations."""

from __future__ import annotations

from dataclasses import dataclass

from ig_trading_lib.errors import DealConfirmationError, IGError
from ig_trading_lib.operations.dealing import (
    AmendPositionRequest,
    AmendWorkingOrderRequest,
    AsyncConfirmationsOperations,
    AsyncPositionsOperations,
    AsyncWorkingOrdersOperations,
    ClosePositionRequest,
    ConfirmationsOperations,
    CreatePositionRequest,
    CreateWorkingOrderRequest,
    DealConfirmationResponse,
    PositionsOperations,
    WorkingOrdersOperations,
)


@dataclass(frozen=True, slots=True)
class PositionWorkflow:
    positions: PositionsOperations
    confirmations: ConfirmationsOperations

    def open_and_confirm(self, request: CreatePositionRequest) -> DealConfirmationResponse:
        result = self.positions.create(request)
        return _confirm(self.confirmations, result.deal_reference)

    def amend_and_confirm(
        self, deal_id: str, request: AmendPositionRequest
    ) -> DealConfirmationResponse:
        result = self.positions.amend(deal_id, request)
        return _confirm(self.confirmations, result.deal_reference)

    def close_and_confirm(self, request: ClosePositionRequest) -> DealConfirmationResponse:
        result = self.positions.close(request)
        return _confirm(self.confirmations, result.deal_reference)


@dataclass(frozen=True, slots=True)
class AsyncPositionWorkflow:
    positions: AsyncPositionsOperations
    confirmations: AsyncConfirmationsOperations

    async def open_and_confirm(self, request: CreatePositionRequest) -> DealConfirmationResponse:
        result = await self.positions.create(request)
        return await _confirm_async(self.confirmations, result.deal_reference)

    async def amend_and_confirm(
        self, deal_id: str, request: AmendPositionRequest
    ) -> DealConfirmationResponse:
        result = await self.positions.amend(deal_id, request)
        return await _confirm_async(self.confirmations, result.deal_reference)

    async def close_and_confirm(self, request: ClosePositionRequest) -> DealConfirmationResponse:
        result = await self.positions.close(request)
        return await _confirm_async(self.confirmations, result.deal_reference)


@dataclass(frozen=True, slots=True)
class WorkingOrderWorkflow:
    working_orders: WorkingOrdersOperations
    confirmations: ConfirmationsOperations

    def place_and_confirm(self, request: CreateWorkingOrderRequest) -> DealConfirmationResponse:
        result = self.working_orders.create(request)
        return _confirm(self.confirmations, result.deal_reference)

    def amend_and_confirm(
        self, deal_id: str, request: AmendWorkingOrderRequest
    ) -> DealConfirmationResponse:
        result = self.working_orders.amend(deal_id, request)
        return _confirm(self.confirmations, result.deal_reference)

    def cancel_and_confirm(self, deal_id: str) -> DealConfirmationResponse:
        result = self.working_orders.delete(deal_id)
        return _confirm(self.confirmations, result.deal_reference)


@dataclass(frozen=True, slots=True)
class AsyncWorkingOrderWorkflow:
    working_orders: AsyncWorkingOrdersOperations
    confirmations: AsyncConfirmationsOperations

    async def place_and_confirm(
        self, request: CreateWorkingOrderRequest
    ) -> DealConfirmationResponse:
        result = await self.working_orders.create(request)
        return await _confirm_async(self.confirmations, result.deal_reference)

    async def amend_and_confirm(
        self, deal_id: str, request: AmendWorkingOrderRequest
    ) -> DealConfirmationResponse:
        result = await self.working_orders.amend(deal_id, request)
        return await _confirm_async(self.confirmations, result.deal_reference)

    async def cancel_and_confirm(self, deal_id: str) -> DealConfirmationResponse:
        result = await self.working_orders.delete(deal_id)
        return await _confirm_async(self.confirmations, result.deal_reference)


def _confirm(
    confirmations: ConfirmationsOperations, deal_reference: str
) -> DealConfirmationResponse:
    try:
        return confirmations.get(deal_reference)
    except IGError as error:
        raise DealConfirmationError(deal_reference, cause=error) from error


async def _confirm_async(
    confirmations: AsyncConfirmationsOperations, deal_reference: str
) -> DealConfirmationResponse:
    try:
        return await confirmations.get(deal_reference)
    except IGError as error:
        raise DealConfirmationError(deal_reference, cause=error) from error
