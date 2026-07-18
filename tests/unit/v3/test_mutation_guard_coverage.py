import httpx
import pytest

from ig_trading_lib import (
    Environment,
    IGClient,
    IGConfig,
    LiveTradingPermissionError,
    SessionCredentials,
)


@pytest.mark.parametrize(
    ("action"),
    [
        lambda client: client.watchlists.create({"name": "agent-list"}),
        lambda client: client.accounts.update_preferences({"trailingStopsEnabled": True}),
        lambda client: client.watchlists.delete("/agent-list"),
    ],
)
def test_live_resource_mutations_require_a_permit_before_network_io(action: object) -> None:
    def forbidden_request(_: httpx.Request) -> httpx.Response:
        raise AssertionError("A rejected live mutation must not authenticate or send a request.")

    client = IGClient(
        IGConfig(
            environment=Environment.LIVE,
            credentials=SessionCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        ),
        http_client=httpx.Client(transport=httpx.MockTransport(forbidden_request)),
    )

    with pytest.raises(LiveTradingPermissionError):
        action(client)  # type: ignore[operator]
