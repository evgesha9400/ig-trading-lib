# Trading safety

Every operation classified as a mutation in the authoritative manifest crosses the same
`TradingGuard` before authentication or network I/O.

```python
from ig_trading_lib import IG, TradingPermit

with IG(live_config, trading_permit=TradingPermit()) as ig:
    confirmation = ig.workflows.positions.open_and_confirm(request)
```

- Demo mutations do not require a permit.
- Live mutations require an explicit `TradingPermit`.
- Safe reads may retry.
- Mutations never retry automatically after an uncertain outcome.
- `AmbiguousExecutionError` means reconcile provider state before another mutation.
