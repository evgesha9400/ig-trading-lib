"""Offline smoke test executed against an installed distribution."""

from __future__ import annotations

import asyncio
import importlib.util

import httpx

from ig_trading_lib import (
    IG,
    AsyncIG,
    CreatePositionRequest,
    Environment,
    IGConfig,
    MarketSearchResponse,
    SessionCredentials,
)


def _config() -> IGConfig:
    return IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials("key", "identifier", "password"),
    )


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("/session"):
        return httpx.Response(
            200,
            headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            json={"currentAccountId": "ABC123"},
        )
    return httpx.Response(200, json={"markets": [{"epic": "EPIC", "futureField": 1}]})


def _sync_smoke() -> None:
    with IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(_handler))) as ig:
        response = ig.operations.markets.search("EURUSD")
        assert isinstance(response, MarketSearchResponse)
        assert response.markets[0].future_field == 1
        assert set(ig.workflows.__dataclass_fields__) == {
            "discovery",
            "portfolio",
            "positions",
            "working_orders",
        }


async def _async_smoke() -> None:
    async with AsyncIG(
        _config(),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(_handler)),
    ) as ig:
        response = await ig.operations.markets.search("EURUSD")
        assert response.markets[0].epic == "EPIC"


def main() -> None:
    request = CreatePositionRequest(
        epic="EPIC",
        direction="BUY",
        size=1,
        order_type="MARKET",
        currency_code="GBP",
    )
    assert request.to_wire()["currencyCode"] == "GBP"
    assert importlib.util.find_spec("ig_trading_lib.client") is None
    _sync_smoke()
    asyncio.run(_async_smoke())


if __name__ == "__main__":
    main()
