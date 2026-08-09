# Getting started

Use Python 3.11, 3.12, or 3.13, then install the package into your application environment.

```bash
pip install ig-trading-lib
```

Use a demo account while building and testing an integration.

## Market operations and discovery

`IG` exposes one-operation calls under `operations` and composed behavior under `workflows`.

Call `ig.operations.markets.search(search_term="EURUSD")` for typed search results, or
`ig.workflows.discovery.find_market(search_term="EURUSD", epic="CS.D.EURUSD.TODAY.IP")` to
search, select the exact epic, and retrieve typed details.

Use `AsyncIG` with the same arguments and result types, adding `await` to each operation or
workflow call.

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
