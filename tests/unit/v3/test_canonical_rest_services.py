import httpx

from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials, TradingPermit


def test_canonical_services_use_documented_paths_and_versions() -> None:
    calls: list[tuple[str, str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, request.url.path, request.headers["Version"]))
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        if request.url.path == "/gateway/deal/positions":
            return httpx.Response(200, json={"positions": [{"dealId": "D1"}]})
        if request.url.path == "/gateway/deal/positions/D1":
            return httpx.Response(200, json={"position": {"dealId": "D1"}})
        if request.url.path == "/gateway/deal/client-sentiment":
            return httpx.Response(200, json={"clientSentiment": []})
        if request.url.path == "/gateway/deal/working-orders":
            return httpx.Response(200, json={"workingOrders": []})
        raise AssertionError(f"Unexpected request: {request.method} {request.url.path}")

    client = IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert client.positions.list().positions[0]["deal_id"] == "D1"
    assert client.positions.get("D1").position["deal_id"] == "D1"
    assert client.sentiment.get().client_sentiment == []
    assert client.working_orders.list(item_key="workingOrders").items == ()

    assert calls[1:] == [
        ("GET", "/gateway/deal/positions", "2"),
        ("GET", "/gateway/deal/positions/D1", "2"),
        ("GET", "/gateway/deal/client-sentiment", "1"),
        ("GET", "/gateway/deal/working-orders", "2"),
    ]


def test_sync_position_mutations_use_the_documented_otc_versions() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        return httpx.Response(200, json={"dealReference": request.method})

    client = IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        trading_permit=TradingPermit(),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert client.positions.update("D1", {"limitLevel": "2"}).deal_reference == "PUT"
    assert client.positions.close({"dealId": "D1"}).deal_reference == "DELETE"
