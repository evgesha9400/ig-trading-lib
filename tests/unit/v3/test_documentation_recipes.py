"""Execute the documented recipe sources against local mock transports only."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest

from examples.recipes.agent_discovery import load_agent_context, select_documented_operation
from examples.recipes.confirmation_handling import (
    get_confirmation,
    get_confirmation_async,
)
from examples.recipes.error_recovery import (
    recover_market_search,
    recover_market_search_async,
)
from examples.recipes.historical_pagination import (
    list_activity,
    list_activity_async,
)
from examples.recipes.market_discovery import discover_markets, discover_markets_async
from examples.recipes.safe_mutations import create_position, create_position_async
from examples.recipes.streaming import (
    aiter_market_price_updates,
    iter_market_price_updates,
    market_price_subscription,
)
from ig_trading_lib import (
    AsyncIGClient,
    Environment,
    IGClient,
    IGConfig,
    LiveTradingPermissionError,
    SessionCredentials,
    TradingPermit,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _config(environment: Environment = Environment.DEMO, *, max_retries: int = 0) -> IGConfig:
    return IGConfig(
        environment=environment,
        credentials=SessionCredentials("api-key", "identifier", "password"),
        max_retries=max_retries,
    )


def _sync_client(handler: Any, *, permit: TradingPermit | None = None) -> IGClient:
    return IGClient(
        _config(),
        trading_permit=permit,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def _async_client(handler: Any, *, permit: TradingPermit | None = None) -> AsyncIGClient:
    return AsyncIGClient(
        _config(),
        trading_permit=permit,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def _authenticated_response(request: httpx.Request) -> httpx.Response | None:
    if request.url.path == "/gateway/deal/session":
        return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
    return None


def test_market_discovery_recipes_are_deterministic() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        assert request.url.params["searchTerm"] == "EURUSD"
        return httpx.Response(200, json={"markets": [{"epic": "CS.D.EURUSD.TODAY.IP"}]})

    assert discover_markets(_sync_client(handler), "EURUSD") == ("CS.D.EURUSD.TODAY.IP",)


@pytest.mark.asyncio
async def test_async_market_discovery_recipe_is_deterministic() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        return httpx.Response(200, json={"markets": [{"epic": "CS.D.EURUSD.TODAY.IP"}]})

    client = _async_client(handler)
    assert await discover_markets_async(client, "EURUSD") == ("CS.D.EURUSD.TODAY.IP",)
    await client.close()


def test_historical_pagination_and_confirmation_recipes_follow_provider_links() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json={"activities": [{"id": "second"}]})
        if request.url.path == "/gateway/deal/history/activity":
            return httpx.Response(
                200,
                json={
                    "activities": [{"id": "first"}],
                    "metadata": {"paging": {"next": "/history/activity?page=2"}},
                },
            )
        if request.url.path == "/gateway/deal/confirms/REF-1":
            return httpx.Response(200, json={"dealStatus": "ACCEPTED"})
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = _sync_client(handler)
    assert [item.id for item in list_activity(client)] == ["first", "second"]
    assert get_confirmation(client, "REF-1").deal_status == "ACCEPTED"


@pytest.mark.asyncio
async def test_async_historical_pagination_and_confirmation_recipes_follow_provider_links() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json={"activities": [{"id": "second"}]})
        if request.url.path == "/gateway/deal/history/activity":
            return httpx.Response(
                200,
                json={
                    "activities": [{"id": "first"}],
                    "metadata": {"paging": {"next": "/history/activity?page=2"}},
                },
            )
        if request.url.path == "/gateway/deal/confirms/REF-1":
            return httpx.Response(200, json={"dealStatus": "ACCEPTED"})
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = _async_client(handler)
    assert [item.id async for item in list_activity_async(client)] == ["first", "second"]
    assert (await get_confirmation_async(client, "REF-1")).deal_status == "ACCEPTED"
    await client.close()


def test_safe_mutation_recipe_requires_a_client_with_a_permit() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        assert request.method == "POST"
        return httpx.Response(200, json={"dealReference": "REF-1"})

    demo_client = _sync_client(handler, permit=TradingPermit())
    assert (
        create_position(demo_client, {"epic": "EPIC", "direction": "BUY", "size": "1"}) == "REF-1"
    )

    live_client = IGClient(
        _config(Environment.LIVE),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    with pytest.raises(LiveTradingPermissionError):
        create_position(live_client, {"epic": "EPIC", "direction": "BUY", "size": "1"})


@pytest.mark.asyncio
async def test_async_safe_mutation_recipe_is_deterministic() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if response := _authenticated_response(request):
            return response
        return httpx.Response(200, json={"dealReference": "REF-1"})

    client = _async_client(handler, permit=TradingPermit())
    assert (
        await create_position_async(client, {"epic": "EPIC", "direction": "BUY", "size": "1"})
        == "REF-1"
    )
    await client.close()


def test_error_recovery_recipes_signal_retry_without_reissuing_a_request() -> None:
    calls = 0
    delays: list[float | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if response := _authenticated_response(request):
            return response
        calls += 1
        return httpx.Response(429, headers={"Retry-After": "7"}, json={"errorCode": "limit"})

    assert recover_market_search(_sync_client(handler), "EURUSD", delays.append) == ()
    assert calls == 1
    assert delays == [7.0]


@pytest.mark.asyncio
async def test_async_error_recovery_recipe_signals_retry_without_reissuing_a_request() -> None:
    calls = 0
    delays: list[float | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if response := _authenticated_response(request):
            return response
        calls += 1
        return httpx.Response(429, headers={"Retry-After": "7"}, json={"errorCode": "limit"})

    client = _async_client(handler)
    assert await recover_market_search_async(client, "EURUSD", delays.append) == ()
    assert calls == 1
    assert delays == [7.0]
    await client.close()


class _Streaming:
    def iter_updates(self, subscription: Any) -> Iterator[str]:
        assert subscription.items == ("MARKET:CS.D.EURUSD.TODAY.IP",)
        yield "sync-update"

    async def aiter_updates(self, subscription: Any) -> AsyncIterator[str]:
        assert subscription.fields == ("BID", "OFFER", "UPDATE_TIME")
        yield "async-update"


class _StreamingClient:
    streaming = _Streaming()


@pytest.mark.asyncio
async def test_streaming_recipe_builds_a_subscription_and_delegates_iteration() -> None:
    client = _StreamingClient()

    subscription = market_price_subscription("CS.D.EURUSD.TODAY.IP")
    assert subscription.key == "market-prices"
    assert list(iter_market_price_updates(client, "CS.D.EURUSD.TODAY.IP")) == ["sync-update"]
    assert [
        update async for update in aiter_market_price_updates(client, "CS.D.EURUSD.TODAY.IP")
    ] == ["async-update"]


def test_agent_discovery_recipe_only_selects_documented_operations() -> None:
    context = load_agent_context(PROJECT_ROOT / "docs" / "reference" / "public-api-index.json")
    operation = select_documented_operation(context, "market_search")

    assert context["generated_from"]["contract"] == "docs/contracts/public-api.yml"
    assert operation == {
        "category": "markets",
        "method": "GET",
        "name": "market_search",
        "path_template": "/markets",
    }
    with pytest.raises(KeyError):
        select_documented_operation(context, "invented_operation")
