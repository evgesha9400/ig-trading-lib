<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Categories operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.categories.list()`

List top-level market-navigation categories.

Official IG reference: [https://labs.ig.com/reference/categories.html](https://labs.ig.com/reference/categories.html)

### Signatures

- Sync: `() -> 'CategoriesResponse'`
- Async: `() -> 'CategoriesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.categories.list()
```

### Async example

```python
result = await ig.operations.categories.list()
```

### Response shape: `CategoriesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `categories[]` | `tuple[Category, ...]` | default: `()` |
| `categories[].code` | `str` | required |
| `categories[].non_tradeable` | `bool` | required |

### Response example

```json
{
  "categories": [
    {
      "code": "example",
      "non_tradeable": true
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

## `ig.operations.categories.list_instruments()`

List instruments inside a market-navigation category.

Official IG reference: [https://labs.ig.com/reference/categories-category-id-instruments.html](https://labs.ig.com/reference/categories-category-id-instruments.html)

### Signatures

- Sync: `(category_id: 'str', query: 'CategoryInstrumentsQuery | None' = None) -> 'CategoryInstrumentsResponse'`
- Async: `(category_id: 'str', query: 'CategoryInstrumentsQuery | None' = None) -> 'CategoryInstrumentsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `category_id` | `str` | required | - | IG market-navigation category identifier. |
| `query` | `CategoryInstrumentsQuery | None` | None | - | Optional typed query controls; `None` uses provider defaults. |
| `query.page_number` | `int` | default: `0` | >= `0` | Provider page number. |
| `query.page_size` | `int` | default: `150` | >= `1`; <= `1000` | Maximum records requested per provider page. |
| `query.reference_epic` | `str | None` | default: `None` | - | Optional epic used as a category-navigation reference point. |
| `query.maturity_type` | `str | None` | default: `None` | - | Optional provider maturity filter for category instruments. |

### Sync example

```python
from ig_trading_lib.operations.markets import CategoryInstrumentsQuery

result = ig.operations.categories.list_instruments(category_id="CURRENCIES", query=CategoryInstrumentsQuery(page_size=100))
```

### Async example

```python
from ig_trading_lib.operations.markets import CategoryInstrumentsQuery

result = await ig.operations.categories.list_instruments(category_id="CURRENCIES", query=CategoryInstrumentsQuery(page_size=100))
```

### Response shape: `CategoryInstrumentsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `instruments[]` | `tuple[CategoryInstrument, ...]` | default: `()` |
| `instruments[].epic` | `str` | required |
| `instruments[].instrument_name` | `str | None` | default: `None` |
| `instruments[].expiry` | `str | None` | default: `None` |
| `instruments[].instrument_type` | `str | None` | default: `None` |
| `instruments[].lot_size` | `Decimal | None` | default: `None` |
| `instruments[].otc_tradeable` | `bool | None` | default: `None` |
| `instruments[].market_status` | `str | None` | default: `None` |
| `instruments[].delay_time` | `int | None` | default: `None` |
| `instruments[].bid` | `Decimal | None` | default: `None` |
| `instruments[].offer` | `Decimal | None` | default: `None` |
| `instruments[].high` | `Decimal | None` | default: `None` |
| `instruments[].low` | `Decimal | None` | default: `None` |
| `instruments[].net_change` | `Decimal | None` | default: `None` |
| `instruments[].percentage_change` | `Decimal | None` | default: `None` |
| `instruments[].update_time` | `str | None` | default: `None` |
| `instruments[].scaling_factor` | `Decimal | None` | default: `None` |
| `metadata` | `PagingMetadata` | required |
| `metadata.page_number` | `int` | required |
| `metadata.page_size` | `int` | required |

### Response example

```json
{
  "instruments": [
    {
      "epic": "CS.D.EURUSD.CFD.IP",
      "instrument_name": "EUR/USD",
      "expiry": "-",
      "instrument_type": "example",
      "lot_size": "1.0",
      "otc_tradeable": true,
      "market_status": "TRADEABLE",
      "delay_time": 1,
      "bid": "1.0",
      "offer": "1.0",
      "high": "1.0",
      "low": "1.0",
      "net_change": "1.0",
      "percentage_change": "1.0",
      "update_time": "12:34:56",
      "scaling_factor": "1.0"
    }
  ],
  "metadata": {
    "page_number": 1,
    "page_size": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- `page_size` is limited to 1-1000 and `page_number` starts at 0.

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
