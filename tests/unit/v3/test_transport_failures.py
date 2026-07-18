import httpx
import pytest

from ig_trading_lib import (
    AmbiguousExecutionError,
    Environment,
    IGClient,
    IGConfig,
    SessionCredentials,
    TransportError,
)


def _client(handler: httpx.MockTransport) -> IGClient:
    return IGClient(
        IGConfig(
            environment=Environment.DEMO,
            credentials=SessionCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        ),
        http_client=httpx.Client(transport=handler),
    )


def test_read_network_failure_raises_a_typed_transport_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        raise httpx.ReadTimeout("network stalled", request=request)

    with pytest.raises(TransportError):
        _client(httpx.MockTransport(handler)).markets.search("EURUSD")


def test_mutation_network_failure_raises_an_ambiguous_execution_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/gateway/deal/session":
            return httpx.Response(200, headers={"CST": "cst", "X-SECURITY-TOKEN": "security"})
        raise httpx.ReadTimeout("network stalled", request=request)

    with pytest.raises(AmbiguousExecutionError):
        _client(httpx.MockTransport(handler)).positions.create({"epic": "CS.D.EURUSD.TODAY.IP"})
