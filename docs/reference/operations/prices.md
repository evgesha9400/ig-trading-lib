<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Prices operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.prices.list()`

List historical prices using the v3 paging and allowance model.

Official IG reference: [https://labs.ig.com/reference/prices-epic.html](https://labs.ig.com/reference/prices-epic.html)

### Signatures

- Sync: `(epic: 'str', query: 'PricesQuery | None' = None) -> 'PricesResponse'`
- Async: `(epic: 'str', query: 'PricesQuery | None' = None) -> 'PricesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epic` | `str` | required | - | IG market epic. |
| `query` | `PricesQuery | None` | None | - | Optional typed query controls; `None` uses provider defaults. |
| `query.resolution` | `Literal['DAY', 'HOUR', 'HOUR_2', 'HOUR_3', 'HOUR_4', 'MINUTE', 'MINUTE_2', 'MINUTE_3', 'MINUTE_5', 'MINUTE_10', 'MINUTE_15', 'MINUTE_30', 'MONTH', 'SECOND', 'WEEK']` | default: `'MINUTE'` | - | IG historical-price resolution. |
| `query.from_date` | `datetime | str | None` | default: `None` | - | Inclusive beginning of the requested time range. |
| `query.to_date` | `datetime | str | None` | default: `None` | - | Inclusive end of the requested time range. |
| `query.max_points` | `int | None` | default: `None` | >= `1` | Maximum number of historical price points to return. |
| `query.page_size` | `int | None` | default: `None` | >= `0` | Maximum records requested per provider page. |
| `query.page_number` | `int | None` | default: `None` | >= `1` | Provider page number. |

### Sync example

```python
from ig_trading_lib.operations.markets import PricesQuery

result = ig.operations.prices.list(epic="CS.D.EURUSD.CFD.IP", query=PricesQuery(resolution="HOUR", max_points=100))
```

### Async example

```python
from ig_trading_lib.operations.markets import PricesQuery

result = await ig.operations.prices.list(epic="CS.D.EURUSD.CFD.IP", query=PricesQuery(resolution="HOUR", max_points=100))
```

### Response shape: `PricesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `prices[]` | `tuple[PricePoint, ...]` | default: `()` |
| `prices[].snapshot_time` | `datetime | str | None` | default: `None` |
| `prices[].snapshot_time_utc` | `str | None` | default: `None` |
| `prices[].open_price` | `PriceValue | None` | default: `None` |
| `prices[].open_price.bid` | `Decimal | None` | default: `None` |
| `prices[].open_price.ask` | `Decimal | None` | default: `None` |
| `prices[].open_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].close_price` | `PriceValue | None` | default: `None` |
| `prices[].close_price.bid` | `Decimal | None` | default: `None` |
| `prices[].close_price.ask` | `Decimal | None` | default: `None` |
| `prices[].close_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].high_price` | `PriceValue | None` | default: `None` |
| `prices[].high_price.bid` | `Decimal | None` | default: `None` |
| `prices[].high_price.ask` | `Decimal | None` | default: `None` |
| `prices[].high_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].low_price` | `PriceValue | None` | default: `None` |
| `prices[].low_price.bid` | `Decimal | None` | default: `None` |
| `prices[].low_price.ask` | `Decimal | None` | default: `None` |
| `prices[].low_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].last_traded_volume` | `float | None` | default: `None` |
| `instrument_type` | `str | None` | default: `None` |
| `metadata` | `PriceMetadata | None` | default: `None` |
| `metadata.page_data` | `PricePageData | None` | default: `None` |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.allowance` | `PriceAllowance | None` | default: `None` |
| `metadata.allowance.allowance_expiry` | `int` | required |
| `metadata.allowance.remaining_allowance` | `int` | required |
| `metadata.allowance.total_allowance` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |
| `allowance` | `PriceAllowance | None` | default: `None` |
| `allowance.allowance_expiry` | `int` | required |
| `allowance.remaining_allowance` | `int` | required |
| `allowance.total_allowance` | `int` | required |

### Response example

```json
{
  "prices": [
    {
      "snapshot_time": "2026-08-08T12:34:56Z",
      "snapshot_time_utc": "example",
      "open_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "close_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "high_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "low_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "last_traded_volume": 1.0
    }
  ],
  "instrument_type": "example",
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "allowance": {
      "allowance_expiry": 1,
      "remaining_allowance": 1,
      "total_allowance": 1
    },
    "size": 1
  },
  "allowance": {
    "allowance_expiry": 1,
    "remaining_allowance": 1,
    "total_allowance": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- IG historical-price allowances and maximum ranges vary by account and resolution.

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

## `ig.operations.prices.list_points()`

List a fixed number of historical price points using the v2 endpoint.

Official IG reference: [https://labs.ig.com/reference/prices-epic-resolution-numpoints.html](https://labs.ig.com/reference/prices-epic-resolution-numpoints.html)

### Signatures

- Sync: `(epic: 'str', resolution: 'str', num_points: 'int') -> 'PricesResponse'`
- Async: `(epic: 'str', resolution: 'str', num_points: 'int') -> 'PricesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epic` | `str` | required | - | IG market epic. |
| `resolution` | `str` | required | - | IG historical-price resolution. |
| `num_points` | `int` | required | - | Number of historical price points requested. |

### Sync example

```python
result = ig.operations.prices.list_points(epic="CS.D.EURUSD.CFD.IP", resolution="HOUR", num_points=100)
```

### Async example

```python
result = await ig.operations.prices.list_points(epic="CS.D.EURUSD.CFD.IP", resolution="HOUR", num_points=100)
```

### Response shape: `PricesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `prices[]` | `tuple[PricePoint, ...]` | default: `()` |
| `prices[].snapshot_time` | `datetime | str | None` | default: `None` |
| `prices[].snapshot_time_utc` | `str | None` | default: `None` |
| `prices[].open_price` | `PriceValue | None` | default: `None` |
| `prices[].open_price.bid` | `Decimal | None` | default: `None` |
| `prices[].open_price.ask` | `Decimal | None` | default: `None` |
| `prices[].open_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].close_price` | `PriceValue | None` | default: `None` |
| `prices[].close_price.bid` | `Decimal | None` | default: `None` |
| `prices[].close_price.ask` | `Decimal | None` | default: `None` |
| `prices[].close_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].high_price` | `PriceValue | None` | default: `None` |
| `prices[].high_price.bid` | `Decimal | None` | default: `None` |
| `prices[].high_price.ask` | `Decimal | None` | default: `None` |
| `prices[].high_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].low_price` | `PriceValue | None` | default: `None` |
| `prices[].low_price.bid` | `Decimal | None` | default: `None` |
| `prices[].low_price.ask` | `Decimal | None` | default: `None` |
| `prices[].low_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].last_traded_volume` | `float | None` | default: `None` |
| `instrument_type` | `str | None` | default: `None` |
| `metadata` | `PriceMetadata | None` | default: `None` |
| `metadata.page_data` | `PricePageData | None` | default: `None` |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.allowance` | `PriceAllowance | None` | default: `None` |
| `metadata.allowance.allowance_expiry` | `int` | required |
| `metadata.allowance.remaining_allowance` | `int` | required |
| `metadata.allowance.total_allowance` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |
| `allowance` | `PriceAllowance | None` | default: `None` |
| `allowance.allowance_expiry` | `int` | required |
| `allowance.remaining_allowance` | `int` | required |
| `allowance.total_allowance` | `int` | required |

### Response example

```json
{
  "prices": [
    {
      "snapshot_time": "2026-08-08T12:34:56Z",
      "snapshot_time_utc": "example",
      "open_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "close_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "high_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "low_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "last_traded_volume": 1.0
    }
  ],
  "instrument_type": "example",
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "allowance": {
      "allowance_expiry": 1,
      "remaining_allowance": 1,
      "total_allowance": 1
    },
    "size": 1
  },
  "allowance": {
    "allowance_expiry": 1,
    "remaining_allowance": 1,
    "total_allowance": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Resolution values and point limits are enforced by IG.

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

## `ig.operations.prices.list_date_range()`

List historical prices for an explicit date range using the v2 endpoint.

Official IG reference: [https://labs.ig.com/reference/prices-epic-dates-new.html](https://labs.ig.com/reference/prices-epic-dates-new.html)

### Signatures

- Sync: `(epic: 'str', resolution: 'str', start_date: 'datetime | str', end_date: 'datetime | str') -> 'PricesResponse'`
- Async: `(epic: 'str', resolution: 'str', start_date: 'datetime | str', end_date: 'datetime | str') -> 'PricesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epic` | `str` | required | - | IG market epic. |
| `resolution` | `str` | required | - | IG historical-price resolution. |
| `start_date` | `datetime | str` | required | - | Inclusive beginning of the requested time range. |
| `end_date` | `datetime | str` | required | - | Inclusive end of the requested time range. |

### Sync example

```python
result = ig.operations.prices.list_date_range(epic="CS.D.EURUSD.CFD.IP", resolution="HOUR", start_date="2026-08-01T00:00:00", end_date="2026-08-08T00:00:00")
```

### Async example

```python
result = await ig.operations.prices.list_date_range(epic="CS.D.EURUSD.CFD.IP", resolution="HOUR", start_date="2026-08-01T00:00:00", end_date="2026-08-08T00:00:00")
```

### Response shape: `PricesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `prices[]` | `tuple[PricePoint, ...]` | default: `()` |
| `prices[].snapshot_time` | `datetime | str | None` | default: `None` |
| `prices[].snapshot_time_utc` | `str | None` | default: `None` |
| `prices[].open_price` | `PriceValue | None` | default: `None` |
| `prices[].open_price.bid` | `Decimal | None` | default: `None` |
| `prices[].open_price.ask` | `Decimal | None` | default: `None` |
| `prices[].open_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].close_price` | `PriceValue | None` | default: `None` |
| `prices[].close_price.bid` | `Decimal | None` | default: `None` |
| `prices[].close_price.ask` | `Decimal | None` | default: `None` |
| `prices[].close_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].high_price` | `PriceValue | None` | default: `None` |
| `prices[].high_price.bid` | `Decimal | None` | default: `None` |
| `prices[].high_price.ask` | `Decimal | None` | default: `None` |
| `prices[].high_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].low_price` | `PriceValue | None` | default: `None` |
| `prices[].low_price.bid` | `Decimal | None` | default: `None` |
| `prices[].low_price.ask` | `Decimal | None` | default: `None` |
| `prices[].low_price.last_traded` | `Decimal | None` | default: `None` |
| `prices[].last_traded_volume` | `float | None` | default: `None` |
| `instrument_type` | `str | None` | default: `None` |
| `metadata` | `PriceMetadata | None` | default: `None` |
| `metadata.page_data` | `PricePageData | None` | default: `None` |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.allowance` | `PriceAllowance | None` | default: `None` |
| `metadata.allowance.allowance_expiry` | `int` | required |
| `metadata.allowance.remaining_allowance` | `int` | required |
| `metadata.allowance.total_allowance` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |
| `allowance` | `PriceAllowance | None` | default: `None` |
| `allowance.allowance_expiry` | `int` | required |
| `allowance.remaining_allowance` | `int` | required |
| `allowance.total_allowance` | `int` | required |

### Response example

```json
{
  "prices": [
    {
      "snapshot_time": "2026-08-08T12:34:56Z",
      "snapshot_time_utc": "example",
      "open_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "close_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "high_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "low_price": {
        "bid": "1.0",
        "ask": "1.0",
        "last_traded": "1.0"
      },
      "last_traded_volume": 1.0
    }
  ],
  "instrument_type": "example",
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "allowance": {
      "allowance_expiry": 1,
      "remaining_allowance": 1,
      "total_allowance": 1
    },
    "size": 1
  },
  "allowance": {
    "allowance_expiry": 1,
    "remaining_allowance": 1,
    "total_allowance": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Date format, range length, resolution, and allowance are enforced by IG.

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
