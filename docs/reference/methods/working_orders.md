<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Working Orders methods

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.working_orders.list()`

List all working orders for the active account.

Official IG reference: [https://labs.ig.com/reference/working-orders.html](https://labs.ig.com/reference/working-orders.html)

### Signatures

- Sync: `() -> 'WorkingOrdersResponse'`
- Async: `() -> 'WorkingOrdersResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.working_orders.list()
```

### Async example

```python
result = await ig.operations.working_orders.list()
```

### Response shape: `WorkingOrdersResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `working_orders[]` | `tuple[WorkingOrderSummary, ...]` | default: `()` |
| `working_orders[].working_order_data` | `WorkingOrderData` | required |
| `working_orders[].working_order_data.created_date` | `str | None` | default: `None` |
| `working_orders[].working_order_data.created_date_utc` | `str | None` | default: `None` |
| `working_orders[].working_order_data.currency_code` | `str | None` | default: `None` |
| `working_orders[].working_order_data.deal_id` | `str` | required |
| `working_orders[].working_order_data.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `working_orders[].working_order_data.dma` | `bool | None` | default: `None` |
| `working_orders[].working_order_data.epic` | `str` | required |
| `working_orders[].working_order_data.good_till_date` | `str | None` | default: `None` |
| `working_orders[].working_order_data.good_till_date_iso` | `str | None` | default: `None` |
| `working_orders[].working_order_data.guaranteed_stop` | `bool | None` | default: `None` |
| `working_orders[].working_order_data.limit_distance` | `Decimal | None` | default: `None` |
| `working_orders[].working_order_data.limited_risk_premium` | `Decimal | None` | default: `None` |
| `working_orders[].working_order_data.order_level` | `Decimal | None` | default: `None` |
| `working_orders[].working_order_data.order_size` | `Decimal | None` | default: `None` |
| `working_orders[].working_order_data.order_type` | `str | None` | default: `None` |
| `working_orders[].working_order_data.stop_distance` | `Decimal | None` | default: `None` |
| `working_orders[].working_order_data.time_in_force` | `str | None` | default: `None` |
| `working_orders[].market_data` | `WorkingOrderMarket` | required |
| `working_orders[].market_data.bid` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.delay_time` | `int | None` | default: `None` |
| `working_orders[].market_data.epic` | `str` | required |
| `working_orders[].market_data.expiry` | `str | None` | default: `None` |
| `working_orders[].market_data.high` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.instrument_name` | `str | None` | default: `None` |
| `working_orders[].market_data.instrument_type` | `str | None` | default: `None` |
| `working_orders[].market_data.low` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.market_status` | `str | None` | default: `None` |
| `working_orders[].market_data.net_change` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.offer` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.percentage_change` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.scaling_factor` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.streaming_prices_available` | `bool | None` | default: `None` |
| `working_orders[].market_data.update_time` | `str | None` | default: `None` |
| `working_orders[].market_data.update_time_utc` | `str | None` | default: `None` |
| `working_orders[].market_data.lot_size` | `Decimal | None` | default: `None` |
| `working_orders[].market_data.exchange_id` | `str | None` | default: `None` |

### Response example

```json
{
  "working_orders": [
    {
      "working_order_data": {
        "created_date": "example",
        "created_date_utc": "example",
        "currency_code": "GBP",
        "deal_id": "DIAAAABBBCCC",
        "direction": "BUY",
        "dma": true,
        "epic": "CS.D.EURUSD.CFD.IP",
        "good_till_date": "example",
        "good_till_date_iso": "example",
        "guaranteed_stop": true,
        "limit_distance": "1.0",
        "limited_risk_premium": "1.0",
        "order_level": "1.0",
        "order_size": "1.0",
        "order_type": "example",
        "stop_distance": "1.0",
        "time_in_force": "example"
      },
      "market_data": {
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
        "lot_size": "1.0",
        "exchange_id": "example"
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

## `ig.operations.working_orders.create()`

Create an OTC working order and return its deal reference.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc.html](https://labs.ig.com/reference/working-orders-otc.html)

### Signatures

- Sync: `(request: 'CreateWorkingOrderRequest') -> 'DealReferenceResponse'`
- Async: `(request: 'CreateWorkingOrderRequest') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CreateWorkingOrderRequest` | required | - | Validated typed request body. |
| `request.epic` | `str` | required | minimum length `1` | IG market epic. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.level` | `Decimal` | required | - | Requested order or quote price level. |
| `request.order_type` | `Literal['LIMIT', 'STOP']` | required | - | Provider order type for the requested deal. |
| `request.currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter deal currency code. |
| `request.deal_reference` | `str | None` | default: `None` | minimum length `1`; maximum length `30` | Client or provider reference used to correlate a deal. |
| `request.expiry` | `str` | default: `'-'` | - | Market expiry, or `-` for a non-expiring market. |
| `request.force_open` | `bool` | default: `True` | - | Whether the deal must create a separate position. |
| `request.guaranteed_stop` | `bool` | default: `False` | - | Whether the stop is guaranteed by IG. |
| `request.good_till_date` | `str | None` | default: `None` | - | Expiry timestamp for a `GOOD_TILL_DATE` working order. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.time_in_force` | `Literal['GOOD_TILL_CANCELLED', 'GOOD_TILL_DATE']` | default: `'GOOD_TILL_CANCELLED'` | - | Provider rule controlling how long or how aggressively an order executes. |

### Sync example

```python
from ig_trading_lib.operations.dealing import CreateWorkingOrderRequest

result = ig.operations.working_orders.create(request=CreateWorkingOrderRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", level="1.0700", order_type="LIMIT", currency_code="GBP"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import CreateWorkingOrderRequest

result = await ig.operations.working_orders.create(request=CreateWorkingOrderRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", level="1.0700", order_type="LIMIT", currency_code="GBP"))
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
- Good-till-date, stop, limit, and guaranteed-stop combinations are validated before sending.

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

## `ig.operations.working_orders.amend()`

Amend an existing OTC working order.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc-deal-id.html](https://labs.ig.com/reference/working-orders-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str', request: 'AmendWorkingOrderRequest') -> 'DealReferenceResponse'`
- Async: `(deal_id: 'str', request: 'AmendWorkingOrderRequest') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |
| `request` | `AmendWorkingOrderRequest` | required | - | Validated typed request body. |
| `request.level` | `Decimal` | required | - | Requested order or quote price level. |
| `request.order_type` | `Literal['LIMIT', 'STOP']` | required | - | Provider order type for the requested deal. |
| `request.time_in_force` | `Literal['GOOD_TILL_CANCELLED', 'GOOD_TILL_DATE']` | required | - | Provider rule controlling how long or how aggressively an order executes. |
| `request.good_till_date` | `str | None` | default: `None` | - | Expiry timestamp for a `GOOD_TILL_DATE` working order. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |

### Sync example

```python
from ig_trading_lib.operations.dealing import AmendWorkingOrderRequest

result = ig.operations.working_orders.amend(deal_id="DIAAAABBBCCC", request=AmendWorkingOrderRequest(level="1.0710", order_type="LIMIT", time_in_force="GOOD_TILL_CANCELLED"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import AmendWorkingOrderRequest

result = await ig.operations.working_orders.amend(deal_id="DIAAAABBBCCC", request=AmendWorkingOrderRequest(level="1.0710", order_type="LIMIT", time_in_force="GOOD_TILL_CANCELLED"))
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
- Good-till-date, stop, limit, and guaranteed-stop combinations are validated before sending.

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

## `ig.operations.working_orders.delete()`

Delete an existing OTC working order.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc-deal-id.html](https://labs.ig.com/reference/working-orders-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str') -> 'DealReferenceResponse'`
- Async: `(deal_id: 'str') -> 'DealReferenceResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |

### Sync example

```python
result = ig.operations.working_orders.delete(deal_id="DIAAAABBBCCC")
```

### Async example

```python
result = await ig.operations.working_orders.delete(deal_id="DIAAAABBBCCC")
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
- Deletion is accepted asynchronously by IG and returns a deal reference.

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

## `ig.workflows.working_orders.place_and_confirm()`

Place a working order and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc.html](https://labs.ig.com/reference/working-orders-otc.html)

### Signatures

- Sync: `(request: 'CreateWorkingOrderRequest') -> 'DealConfirmationResponse'`
- Async: `(request: 'CreateWorkingOrderRequest') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CreateWorkingOrderRequest` | required | - | Validated typed request body. |
| `request.epic` | `str` | required | minimum length `1` | IG market epic. |
| `request.direction` | `Literal['BUY', 'SELL']` | required | - | Deal direction; `BUY` or `SELL`. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.level` | `Decimal` | required | - | Requested order or quote price level. |
| `request.order_type` | `Literal['LIMIT', 'STOP']` | required | - | Provider order type for the requested deal. |
| `request.currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter deal currency code. |
| `request.deal_reference` | `str | None` | default: `None` | minimum length `1`; maximum length `30` | Client or provider reference used to correlate a deal. |
| `request.expiry` | `str` | default: `'-'` | - | Market expiry, or `-` for a non-expiring market. |
| `request.force_open` | `bool` | default: `True` | - | Whether the deal must create a separate position. |
| `request.guaranteed_stop` | `bool` | default: `False` | - | Whether the stop is guaranteed by IG. |
| `request.good_till_date` | `str | None` | default: `None` | - | Expiry timestamp for a `GOOD_TILL_DATE` working order. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.time_in_force` | `Literal['GOOD_TILL_CANCELLED', 'GOOD_TILL_DATE']` | default: `'GOOD_TILL_CANCELLED'` | - | Provider rule controlling how long or how aggressively an order executes. |

### Sync example

```python
from ig_trading_lib.operations.dealing import CreateWorkingOrderRequest

result = ig.workflows.working_orders.place_and_confirm(request=CreateWorkingOrderRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", level="1.0700", order_type="LIMIT", currency_code="GBP"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import CreateWorkingOrderRequest

result = await ig.workflows.working_orders.place_and_confirm(request=CreateWorkingOrderRequest(epic="CS.D.EURUSD.CFD.IP", direction="BUY", size="1", level="1.0700", order_type="LIMIT", currency_code="GBP"))
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
- A returned `DealConfirmationError` means the order may already have been placed.

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

## `ig.workflows.working_orders.amend_and_confirm()`

Amend a working order and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc-deal-id.html](https://labs.ig.com/reference/working-orders-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str', request: 'AmendWorkingOrderRequest') -> 'DealConfirmationResponse'`
- Async: `(deal_id: 'str', request: 'AmendWorkingOrderRequest') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |
| `request` | `AmendWorkingOrderRequest` | required | - | Validated typed request body. |
| `request.level` | `Decimal` | required | - | Requested order or quote price level. |
| `request.order_type` | `Literal['LIMIT', 'STOP']` | required | - | Provider order type for the requested deal. |
| `request.time_in_force` | `Literal['GOOD_TILL_CANCELLED', 'GOOD_TILL_DATE']` | required | - | Provider rule controlling how long or how aggressively an order executes. |
| `request.good_till_date` | `str | None` | default: `None` | - | Expiry timestamp for a `GOOD_TILL_DATE` working order. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.limit_distance` | `Decimal | None` | default: `None` | - | Limit distance in market points; mutually exclusive with `limit_level`. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |
| `request.stop_distance` | `Decimal | None` | default: `None` | - | Stop distance in market points; mutually exclusive with `stop_level`. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |

### Sync example

```python
from ig_trading_lib.operations.dealing import AmendWorkingOrderRequest

result = ig.workflows.working_orders.amend_and_confirm(deal_id="DIAAAABBBCCC", request=AmendWorkingOrderRequest(level="1.0710", order_type="LIMIT", time_in_force="GOOD_TILL_CANCELLED"))
```

### Async example

```python
from ig_trading_lib.operations.dealing import AmendWorkingOrderRequest

result = await ig.workflows.working_orders.amend_and_confirm(deal_id="DIAAAABBBCCC", request=AmendWorkingOrderRequest(level="1.0710", order_type="LIMIT", time_in_force="GOOD_TILL_CANCELLED"))
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

## `ig.workflows.working_orders.cancel_and_confirm()`

Cancel a working order and retrieve its final deal confirmation.

Official IG reference: [https://labs.ig.com/reference/working-orders-otc-deal-id.html](https://labs.ig.com/reference/working-orders-otc-deal-id.html)

### Signatures

- Sync: `(deal_id: 'str') -> 'DealConfirmationResponse'`
- Async: `(deal_id: 'str') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_id` | `str` | required | - | IG identifier of an existing position or working order. |

### Sync example

```python
result = ig.workflows.working_orders.cancel_and_confirm(deal_id="DIAAAABBBCCC")
```

### Async example

```python
result = await ig.workflows.working_orders.cancel_and_confirm(deal_id="DIAAAABBBCCC")
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
- A returned `DealConfirmationError` means the cancellation may already have succeeded.

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
