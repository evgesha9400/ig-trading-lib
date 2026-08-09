<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Indicative Costs operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.indicative_costs.quote_open()`

Calculate indicative costs for opening a position.

Official IG reference: [https://labs.ig.com/reference/indicative-costs-and-charges-open.html](https://labs.ig.com/reference/indicative-costs-and-charges-open.html)

### Signatures

- Sync: `(request: 'OpenIndicativeCostRequest') -> 'OpenIndicativeCostResponse'`
- Async: `(request: 'OpenIndicativeCostRequest') -> 'OpenIndicativeCostResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `OpenIndicativeCostRequest` | required | - | Validated typed request body. |
| `request.ask` | `Decimal` | required | - | Current provider ask price used for an indicative calculation. |
| `request.bid` | `Decimal` | required | - | Current provider bid price used for an indicative calculation. |
| `request.deal_currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter currency code used for the cost calculation. |
| `request.deal_reference` | `str` | required | minimum length `1` | Client or provider reference used to correlate a deal. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` | - | Deal direction; `BUY` or `SELL`. |
| `request.epic` | `str | None` | default: `None` | - | IG market epic. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.instrument_id` | `str | None` | default: `None` | - | Provider instrument identifier used by indicative-cost operations. |
| `request.knockout_premium` | `Decimal | None` | default: `None` | - | Knockout premium used in an indicative-cost calculation. |
| `request.price_level` | `Decimal | None` | default: `None` | - | Current price level used in an indicative-cost calculation. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |

### Sync example

```python
from ig_trading_lib.operations.costs import OpenIndicativeCostRequest

result = ig.operations.indicative_costs.quote_open(request=OpenIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-1", size="1"))
```

### Async example

```python
from ig_trading_lib.operations.costs import OpenIndicativeCostRequest

result = await ig.operations.indicative_costs.quote_open(request=OpenIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-1", size="1"))
```

### Response shape: `OpenIndicativeCostResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `borrowing_charge` | `Decimal | None` | default: `None` |
| `closing_commission` | `Decimal | None` | default: `None` |
| `closing_fx_fee` | `Decimal | None` | default: `None` |
| `closing_iftt` | `Decimal | None` | default: `None` |
| `closing_spread` | `Decimal | None` | default: `None` |
| `currency_code_iso` | `str | None` | default: `None` |
| `daily_running_fx_fee` | `Decimal | None` | default: `None` |
| `etp_entry_cost` | `Decimal | None` | default: `None` |
| `etp_exit_cost` | `Decimal | None` | default: `None` |
| `etp_ongoing_cost` | `Decimal | None` | default: `None` |
| `guaranteed_stop_deposit` | `Decimal | None` | default: `None` |
| `guaranteed_stop_return` | `Decimal | None` | default: `None` |
| `indicative_quote_reference` | `str | None` | default: `None` |
| `inducements` | `Decimal | None` | default: `None` |
| `knockout_premium_deposit` | `Decimal | None` | default: `None` |
| `knockout_premium_return` | `Decimal | None` | default: `None` |
| `notional_value` | `Decimal | None` | default: `None` |
| `notional_value_in_user_currency` | `Decimal | None` | default: `None` |
| `opening_commission` | `Decimal | None` | default: `None` |
| `opening_fx_fee` | `Decimal | None` | default: `None` |
| `opening_iftt` | `Decimal | None` | default: `None` |
| `opening_spread` | `Decimal | None` | default: `None` |
| `overnight_funding_fee` | `Decimal | None` | default: `None` |

### Response example

```json
{
  "borrowing_charge": "1.0",
  "closing_commission": "1.0",
  "closing_fx_fee": "1.0",
  "closing_iftt": "1.0",
  "closing_spread": "1.0",
  "currency_code_iso": "example",
  "daily_running_fx_fee": "1.0",
  "etp_entry_cost": "1.0",
  "etp_exit_cost": "1.0",
  "etp_ongoing_cost": "1.0",
  "guaranteed_stop_deposit": "1.0",
  "guaranteed_stop_return": "1.0",
  "indicative_quote_reference": "example",
  "inducements": "1.0",
  "knockout_premium_deposit": "1.0",
  "knockout_premium_return": "1.0",
  "notional_value": "1.0",
  "notional_value_in_user_currency": "1.0",
  "opening_commission": "1.0",
  "opening_fx_fee": "1.0",
  "opening_iftt": "1.0",
  "opening_spread": "1.0",
  "overnight_funding_fee": "1.0"
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The result is indicative and can differ from costs at execution time.

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

## `ig.operations.indicative_costs.quote_close()`

Calculate indicative costs for closing a position.

Official IG reference: [https://labs.ig.com/reference/indicative-costs-and-charges-close.html](https://labs.ig.com/reference/indicative-costs-and-charges-close.html)

### Signatures

- Sync: `(request: 'CloseIndicativeCostRequest') -> 'CloseIndicativeCostResponse'`
- Async: `(request: 'CloseIndicativeCostRequest') -> 'CloseIndicativeCostResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `CloseIndicativeCostRequest` | required | - | Validated typed request body. |
| `request.ask` | `Decimal` | required | - | Current provider ask price used for an indicative calculation. |
| `request.bid` | `Decimal` | required | - | Current provider bid price used for an indicative calculation. |
| `request.deal_currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter currency code used for the cost calculation. |
| `request.deal_reference` | `str` | required | minimum length `1` | Client or provider reference used to correlate a deal. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` | - | Deal direction; `BUY` or `SELL`. |
| `request.epic` | `str | None` | default: `None` | - | IG market epic. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.instrument_id` | `str | None` | default: `None` | - | Provider instrument identifier used by indicative-cost operations. |
| `request.knockout_premium` | `Decimal | None` | default: `None` | - | Knockout premium used in an indicative-cost calculation. |
| `request.price_level` | `Decimal | None` | default: `None` | - | Current price level used in an indicative-cost calculation. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.opening_level` | `Decimal` | required | - | Original opening price used for close or edit cost calculations. |

### Sync example

```python
from ig_trading_lib.operations.costs import CloseIndicativeCostRequest

result = ig.operations.indicative_costs.quote_close(request=CloseIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-2", size="1", opening_level="1.0700"))
```

### Async example

```python
from ig_trading_lib.operations.costs import CloseIndicativeCostRequest

result = await ig.operations.indicative_costs.quote_close(request=CloseIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-2", size="1", opening_level="1.0700"))
```

### Response shape: `CloseIndicativeCostResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `close` | `ClosingIndicativeCost | None` | default: `None` |
| `close.closing_commission` | `Decimal | None` | default: `None` |
| `close.closing_fx_fee` | `Decimal | None` | default: `None` |
| `close.closing_iftt` | `Decimal | None` | default: `None` |
| `close.closing_spread` | `Decimal | None` | default: `None` |
| `close.etp_exit_cost` | `Decimal | None` | default: `None` |
| `close.guaranteed_stop_return` | `Decimal | None` | default: `None` |
| `close.indicative_quote_reference` | `str | None` | default: `None` |
| `close.knockout_premium_return` | `Decimal | None` | default: `None` |
| `close.notional_value` | `Decimal | None` | default: `None` |
| `close.notional_value_in_user_currency` | `Decimal | None` | default: `None` |
| `currency_code_iso` | `str | None` | default: `None` |

### Response example

```json
{
  "close": {
    "closing_commission": "1.0",
    "closing_fx_fee": "1.0",
    "closing_iftt": "1.0",
    "closing_spread": "1.0",
    "etp_exit_cost": "1.0",
    "guaranteed_stop_return": "1.0",
    "indicative_quote_reference": "example",
    "knockout_premium_return": "1.0",
    "notional_value": "1.0",
    "notional_value_in_user_currency": "1.0"
  },
  "currency_code_iso": "example"
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The result is indicative and requires the original opening level.

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

## `ig.operations.indicative_costs.quote_edit()`

Calculate indicative costs for editing a position.

Official IG reference: [https://labs.ig.com/reference/indicative-costs-and-charges-edit.html](https://labs.ig.com/reference/indicative-costs-and-charges-edit.html)

### Signatures

- Sync: `(request: 'EditIndicativeCostRequest') -> 'EditIndicativeCostResponse'`
- Async: `(request: 'EditIndicativeCostRequest') -> 'EditIndicativeCostResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `EditIndicativeCostRequest` | required | - | Validated typed request body. |
| `request.ask` | `Decimal` | required | - | Current provider ask price used for an indicative calculation. |
| `request.bid` | `Decimal` | required | - | Current provider bid price used for an indicative calculation. |
| `request.deal_currency_code` | `str` | required | minimum length `3`; maximum length `3` | Three-letter currency code used for the cost calculation. |
| `request.deal_reference` | `str` | required | minimum length `1` | Client or provider reference used to correlate a deal. |
| `request.size` | `Decimal` | required | > `0` | Positive deal size. |
| `request.direction` | `Literal['BUY', 'SELL'] | None` | default: `None` | - | Deal direction; `BUY` or `SELL`. |
| `request.epic` | `str | None` | default: `None` | - | IG market epic. |
| `request.guaranteed_stop` | `bool | None` | default: `None` | - | Whether the stop is guaranteed by IG. |
| `request.instrument_id` | `str | None` | default: `None` | - | Provider instrument identifier used by indicative-cost operations. |
| `request.knockout_premium` | `Decimal | None` | default: `None` | - | Knockout premium used in an indicative-cost calculation. |
| `request.price_level` | `Decimal | None` | default: `None` | - | Current price level used in an indicative-cost calculation. |
| `request.stop_level` | `Decimal | None` | default: `None` | - | Absolute stop level; mutually exclusive with `stop_distance`. |
| `request.opening_level` | `Decimal` | required | - | Original opening price used for close or edit cost calculations. |
| `request.edit_type` | `str | None` | default: `None` | - | Provider edit-cost calculation type. |
| `request.limit_level` | `Decimal | None` | default: `None` | - | Absolute limit level; mutually exclusive with `limit_distance`. |

### Sync example

```python
from ig_trading_lib.operations.costs import EditIndicativeCostRequest

result = ig.operations.indicative_costs.quote_edit(request=EditIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-3", size="1", opening_level="1.0700"))
```

### Async example

```python
from ig_trading_lib.operations.costs import EditIndicativeCostRequest

result = await ig.operations.indicative_costs.quote_edit(request=EditIndicativeCostRequest(ask="1.0813", bid="1.0812", deal_currency_code="GBP", deal_reference="COST-3", size="1", opening_level="1.0700"))
```

### Response shape: `EditIndicativeCostResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `currency_code_iso` | `str | None` | default: `None` |
| `limit` | `ClosingIndicativeCost | None` | default: `None` |
| `limit.closing_commission` | `Decimal | None` | default: `None` |
| `limit.closing_fx_fee` | `Decimal | None` | default: `None` |
| `limit.closing_iftt` | `Decimal | None` | default: `None` |
| `limit.closing_spread` | `Decimal | None` | default: `None` |
| `limit.etp_exit_cost` | `Decimal | None` | default: `None` |
| `limit.guaranteed_stop_return` | `Decimal | None` | default: `None` |
| `limit.indicative_quote_reference` | `str | None` | default: `None` |
| `limit.knockout_premium_return` | `Decimal | None` | default: `None` |
| `limit.notional_value` | `Decimal | None` | default: `None` |
| `limit.notional_value_in_user_currency` | `Decimal | None` | default: `None` |
| `stop` | `ClosingIndicativeCost | None` | default: `None` |
| `stop.closing_commission` | `Decimal | None` | default: `None` |
| `stop.closing_fx_fee` | `Decimal | None` | default: `None` |
| `stop.closing_iftt` | `Decimal | None` | default: `None` |
| `stop.closing_spread` | `Decimal | None` | default: `None` |
| `stop.etp_exit_cost` | `Decimal | None` | default: `None` |
| `stop.guaranteed_stop_return` | `Decimal | None` | default: `None` |
| `stop.indicative_quote_reference` | `str | None` | default: `None` |
| `stop.knockout_premium_return` | `Decimal | None` | default: `None` |
| `stop.notional_value` | `Decimal | None` | default: `None` |
| `stop.notional_value_in_user_currency` | `Decimal | None` | default: `None` |

### Response example

```json
{
  "currency_code_iso": "example",
  "limit": {
    "closing_commission": "1.0",
    "closing_fx_fee": "1.0",
    "closing_iftt": "1.0",
    "closing_spread": "1.0",
    "etp_exit_cost": "1.0",
    "guaranteed_stop_return": "1.0",
    "indicative_quote_reference": "example",
    "knockout_premium_return": "1.0",
    "notional_value": "1.0",
    "notional_value_in_user_currency": "1.0"
  },
  "stop": {
    "closing_commission": "1.0",
    "closing_fx_fee": "1.0",
    "closing_iftt": "1.0",
    "closing_spread": "1.0",
    "etp_exit_cost": "1.0",
    "guaranteed_stop_return": "1.0",
    "indicative_quote_reference": "example",
    "knockout_premium_return": "1.0",
    "notional_value": "1.0",
    "notional_value_in_user_currency": "1.0"
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The result is indicative and depends on the supplied edit context.

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

## `ig.operations.indicative_costs.get_durable_medium()`

Download the durable-medium document for an indicative quote.

Official IG reference: [https://labs.ig.com/reference/indicative-costs-and-charges-durable-medium.html](https://labs.ig.com/reference/indicative-costs-and-charges-durable-medium.html)

### Signatures

- Sync: `(quote_reference: 'str') -> 'DurableMediumResponse'`
- Async: `(quote_reference: 'str') -> 'DurableMediumResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `quote_reference` | `str` | required | - | IG indicative-cost quote reference. |

### Sync example

```python
result = ig.operations.indicative_costs.get_durable_medium(quote_reference="COST-1")
```

### Async example

```python
result = await ig.operations.indicative_costs.get_durable_medium(quote_reference="COST-1")
```

### Response shape: `DurableMediumResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `content` | `bytes` | required |
| `content_type` | `str | None` | default: `None` |

### Response example

```json
{
  "content": "<binary data>",
  "content_type": "example"
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The response contains binary document bytes and may be unavailable after IG's retention window.

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

## `ig.operations.indicative_costs.history()`

List historical indicative-cost disclosures for a date range.

Official IG reference: [https://labs.ig.com/reference/indicative-costs-and-charges-history-dates.html](https://labs.ig.com/reference/indicative-costs-and-charges-history-dates.html)

### Signatures

- Sync: `(from_date: 'datetime | str', to_date: 'datetime | str', query: 'IndicativeCostHistoryQuery | None' = None) -> 'IndicativeCostHistoryResponse'`
- Async: `(from_date: 'datetime | str', to_date: 'datetime | str', query: 'IndicativeCostHistoryQuery | None' = None) -> 'IndicativeCostHistoryResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `from_date` | `datetime | str` | required | - | Inclusive beginning of the requested time range. |
| `to_date` | `datetime | str` | required | - | Inclusive end of the requested time range. |
| `query` | `IndicativeCostHistoryQuery | None` | None | - | Optional typed query controls; `None` uses provider defaults. |
| `query.page_size` | `int | None` | default: `None` | >= `0` | Maximum records requested per provider page. |
| `query.page_number` | `int | None` | default: `None` | >= `0` | Provider page number. |
| `query.type` | `str | None` | default: `None` | minimum length `1` | Provider history or transaction type filter. |

### Sync example

```python
from ig_trading_lib.operations.costs import IndicativeCostHistoryQuery

result = ig.operations.indicative_costs.history(from_date="2026-08-01T00:00:00", to_date="2026-08-08T00:00:00", query=IndicativeCostHistoryQuery(page_size=50))
```

### Async example

```python
from ig_trading_lib.operations.costs import IndicativeCostHistoryQuery

result = await ig.operations.indicative_costs.history(from_date="2026-08-01T00:00:00", to_date="2026-08-08T00:00:00", query=IndicativeCostHistoryQuery(page_size=50))
```

### Response shape: `IndicativeCostHistoryResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `costs_and_charges_history[]` | `tuple[IndicativeCostHistoryEntry, ...]` | default: `()` |
| `costs_and_charges_history[].created_timestamp` | `str | None` | default: `None` |
| `costs_and_charges_history[].direction` | `str | None` | default: `None` |
| `costs_and_charges_history[].indicative_quote_reference` | `str | None` | default: `None` |
| `costs_and_charges_history[].instrument_name` | `str | None` | default: `None` |
| `costs_and_charges_history[].type` | `str | None` | default: `None` |
| `pagination` | `IndicativeCostHistoryPagination | None` | default: `None` |
| `pagination.page_number` | `int | None` | default: `None` |
| `pagination.page_size` | `int | None` | default: `None` |
| `pagination.total_elements` | `int | None` | default: `None` |
| `pagination.total_pages` | `int | None` | default: `None` |

### Response example

```json
{
  "costs_and_charges_history": [
    {
      "created_timestamp": "example",
      "direction": "example",
      "indicative_quote_reference": "example",
      "instrument_name": "EUR/USD",
      "type": "example"
    }
  ],
  "pagination": {
    "page_number": 1,
    "page_size": 1,
    "total_elements": 1,
    "total_pages": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- History depth and page availability are controlled by IG.

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
