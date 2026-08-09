"""Open and confirm a typed position request."""

from ig_trading_lib import IG, AsyncIG, CreatePositionRequest, DealConfirmationResponse


def open_position(ig: IG, request: CreatePositionRequest) -> DealConfirmationResponse:
    return ig.workflows.positions.open_and_confirm(request)


async def open_position_async(
    ig: AsyncIG, request: CreatePositionRequest
) -> DealConfirmationResponse:
    return await ig.workflows.positions.open_and_confirm(request)
