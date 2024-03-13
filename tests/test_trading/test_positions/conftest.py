from typing import Dict

from pytest import fixture

from ig_trading_lib import Tokens
from trading.positions import PositionService


@fixture
def api_key() -> str:
    return "test_api_key"


@fixture
def tokens() -> Tokens:
    return Tokens(cst_token="test_cst_token", x_security_token="test_x_security_token")


@fixture
def open_position() -> Dict:
    return {
        "position": {
            "contractSize": 1.0,
            "createdDate": "2024/03/11 19:04:55:000",
            "createdDateUTC": "2024-03-11T19:04:55",
            "dealId": "DIAAAAPH7CKXGBB",
            "dealReference": "S54S41HRQEEGG19",
            "size": 0.5,
            "direction": "BUY",
            "limitLevel": None,
            "level": 86374.0,
            "currency": "GBP",
            "controlledRisk": False,
            "stopLevel": None,
            "trailingStep": None,
            "trailingStopDistance": None,
            "limitedRiskPremium": None,
        },
        "market": {
            "instrumentName": "NVIDIA Corp (All Sessions)",
            "expiry": "DFB",
            "epic": "UC.D.NVDA.DAILY.IP",
            "instrumentType": "SHARES",
            "lotSize": 1.0,
            "high": 89754.0,
            "low": 84219.0,
            "percentageChange": -1.54,
            "netChange": -1349.9,
            "bid": 86153.0,
            "offer": 86203.0,
            "updateTime": "19:10:48",
            "updateTimeUTC": "19:10:48",
            "delayTime": 0,
            "streamingPricesAvailable": False,
            "marketStatus": "TRADEABLE",
            "scalingFactor": 1,
        },
    }


@fixture
def position_service(api_key, tokens) -> PositionService:
    return PositionService(
        api_key=api_key, tokens=tokens, base_url="https://demo-api.ig.com"
    )
