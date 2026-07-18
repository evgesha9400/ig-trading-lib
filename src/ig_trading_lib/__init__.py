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
from ig_trading_lib.errors import (
    AmbiguousExecutionError,
    AuthenticationError,
    AuthorizationError,
    IGError,
    ProviderRejectionError,
    RateLimitError,
    ResourceNotFoundError,
    TransportError,
)
from ig_trading_lib.models import IGModel, Page

__all__ = [
    "AmbiguousExecutionError",
    "AuthenticationError",
    "AuthorizationError",
    "Environment",
    "IGClient",
    "IGConfig",
    "IGError",
    "IGModel",
    "LiveTradingPermissionError",
    "OAuthCredentials",
    "Page",
    "ProviderRejectionError",
    "RateLimitError",
    "ResourceNotFoundError",
    "SessionCredentials",
    "TradingPermit",
    "TransportError",
]
