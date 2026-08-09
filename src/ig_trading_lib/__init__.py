"""Typed IG operations and safe trading workflows."""

from ig_trading_lib.api import IG, AsyncIG
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
    DealConfirmationError,
    IGError,
    ProviderRejectionError,
    RateLimitError,
    ResourceNotFoundError,
    StreamingDataLossError,
    StreamingSubscriptionError,
    TransportError,
)
from ig_trading_lib.operations.dealing import (
    AmendPositionRequest,
    AmendWorkingOrderRequest,
    ClosePositionRequest,
    CreatePositionRequest,
    CreateWorkingOrderRequest,
    DealConfirmationResponse,
)
from ig_trading_lib.operations.markets import MarketGetResponse, MarketSearchResponse
from ig_trading_lib.streaming import StreamSubscription, StreamUpdate

__all__ = [
    "AmbiguousExecutionError",
    "AmendPositionRequest",
    "AmendWorkingOrderRequest",
    "AsyncIG",
    "AuthenticationError",
    "AuthorizationError",
    "ClosePositionRequest",
    "CreatePositionRequest",
    "CreateWorkingOrderRequest",
    "DealConfirmationError",
    "DealConfirmationResponse",
    "Environment",
    "IG",
    "IGConfig",
    "IGError",
    "LiveTradingPermissionError",
    "MarketGetResponse",
    "MarketSearchResponse",
    "OAuthCredentials",
    "ProviderRejectionError",
    "RateLimitError",
    "ResourceNotFoundError",
    "SessionCredentials",
    "StreamSubscription",
    "StreamUpdate",
    "StreamingDataLossError",
    "StreamingSubscriptionError",
    "TradingPermit",
    "TransportError",
]
