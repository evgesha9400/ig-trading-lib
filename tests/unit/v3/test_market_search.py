import httpx

from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials


def test_market_search_authenticates_and_exposes_snake_case_fields() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            assert request.headers["Version"] == "2"
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={"currentAccountId": "ABC123"},
            )

        assert request.url.path == "/gateway/deal/markets"
        assert request.headers["CST"] == "cst"
        assert request.headers["X-SECURITY-TOKEN"] == "security"
        assert request.url.params["searchTerm"] == "EURUSD"
        return httpx.Response(
            200,
            json={"markets": [{"epic": "CS.D.EURUSD.TODAY.IP", "marketStatus": "TRADEABLE"}]},
        )

    client = IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        ),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    page = client.markets.search("EURUSD")

    assert page.items[0].epic == "CS.D.EURUSD.TODAY.IP"
    assert page.items[0].market_status == "TRADEABLE"
    assert len(requests) == 2
