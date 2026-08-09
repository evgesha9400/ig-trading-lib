import asyncio
import json

import httpx
import pytest

from ig_trading_lib import AsyncIG, Environment, IGConfig, OAuthCredentials


@pytest.mark.asyncio
async def test_expired_oauth_token_refreshes_once_for_concurrent_safe_reads() -> None:
    refresh_requests = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal refresh_requests
        if request.url.path == "/gateway/deal/session":
            assert request.headers["Version"] == "3"
            return httpx.Response(
                200,
                json={
                    "accountId": "ABC123",
                    "lightstreamerEndpoint": "https://stream.example.test",
                    "oauthToken": {
                        "access_token": "expired-token",
                        "refresh_token": "refresh-token",
                        "expires_in": "0",
                    },
                },
            )
        if request.url.path == "/gateway/deal/session/refresh-token":
            refresh_requests += 1
            assert json.loads(request.content) == {"refresh_token": "refresh-token"}
            return httpx.Response(
                200,
                json={
                    "access_token": "fresh-token",
                    "refresh_token": "next-refresh-token",
                    "expires_in": "3600",
                },
            )
        assert request.headers["Authorization"] == "Bearer fresh-token"
        return httpx.Response(200, json={"markets": [{"epic": "CS.D.EURUSD.TODAY.IP"}]})

    client = AsyncIG(
        IGConfig(
            environment=Environment.DEMO,
            credentials=OAuthCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        ),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    first, second = await asyncio.gather(
        client.operations.markets.search("EURUSD"),
        client.operations.markets.search("GBPUSD"),
    )

    assert first.markets[0].epic == "CS.D.EURUSD.TODAY.IP"
    assert second.markets[0].epic == "CS.D.EURUSD.TODAY.IP"
    assert refresh_requests == 1
