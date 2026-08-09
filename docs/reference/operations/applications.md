<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Applications operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.applications.list()`

List API applications associated with the authenticated client.

Official IG reference: [https://labs.ig.com/reference/operations-application.html](https://labs.ig.com/reference/operations-application.html)

### Signatures

- Sync: `() -> 'ApplicationsResponse'`
- Async: `() -> 'ApplicationsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.applications.list()
```

### Async example

```python
result = await ig.operations.applications.list()
```

### Response shape: `ApplicationsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `applications[]` | `tuple[Application, ...]` | default: `()` |
| `applications[].allow_equities` | `bool | None` | default: `None` |
| `applications[].allow_quote_orders` | `bool | None` | default: `None` |
| `applications[].allowance_account_historical_data` | `int | None` | default: `None` |
| `applications[].allowance_account_overall` | `int | None` | default: `None` |
| `applications[].allowance_account_trading` | `int | None` | default: `None` |
| `applications[].allowance_application_overall` | `int | None` | default: `None` |
| `applications[].api_key` | `str | None` | default: `None` |
| `applications[].concurrent_subscriptions_limit` | `int | None` | default: `None` |
| `applications[].created_date` | `str | None` | default: `None` |
| `applications[].name` | `str | None` | default: `None` |
| `applications[].status` | `str | None` | default: `None` |

### Response example

```json
{
  "applications": [
    {
      "allow_equities": true,
      "allow_quote_orders": true,
      "allowance_account_historical_data": 1,
      "allowance_account_overall": 1,
      "allowance_account_trading": 1,
      "allowance_application_overall": 1,
      "api_key": "example",
      "concurrent_subscriptions_limit": 1,
      "created_date": "example",
      "name": "Example",
      "status": "ENABLED"
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Application administration may require elevated account permissions.

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

## `ig.operations.applications.update()`

Update one API application's status and allowances.

Official IG reference: [https://labs.ig.com/reference/operations-application.html](https://labs.ig.com/reference/operations-application.html)

### Signatures

- Sync: `(request: 'UpdateApplicationRequest') -> 'Application'`
- Async: `(request: 'UpdateApplicationRequest') -> 'Application'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `UpdateApplicationRequest` | required | - | Validated typed request body. |
| `request.api_key` | `str` | required | minimum length `1` | Application API key whose settings are updated. |
| `request.status` | `Literal['DISABLED', 'ENABLED', 'REVOKED']` | required | - | Application status to assign. |
| `request.allowance_account_overall` | `int` | required | >= `0` | Overall request allowance assigned to the application. |
| `request.allowance_account_trading` | `int` | required | >= `0` | Trading request allowance assigned to the application. |

### Sync example

```python
from ig_trading_lib.operations.applications import UpdateApplicationRequest

result = ig.operations.applications.update(request=UpdateApplicationRequest(api_key="example-key", status="ENABLED", allowance_account_overall=60, allowance_account_trading=30))
```

### Async example

```python
from ig_trading_lib.operations.applications import UpdateApplicationRequest

result = await ig.operations.applications.update(request=UpdateApplicationRequest(api_key="example-key", status="ENABLED", allowance_account_overall=60, allowance_account_trading=30))
```

### Response shape: `Application`

| Field | Type | Required/default |
| --- | --- | --- |
| `allow_equities` | `bool | None` | default: `None` |
| `allow_quote_orders` | `bool | None` | default: `None` |
| `allowance_account_historical_data` | `int | None` | default: `None` |
| `allowance_account_overall` | `int | None` | default: `None` |
| `allowance_account_trading` | `int | None` | default: `None` |
| `allowance_application_overall` | `int | None` | default: `None` |
| `api_key` | `str | None` | default: `None` |
| `concurrent_subscriptions_limit` | `int | None` | default: `None` |
| `created_date` | `str | None` | default: `None` |
| `name` | `str | None` | default: `None` |
| `status` | `str | None` | default: `None` |

### Response example

```json
{
  "allow_equities": true,
  "allow_quote_orders": true,
  "allowance_account_historical_data": 1,
  "allowance_account_overall": 1,
  "allowance_account_trading": 1,
  "allowance_application_overall": 1,
  "api_key": "example",
  "concurrent_subscriptions_limit": 1,
  "created_date": "example",
  "name": "Example",
  "status": "ENABLED"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- IG can cap requested allowances below the supplied values.

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

## `ig.operations.applications.disable()`

Disable the API key used by the current session.

Official IG reference: [https://labs.ig.com/reference/operations-application-disable.html](https://labs.ig.com/reference/operations-application-disable.html)

### Signatures

- Sync: `() -> 'Application'`
- Async: `() -> 'Application'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.applications.disable()
```

### Async example

```python
result = await ig.operations.applications.disable()
```

### Response shape: `Application`

| Field | Type | Required/default |
| --- | --- | --- |
| `allow_equities` | `bool | None` | default: `None` |
| `allow_quote_orders` | `bool | None` | default: `None` |
| `allowance_account_historical_data` | `int | None` | default: `None` |
| `allowance_account_overall` | `int | None` | default: `None` |
| `allowance_account_trading` | `int | None` | default: `None` |
| `allowance_application_overall` | `int | None` | default: `None` |
| `api_key` | `str | None` | default: `None` |
| `concurrent_subscriptions_limit` | `int | None` | default: `None` |
| `created_date` | `str | None` | default: `None` |
| `name` | `str | None` | default: `None` |
| `status` | `str | None` | default: `None` |

### Response example

```json
{
  "allow_equities": true,
  "allow_quote_orders": true,
  "allowance_account_historical_data": 1,
  "allowance_account_overall": 1,
  "allowance_account_trading": 1,
  "allowance_application_overall": 1,
  "api_key": "example",
  "concurrent_subscriptions_limit": 1,
  "created_date": "example",
  "name": "Example",
  "status": "ENABLED"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Disabling the current key can prevent subsequent calls from the client.

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
