"""Signal a scheduler to retry idempotent reads without retrying mutations here."""

from __future__ import annotations

from collections.abc import Callable

from ig_trading_lib import AsyncIGClient, IGClient, RateLimitError, TransportError


def recover_market_search(
    client: IGClient,
    search_term: str,
    schedule_retry: Callable[[float | None], None],
) -> tuple[str, ...]:
    """Return markets or delegate a safe read retry decision to the caller."""
    try:
        return tuple(market.epic for market in client.markets.search(search_term).items)
    except RateLimitError as error:
        schedule_retry(error.retry_after_seconds)
    except TransportError:
        schedule_retry(None)
    return ()


async def recover_market_search_async(
    client: AsyncIGClient,
    search_term: str,
    schedule_retry: Callable[[float | None], None],
) -> tuple[str, ...]:
    """Return async markets or delegate a safe read retry decision to the caller."""
    try:
        markets = await client.markets.search(search_term)
        return tuple(market.epic for market in markets.items)
    except RateLimitError as error:
        schedule_retry(error.retry_after_seconds)
    except TransportError:
        schedule_retry(None)
    return ()
