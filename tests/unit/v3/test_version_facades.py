import httpx
import pytest

from ig_trading_lib import (
    AsyncIGClient,
    Environment,
    IGClient,
    IGConfig,
    LiveTradingPermissionError,
    SessionCredentials,
)


def test_version_facades_preserve_ig_wire_payloads_and_endpoint_versions() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session" and "CST" not in request.headers:
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        assert request.url.path == "/gateway/deal/positions/otc"
        assert request.headers["Version"] == "2"
        return httpx.Response(200, json={"dealReference": "DIAAAABBBCCC123"})

    client = IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.v2.positions.create({"epic": "CS.D.EURUSD.TODAY.IP"}, suffix="/otc")

    assert response == {"dealReference": "DIAAAABBBCCC123"}


def test_version_facades_apply_the_live_mutation_guard_before_authentication() -> None:
    client = IGClient(
        IGConfig(
            environment=Environment.LIVE,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        http_client=httpx.Client(
            transport=httpx.MockTransport(lambda _: pytest.fail("network call"))
        ),
    )

    with pytest.raises(LiveTradingPermissionError):
        client.v1.watchlists.create({"name": "unsafe"})


@pytest.mark.asyncio
async def test_async_version_facades_match_the_raw_sync_surface() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session" and "CST" not in request.headers:
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        assert request.headers["Version"] == "1"
        return httpx.Response(200, json={"accountId": "ABC123"})

    client = AsyncIGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    response = await client.v1.request("GET", "/session")

    assert response == {"accountId": "ABC123"}
