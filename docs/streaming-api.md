# Streaming operations

Streaming is an IG protocol capability, so it lives in the faithful operation layer.

```python
from ig_trading_lib import StreamSubscription

subscription = StreamSubscription(
    key="prices",
    mode="MERGE",
    items=("MARKET:CS.D.EURUSD.CFD.IP",),
    fields=("BID", "OFFER"),
)

with IG(config) as ig:
    for update in ig.operations.streaming.subscribe(subscription):
        print(update.changed_fields)
```

The library owns session-token bridging, callback isolation, bounded buffering, subscription-loss
errors, and one controlled authentication recovery attempt.
