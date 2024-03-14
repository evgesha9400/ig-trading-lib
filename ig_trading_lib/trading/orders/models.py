from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, condecimal, field_validator


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


OrderType = Literal["LIMIT", "STOP"]


TimeInForce = Literal["GOOD_TILL_CANCELLED", "GOOD_TILL_DATE"]


MarketStatus = Literal[
    "CLOSED",
    "EDITS_ONLY",
    "OFFLINE",
    "ON_AUCTION",
    "ON_AUCTION_NO_EDITS",
    "SUSPENDED",
    "TRADEABLE",
]


Direction = Literal["BUY", "SELL"]


class MarketData(BaseModel):
    instrumentName: str
    exchangeId: str
    expiry: str
    marketStatus: MarketStatus
    epic: str
    instrumentType: InstrumentType
    lotSize: condecimal(decimal_places=2)
    high: condecimal(decimal_places=2)
    low: condecimal(decimal_places=2)
    percentageChange: condecimal(decimal_places=2)
    netChange: condecimal(decimal_places=2)
    bid: condecimal(decimal_places=2)
    offer: condecimal(decimal_places=2)
    updateTime: str
    updateTimeUTC: str
    delayTime: int
    streamingPricesAvailable: bool
    scalingFactor: int


class WorkingOrderData(BaseModel):
    dealId: str
    direction: Direction
    epic: str
    orderSize: condecimal(decimal_places=2)
    orderLevel: condecimal(decimal_places=2)
    timeInForce: TimeInForce
    goodTillDate: Optional[datetime] = None
    goodTillDateISO: Optional[datetime] = None
    createdDate: datetime
    createdDateUTC: datetime
    guaranteedStop: bool
    orderType: OrderType
    stopDistance: Optional[condecimal(decimal_places=2)] = None
    limitDistance: Optional[condecimal(decimal_places=2)] = None
    currencyCode: str
    dma: Optional[bool] = None
    limitedRiskPremium: Optional[condecimal(decimal_places=2)] = None

    @field_validator("goodTillDate", mode="before")
    @classmethod
    def parse_good_till_date(cls, v: Optional[str]) -> Optional[datetime]:
        if v is not None:
            try:
                return datetime.strptime(v, "%Y/%m/%d %H:%M")
            except ValueError:
                raise ValueError(f"Invalid datetime format for goodTillDate value {v}")


    @field_validator("createdDate", mode="before")
    @classmethod
    def parse_created_date(cls, v: Optional[str]) -> Optional[datetime]:
        try:
            return datetime.strptime(v, "%Y/%m/%d %H:%M:%S:%f")
        except ValueError:
            raise ValueError(f"Invalid datetime format for createdDate value {v}")


class WorkingOrder(BaseModel):
    workingOrderData: WorkingOrderData
    marketData: MarketData


class WorkingOrders(BaseModel):
    workingOrders: List[WorkingOrder]
