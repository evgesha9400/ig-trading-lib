"""Retrieve a confirmation after a mutation returns a deal reference."""

from __future__ import annotations

from ig_trading_lib import AsyncIGClient, IGClient, IGModel


def get_confirmation(client: IGClient, deal_reference: str) -> IGModel:
    """Return IG's typed confirmation payload for one deal reference."""
    return client.confirms.get(f"/{deal_reference}")


async def get_confirmation_async(client: AsyncIGClient, deal_reference: str) -> IGModel:
    """Return IG's asynchronous typed confirmation payload for one deal reference."""
    return await client.confirms.get(f"/{deal_reference}")
