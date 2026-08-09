<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Session operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.session.get()`

Read the active session and optionally request CST/XST tokens.

Official IG reference: [https://labs.ig.com/reference/session.html](https://labs.ig.com/reference/session.html)

### Signatures

- Sync: `(*, fetch_session_tokens: 'bool' = False) -> 'SessionResponse'`
- Async: `(*, fetch_session_tokens: 'bool' = False) -> 'SessionResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `fetch_session_tokens` | `bool` | False | - | Whether CST and XST session tokens are requested from IG. |

### Sync example

```python
result = ig.operations.session.get(fetch_session_tokens=True)
```

### Async example

```python
result = await ig.operations.session.get(fetch_session_tokens=True)
```

### Response shape: `SessionResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `account_id` | `str | None` | default: `None` |
| `client_id` | `str | None` | default: `None` |
| `currency` | `str | None` | default: `None` |
| `lightstreamer_endpoint` | `str | None` | default: `None` |
| `locale` | `str | None` | default: `None` |
| `timezone_offset` | `int | None` | default: `None` |
| `cst` | `str | None` | default: `None` |
| `security_token` | `str | None` | default: `None` |

### Response example

```json
{
  "account_id": "ABC123",
  "client_id": "example",
  "currency": "GBP",
  "lightstreamer_endpoint": "example",
  "locale": "example",
  "timezone_offset": 1,
  "cst": "example",
  "security_token": "example"
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Session tokens are sensitive, excluded from model repr, and must never be logged.

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

## `ig.operations.session.switch_account()`

Switch the current session to another accessible account.

Official IG reference: [https://labs.ig.com/reference/session.html](https://labs.ig.com/reference/session.html)

### Signatures

- Sync: `(request: 'SwitchAccountRequest') -> 'SwitchAccountResponse'`
- Async: `(request: 'SwitchAccountRequest') -> 'SwitchAccountResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `SwitchAccountRequest` | required | - | Validated typed request body. |
| `request.account_id` | `str` | required | minimum length `1` | IG account identifier to switch to. |
| `request.default_account` | `bool` | default: `False` | - | Whether the switched account becomes the login default. |

### Sync example

```python
from ig_trading_lib.operations.session import SwitchAccountRequest

result = ig.operations.session.switch_account(request=SwitchAccountRequest(account_id="ABC123"))
```

### Async example

```python
from ig_trading_lib.operations.session import SwitchAccountRequest

result = await ig.operations.session.switch_account(request=SwitchAccountRequest(account_id="ABC123"))
```

### Response shape: `SwitchAccountResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `dealing_enabled` | `bool | None` | default: `None` |
| `has_active_demo_accounts` | `bool | None` | default: `None` |
| `has_active_live_accounts` | `bool | None` | default: `None` |
| `trailing_stops_enabled` | `bool | None` | default: `None` |

### Response example

```json
{
  "dealing_enabled": true,
  "has_active_demo_accounts": true,
  "has_active_live_accounts": true,
  "trailing_stops_enabled": true
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- The target account must be available to the authenticated client.

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

## `ig.operations.session.delete()`

Log out the current IG session and invalidate local tokens.

Official IG reference: [https://labs.ig.com/reference/session.html](https://labs.ig.com/reference/session.html)

### Signatures

- Sync: `() -> 'DeleteSessionResponse'`
- Async: `() -> 'DeleteSessionResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.session.delete()
```

### Async example

```python
result = await ig.operations.session.delete()
```

### Response shape: `DeleteSessionResponse`

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
- A successful call makes subsequent operations authenticate again.

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

## `ig.operations.session.get_encryption_key()`

Retrieve IG's password-encryption key and timestamp.

Official IG reference: [https://labs.ig.com/reference/session-encryption-key.html](https://labs.ig.com/reference/session-encryption-key.html)

### Signatures

- Sync: `() -> 'EncryptionKeyResponse'`
- Async: `() -> 'EncryptionKeyResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.session.get_encryption_key()
```

### Async example

```python
result = await ig.operations.session.get_encryption_key()
```

### Response shape: `EncryptionKeyResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `encryption_key` | `str` | required |
| `time_stamp` | `int` | required |

### Response example

```json
{
  "encryption_key": "example",
  "time_stamp": 1
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- The key is time-sensitive and intended only for IG's encrypted-login flow.

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
