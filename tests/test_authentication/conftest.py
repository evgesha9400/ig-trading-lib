import logging
from pytest import fixture

logging.basicConfig(level=logging.INFO)


@fixture
def test_account_info():
    return {
        "accountType": "SPREADBET",
        "accountInfo": {
            "balance": 9999999.0,
            "deposit": 0.0,
            "profitLoss": 0.0,
            "available": 9999999.0,
        },
        "currencyIsoCode": "GBP",
        "currencySymbol": "£",
        "currentAccountId": "ABC123",
        "lightstreamerEndpoint": "https://demo-apd.marketdatasystems.com",
        "accounts": [
            {
                "accountId": "ABC124",
                "accountName": "CFD",
                "preferred": False,
                "accountType": "CFD",
            },
            {
                "accountId": "ABC123",
                "accountName": "Spread bet",
                "preferred": True,
                "accountType": "SPREADBET",
            },
        ],
        "clientId": "123456789",
        "timezoneOffset": 0,
        "hasActiveDemoAccounts": True,
        "hasActiveLiveAccounts": True,
        "trailingStopsEnabled": False,
        "reroutingEnvironment": None,
        "dealingEnabled": True,
    }
