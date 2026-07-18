import httpx
import pytest

from ig_trading_lib import (
    Environment,
    IGClient,
    IGConfig,
    ProviderRejectionError,
    SessionCredentials,
)


def test_errors_redact_provider_credentials_and_every_request_has_a_correlation_id() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        return httpx.Response(
            400,
            json={
                "errorCode": "invalid.input",
                "accessToken": "provider-secret",
                "password": "provider-password",
            },
        )

    credentials = SessionCredentials(
        api_key="api-key",
        identifier="identifier",
        password="password",
    )
    client = IGClient(
        IGConfig(environment=Environment.DEMO, credentials=credentials),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ProviderRejectionError) as raised:
        client.markets.search("EURUSD")

    assert "api-key" not in repr(credentials)
    assert "password" not in repr(credentials)
    assert raised.value.details["accessToken"] == "[REDACTED]"
    assert raised.value.details["password"] == "[REDACTED]"
    assert all(request.headers["X-CORRELATION-ID"] for request in requests)
