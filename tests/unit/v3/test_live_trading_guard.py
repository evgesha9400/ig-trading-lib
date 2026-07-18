import pytest

from ig_trading_lib import (
    Environment,
    IGClient,
    IGConfig,
    LiveTradingPermissionError,
    SessionCredentials,
)


def test_live_position_creation_requires_explicit_trading_permit() -> None:
    client = IGClient(
        IGConfig(
            environment=Environment.LIVE,
            credentials=SessionCredentials(
                api_key="api-key",
                identifier="identifier",
                password="password",
            ),
        )
    )

    with pytest.raises(LiveTradingPermissionError):
        client.positions.create({"epic": "CS.D.EURUSD.TODAY.IP"})
