import time

import pytest

from ig_trading_lib import IG, Environment, IGConfig, IGError, SessionCredentials
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


def test_owned_transports_close_without_opening_network_connections() -> None:
    sync_transport = SyncTransport(_config())
    sync_transport.close()


def test_sync_client_context_manager_closes_owned_resources() -> None:
    with IG(_config()) as client:
        assert set(vars(client)) >= {"operations", "workflows"}


@pytest.mark.asyncio
async def test_owned_async_transport_closes_without_opening_network_connections() -> None:
    async_transport = AsyncTransport(_config())
    await async_transport.close()
