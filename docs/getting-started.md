# Getting started

This path teaches the complete mental model: discover, inspect, trade, confirm, monitor, then
amend or close.

## 1. Install library v4

```bash
pip install ig-trading-lib==4.0.2
```

## 2. Configure the demo environment

```python
from ig_trading_lib import Environment, IGConfig, SessionCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(
        api_key="your-api-key",
        identifier="your-identifier",
        password="your-password",
    ),
)
```

Use the demo environment first. Keep credentials outside source control.

## 3. Discover and inspect with operations

```python
from ig_trading_lib import IG

with IG(config) as ig:
    matches = ig.operations.markets.search("EUR/USD")
    epic = matches.markets[0].epic
    market = ig.operations.markets.get(epic)
```

`operations` mirrors IG. You choose the business operation; the library chooses the HTTP path and
provider protocol version.

## 4. Trade and confirm with a workflow

```python
from ig_trading_lib import CreatePositionRequest, IG, TradingPermit

request = CreatePositionRequest(
    epic=epic,
    direction="BUY",
    size=1,
    order_type="MARKET",
    currency_code="GBP",
)

with IG(config, trading_permit=TradingPermit()) as ig:
    confirmation = ig.workflows.positions.open_and_confirm(request)
```

`workflows` composes operations. `open_and_confirm` creates the position and retrieves its deal
confirmation through the faithful operation layer.

## 5. Monitor, amend, or close

- Monitor prices with `ig.operations.streaming.subscribe(...)`.
- Amend risk controls with `ig.workflows.positions.amend_and_confirm(...)`.
- Close exposure with `ig.workflows.positions.close_and_confirm(...)`.
- Snapshot accounts and open exposure with `ig.workflows.portfolio.snapshot()`.

## 6. Handle uncertain mutation outcomes

```python
from ig_trading_lib import AmbiguousExecutionError, DealConfirmationError

try:
    confirmation = ig.workflows.positions.open_and_confirm(request)
except AmbiguousExecutionError as error:
    # Reconcile by deal reference or account state before another mutation.
    raise
except DealConfirmationError as error:
    # The mutation succeeded. Retry only the safe confirmation read.
    confirmation = ig.operations.confirmations.get(error.deal_reference)
```

The library retries safe reads only. It does not blindly retry a trade whose outcome may be
unknown. A failed confirmation lookup retains the accepted mutation's deal reference.

## 7. Use the async root in an async application

```python
from ig_trading_lib import AsyncIG

async with AsyncIG(config) as ig:
    matches = await ig.operations.markets.search("EUR/USD")
```

Async operations are awaited and keep blocking HTTP work out of the event loop.
