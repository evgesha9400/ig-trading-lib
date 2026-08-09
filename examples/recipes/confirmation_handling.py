"""Retrieve a typed confirmation by deal reference."""

from ig_trading_lib import IG, AsyncIG, DealConfirmationResponse


def get_confirmation(ig: IG, deal_reference: str) -> DealConfirmationResponse:
    return ig.operations.confirmations.get(deal_reference)


async def get_confirmation_async(ig: AsyncIG, deal_reference: str) -> DealConfirmationResponse:
    return await ig.operations.confirmations.get(deal_reference)
