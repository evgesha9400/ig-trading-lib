<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Positions methods

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.positions.list()`

List all open positions for the active account.

Official IG reference: [https://labs.ig.com/reference/positions.html](https://labs.ig.com/reference/positions.html)

### Signatures

- Sync: `() -> 'PositionsResponse'`
- Async: `() -> 'PositionsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.positions.list()
```

### Async example

```python
result = await ig.operations.positions.list()
```

### Response shape: `PositionsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `positions[]` | `tuple[PositionSummary, ...]` | default: `()` |
| `positions[].position` | `Position` | required |
| `positions[].position.contract_size` | `Decimal | None` | default: `None` |
| `positions[].position.controlled_risk` | `bool | None` | default: `None` |
| `positions[].position.created_date` | `str | None` | default: `None` |
| `positions[].position.created_date_utc` | `str | None` | default: `None` |
| `positions[].position.currency` | `str | None` | default: `None` |
| `positions[].position.deal_id` | `str` | required |
| `positions[].position.deal_reference` | `str | None` | default: `None` |
| `positions[].position.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `positions[].position.size` | `Decimal | None` | default: `None` |
| `positions[].position.level` | `Decimal | None` | default: `None` |
| `positions[].position.limit_level` | `Decimal | None` | default: `None` |
| `positions[].position.limited_risk_premium` | `Decimal | None` | default: `None` |
| `positions[].position.stop_level` | `Decimal | None` | default: `None` |
| `positions[].position.trailing_step` | `Decimal | None` | default: `None` |
| `positions[].position.trailing_stop_distance` | `Decimal | None` | default: `None` |
| `positions[].market` | `DealingMarket` | required |
| `positions[].market.bid` | `Decimal | None` | default: `None` |
| `positions[].market.delay_time` | `int | None` | default: `None` |
| `positions[].market.epic` | `str` | required |
| `positions[].market.expiry` | `str | None` | default: `None` |
| `positions[].market.high` | `Decimal | None` | default: `None` |
| `positions[].market.instrument_name` | `str | None` | default: `None` |
| `positions[].market.instrument_type` | `str | None` | default: `None` |
| `positions[].market.low` | `Decimal | None` | default: `None` |
| `positions[].market.market_status` | `str | None` | default: `None` |
| `positions[].market.net_change` | `Decimal | None` | default: `None` |
| `positions[].market.offer` | `Decimal | None` | default: `None` |
| `positions[].market.percentage_change` | `Decimal | None` | default: `None` |
| `positions[].market.scaling_factor` | `Decimal | None` | default: `None` |
| `positions[].market.streaming_prices_available` | `bool | None` | default: `None` |
| `positions[].market.update_time` | `str | None` | default: `None` |
| `positions[].market.update_time_utc` | `str | None` | default: `None` |
| `positions[].market.lot_size` | `Decimal | None` | default: `None` |

### Response example

```json
{
  "positions": [
    {
      "position": {
        "contract_size": "1.0",
        "controlled_risk": true,
        "created_date": "example",
        "created_date_utc": "example",
        "currency": "GBP",
        "deal_id": "DIAAAABBBCCC",
        "deal_reference": "ABC123",
        "direction": "BUY",
        "size": "1.0",
        "level": "1.0",
        "limit_level": "1.0",
        "limited_risk_premium": "1.0",
        "stop_level": "1.0",
        "trailing_step": "1.0",
        "trailing_stop_distance": "1.0"
      },
      "market": {
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

## `ig.operations.positions.get()`

Retrieve one open position by deal identifier.

Official IG reference: [https://labs.ig.com/reference/positions-deal-id.html](https://labs.ig.com/reference/positions-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str') -> 'PositionResponse'`
- Async: `(deal_id: 'str') -> 'PositionResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |

### Sync example

```python
result = ig.operations.positions.get(deal_id="DIAAAABBBCCC")
```

### Async example

```python
result = await ig.operations.positions.get(deal_id="DIAAAABBBCCC")
```

### Response shape: `PositionResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `position` | `Position` | required |
| `position.contract_size` | `Decimal | None` | default: `None` |
| `position.controlled_risk` | `bool | None` | default: `None` |
| `position.created_date` | `str | None` | default: `None` |
| `position.created_date_utc` | `str | None` | default: `None` |
| `position.currency` | `str | None` | default: `None` |
| `position.deal_id` | `str` | required |
| `position.deal_reference` | `str | None` | default: `None` |
| `position.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `position.size` | `Decimal | None` | default: `None` |
| `position.level` | `Decimal | None` | default: `None` |
| `position.limit_level` | `Decimal | None` | default: `None` |
| `position.limited_risk_premium` | `Decimal | None` | default: `None` |
| `position.stop_level` | `Decimal | None` | default: `None` |
| `position.trailing_step` | `Decimal | None` | default: `None` |
| `position.trailing_stop_distance` | `Decimal | None` | default: `None` |
| `market` | `DealingMarket` | required |
| `market.bid` | `Decimal | None` | default: `None` |
| `market.delay_time` | `int | None` | default: `None` |
| `market.epic` | `str` | required |
| `market.expiry` | `str | None` | default: `None` |
| `market.high` | `Decimal | None` | default: `None` |
| `market.instrument_name` | `str | None` | default: `None` |
| `market.instrument_type` | `str | None` | default: `None` |
| `market.low` | `Decimal | None` | default: `None` |
| `market.market_status` | `str | None` | default: `None` |
| `market.net_change` | `Decimal | None` | default: `None` |
| `market.offer` | `Decimal | None` | default: `None` |
| `market.percentage_change` | `Decimal | None` | default: `None` |
| `market.scaling_factor` | `Decimal | None` | default: `None` |
| `market.streaming_prices_available` | `bool | None` | default: `None` |
| `market.update_time` | `str | None` | default: `None` |
| `market.update_time_utc` | `str | None` | default: `None` |
| `market.lot_size` | `Decimal | None` | default: `None` |

### Response example

```json
{
  "position": {
    "contract_size": "1.0",
    "controlled_risk": true,
    "created_date": "example",
    "created_date_utc": "example",
    "currency": "GBP",
    "deal_id": "DIAAAABBBCCC",
    "deal_reference": "ABC123",
    "direction": "BUY",
    "size": "1.0",
    "level": "1.0",
    "limit_level": "1.0",
    "limited_risk_premium": "1.0",
    "stop_level": "1.0",
    "trailing_step": "1.0",
    "trailing_stop_distance": "1.0"
  },
  "market": {
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
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The position must belong to the active account.

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

## `ig.operations.positions.create()`

Create an OTC position and return its deal reference.

Official IG reference: [https://labs.ig.com/reference/positions-otc.html](https://labs.ig.com/reference/positions-otc.html)

### Signatures

- Sync: `(request: 'CreatePositionRequest') -> 'DealReferenceResponse'`
- Async: `(request: 'CreatePositionRequest') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CreatePositionRequest` | required | - | Validated typed request body. |
| `request.epic` | `str` | required | minimum length `1` | IG market epic. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.order_type` | `Literal['LIMIT', 'MARKET', 'QUOTE']` | required | - | Provider order type for the requested deal. |
| `request.currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter deal currency code. |
| `request.expiry` | `str` | default: `'-'` | - | Market expiry, or `-` for a non-expiring market. |
| `request.force_open` | `bool` | default: `True` | - | Whether the deal must create a separate position. |
| `request.guaranteed_stop` | `bool` | default: `False` | - | Whether the stop is guaranteed by IG. |
| `request.level` | `Decimal | None` | default: `None` | - | Requested order or quote price level. |
| `request.quote_id` | `str | None` | default: `None` | - | IG quote identifier required for a `QUOTE` order. |
| `request.time_in_force` | `Literal['EXECUTE_AND_ELIMINATE', 'FILL_OR_KILL'] | None` | default: `None` | - | Provider rule controlling how long or how aggressively an order executes. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.trailing_stop` | `bool | None` | default: `None` | - | Whether trailing-stop behavior is enabled. |
| `request.trailing_stop_increment` | `Decimal | None` | default: `None` | - | Minimum movement before a trailing stop advances. |
| `request.deal_reference` | `str | None` | default: `None` | - | Client or provider reference used to correlate a deal. |

### Sync example

```python
from ig_trading_lib.operations.dealing import CreatePositionRequest

result = ig.operations.positions.create(request=CreatePositionRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", order_type="MARKET", currency_code="GBP"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import CreatePositionRequest

result = await ig.operations.positions.create(request=CreatePositionRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", order_type="MARKET", currency_code="GBP"))
```

### Response shape: `DealReferenceResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `deal_reference` | `str` | required |

### Response example

```json
{
  "deal_reference": "ABC123"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Order-level, stop, limit, force-open, quote, and trailing-stop combinations are validated before sending.

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

## `ig.operations.positions.amend()`

Amend stops or limits on an open position.

Official IG reference: [https://labs.ig.com/reference/positions-otc-deal-id.html](https://labs.ig.com/reference/positions-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str', request: 'AmendPositionRequest') -> 'DealReferenceResponse'`
- Async: `(deal_id: 'str', request: 'AmendPositionRequest') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |
| `request` | `AmendPositionRequest` | required | - | Validated typed request body. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.trailing_stop` | `bool | None` | default: `None` | - | Whether trailing-stop behavior is enabled. |
| `request.trailing_stop_distance` | `Decimal | None` | default: `None` | - | Distance maintained by an amended trailing stop. |
| `request.trailing_stop_increment` | `Decimal | None` | default: `None` | - | Minimum movement before a trailing stop advances. |

### Sync example

```python
from ig_trading_lib.operations.dealing import AmendPositionRequest

result = ig.operations.positions.amend(deal_id="DIAAAABBBCCC", request=AmendPositionRequest(limit_level="1.0900"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import AmendPositionRequest

result = await ig.operations.positions.amend(deal_id="DIAAAABBBCCC", request=AmendPositionRequest(limit_level="1.0900"))
```

### Response shape: `DealReferenceResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `deal_reference` | `str` | required |

### Response example

```json
{
  "deal_reference": "ABC123"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Guaranteed and trailing-stop amendments require provider-valid field combinations.

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

## `ig.operations.positions.close()`

Close all or part of an OTC position.

Official IG reference: [https://labs.ig.com/reference/positions-otc.html](https://labs.ig.com/reference/positions-otc.html)

### Signatures

- Sync: `(request: 'ClosePositionRequest') -> 'DealReferenceResponse'`
- Async: `(request: 'ClosePositionRequest') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `ClosePositionRequest` | required | - | Validated typed request body. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.order_type` | `Literal['LIMIT', 'MARKET', 'QUOTE']` | default: `'MARKET'` | - | Provider order type for the requested deal. |
| `request.deal_id` | `str | None` | default: `None` | - | IG identifier of an existing position or working order. |
| `request.epic` | `str | None` | default: `None` | - | IG market epic. |
| `request.expiry` | `str | None` | default: `None` | - | Market expiry, or `-` for a non-expiring market. |
| `request.level` | `Decimal | None` | default: `None` | - | Requested order or quote price level. |
| `request.quote_id` | `str | None` | default: `None` | - | IG quote identifier required for a `QUOTE` order. |
| `request.time_in_force` | `Literal['EXECUTE_AND_ELIMINATE', 'FILL_OR_KILL'] | None` | default: `None` | - | Provider rule controlling how long or how aggressively an order executes. |

### Sync example

```python
from ig_trading_lib.operations.dealing import ClosePositionRequest

result = ig.operations.positions.close(request=ClosePositionRequest(direction="SELL", size="1", deal_id="DIAAAABBBCCC"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import ClosePositionRequest

result = await ig.operations.positions.close(request=ClosePositionRequest(direction="SELL", size="1", deal_id="DIAAAABBBCCC"))
```

### Response shape: `DealReferenceResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `deal_reference` | `str` | required |

### Response example

```json
{
  "deal_reference": "ABC123"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Identify the position by exactly one of `deal_id` or `epic`; `epic` also requires `expiry`.

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

## `ig.workflows.positions.open_and_confirm()`

Open a position and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/positions-otc.html](https://labs.ig.com/reference/positions-otc.html)

### Signatures

- Sync: `(request: 'CreatePositionRequest') -> 'DealConfirmationResponse'`
- Async: `(request: 'CreatePositionRequest') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CreatePositionRequest` | required | - | Validated typed request body. |
| `request.epic` | `str` | required | minimum length `1` | IG market epic. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.order_type` | `Literal['LIMIT', 'MARKET', 'QUOTE']` | required | - | Provider order type for the requested deal. |
| `request.currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter deal currency code. |
| `request.expiry` | `str` | default: `'-'` | - | Market expiry, or `-` for a non-expiring market. |
| `request.force_open` | `bool` | default: `True` | - | Whether the deal must create a separate position. |
| `request.guaranteed_stop` | `bool` | default: `False` | - | Whether the stop is guaranteed by IG. |
| `request.level` | `Decimal | None` | default: `None` | - | Requested order or quote price level. |
| `request.quote_id` | `str | None` | default: `None` | - | IG quote identifier required for a `QUOTE` order. |
| `request.time_in_force` | `Literal['EXECUTE_AND_ELIMINATE', 'FILL_OR_KILL'] | None` | default: `None` | - | Provider rule controlling how long or how aggressively an order executes. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.trailing_stop` | `bool | None` | default: `None` | - | Whether trailing-stop behavior is enabled. |
| `request.trailing_stop_increment` | `Decimal | None` | default: `None` | - | Minimum movement before a trailing stop advances. |
| `request.deal_reference` | `str | None` | default: `None` | - | Client or provider reference used to correlate a deal. |

### Sync example

```python
from ig_trading_lib.operations.dealing import CreatePositionRequest

result = ig.workflows.positions.open_and_confirm(request=CreatePositionRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", order_type="MARKET", currency_code="GBP"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import CreatePositionRequest

result = await ig.workflows.positions.open_and_confirm(request=CreatePositionRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", order_type="MARKET", currency_code="GBP"))
```

### Response shape: `DealConfirmationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `affected_deals[]` | `tuple[AffectedDeal, ...]` | default: `()` |
| `affected_deals[].deal_id` | `str` | required |
| `affected_deals[].status` | `str` | required |
| `date` | `str | None` | default: `None` |
| `deal_reference` | `str` | required |
| `deal_id` | `str | None` | default: `None` |
| `deal_status` | `str | None` | default: `None` |
| `direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `epic` | `str | None` | default: `None` |
| `expiry` | `str | None` | default: `None` |
| `guaranteed_stop` | `bool | None` | default: `None` |
| `level` | `Decimal | None` | default: `None` |
| `limit_distance` | `Decimal | None` | default: `None` |
| `limit_level` | `Decimal | None` | default: `None` |
| `profit` | `Decimal | None` | default: `None` |
| `profit_currency` | `str | None` | default: `None` |
| `reason` | `str | None` | default: `None` |
| `size` | `Decimal | None` | default: `None` |
| `status` | `str | None` | default: `None` |
| `stop_distance` | `Decimal | None` | default: `None` |
| `stop_level` | `Decimal | None` | default: `None` |
| `trailing_stop` | `bool | None` | default: `None` |

### Response example

```json
{
  "affected_deals": [
    {
      "deal_id": "DIAAAABBBCCC",
      "status": "ENABLED"
    }
  ],
  "date": "example",
  "deal_reference": "ABC123",
  "deal_id": "DIAAAABBBCCC",
  "deal_status": "example",
  "direction": "BUY",
  "epic": "CS.D.EURUSD.CFD.IP",
  "expiry": "-",
  "guaranteed_stop": true,
  "level": "1.0",
  "limit_distance": "1.0",
  "limit_level": "1.0",
  "profit": "1.0",
  "profit_currency": "example",
  "reason": "example",
  "size": "1.0",
  "status": "ENABLED",
  "stop_distance": "1.0",
  "stop_level": "1.0",
  "trailing_stop": true
}
```

### Limitations

- A workflow performs a mutation followed by a separate confirmation request.
- Confirmation failure does not roll back an accepted mutation.
- A returned `DealConfirmationError` means the open request may already have succeeded.

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
| `DealConfirmationError` | IG accepted a mutation but its follow-up confirmation could not be retrieved. | Preserve `deal_reference` from the exception and reconcile it; do not replay the mutation. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.workflows.positions.amend_and_confirm()`

Amend a position and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/positions-otc-deal-id.html](https://labs.ig.com/reference/positions-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str', request: 'AmendPositionRequest') -> 'DealConfirmationResponse'`
- Async: `(deal_id: 'str', request: 'AmendPositionRequest') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |
| `request` | `AmendPositionRequest` | required | - | Validated typed request body. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.trailing_stop` | `bool | None` | default: `None` | - | Whether trailing-stop behavior is enabled. |
| `request.trailing_stop_distance` | `Decimal | None` | default: `None` | - | Distance maintained by an amended trailing stop. |
| `request.trailing_stop_increment` | `Decimal | None` | default: `None` | - | Minimum movement before a trailing stop advances. |

### Sync example

```python
from ig_trading_lib.operations.dealing import AmendPositionRequest

result = ig.workflows.positions.amend_and_confirm(deal_id="DIAAAABBBCCC", request=AmendPositionRequest(limit_level="1.0900"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import AmendPositionRequest

result = await ig.workflows.positions.amend_and_confirm(deal_id="DIAAAABBBCCC", request=AmendPositionRequest(limit_level="1.0900"))
```

### Response shape: `DealConfirmationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `affected_deals[]` | `tuple[AffectedDeal, ...]` | default: `()` |
| `affected_deals[].deal_id` | `str` | required |
| `affected_deals[].status` | `str` | required |
| `date` | `str | None` | default: `None` |
| `deal_reference` | `str` | required |
| `deal_id` | `str | None` | default: `None` |
| `deal_status` | `str | None` | default: `None` |
| `direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `epic` | `str | None` | default: `None` |
| `expiry` | `str | None` | default: `None` |
| `guaranteed_stop` | `bool | None` | default: `None` |
| `level` | `Decimal | None` | default: `None` |
| `limit_distance` | `Decimal | None` | default: `None` |
| `limit_level` | `Decimal | None` | default: `None` |
| `profit` | `Decimal | None` | default: `None` |
| `profit_currency` | `str | None` | default: `None` |
| `reason` | `str | None` | default: `None` |
| `size` | `Decimal | None` | default: `None` |
| `status` | `str | None` | default: `None` |
| `stop_distance` | `Decimal | None` | default: `None` |
| `stop_level` | `Decimal | None` | default: `None` |
| `trailing_stop` | `bool | None` | default: `None` |

### Response example

```json
{
  "affected_deals": [
    {
      "deal_id": "DIAAAABBBCCC",
      "status": "ENABLED"
    }
  ],
  "date": "example",
  "deal_reference": "ABC123",
  "deal_id": "DIAAAABBBCCC",
  "deal_status": "example",
  "direction": "BUY",
  "epic": "CS.D.EURUSD.CFD.IP",
  "expiry": "-",
  "guaranteed_stop": true,
  "level": "1.0",
  "limit_distance": "1.0",
  "limit_level": "1.0",
  "profit": "1.0",
  "profit_currency": "example",
  "reason": "example",
  "size": "1.0",
  "status": "ENABLED",
  "stop_distance": "1.0",
  "stop_level": "1.0",
  "trailing_stop": true
}
```

### Limitations

- A workflow performs a mutation followed by a separate confirmation request.
- Confirmation failure does not roll back an accepted mutation.
- A returned `DealConfirmationError` means the amendment may already have succeeded.

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
| `DealConfirmationError` | IG accepted a mutation but its follow-up confirmation could not be retrieved. | Preserve `deal_reference` from the exception and reconcile it; do not replay the mutation. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |

## `ig.workflows.positions.close_and_confirm()`

Close a position and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/positions-otc.html](https://labs.ig.com/reference/positions-otc.html)

### Signatures

- Sync: `(request: 'ClosePositionRequest') -> 'DealConfirmationResponse'`
- Async: `(request: 'ClosePositionRequest') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `ClosePositionRequest` | required | - | Validated typed request body. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.order_type` | `Literal['LIMIT', 'MARKET', 'QUOTE']` | default: `'MARKET'` | - | Provider order type for the requested deal. |
| `request.deal_id` | `str | None` | default: `None` | - | IG identifier of an existing position or working order. |
| `request.epic` | `str | None` | default: `None` | - | IG market epic. |
| `request.expiry` | `str | None` | default: `None` | - | Market expiry, or `-` for a non-expiring market. |
| `request.level` | `Decimal | None` | default: `None` | - | Requested order or quote price level. |
| `request.quote_id` | `str | None` | default: `None` | - | IG quote identifier required for a `QUOTE` order. |
| `request.time_in_force` | `Literal['EXECUTE_AND_ELIMINATE', 'FILL_OR_KILL'] | None` | default: `None` | - | Provider rule controlling how long or how aggressively an order executes. |

### Sync example

```python
from ig_trading_lib.operations.dealing import ClosePositionRequest

result = ig.workflows.positions.close_and_confirm(request=ClosePositionRequest(direction="SELL", size="1", deal_id="DIAAAABBBCCC"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import ClosePositionRequest

result = await ig.workflows.positions.close_and_confirm(request=ClosePositionRequest(direction="SELL", size="1", deal_id="DIAAAABBBCCC"))
```

### Response shape: `DealConfirmationResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `affected_deals[]` | `tuple[AffectedDeal, ...]` | default: `()` |
| `affected_deals[].deal_id` | `str` | required |
| `affected_deals[].status` | `str` | required |
| `date` | `str | None` | default: `None` |
| `deal_reference` | `str` | required |
| `deal_id` | `str | None` | default: `None` |
| `deal_status` | `str | None` | default: `None` |
| `direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `epic` | `str | None` | default: `None` |
| `expiry` | `str | None` | default: `None` |
| `guaranteed_stop` | `bool | None` | default: `None` |
| `level` | `Decimal | None` | default: `None` |
| `limit_distance` | `Decimal | None` | default: `None` |
| `limit_level` | `Decimal | None` | default: `None` |
| `profit` | `Decimal | None` | default: `None` |
| `profit_currency` | `str | None` | default: `None` |
| `reason` | `str | None` | default: `None` |
| `size` | `Decimal | None` | default: `None` |
| `status` | `str | None` | default: `None` |
| `stop_distance` | `Decimal | None` | default: `None` |
| `stop_level` | `Decimal | None` | default: `None` |
| `trailing_stop` | `bool | None` | default: `None` |

### Response example

```json
{
  "affected_deals": [
    {
      "deal_id": "DIAAAABBBCCC",
      "status": "ENABLED"
    }
  ],
  "date": "example",
  "deal_reference": "ABC123",
  "deal_id": "DIAAAABBBCCC",
  "deal_status": "example",
  "direction": "BUY",
  "epic": "CS.D.EURUSD.CFD.IP",
  "expiry": "-",
  "guaranteed_stop": true,
  "level": "1.0",
  "limit_distance": "1.0",
  "limit_level": "1.0",
  "profit": "1.0",
  "profit_currency": "example",
  "reason": "example",
  "size": "1.0",
  "status": "ENABLED",
  "stop_distance": "1.0",
  "stop_level": "1.0",
  "trailing_stop": true
}
```

### Limitations

- A workflow performs a mutation followed by a separate confirmation request.
- Confirmation failure does not roll back an accepted mutation.
- A returned `DealConfirmationError` means the close request may already have succeeded.

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
| `DealConfirmationError` | IG accepted a mutation but its follow-up confirmation could not be retrieved. | Preserve `deal_reference` from the exception and reconcile it; do not replay the mutation. |
| `ValidationError` | Request construction failed or an IG response did not match the declared model. | Correct invalid request fields; report provider response drift with redacted diagnostics. |
