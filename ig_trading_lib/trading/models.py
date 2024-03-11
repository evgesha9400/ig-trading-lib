from typing import List, Optional, Literal

from pydantic import BaseModel, condecimal, conint


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
MarketStatusType = Literal[
    "TRADEABLE",
    "CLOSED",
    "EDITS_ONLY",
    "OFFLINE",
    "ON_AUCTION",
    "ON_AUCTION_NO_EDITS",
    "SUSPENDED",
]


class Market(BaseModel):
    instrumentName: str
    expiry: str
    epic: str
    instrumentType: InstrumentType
    lotSize: float
    high: float
    low: float
    percentageChange: float
    netChange: float
    bid: float
    offer: float
    updateTime: str
    updateTimeUTC: str
    delayTime: int
    streamingPricesAvailable: bool
    marketStatus: MarketStatusType
    scalingFactor: int


class Position(BaseModel):
    contractSize: condecimal(decimal_places=2)
    controlledRisk: bool
    createdDate: str
    createdDateUTC: str
    currency: str
    dealId: str
    dealReference: str
    direction: Literal["BUY", "SELL"]
    level: condecimal(decimal_places=2)
    limitLevel: Optional[condecimal(decimal_places=2)] = None
    limitedRiskPremium: Optional[condecimal(decimal_places=2)] = None
    size: condecimal(decimal_places=2)
    stopLevel: Optional[condecimal(decimal_places=2)] = None
    trailingStep: Optional[conint(ge=0)] = None
    trailingStopDistance: Optional[condecimal(decimal_places=2)] = None


class OpenPosition(BaseModel):
    position: Position
    market: Market


class OpenPositions(BaseModel):
    positions: List[OpenPosition]
