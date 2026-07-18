"""Submit provider-defined order bodies through the guarded position facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ig_trading_lib import AsyncIGClient, IGClient


def create_position(client: IGClient, provider_request: Mapping[str, Any]) -> str:
    """Create a position and return its provider deal reference after caller review."""
    return str(client.positions.create(provider_request).deal_reference)


async def create_position_async(client: AsyncIGClient, provider_request: Mapping[str, Any]) -> str:
    """Create a position asynchronously and return its provider deal reference."""
    response = await client.positions.create(provider_request)
    return str(response.deal_reference)
