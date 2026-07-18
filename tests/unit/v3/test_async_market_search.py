import httpx
import pytest

from ig_trading_lib import AsyncIGClient, Environment, IGConfig, SessionCredentials


@pytest.mark.asyncio
async def test_async_client_matches_market_search_and_context_manager_behaviour() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        assert request.url.path == "/gateway/deal/markets"
        assert request.headers["CST"] == "cst"
        assert request.url.params["searchTerm"] == "EURUSD"
        return httpx.Response(200, json={"markets": [{"marketStatus": "TRADEABLE"}]})

    async with AsyncIGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        ),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        page = await client.markets.search("EURUSD")

    assert page.items[0].market_status == "TRADEABLE"
