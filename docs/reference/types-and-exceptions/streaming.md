# Streaming types

Streaming is still an operation: call
[`ig.operations.streaming.subscribe()`](../operations/streaming.md) with a `StreamSubscription` and
consume `StreamUpdate` values.

```python
from ig_trading_lib import StreamSubscription

subscription = StreamSubscription(
    key="prices",
    mode="MERGE",
    items=("MARKET:CS.D.EURUSD.CFD.IP",),
    fields=("BID", "OFFER"),
)

for update in ig.operations.streaming.subscribe(subscription):
    print(update.item_name, update.changed_fields)
```

| Type | Purpose | Lifetime |
| --- | --- | --- |
| `StreamSubscription` | Immutable declaration of items, fields, mode, snapshot, and frequency. | Reusable across subscriptions. |
| `StreamUpdate` | Immutable copy of one Lightstreamer update. | Owned by the consumer after delivery. |

## Limitations

- `mode` is `MERGE` or `DISTINCT`.
- The consumer must keep pace with the configured local buffer.
- `StreamingDataLossError` means local state is stale and must be rebuilt from a fresh snapshot.
- The synchronous operation returns an iterator; the asynchronous operation returns an async iterator.

## Subscription

::: ig_trading_lib.streaming.StreamSubscription

## Update

::: ig_trading_lib.streaming.StreamUpdate
