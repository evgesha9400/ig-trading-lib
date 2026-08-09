<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Activity operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.activity.list()`

List account activity with the v3 query controls.

Official IG reference: [https://labs.ig.com/reference/history-activity.html](https://labs.ig.com/reference/history-activity.html)

### Signatures

- Sync: `(query: 'ActivityQuery | None' = None) -> 'ActivityResponse'`
- Async: `(query: 'ActivityQuery | None' = None) -> 'ActivityResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `query` | `ActivityQuery | None` | None | - | Optional typed query controls; `None` uses provider defaults. |
| `query.from_date` | `date | datetime | str | None` | default: `None` | - | Inclusive beginning of the requested time range. |
| `query.to_date` | `date | datetime | str | None` | default: `None` | - | Inclusive end of the requested time range. |
| `query.detailed` | `bool | None` | default: `None` | - | Whether IG should include detailed activity records. |
| `query.deal_id` | `str | None` | default: `None` | - | IG identifier of an existing position or working order. |
| `query.filter` | `str | None` | default: `None` | - | Provider filter controlling the records or market detail returned. |
| `query.page_size` | `int | None` | default: `None` | >= `10`; <= `500` | Maximum records requested per provider page. |

### Sync example

```python
from ig_trading_lib.operations.accounts import ActivityQuery

result = ig.operations.activity.list(query=ActivityQuery(page_size=50))
```

### Async example

```python
from ig_trading_lib.operations.accounts import ActivityQuery

result = await ig.operations.activity.list(query=ActivityQuery(page_size=50))
```

### Response shape: `ActivityResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `activities[]` | `tuple[Activity, ...]` | default: `()` |
| `activities[].action_status` | `str | None` | default: `None` |
| `activities[].activity` | `str | None` | default: `None` |
| `activities[].activity_history_id` | `str | None` | default: `None` |
| `activities[].channel` | `str | None` | default: `None` |
| `activities[].currency` | `str | None` | default: `None` |
| `activities[].date` | `str | None` | default: `None` |
| `activities[].deal_id` | `str | None` | default: `None` |
| `activities[].description` | `str | None` | default: `None` |
| `activities[].details` | `ActivityDetails | None` | default: `None` |
| `activities[].details.actions[]` | `tuple[ActivityAction, ...]` | default: `()` |
| `activities[].details.actions[].action_type` | `str | None` | default: `None` |
| `activities[].details.actions[].affected_deal_id` | `str | None` | default: `None` |
| `activities[].details.actions[].currency` | `str | None` | default: `None` |
| `activities[].details.actions[].deal_reference` | `str | None` | default: `None` |
| `activities[].details.actions[].direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `activities[].details.actions[].good_till_date` | `str | None` | default: `None` |
| `activities[].details.actions[].guaranteed_stop` | `bool | None` | default: `None` |
| `activities[].details.actions[].level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].market_name` | `str | None` | default: `None` |
| `activities[].details.actions[].size` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_step` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.epic` | `str | None` | default: `None` |
| `activities[].details.period` | `str | None` | default: `None` |
| `activities[].details.status` | `str | None` | default: `None` |
| `activities[].details.type` | `str | None` | default: `None` |
| `activities[].epic` | `str | None` | default: `None` |
| `activities[].level` | `Decimal | str | None` | default: `None` |
| `activities[].limit` | `Decimal | str | None` | default: `None` |
| `activities[].market_name` | `str | None` | default: `None` |
| `activities[].period` | `str | None` | default: `None` |
| `activities[].result` | `str | None` | default: `None` |
| `activities[].size` | `Decimal | str | None` | default: `None` |
| `activities[].stop` | `Decimal | str | None` | default: `None` |
| `activities[].stop_type` | `str | None` | default: `None` |
| `activities[].time` | `str | None` | default: `None` |
| `metadata` | `CursorMetadata | None` | default: `None` |
| `metadata.paging` | `CursorPaging` | required |
| `metadata.paging.next` | `str | None` | default: `None` |
| `metadata.paging.size` | `int | None` | default: `None` |

### Response example

```json
{
  "activities": [
    {
      "action_status": "example",
      "activity": "example",
      "activity_history_id": "example",
      "channel": "example",
      "currency": "GBP",
      "date": "example",
      "deal_id": "DIAAAABBBCCC",
      "description": "example",
      "details": {
        "actions": [
          {
            "action_type": "example",
            "affected_deal_id": "example",
            "currency": "GBP",
            "deal_reference": "ABC123",
            "direction": "BUY",
            "good_till_date": "example",
            "guaranteed_stop": true,
            "level": "1.0",
            "limit_distance": "1.0",
            "limit_level": "1.0",
            "market_name": "example",
            "size": "1.0",
            "stop_distance": "1.0",
            "stop_level": "1.0",
            "trailing_step": "1.0",
            "trailing_stop_distance": "1.0"
          }
        ],
        "epic": "CS.D.EURUSD.CFD.IP",
        "period": "example",
        "status": "ENABLED",
        "type": "example"
      },
      "epic": "CS.D.EURUSD.CFD.IP",
      "level": "1.0",
      "limit": "1.0",
      "market_name": "example",
      "period": "example",
      "result": "example",
      "size": "1.0",
      "stop": "1.0",
      "stop_type": "example",
      "time": "example"
    }
  ],
  "metadata": {
    "paging": {
      "next": "example",
      "size": 1
    }
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- IG restricts activity history to provider-defined date and page windows.

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

## `ig.operations.activity.list_by_date_range()`

List account activity between two dates using the v2 endpoint.

Official IG reference: [https://labs.ig.com/reference/history-activity-dates.html](https://labs.ig.com/reference/history-activity-dates.html)

### Signatures

- Sync: `(from_date: 'date | datetime | str', to_date: 'date | datetime | str') -> 'ActivityResponse'`
- Async: `(from_date: 'date | datetime | str', to_date: 'date | datetime | str') -> 'ActivityResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `from_date` | `date | datetime | str` | required | - | Inclusive beginning of the requested time range. |
| `to_date` | `date | datetime | str` | required | - | Inclusive end of the requested time range. |

### Sync example

```python
result = ig.operations.activity.list_by_date_range(from_date="2026-08-01", to_date="2026-08-08")
```

### Async example

```python
result = await ig.operations.activity.list_by_date_range(from_date="2026-08-01", to_date="2026-08-08")
```

### Response shape: `ActivityResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `activities[]` | `tuple[Activity, ...]` | default: `()` |
| `activities[].action_status` | `str | None` | default: `None` |
| `activities[].activity` | `str | None` | default: `None` |
| `activities[].activity_history_id` | `str | None` | default: `None` |
| `activities[].channel` | `str | None` | default: `None` |
| `activities[].currency` | `str | None` | default: `None` |
| `activities[].date` | `str | None` | default: `None` |
| `activities[].deal_id` | `str | None` | default: `None` |
| `activities[].description` | `str | None` | default: `None` |
| `activities[].details` | `ActivityDetails | None` | default: `None` |
| `activities[].details.actions[]` | `tuple[ActivityAction, ...]` | default: `()` |
| `activities[].details.actions[].action_type` | `str | None` | default: `None` |
| `activities[].details.actions[].affected_deal_id` | `str | None` | default: `None` |
| `activities[].details.actions[].currency` | `str | None` | default: `None` |
| `activities[].details.actions[].deal_reference` | `str | None` | default: `None` |
| `activities[].details.actions[].direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `activities[].details.actions[].good_till_date` | `str | None` | default: `None` |
| `activities[].details.actions[].guaranteed_stop` | `bool | None` | default: `None` |
| `activities[].details.actions[].level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].market_name` | `str | None` | default: `None` |
| `activities[].details.actions[].size` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_step` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.epic` | `str | None` | default: `None` |
| `activities[].details.period` | `str | None` | default: `None` |
| `activities[].details.status` | `str | None` | default: `None` |
| `activities[].details.type` | `str | None` | default: `None` |
| `activities[].epic` | `str | None` | default: `None` |
| `activities[].level` | `Decimal | str | None` | default: `None` |
| `activities[].limit` | `Decimal | str | None` | default: `None` |
| `activities[].market_name` | `str | None` | default: `None` |
| `activities[].period` | `str | None` | default: `None` |
| `activities[].result` | `str | None` | default: `None` |
| `activities[].size` | `Decimal | str | None` | default: `None` |
| `activities[].stop` | `Decimal | str | None` | default: `None` |
| `activities[].stop_type` | `str | None` | default: `None` |
| `activities[].time` | `str | None` | default: `None` |
| `metadata` | `CursorMetadata | None` | default: `None` |
| `metadata.paging` | `CursorPaging` | required |
| `metadata.paging.next` | `str | None` | default: `None` |
| `metadata.paging.size` | `int | None` | default: `None` |

### Response example

```json
{
  "activities": [
    {
      "action_status": "example",
      "activity": "example",
      "activity_history_id": "example",
      "channel": "example",
      "currency": "GBP",
      "date": "example",
      "deal_id": "DIAAAABBBCCC",
      "description": "example",
      "details": {
        "actions": [
          {
            "action_type": "example",
            "affected_deal_id": "example",
            "currency": "GBP",
            "deal_reference": "ABC123",
            "direction": "BUY",
            "good_till_date": "example",
            "guaranteed_stop": true,
            "level": "1.0",
            "limit_distance": "1.0",
            "limit_level": "1.0",
            "market_name": "example",
            "size": "1.0",
            "stop_distance": "1.0",
            "stop_level": "1.0",
            "trailing_step": "1.0",
            "trailing_stop_distance": "1.0"
          }
        ],
        "epic": "CS.D.EURUSD.CFD.IP",
        "period": "example",
        "status": "ENABLED",
        "type": "example"
      },
      "epic": "CS.D.EURUSD.CFD.IP",
      "level": "1.0",
      "limit": "1.0",
      "market_name": "example",
      "period": "example",
      "result": "example",
      "size": "1.0",
      "stop": "1.0",
      "stop_type": "example",
      "time": "example"
    }
  ],
  "metadata": {
    "paging": {
      "next": "example",
      "size": 1
    }
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Date strings must use a format accepted by IG.

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

## `ig.operations.activity.list_by_period()`

List recent account activity for a provider period.

Official IG reference: [https://labs.ig.com/reference/history-activity-period.html](https://labs.ig.com/reference/history-activity-period.html)

### Signatures

- Sync: `(period: 'str') -> 'ActivityResponse'`
- Async: `(period: 'str') -> 'ActivityResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `period` | `str` | required | - | ISO-8601-style provider period such as `P7D`. |

### Sync example

```python
result = ig.operations.activity.list_by_period(period="P7D")
```

### Async example

```python
result = await ig.operations.activity.list_by_period(period="P7D")
```

### Response shape: `ActivityResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `activities[]` | `tuple[Activity, ...]` | default: `()` |
| `activities[].action_status` | `str | None` | default: `None` |
| `activities[].activity` | `str | None` | default: `None` |
| `activities[].activity_history_id` | `str | None` | default: `None` |
| `activities[].channel` | `str | None` | default: `None` |
| `activities[].currency` | `str | None` | default: `None` |
| `activities[].date` | `str | None` | default: `None` |
| `activities[].deal_id` | `str | None` | default: `None` |
| `activities[].description` | `str | None` | default: `None` |
| `activities[].details` | `ActivityDetails | None` | default: `None` |
| `activities[].details.actions[]` | `tuple[ActivityAction, ...]` | default: `()` |
| `activities[].details.actions[].action_type` | `str | None` | default: `None` |
| `activities[].details.actions[].affected_deal_id` | `str | None` | default: `None` |
| `activities[].details.actions[].currency` | `str | None` | default: `None` |
| `activities[].details.actions[].deal_reference` | `str | None` | default: `None` |
| `activities[].details.actions[].direction` | `Literal['BUY', 'SELL'] | None` | default: `None` |
| `activities[].details.actions[].good_till_date` | `str | None` | default: `None` |
| `activities[].details.actions[].guaranteed_stop` | `bool | None` | default: `None` |
| `activities[].details.actions[].level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].limit_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].market_name` | `str | None` | default: `None` |
| `activities[].details.actions[].size` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].stop_level` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_step` | `Decimal | None` | default: `None` |
| `activities[].details.actions[].trailing_stop_distance` | `Decimal | None` | default: `None` |
| `activities[].details.epic` | `str | None` | default: `None` |
| `activities[].details.period` | `str | None` | default: `None` |
| `activities[].details.status` | `str | None` | default: `None` |
| `activities[].details.type` | `str | None` | default: `None` |
| `activities[].epic` | `str | None` | default: `None` |
| `activities[].level` | `Decimal | str | None` | default: `None` |
| `activities[].limit` | `Decimal | str | None` | default: `None` |
| `activities[].market_name` | `str | None` | default: `None` |
| `activities[].period` | `str | None` | default: `None` |
| `activities[].result` | `str | None` | default: `None` |
| `activities[].size` | `Decimal | str | None` | default: `None` |
| `activities[].stop` | `Decimal | str | None` | default: `None` |
| `activities[].stop_type` | `str | None` | default: `None` |
| `activities[].time` | `str | None` | default: `None` |
| `metadata` | `CursorMetadata | None` | default: `None` |
| `metadata.paging` | `CursorPaging` | required |
| `metadata.paging.next` | `str | None` | default: `None` |
| `metadata.paging.size` | `int | None` | default: `None` |

### Response example

```json
{
  "activities": [
    {
      "action_status": "example",
      "activity": "example",
      "activity_history_id": "example",
      "channel": "example",
      "currency": "GBP",
      "date": "example",
      "deal_id": "DIAAAABBBCCC",
      "description": "example",
      "details": {
        "actions": [
          {
            "action_type": "example",
            "affected_deal_id": "example",
            "currency": "GBP",
            "deal_reference": "ABC123",
            "direction": "BUY",
            "good_till_date": "example",
            "guaranteed_stop": true,
            "level": "1.0",
            "limit_distance": "1.0",
            "limit_level": "1.0",
            "market_name": "example",
            "size": "1.0",
            "stop_distance": "1.0",
            "stop_level": "1.0",
            "trailing_step": "1.0",
            "trailing_stop_distance": "1.0"
          }
        ],
        "epic": "CS.D.EURUSD.CFD.IP",
        "period": "example",
        "status": "ENABLED",
        "type": "example"
      },
      "epic": "CS.D.EURUSD.CFD.IP",
      "level": "1.0",
      "limit": "1.0",
      "market_name": "example",
      "period": "example",
      "result": "example",
      "size": "1.0",
      "stop": "1.0",
      "stop_type": "example",
      "time": "example"
    }
  ],
  "metadata": {
    "paging": {
      "next": "example",
      "size": 1
    }
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Supported period syntax and maximum history are controlled by IG.

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
