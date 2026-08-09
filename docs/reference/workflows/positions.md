<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Positions workflows

Examples assume an initialized synchronous or asynchronous client named `ig`.

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
