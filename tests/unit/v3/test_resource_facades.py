import httpx

from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials


def test_accounts_facade_uses_the_shared_authenticated_transport() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={},
            )

        assert request.url.path == "/gateway/deal/accounts"
        assert request.headers["Version"] == "1"
        return httpx.Response(200, json={"accounts": [{"accountId": "ABC123"}]})

    client = IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials("api-key", "identifier", "password"),
        ),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    page = client.accounts.list()

    assert page.items[0].account_id == "ABC123"
