"""Production-ready Python client for IG's REST and streaming APIs."""

from ig_trading_lib.api import IG, AsyncIG
from ig_trading_lib.client import AsyncIGClient, IGClient
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
    StreamingDataLossError,
    StreamingSubscriptionError,
    TransportError,
)
from ig_trading_lib.models import IGModel, Page
from ig_trading_lib.operations.markets import MarketGetResponse, MarketSearchResponse
from ig_trading_lib.streaming import (
    AsyncStreamingClient,
    StreamingClient,
    StreamSubscription,
    StreamUpdate,
)

__all__ = [
    "AmbiguousExecutionError",
    "AsyncIG",
    "AsyncIGClient",
    "AsyncStreamingClient",
    "AuthenticationError",
    "AuthorizationError",
    "Environment",
    "IG",
    "IGClient",
    "IGConfig",
    "IGError",
    "IGModel",
    "LiveTradingPermissionError",
    "MarketGetResponse",
    "MarketSearchResponse",
    "OAuthCredentials",
    "Page",
    "ProviderRejectionError",
    "RateLimitError",
    "ResourceNotFoundError",
    "SessionCredentials",
    "StreamSubscription",
    "StreamUpdate",
    "StreamingClient",
    "StreamingDataLossError",
    "StreamingSubscriptionError",
    "TradingPermit",
    "TransportError",
]
