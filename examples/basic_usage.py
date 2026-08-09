"""List matching demo markets with the v4 operation layer."""

import os

from ig_trading_lib import IG, Environment, IGConfig, SessionCredentials


def main() -> None:
    config = IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials(
            api_key=os.environ.get("IG_API_KEY", "your_api_key"),
            identifier=os.environ.get("IG_ACCOUNT_IDENTIFIER", "your_account_identifier"),
            password=os.environ.get("IG_ACCOUNT_PASSWORD", "your_account_password"),
        ),
    )
    with IG(config) as ig:
        for market in ig.operations.markets.search("EURUSD").markets:
            print(market.epic, market.market_status)


if __name__ == "__main__":
    main()
