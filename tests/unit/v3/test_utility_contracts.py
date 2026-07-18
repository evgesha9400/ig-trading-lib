import time

import pytest

from ig_trading_lib import Environment, IGClient, IGConfig, IGError, SessionCredentials
from ig_trading_lib.async_services import AsyncResourceClient
from ig_trading_lib.services import ResourceClient
from ig_trading_lib.transport import AsyncTransport, SessionTokens, SyncTransport


def _config(environment: Environment = Environment.DEMO) -> IGConfig:
    return IGConfig(environment, SessionCredentials("api-key", "identifier", "password"))


def test_configuration_token_and_error_helpers_preserve_safe_values() -> None:
    assert _config(Environment.LIVE).base_url == "https://api.ig.com/gateway/deal"
    assert SessionTokens(refresh_token="refresh", expires_at=time.monotonic() - 1).needs_refresh
    assert not SessionTokens(access_token="token").needs_refresh

    error = IGError(
        "failure",
        details={"diagnostics": [{"password": "secret"}], "access_token": "token"},
    )

    assert error.details == {
        "diagnostics": [{"password": "[REDACTED]"}],
        "access_token": "[REDACTED]",
    }


def test_page_helpers_handle_list_and_invalid_payloads() -> None:
    assert ResourceClient._to_page([{"value": 1}], None).items[0].value == 1
    assert ResourceClient._to_page("invalid", None).items == ()
    assert AsyncResourceClient._to_page([{"value": 2}], None).items[0].value == 2
    assert AsyncResourceClient._to_page("invalid", None).items == ()


def test_owned_transports_close_without_opening_network_connections() -> None:
    sync_transport = SyncTransport(_config())
    sync_transport.close()


def test_sync_client_context_manager_closes_owned_resources() -> None:
    with IGClient(_config()) as client:
        assert client.config.environment is Environment.DEMO


@pytest.mark.asyncio
async def test_owned_async_transport_closes_without_opening_network_connections() -> None:
    async_transport = AsyncTransport(_config())
    await async_transport.close()
