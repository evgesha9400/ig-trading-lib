# Getting started

Use Python 3.11, 3.12, or 3.13, then install the package into your application environment.

```bash
pip install ig-trading-lib
```

Use a demo account while building and testing an integration.

## Synchronous client

```python
from ig_trading_lib import Environment, IGClient, IGConfig, SessionCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(
        api_key="…",
        identifier="…",
        password="…",
    ),
)

with IGClient(config) as client:
    markets = client.markets.search("EURUSD")
    for market in markets.items:
        print(market.epic, market.market_status)
```

## Asynchronous client

```python
import asyncio

from ig_trading_lib import AsyncIGClient, Environment, IGConfig, SessionCredentials


async def main() -> None:
    config = IGConfig(
        environment=Environment.DEMO,
        credentials=SessionCredentials(
            api_key="…",
            identifier="…",
            password="…",
        ),
    )

    async with AsyncIGClient(config) as client:
        accounts = await client.accounts.list()
        print(accounts.items)


asyncio.run(main())
```

## Live mutations

Live accounts require an explicit permit for the guarded mutation surfaces. Read [Trading safety](api-guide/trading-safety.md) before passing `TradingPermit()`.
