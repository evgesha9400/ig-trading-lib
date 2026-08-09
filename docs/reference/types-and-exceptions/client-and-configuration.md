# Client and configuration

These types create one client. The client then exposes exactly
[`operations`](../operations/index.md) and [`workflows`](../workflows/index.md).

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
    accounts = ig.operations.accounts.list()
```

| Type | Purpose | Important limitation |
| --- | --- | --- |
| `IG` | Synchronous composition root. | Close it with a context manager or `close()`. |
| `AsyncIG` | Asynchronous composition root. | Close it with `async with` or `await close()`. |
| `IGConfig` | Immutable environment, credentials, timeout, retry, and account selection. | One instance targets one environment. |
| `Environment` | Selects `DEMO` or `LIVE`. | It does not itself permit live mutations. |
| `SessionCredentials` | Authenticates through an IG session. | Values are secrets and must not be logged. |
| `OAuthCredentials` | Authenticates through IG OAuth. | Values are secrets and must not be logged. |
| `TradingPermit` | Explicitly acknowledges live account mutations. | Required only for mutations against `LIVE`. |

## Client roots

::: ig_trading_lib.api.IG

::: ig_trading_lib.api.AsyncIG

## Configuration

::: ig_trading_lib.core.IGConfig

::: ig_trading_lib.core.Environment

::: ig_trading_lib.core.SessionCredentials

::: ig_trading_lib.core.OAuthCredentials

::: ig_trading_lib.core.TradingPermit
