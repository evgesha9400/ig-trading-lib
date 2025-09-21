from typing import List, Literal, Optional

from pydantic import BaseModel, condecimal


class DealReference(BaseModel):
    dealReference: str


InstrumentType = Literal[
    "SHARES",
    "BINARY",
    "BUNGEE_CAPPED",
    "BUNGEE_COMMODITIES",
    "BUNGEE_CURRENCIES",
    "BUNGEE_INDICES",
    "COMMODITIES",
    "CURRENCIES",
    "INDICES",
    "KNOCKOUTS_COMMODITIES",
    "KNOCKOUTS_CURRENCIES",
    "KNOCKOUTS_INDICES",
    "KNOCKOUTS_SHARES",
    "OPT_COMMODITIES",
    "OPT_CURRENCIES",
    "OPT_INDICES",
    "OPT_RATES",
    "OPT_SHARES",
    "RATES",
    "SECTORS",
    "SPRINT_MARKET",
    "TEST_MARKET",
    "UNKNOWN",
]


Direction = Literal["BUY", "SELL"]


DealStatus = Literal["ACCEPTED", "REJECTED"]


PositionStatus = Literal["AMENDED", "CLOSED", "DELETED", "OPEN", "PARTIALLY_CLOSED"]


DealReason = Literal[
    "ACCOUNT_NOT_ENABLED_TO_TRADING",
    "ATTACHED_ORDER_LEVEL_ERROR",
    "ATTACHED_ORDER_TRAILING_STOP_ERROR",
    "CANNOT_CHANGE_STOP_TYPE",
    "CANNOT_REMOVE_STOP",
    "CLOSING_ONLY_TRADES_ACCEPTED_ON_THIS_MARKET",
    "CLOSINGS_ONLY_ACCOUNT",
    "CONFLICTING_ORDER",
    "CONTACT_SUPPORT_INSTRUMENT_ERROR",
    "CR_SPACING",
    "DUPLICATE_ORDER_ERROR",
    "EXCHANGE_MANUAL_OVERRIDE",
    "EXPIRY_LESS_THAN_SPRINT_MARKET_MIN_EXPIRY",
    "FINANCE_REPEAT_DEALING",
    "FORCE_OPEN_ON_SAME_MARKET_DIFFERENT_CURRENCY",
    "GENERAL_ERROR",
    "GOOD_TILL_DATE_IN_THE_PAST",
    "INSTRUMENT_NOT_FOUND",
    "INSTRUMENT_NOT_TRADEABLE_IN_THIS_CURRENCY",
    "INSUFFICIENT_FUNDS",
    "LEVEL_TOLERANCE_ERROR",
    "LIMIT_ORDER_WRONG_SIDE_OF_MARKET",
    "MANUAL_ORDER_TIMEOUT",
    "MARGIN_ERROR",
    "MARKET_CLOSED",
    "MARKET_CLOSED_WITH_EDITS",
    "MARKET_CLOSING",
    "MARKET_NOT_BORROWABLE",
    "MARKET_OFFLINE",
    "MARKET_ORDERS_NOT_ALLOWED_ON_INSTRUMENT",
    "MARKET_PHONE_ONLY",
    "MARKET_ROLLED",
    "MARKET_UNAVAILABLE_TO_CLIENT",
    "MAX_AUTO_SIZE_EXCEEDED",
    "MINIMUM_ORDER_SIZE_ERROR",
    "MOVE_AWAY_ONLY_LIMIT",
    "MOVE_AWAY_ONLY_STOP",
    "MOVE_AWAY_ONLY_TRIGGER_LEVEL",
    "NCR_POSITIONS_ON_CR_ACCOUNT",
    "OPPOSING_DIRECTION_ORDERS_NOT_ALLOWED",
    "OPPOSING_POSITIONS_NOT_ALLOWED",
    "ORDER_DECLINED",
    "ORDER_LOCKED",
    "ORDER_NOT_FOUND",
    "ORDER_SIZE_CANNOT_BE_FILLED",
    "OVER_NORMAL_MARKET_SIZE",
    "PARTIALY_CLOSED_POSITION_NOT_DELETED",
    "POSITION_ALREADY_EXISTS_IN_OPPOSITE_DIRECTION",
    "POSITION_NOT_AVAILABLE_TO_CANCEL",
    "POSITION_NOT_AVAILABLE_TO_CLOSE",
    "POSITION_NOT_FOUND",
    "REJECT_CFD_ORDER_ON_SPREADBET_ACCOUNT",
    "REJECT_SPREADBET_ORDER_ON_CFD_ACCOUNT",
    "SIZE_INCREMENT",
    "SPRINT_MARKET_EXPIRY_AFTER_MARKET_CLOSE",
    "STOP_OR_LIMIT_NOT_ALLOWED",
    "STOP_REQUIRED_ERROR",
    "STRIKE_LEVEL_TOLERANCE",
    "SUCCESS",
    "TRAILING_STOP_NOT_ALLOWED",
    "UNKNOWN",
    "WRONG_SIDE_OF_MARKET",
]


class AffectedDeal(BaseModel):
    dealId: str
    status: PositionStatus


class DealConfirmation(BaseModel):
    affectedDeals: List[AffectedDeal]
    dealId: Optional[str] = None
    status: Optional[str] = None
    date: Optional[str] = None
    dealReference: Optional[str] = None
    dealStatus: Optional[DealStatus] = None
    direction: Optional[Direction] = None
    epic: Optional[str] = None
    expiry: Optional[str] = None
    guaranteedStop: Optional[bool] = None
    level: Optional[condecimal(decimal_places=2)] = None
    limitDistance: Optional[condecimal(decimal_places=2)] = None
    limitLevel: Optional[condecimal(decimal_places=2)] = None
    profit: Optional[condecimal(decimal_places=2)] = None
    profitCurrency: Optional[str] = None
    reason: Optional[DealReason] = None
    size: Optional[condecimal(decimal_places=2)] = None
    stopDistance: Optional[condecimal(decimal_places=2)] = None
    stopLevel: Optional[condecimal(decimal_places=2)] = None
    trailingStop: Optional[bool] = None
