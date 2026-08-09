import json

import httpx
import pytest

from ig_trading_lib import (
    AmbiguousExecutionError,
    AsyncIG,
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


def _async_client(
    handler: httpx.MockTransport,
    *,
    credentials: SessionCredentials | OAuthCredentials | None = None,
    max_retries: int = 0,
) -> AsyncIG:
    return AsyncIG(
        IGConfig(
            environment=Environment.DEMO,
            credentials=credentials or SessionCredentials("api-key", "identifier", "password"),
            max_retries=max_retries,
        ),
        http_client=httpx.AsyncClient(transport=handler),
    )


@pytest.mark.asyncio
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
async def test_async_transport_maps_provider_statuses_to_typed_errors(
    status: int, error_type: type[Exception]
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        return httpx.Response(status, json={"errorCode": "provider.failure"})

    with pytest.raises(error_type):
        await _async_client(httpx.MockTransport(handler)).operations.markets.search("EURUSD")


@pytest.mark.asyncio
async def test_async_transport_retries_safe_requests_and_marks_mutation_outcomes_ambiguous() -> (
    None
):
    attempts = 0

    def retry_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        attempts += 1
        if attempts == 1:
            raise httpx.ReadTimeout("temporary", request=request)
        return httpx.Response(200, json={"markets": []})

    assert (
        await _async_client(
            httpx.MockTransport(retry_handler), max_retries=1
        ).operations.markets.search("EURUSD")
    ).markets == ()
    assert attempts == 2

    def mutation_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        raise httpx.ReadTimeout("ambiguous", request=request)

    with pytest.raises(AmbiguousExecutionError):
        await _async_client(httpx.MockTransport(mutation_handler))._transport.request(
            "POST", "/positions/otc", version=2, json={"epic": "EPIC"}
        )


@pytest.mark.asyncio
async def test_async_oauth_streaming_session_and_forced_refresh() -> None:
    initial_logins = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal initial_logins
        if request.url.path == "/gateway/deal/session" and "Authorization" not in request.headers:
            initial_logins += 1
            return httpx.Response(
                200,
                json={
                    "accountId": "ABC123",
                    "lightstreamerEndpoint": "https://stream.example.test",
                    "oauthToken": {
                        "access_token": f"token-{initial_logins}",
                        "refresh_token": "refresh",
                        "expires_in": "0",
                    },
                },
            )
        if request.url.path == "/gateway/deal/session/refresh-token":
            assert json.loads(request.content) == {"refresh_token": "refresh"}
            return httpx.Response(
                200,
                json={"access_token": "fresh", "refresh_token": "refresh", "expires_in": "3600"},
            )
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
                json={
                    "accountId": "ABC123",
                    "lightstreamerEndpoint": "https://stream.example.test",
                },
            )
        return httpx.Response(200, json={"markets": []})

    client = _async_client(
        httpx.MockTransport(handler),
        credentials=OAuthCredentials("api-key", "identifier", "password"),
    )

    assert (await client.operations.markets.search("EURUSD")).markets == ()
    assert (await client._transport.streaming_session()).security_token == "security"
    assert (await client._transport.refresh_streaming_session()).account_id == "ABC123"


@pytest.mark.asyncio
async def test_async_authentication_network_failure_is_typed() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("offline", request=request)

    with pytest.raises(TransportError):
        await _async_client(httpx.MockTransport(handler)).operations.markets.search("EURUSD")
