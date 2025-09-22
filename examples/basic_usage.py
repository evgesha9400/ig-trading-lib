import os
import pprint

from ig_trading_lib.authentication import AuthenticationService
from ig_trading_lib.authentication.cache import InMemoryCache
from ig_trading_lib.trading import CreatePosition, IGClient, PositionService

if __name__ == "__main__":
    """This example demonstrates how to use the PositionService to open a position and retrieve open positions."""

    api_key = os.environ.get("IG_API_KEY") or "your_api_key"
    account_identifier = (
        os.environ.get("IG_ACCOUNT_IDENTIFIER") or "your_account_identifier"
    )
    account_password = os.environ.get("IG_ACCOUNT_PASSWORD") or "your_account_password"
    base_url = os.environ.get("IG_BASE_URL") or "https://demo-api.ig.com"

    auth_service = AuthenticationService(
        api_key=api_key,
        account_identifier=account_identifier,
        account_password=account_password,
        base_url=base_url,
        cache=InMemoryCache(),  # Optional caching for tokens
    )
    auth_response = auth_service.authenticate()

    client = IGClient(base_url=base_url, api_key=api_key, tokens=auth_response.tokens)
    position_service = PositionService(client)

    create = CreatePosition.model_validate(
        {
            "currencyCode": "USD",
            "direction": "BUY",
            "epic": "CS.D.GBPUSD.TODAY.IP",
            "expiry": "DFB",
            "forceOpen": True,
            "guaranteedStop": False,
            "orderType": "MARKET",
            "size": 1,
            "timeInForce": "EXECUTE_AND_ELIMINATE",
            "trailingStop": False,
        }
    )
    deal_reference = position_service.create_position(position=create)
    pprint.pprint(deal_reference)

    open_positions = position_service.get_open_positions()
    pprint.pprint(open_positions.model_dump())
