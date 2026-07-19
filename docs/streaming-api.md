# Streaming API

`StreamSubscription` declares a Lightstreamer subscription. No streaming session is opened until `iter_updates()` or `aiter_updates()` begins consuming it.

## Subscribe lazily

The REST client supplies the streaming endpoint, account ID, CST, and security token. The stream bridge turns Lightstreamer callbacks into immutable `StreamUpdate` values.

```python
from ig_trading_lib import StreamSubscription

subscription = StreamSubscription(
    key="eurusd",
    mode="MERGE",
    items=("MARKET:CS.D.EURUSD.TODAY.IP",),
    fields=("BID", "OFFER", "UPDATE_TIME"),
)

with IGClient(config) as client:
    updates = client.streaming.iter_updates(subscription)
    try:
        for update in updates:
            print(update.item_name, update.changed_fields)
    finally:
        updates.close()
```

The asynchronous client exposes `async for update in client.streaming.aiter_updates(subscription)`.

## Handle stream failures

`StreamingSubscriptionError` means IG rejected a subscription. `StreamingDataLossError` means IG reported lost updates or the local consumer buffer overflowed. A terminal streaming-server error triggers one credential-refresh recovery attempt; a failed or repeated recovery is surfaced as `AuthenticationError`. Treat those failures as a signal to reconcile from a REST read before making trading decisions.

Use a finite queue size and process updates promptly. The bridge does not manufacture missed updates.
