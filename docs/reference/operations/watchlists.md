<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Watchlists operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.watchlists.list()`

List watchlists belonging to the active account.

Official IG reference: [https://labs.ig.com/reference/watchlists.html](https://labs.ig.com/reference/watchlists.html)

### Signatures

- Sync: `() -> 'WatchlistsResponse'`
- Async: `() -> 'WatchlistsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.watchlists.list()
```

### Async example

```python
result = await ig.operations.watchlists.list()
```

### Response shape: `WatchlistsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `watchlists[]` | `tuple[Watchlist, ...]` | default: `()` |
| `watchlists[].default_system_watchlist` | `bool | None` | default: `None` |
| `watchlists[].id` | `str` | required |
| `watchlists[].name` | `str | None` | default: `None` |
| `watchlists[].editable` | `bool | None` | default: `None` |
| `watchlists[].deleteable` | `bool | None` | default: `None` |

### Response example

```json
{
  "watchlists": [
    {
      "default_system_watchlist": true,
      "id": "example",
      "name": "Example",
      "editable": true,
      "deleteable": true
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `TransportError` | A network or timeout failure prevented a completed read request. | Retry the idempotent read with bounded backoff. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.operations.watchlists.create()`

Create a watchlist with an optional initial market set.

Official IG reference: [https://labs.ig.com/reference/watchlists.html](https://labs.ig.com/reference/watchlists.html)

### Signatures

- Sync: `(request: 'CreateWatchlistRequest') -> 'CreateWatchlistResponse'`
- Async: `(request: 'CreateWatchlistRequest') -> 'CreateWatchlistResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CreateWatchlistRequest` | required | - | Validated typed request body. |
| `request.name` | `str` | required | minimum length `1` | User-visible watchlist name. |
| `request.epics` | `tuple[str, ...]` | default: `()` | - | Ordered collection of IG market epics. |

### Sync example

```python
from ig_trading_lib.operations.watchlists import CreateWatchlistRequest

result = ig.operations.watchlists.create(request=CreateWatchlistRequest(name="FX majors", epics=("CS.D.EURUSD.CFD.IP",)))
```

### Async example

```python
from ig_trading_lib.operations.watchlists import CreateWatchlistRequest

result = await ig.operations.watchlists.create(request=CreateWatchlistRequest(name="FX majors", epics=("CS.D.EURUSD.CFD.IP",)))
```

### Response shape: `CreateWatchlistResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `status` | `str | None` | default: `None` |
| `watchlist_id` | `str | None` | default: `None` |

### Response example

```json
{
  "status": "ENABLED",
  "watchlist_id": "example"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- The name must be non-empty; market and watchlist limits are controlled by IG.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `AmbiguousExecutionError` | A mutation may have reached IG before a network or timeout failure. | Reconcile account state or query by deal reference; never replay blindly. |
| `LiveTradingPermissionError` | A live-environment mutation was called without an acknowledged `TradingPermit`. | Construct the client with an explicit `TradingPermit` after confirming live intent. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.operations.watchlists.get()`

Retrieve one watchlist and its markets.

Official IG reference: [https://labs.ig.com/reference/watchlists-watchlist-id.html](https://labs.ig.com/reference/watchlists-watchlist-id.html)

### Signatures

- Sync: `(watchlist_id: 'str') -> 'WatchlistResponse'`
- Async: `(watchlist_id: 'str') -> 'WatchlistResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `watchlist_id` | `str` | required | - | IG watchlist identifier. |

### Sync example

```python
result = ig.operations.watchlists.get(watchlist_id="12345")
```

### Async example

```python
result = await ig.operations.watchlists.get(watchlist_id="12345")
```

### Response shape: `WatchlistResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `id` | `str | None` | default: `None` |
| `name` | `str | None` | default: `None` |
| `markets[]` | `tuple[WatchlistMarket, ...]` | default: `()` |
| `markets[].bid` | `Decimal | None` | default: `None` |
| `markets[].delay_time` | `int | None` | default: `None` |
| `markets[].epic` | `str` | required |
| `markets[].expiry` | `str | None` | default: `None` |
| `markets[].high` | `Decimal | None` | default: `None` |
| `markets[].instrument_name` | `str | None` | default: `None` |
| `markets[].instrument_type` | `str | None` | default: `None` |
| `markets[].low` | `Decimal | None` | default: `None` |
| `markets[].market_status` | `str | None` | default: `None` |
| `markets[].net_change` | `Decimal | None` | default: `None` |
| `markets[].offer` | `Decimal | None` | default: `None` |
| `markets[].percentage_change` | `Decimal | None` | default: `None` |
| `markets[].scaling_factor` | `Decimal | None` | default: `None` |
| `markets[].streaming_prices_available` | `bool | None` | default: `None` |
| `markets[].update_time` | `str | None` | default: `None` |
| `markets[].update_time_utc` | `str | None` | default: `None` |
| `markets[].lot_size` | `Decimal | None` | default: `None` |

### Response example

```json
{
  "id": "example",
  "name": "Example",
  "markets": [
    {
      "bid": "1.0",
      "delay_time": 1,
      "epic": "CS.D.EURUSD.CFD.IP",
      "expiry": "-",
      "high": "1.0",
      "instrument_name": "EUR/USD",
      "instrument_type": "example",
      "low": "1.0",
      "market_status": "TRADEABLE",
      "net_change": "1.0",
      "offer": "1.0",
      "percentage_change": "1.0",
      "scaling_factor": "1.0",
      "streaming_prices_available": true,
      "update_time": "12:34:56",
      "update_time_utc": "example",
      "lot_size": "1.0"
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The watchlist must belong to the active account.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `TransportError` | A network or timeout failure prevented a completed read request. | Retry the idempotent read with bounded backoff. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.operations.watchlists.add_market()`

Add one market epic to a watchlist.

Official IG reference: [https://labs.ig.com/reference/watchlists-watchlist-id-epic.html](https://labs.ig.com/reference/watchlists-watchlist-id-epic.html)

### Signatures

- Sync: `(watchlist_id: 'str', request: 'AddWatchlistMarketRequest') -> 'WatchlistMutationResponse'`
- Async: `(watchlist_id: 'str', request: 'AddWatchlistMarketRequest') -> 'WatchlistMutationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `watchlist_id` | `str` | required | - | IG watchlist identifier. |
| `request` | `AddWatchlistMarketRequest` | required | - | Validated typed request body. |
| `request.epic` | `str` | required | minimum length `1` | IG market epic. |

### Sync example

```python
from ig_trading_lib.operations.watchlists import AddWatchlistMarketRequest

result = ig.operations.watchlists.add_market(watchlist_id="12345", request=AddWatchlistMarketRequest(epic="CS.D.EURUSD.CFD.IP"))
```

### Async example

```python
from ig_trading_lib.operations.watchlists import AddWatchlistMarketRequest

result = await ig.operations.watchlists.add_market(watchlist_id="12345", request=AddWatchlistMarketRequest(epic="CS.D.EURUSD.CFD.IP"))
```

### Response shape: `WatchlistMutationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `status` | `str | None` | default: `None` |

### Response example

```json
{
  "status": "ENABLED"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- The market must be available and the watchlist must have remaining capacity.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `AmbiguousExecutionError` | A mutation may have reached IG before a network or timeout failure. | Reconcile account state or query by deal reference; never replay blindly. |
| `LiveTradingPermissionError` | A live-environment mutation was called without an acknowledged `TradingPermit`. | Construct the client with an explicit `TradingPermit` after confirming live intent. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.operations.watchlists.delete()`

Delete one watchlist.

Official IG reference: [https://labs.ig.com/reference/watchlists-watchlist-id.html](https://labs.ig.com/reference/watchlists-watchlist-id.html)

### Signatures

- Sync: `(watchlist_id: 'str') -> 'WatchlistMutationResponse'`
- Async: `(watchlist_id: 'str') -> 'WatchlistMutationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `watchlist_id` | `str` | required | - | IG watchlist identifier. |

### Sync example

```python
result = ig.operations.watchlists.delete(watchlist_id="12345")
```

### Async example

```python
result = await ig.operations.watchlists.delete(watchlist_id="12345")
```

### Response shape: `WatchlistMutationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `status` | `str | None` | default: `None` |

### Response example

```json
{
  "status": "ENABLED"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Deletion is permanent at IG and does not delete any market.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `AmbiguousExecutionError` | A mutation may have reached IG before a network or timeout failure. | Reconcile account state or query by deal reference; never replay blindly. |
| `LiveTradingPermissionError` | A live-environment mutation was called without an acknowledged `TradingPermit`. | Construct the client with an explicit `TradingPermit` after confirming live intent. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.operations.watchlists.remove_market()`

Remove one market epic from a watchlist.

Official IG reference: [https://labs.ig.com/reference/watchlists-watchlist-id-epic.html](https://labs.ig.com/reference/watchlists-watchlist-id-epic.html)

### Signatures

- Sync: `(watchlist_id: 'str', epic: 'str') -> 'WatchlistMutationResponse'`
- Async: `(watchlist_id: 'str', epic: 'str') -> 'WatchlistMutationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `watchlist_id` | `str` | required | - | IG watchlist identifier. |
| `epic` | `str` | required | - | IG market epic. |

### Sync example

```python
result = ig.operations.watchlists.remove_market(watchlist_id="12345", epic="CS.D.EURUSD.CFD.IP")
```

### Async example

```python
result = await ig.operations.watchlists.remove_market(watchlist_id="12345", epic="CS.D.EURUSD.CFD.IP")
```

### Response shape: `WatchlistMutationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `status` | `str | None` | default: `None` |

### Response example

```json
{
  "status": "ENABLED"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- The watchlist and market association must exist for the active account.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `AuthenticationError` | IG rejected the credentials, required session values were absent, or refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access the requested resource or action. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with bounded backoff. |
| `ProviderRejectionError` | IG rejected an otherwise well-formed request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `ResourceNotFoundError` | The requested provider resource does not exist or is inaccessible. | Verify the identifier and active account before retrying. |
| `AmbiguousExecutionError` | A mutation may have reached IG before a network or timeout failure. | Reconcile account state or query by deal reference; never replay blindly. |
| `LiveTradingPermissionError` | A live-environment mutation was called without an acknowledged `TradingPermit`. | Construct the client with an explicit `TradingPermit` after confirming live intent. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |
