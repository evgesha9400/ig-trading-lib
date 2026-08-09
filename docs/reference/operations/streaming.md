<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Streaming operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.streaming.subscribe()`

Subscribe to Lightstreamer updates as a sync or async iterator.

Official IG reference: [https://labs.ig.com/streaming-api-reference.html](https://labs.ig.com/streaming-api-reference.html)

### Signatures

- Sync: `(subscription: 'StreamSubscription') -> 'Iterator[StreamUpdate]'`
- Async: `(subscription: 'StreamSubscription') -> 'AsyncIterator[StreamUpdate]'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `subscription` | `StreamSubscription` | required | - | Declarative Lightstreamer subscription specification. |
| `subscription.key` | `str` | required | - | Caller-defined key copied to every stream update. |
| `subscription.mode` | `Literal['MERGE', 'DISTINCT']` | required | - | Lightstreamer subscription mode; `MERGE` or `DISTINCT`. |
| `subscription.items` | `tuple[str, ...]` | required | - | Lightstreamer item names included in the subscription. |
| `subscription.fields` | `tuple[str, ...]` | required | - | Lightstreamer fields requested for every item. |
| `subscription.data_adapter` | `str | None` | default: `None` | - | Optional Lightstreamer data-adapter name. |
| `subscription.snapshot` | `bool` | default: `True` | - | Whether Lightstreamer should send an initial snapshot. |
| `subscription.max_frequency` | `str | float | None` | default: `None` | - | Maximum update frequency requested from Lightstreamer. |

### Sync example

```python
from ig_trading_lib.streaming import StreamSubscription

for update in ig.operations.streaming.subscribe(subscription=StreamSubscription(key="prices", mode="MERGE", items=("MARKET:CS.D.EURUSD.CFD.IP",), fields=("BID", "OFFER"))):
    print(update)
```

### Async example

```python
from ig_trading_lib.streaming import StreamSubscription

async for update in ig.operations.streaming.subscribe(subscription=StreamSubscription(key="prices", mode="MERGE", items=("MARKET:CS.D.EURUSD.CFD.IP",), fields=("BID", "OFFER"))):
    print(update)
```

### Response shape: `Iterator[StreamUpdate]`

| Field | Type | Required/default |
| --- | --- | --- |
| `subscription_key` | `str` | required |
| `item_name` | `str | None` | required |
| `item_position` | `int` | required |
| `fields` | `Mapping[str, str | None]` | required |
| `changed_fields` | `Mapping[str, str | None]` | required |
| `is_snapshot` | `bool` | required |

### Response example

```json
{
  "subscription_key": "example",
  "item_name": "example",
  "item_position": 1,
  "fields": {
    "BID": "1.0812"
  },
  "changed_fields": {
    "BID": "1.0812"
  },
  "is_snapshot": true
}
```

### Limitations

- Streams are long-lived and require the consumer to keep pace with the configured local buffer.
- Recovery can reconnect once, but consumers must rebuild state after any reported data loss.
- The sync method returns `Iterator[StreamUpdate]`; the async method returns `AsyncIterator[StreamUpdate]`.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `StreamingSubscriptionError` | IG or Lightstreamer rejected the subscription. | Correct the item, field, mode, entitlement, or adapter before resubscribing. |
| `StreamingDataLossError` | IG reported lost updates or the local consumer exhausted its stream buffer. | Treat local state as stale, obtain a fresh snapshot, then resubscribe. |

## `ig.operations.streaming.close()`

Unsubscribe active streams and close the Lightstreamer connection.

Official IG reference: [https://labs.ig.com/streaming-api-reference.html](https://labs.ig.com/streaming-api-reference.html)

### Signatures

- Sync: `() -> 'None'`
- Async: `() -> 'None'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
ig.operations.streaming.close()
```

### Async example

```python
await ig.operations.streaming.close()
```

### Response shape: `None`

| Field | Type | Required/default |
| --- | --- | --- |
| None | - | This method returns no structured response fields. |

### Response example

```json
null
```

### Limitations

- No library-specific failure is expected during normal local cleanup.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| None | No library-specific exception is expected. | No action required. |
