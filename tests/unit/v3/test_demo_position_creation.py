import json

import httpx

from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials


def test_demo_position_creation_sends_the_request_after_authentication() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={},
            )

        assert request.method == "POST"
        assert request.url.path == "/gateway/deal/positions/otc"
        assert request.headers["Version"] == "2"
        assert json.loads(request.content) == {"epic": "CS.D.EURUSD.TODAY.IP"}
        return httpx.Response(200, json={"dealReference": "DIAAAABBBCCC123"})

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

    result = client.positions.create({"epic": "CS.D.EURUSD.TODAY.IP"})

    assert result.deal_reference == "DIAAAABBBCCC123"
