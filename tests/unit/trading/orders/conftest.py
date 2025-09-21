from pytest import fixture

from ig_trading_lib.trading.orders import OrderService


@fixture
def order_service(api_key, tokens) -> OrderService:
    return OrderService(
        api_key=api_key, tokens=tokens, base_url="https://demo-api.ig.com"
    )


@fixture
def working_orders():
    return {
        "workingOrders": [
            {
                "workingOrderData": {
                    "dealId": "DIAAAAPJP4A6DAS",
                    "direction": "SELL",
                    "epic": "CS.D.GBPUSD.TODAY.IP",
                    "orderSize": 0.50,
                    "orderLevel": 12805.0,
                    "timeInForce": "GOOD_TILL_DATE",
                    "goodTillDate": "2024/03/14 23:59",
                    "goodTillDateISO": "2024-03-14T23:59",
                    "createdDate": "2024/03/13 23:41:09:000",
                    "createdDateUTC": "2024-03-13T23:41:09",
                    "guaranteedStop": False,
                    "orderType": "LIMIT",
                    "stopDistance": 5.0,
                    "limitDistance": 8.0,
                    "currencyCode": "GBP",
                    "dma": False,
                    "limitedRiskPremium": None,
                },
                "marketData": {
                    "instrumentName": "GBP/USD",
                    "exchangeId": "FX_BET_ALL",
                    "expiry": "DFB",
                    "marketStatus": "TRADEABLE",
                    "epic": "CS.D.GBPUSD.TODAY.IP",
                    "instrumentType": "CURRENCIES",
                    "lotSize": 10.0,
                    "high": 12805.9,
                    "low": 12788.8,
                    "percentageChange": 0.03,
                    "netChange": 4.4,
                    "bid": 12801.2,
                    "offer": 12802.7,
                    "updateTime": "23:41:22",
                    "updateTimeUTC": "23:41:22",
                    "delayTime": 0,
                    "streamingPricesAvailable": True,
                    "scalingFactor": 1,
                },
            }
        ]
    }
