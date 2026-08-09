import json

import httpx
import pytest

from ig_trading_lib import (
    IG,
    AuthenticationError,
    AuthorizationError,
    Environment,
    IGConfig,
    OAuthCredentials,
    ProviderRejectionError,
    RateLimitError,
    ResourceNotFoundError,
    SessionCredentials,
    TransportError,
)


def _sync_client(
    handler: httpx.MockTransport,
    *,
    credentials: SessionCredentials | OAuthCredentials | None = None,
    max_retries: int = 0,
) -> IG:
    return IG(
        IGConfig(
            environment=Environment.DEMO,
            credentials=credentials or SessionCredentials("api-key", "identifier", "password"),
            max_retries=max_retries,
        ),
        http_client=httpx.Client(transport=handler),
    )


@pytest.mark.parametrize(
    ("status", "error_type"),
    [
        (401, AuthenticationError),
        (403, AuthorizationError),
        (404, ResourceNotFoundError),
        (429, RateLimitError),
        (400, ProviderRejectionError),
    ],
)
def test_sync_transport_maps_provider_statuses_to_typed_errors(
    status: int, error_type: type[Exception]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        return httpx.Response(
            status,
            headers={"X-REQUEST-ID": "provider-request"},
            json={"errorCode": "provider.failure"},
        )

    with pytest.raises(error_type) as raised:
        _sync_client(httpx.MockTransport(handler)).operations.markets.search("EURUSD")

    error = raised.value
    assert error.request_id == "provider-request"
    assert error.operation_id


def test_sync_transport_retries_safe_status_and_network_failures() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        attempts += 1
        if attempts == 1:
            raise httpx.ReadTimeout("temporary", request=request)
        if attempts == 2:
            return httpx.Response(503, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"markets": []})

    page = _sync_client(httpx.MockTransport(handler), max_retries=2).operations.markets.search(
        "EURUSD"
    )

    assert page.markets == ()
    assert attempts == 3


def test_sync_oauth_refresh_and_streaming_session_bridge() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path == "/gateway/deal/session" and "Authorization" not in request.headers:
            return httpx.Response(
                200,
                json={
                    "accountId": "ABC123",
                    "lightstreamerEndpoint": "https://stream.example.test",
                    "oauthToken": {
                        "access_token": "expired",
                        "refresh_token": "refresh",
                        "expires_in": "0",
                    },
                },
            )
        if request.url.path == "/gateway/deal/session/refresh-token":
            assert json.loads(request.content) == {"refresh_token": "refresh"}
            return httpx.Response(
                200,
                json={
                    "access_token": "fresh",
                    "refresh_token": "next-refresh",
                    "expires_in": "3600",
                },
            )
        if request.url.path == "/gateway/deal/session":
            assert request.url.params["fetchSessionTokens"] == "true"
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={
                    "accountId": "ABC123",
                    "lightstreamerEndpoint": "https://stream.example.test",
                },
            )
        assert request.headers["Authorization"] == "Bearer fresh"
        return httpx.Response(200, json={"markets": []})

    client = _sync_client(
        httpx.MockTransport(handler),
        credentials=OAuthCredentials("api-key", "identifier", "password"),
    )

    assert client.operations.markets.search("EURUSD").markets == ()
    session = client._transport.streaming_session()

    assert session.account_id == "ABC123"
    assert session.cst == "cst"
    assert any(request.url.path.endswith("refresh-token") for request in calls)


def test_authentication_network_failure_is_a_typed_transport_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline", request=request)

    with pytest.raises(TransportError):
        _sync_client(httpx.MockTransport(handler)).operations.markets.search("EURUSD")
