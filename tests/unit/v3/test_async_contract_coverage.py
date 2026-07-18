from collections.abc import AsyncIterator

import httpx
import pytest

from ig_trading_lib import AsyncIGClient, Environment, IGConfig, SessionCredentials, TradingPermit
from ig_trading_lib.async_services import AsyncResourceClient


@pytest.mark.asyncio
async def test_async_client_covers_position_and_named_resource_operations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        if request.url.path == "/gateway/deal/positions":
            return httpx.Response(200, json={"positions": []})
        if request.url.path == "/gateway/deal/positions/D1":
            return httpx.Response(200, json={"position": {"dealId": "D1"}})
        if request.url.path == "/gateway/deal/positions/otc/D1":
            return httpx.Response(200, json={"dealReference": "UPDATE"})
        if request.url.path == "/gateway/deal/positions/otc":
            return httpx.Response(200, json={"dealReference": request.method})
        if request.url.path == "/gateway/deal/accounts/preferences":
            return httpx.Response(200, json={"trailingStopsEnabled": True})
        if request.url.path == "/gateway/deal/working-orders":
            return httpx.Response(200, json={"workingOrders": []})
        if request.url.path == "/gateway/deal/watchlists":
            return httpx.Response(200, json={"result": request.method})
        raise AssertionError(f"Unexpected request: {request.method} {request.url.path}")

    async with AsyncIGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        trading_permit=TradingPermit(),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        assert (await client.positions.list()).positions == []
        assert (await client.positions.get("D1")).position["deal_id"] == "D1"
        assert (await client.positions.create({"epic": "EPIC"})).deal_reference == "POST"
        assert (await client.positions.update("D1", {"limitLevel": "2"})).deal_reference == "UPDATE"
        assert (await client.positions.close({"dealId": "D1"})).deal_reference == "DELETE"
        assert (await client.accounts.preferences()).trailing_stops_enabled is True
        assert (
            await client.accounts.update_preferences({"trailingStopsEnabled": True})
        ).trailing_stops_enabled
        assert (await client.working_orders.list(item_key="workingOrders")).items == ()
        assert (await client.watchlists.create({"name": "agent"})).result == "POST"
        assert (await client.watchlists.update({"epic": "EPIC"})).result == "PUT"
        assert (await client.watchlists.delete()).result == "DELETE"


@pytest.mark.asyncio
async def test_async_resource_client_gets_pages_and_raw_version_mutations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json={"items": [{"id": "second"}]})
        if request.method == "GET" and request.url.path.endswith("/resource"):
            return httpx.Response(
                200,
                json={
                    "items": [{"id": "first"}],
                    "metadata": {"paging": {"next": "/resource?page=2"}},
                },
            )
        return httpx.Response(200, json={"rawField": request.method})

    client = AsyncIGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        trading_permit=TradingPermit(),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    resource = AsyncResourceClient(client._transport, "/resource", version=1, guard=client._guard)

    assert (await resource.get("/one")).raw_field == "GET"
    items: list[str] = []
    pages: AsyncIterator[object] = resource.iter_pages()
    async for item in pages:
        items.append(item.id)
    assert items == ["first", "second"]
    assert (await resource.create({"a": 1})).raw_field == "POST"
    assert (await resource.update({"a": 2})).raw_field == "PUT"
    assert (await resource.delete()).raw_field == "DELETE"
    assert await client.v1.request("PUT", "/resource", json={"rawField": "value"}) == {
        "rawField": "PUT"
    }

    await client.close()
