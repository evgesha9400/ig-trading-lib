from decimal import Decimal
from typing import List, Any
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    constr,
    condecimal,
    conint,
    model_validator,
    Field,
    field_serializer,
)


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


class CreatePosition(BaseModel):
    currencyCode: constr(pattern=r"^[A-Z]{3}$")
    direction: Literal["BUY", "SELL"]
    epic: constr(pattern=r"^[A-Za-z0-9._]{6,30}$")
    expiry: constr(pattern=r"^(\d{2}-)?[A-Z]{3}-\d{2}|-|DFB$")
    forceOpen: bool
    guaranteedStop: bool
    orderType: Literal["LIMIT", "MARKET", "QUOTE"]
    timeInForce: Literal["EXECUTE_AND_ELIMINATE", "FILL_OR_KILL"]
    trailingStop: bool
    dealReference: Optional[constr(pattern=r"^[A-Za-z0-9_\-.]{1,30}$")] = None
    level: Optional[condecimal(decimal_places=12)] = None
    limitDistance: Optional[condecimal(decimal_places=2)] = None
    limitLevel: Optional[condecimal(decimal_places=2)] = None
    quoteId: Optional[constr(pattern=r"^[A-Za-z0-9]+$")] = None
    size: condecimal(decimal_places=2, gt=0)
    stopDistance: Optional[condecimal(decimal_places=2)] = None
    stopLevel: Optional[condecimal(decimal_places=2)] = None
    trailingStopIncrement: Optional[condecimal(decimal_places=2)] = None

    @field_serializer(
        "level",
        "limitDistance",
        "limitLevel",
        "size",
        "stopDistance",
        "stopLevel",
        "trailingStopIncrement",
        mode="plain",
    )
    def serialize_decimal(self, v: Optional[Decimal], _info) -> float:
        if v is not None:
            return float(v)

    @model_validator(mode="before")
    @classmethod
    def check_unique_constraints(cls, data: Any):
        if (
            sum(
                [
                    data.get("limitLevel") is not None,
                    data.get("limitDistance") is not None,
                ]
            )
            > 1
        ):
            raise ValueError("Set only one of limitLevel or limitDistance.")
        if (
            sum(
                [
                    data.get("stopLevel") is not None,
                    data.get("stopDistance") is not None,
                ]
            )
            > 1
        ):
            raise ValueError("Set only one of stopLevel or stopDistance.")
        return data

    @model_validator(mode="before")
    @classmethod
    def check_force_open_constraints(cls, data: Any):
        if any(
            [
                data.get("limitDistance") is not None,
                data.get("limitLevel") is not None,
                data.get("stopDistance") is not None,
                data.get("stopLevel") is not None,
            ]
        ) and not data.get("forceOpen"):
            raise ValueError(
                "forceOpen must be true if limit or stop constraints are set."
            )
        return data

    @model_validator(mode="before")
    @classmethod
    def check_guaranteed_stop_constraints(cls, data: Any):
        if data.get("guaranteedStop") and not (
            bool(data.get("stopLevel")) ^ bool(data.get("stopDistance"))
        ):
            raise ValueError(
                "When guaranteedStop is true, specify exactly one of stopLevel or stopDistance."
            )
        return data

    @model_validator(mode="before")
    @classmethod
    def check_order_type_constraints(cls, data: Any):
        order_type = data.get("orderType")
        if order_type == "LIMIT":
            if data.get("quoteId") is not None:
                raise ValueError("Do not set quoteId when orderType is LIMIT.")
            if data.get("level") is None:
                raise ValueError("Set level when orderType is LIMIT.")
        elif order_type == "MARKET":
            if any([data.get("level") is not None, data.get("quoteId") is not None]):
                raise ValueError(
                    "Do not set level or quoteId when orderType is MARKET."
                )
        elif order_type == "QUOTE":
            if not all(
                [data.get("level") is not None, data.get("quoteId") is not None]
            ):
                raise ValueError("Set both level and quoteId when orderType is QUOTE.")
        return data

    @model_validator(mode="before")
    @classmethod
    def check_trailing_stop_constraints(cls, data: Any):
        if data.get("trailingStop"):
            if data.get("stopLevel") is not None:
                raise ValueError("Do not set stopLevel when trailingStop is true.")
            if data.get("guaranteedStop"):
                raise ValueError(
                    "guaranteedStop must be false when trailingStop is true."
                )
            if not all(
                [
                    data.get("stopDistance") is not None,
                    data.get("trailingStopIncrement") is not None,
                ]
            ):
                raise ValueError(
                    "Set both stopDistance and trailingStopIncrement when trailingStop is true."
                )
        return data
