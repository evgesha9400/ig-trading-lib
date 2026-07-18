from ig_trading_lib.trading.client import IGClient, TradingClient
from ig_trading_lib.trading.confirms import get_deal_confirmation
from ig_trading_lib.trading.models import DealConfirmation, DealReference, Direction, InstrumentType
from ig_trading_lib.trading.orders_models import (
    CreateWorkingOrder,
    MarketData,
    UpdateWorkingOrder,
    WorkingOrder,
    WorkingOrderData,
    WorkingOrders,
)
from ig_trading_lib.trading.orders_service import OrderException, OrderService
from ig_trading_lib.trading.positions_models import (
    ClosePosition,
    CreatePosition,
    Market,
    OpenPosition,
    OpenPositions,
    Position,
    UpdatePosition,
)
from ig_trading_lib.trading.positions_service import PositionsError, PositionService

__all__ = [
    "IGClient",
    "TradingClient",
    "DealReference",
    "DealConfirmation",
    "Direction",
    "InstrumentType",
    "MarketData",
    "WorkingOrderData",
    "WorkingOrder",
    "WorkingOrders",
    "CreateWorkingOrder",
    "UpdateWorkingOrder",
    "Market",
    "Position",
    "OpenPosition",
    "OpenPositions",
    "CreatePosition",
    "ClosePosition",
    "UpdatePosition",
    "OrderService",
    "OrderException",
    "PositionService",
    "PositionsError",
    "get_deal_confirmation",
]
