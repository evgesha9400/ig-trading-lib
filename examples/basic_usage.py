"""List matching demo markets with the current v3 public API."""

import os

from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials


def main() -> None:
    """Create a demo client from environment variables and print matching markets."""
    config = IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials(
            api_key=os.environ.get("IG_API_KEY", "your_api_key"),
            identifier=os.environ.get("IG_ACCOUNT_IDENTIFIER", "your_account_identifier"),
            password=os.environ.get("IG_ACCOUNT_PASSWORD", "your_account_password"),
        ),
    )

    with IGClient(config) as client:
        markets = client.markets.search("EURUSD")
        for market in markets.items:
            print(market.epic, market.market_status)


if __name__ == "__main__":
    main()
