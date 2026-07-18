"""Production-ready Python client for IG's REST and streaming APIs."""

from ig_trading_lib.client import IGClient
from ig_trading_lib.core import (
    Environment,
    IGConfig,
    LiveTradingPermissionError,
    OAuthCredentials,
    SessionCredentials,
    TradingPermit,
)

__all__ = [
    "Environment",
    "IGClient",
    "IGConfig",
    "LiveTradingPermissionError",
    "OAuthCredentials",
    "SessionCredentials",
    "TradingPermit",
]
