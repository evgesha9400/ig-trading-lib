# IG Trading Library

Typed operations and safe workflows for IG's REST and streaming APIs.

The library removes protocol decisions from trading code. You call IG concepts such as
`markets.search`, `positions.create`, and `confirmations.get`; the library owns authentication,
endpoint paths, IG protocol versions, response normalisation, safe-read retries, mutation
ambiguity, and streaming recovery.

| Direct HTTP | This library |
| --- | --- |
| Choose a path and protocol version | Call one named operation |
| Build and validate dictionaries | Use typed request and response models |
| Reimplement auth, retry, and redaction | Share one hardened transport |
| Risk retrying an uncertain trade | Receive `AmbiguousExecutionError` |
| Compose trade confirmation manually | Use a safe workflow |

## One mental model

```text
IG(config)
├── operations   one faithful typed IG call
└── workflows    a journey composed only from operations
```

- Use `ig.operations` when the IG reference names the call you need.
- Use `ig.workflows` when you need a complete journey such as open and confirm.
- Use `AsyncIG` with `await` in applications built on `asyncio`.
- Treat library v4 as the Python package version; IG protocol versions stay private.

## Install

```bash
pip install ig-trading-lib==4.0.0
```

Python 3.11–3.13 is supported.

## Discover and inspect

```python
from ig_trading_lib import Environment, IG, IGConfig, SessionCredentials

config = IGConfig(
    environment=Environment.DEMO,
    credentials=SessionCredentials(
        api_key="your-api-key",
        identifier="your-identifier",
        password="your-password",
    ),
)

with IG(config) as ig:
    matches = ig.operations.markets.search("EUR/USD")
    market = ig.operations.markets.get(matches.markets[0].epic)
    print(market.instrument.epic, market.snapshot.bid if market.snapshot else None)
```

Provider-added response fields remain available while documented fields are typed and
normalised to `snake_case`.

## Trade and confirm

```python
from ig_trading_lib import CreatePositionRequest, IG, TradingPermit

request = CreatePositionRequest(
    epic="CS.D.EURUSD.CFD.IP",
    direction="BUY",
    size=1,
    order_type="MARKET",
    currency_code="GBP",
)

with IG(config, trading_permit=TradingPermit()) as ig:
    confirmation = ig.workflows.positions.open_and_confirm(request)
    print(confirmation.deal_status, confirmation.deal_id)
```

`TradingPermit` is mandatory for live mutations. Network failures after a mutation may raise
`AmbiguousExecutionError`; reconcile the deal before deciding whether to issue another request.
If confirmation retrieval fails after IG returns a deal reference, `DealConfirmationError`
preserves that reference so you can retrieve the existing confirmation without replaying the trade.

## Async

```python
from ig_trading_lib import AsyncIG

async with AsyncIG(config) as ig:
    matches = await ig.operations.markets.search("EUR/USD")
```

## Documentation

- [Documentation](https://evgesha9400.github.io/ig-trading-lib/latest/)
- [PyPI](https://pypi.org/project/ig-trading-lib/)
- [Getting started](https://evgesha9400.github.io/ig-trading-lib/latest/getting-started/)
- [Operation reference](https://evgesha9400.github.io/ig-trading-lib/latest/rest-api-reference/markets/)
- [Public Python API](https://evgesha9400.github.io/ig-trading-lib/latest/reference/public-api/)
- [Machine-readable API index](https://evgesha9400.github.io/ig-trading-lib/latest/reference/public-api-index.json)
- [Source](https://github.com/evgesha9400/ig-trading-lib)

The automated suite uses mocked IG responses. It never submits a real demo or live trade.
