"""Delegate safe-read retry decisions without retrying mutations."""

from collections.abc import Callable

from ig_trading_lib import IG, AsyncIG, RateLimitError, TransportError


def recover_market_search(
    ig: IG, search_term: str, schedule_retry: Callable[[float | None], None]
) -> tuple[str, ...]:
    try:
        return tuple(market.epic for market in ig.operations.markets.search(search_term).markets)
    except RateLimitError as error:
        schedule_retry(error.retry_after_seconds)
    except TransportError:
        schedule_retry(None)
    return ()


async def recover_market_search_async(
    ig: AsyncIG, search_term: str, schedule_retry: Callable[[float | None], None]
) -> tuple[str, ...]:
    try:
        response = await ig.operations.markets.search(search_term)
        return tuple(market.epic for market in response.markets)
    except RateLimitError as error:
        schedule_retry(error.retry_after_seconds)
    except TransportError:
        schedule_retry(None)
    return ()
