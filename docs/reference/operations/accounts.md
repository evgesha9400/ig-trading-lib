<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Accounts operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.accounts.list()`

List every account available to the authenticated client.

Official IG reference: [https://labs.ig.com/reference/accounts.html](https://labs.ig.com/reference/accounts.html)

### Signatures

- Sync: `() -> 'AccountsResponse'`
- Async: `() -> 'AccountsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.accounts.list()
```

### Async example

```python
result = await ig.operations.accounts.list()
```

### Response shape: `AccountsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `accounts[]` | `tuple[Account, ...]` | required |
| `accounts[].account_alias` | `str | None` | default: `None` |
| `accounts[].account_id` | `str` | required |
| `accounts[].account_name` | `str | None` | default: `None` |
| `accounts[].account_type` | `str | None` | default: `None` |
| `accounts[].balance` | `AccountBalance | None` | default: `None` |
| `accounts[].balance.available` | `Decimal | None` | default: `None` |
| `accounts[].balance.balance` | `Decimal | None` | default: `None` |
| `accounts[].balance.deposit` | `Decimal | None` | default: `None` |
| `accounts[].balance.profit_loss` | `Decimal | None` | default: `None` |
| `accounts[].can_transfer_from` | `bool | None` | default: `None` |
| `accounts[].can_transfer_to` | `bool | None` | default: `None` |
| `accounts[].currency` | `str | None` | default: `None` |
| `accounts[].preferred` | `bool | None` | default: `None` |
| `accounts[].status` | `str | None` | default: `None` |

### Response example

```json
{
  "accounts": [
    {
      "account_alias": "example",
      "account_id": "ABC123",
      "account_name": "example",
      "account_type": "example",
      "balance": {
        "available": "1.0",
        "balance": "1.0",
        "deposit": "1.0",
        "profit_loss": "1.0"
      },
      "can_transfer_from": true,
      "can_transfer_to": true,
      "currency": "GBP",
      "preferred": true,
      "status": "ENABLED"
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

## `ig.operations.accounts.get_preferences()`

Read trading preferences for the active account.

Official IG reference: [https://labs.ig.com/reference/accounts-preferences.html](https://labs.ig.com/reference/accounts-preferences.html)

### Signatures

- Sync: `() -> 'AccountPreferencesResponse'`
- Async: `() -> 'AccountPreferencesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| None | - | - | - | This method accepts no parameters. |

### Sync example

```python
result = ig.operations.accounts.get_preferences()
```

### Async example

```python
result = await ig.operations.accounts.get_preferences()
```

### Response shape: `AccountPreferencesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `trailing_stops_enabled` | `bool | None` | default: `None` |
| `hedging_mode` | `str | None` | default: `None` |

### Response example

```json
{
  "trailing_stops_enabled": true,
  "hedging_mode": "example"
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

## `ig.operations.accounts.update_preferences()`

Update trading preferences for the active account.

Official IG reference: [https://labs.ig.com/reference/accounts-preferences.html](https://labs.ig.com/reference/accounts-preferences.html)

### Signatures

- Sync: `(request: 'UpdateAccountPreferencesRequest') -> 'UpdateAccountPreferencesResponse'`
- Async: `(request: 'UpdateAccountPreferencesRequest') -> 'UpdateAccountPreferencesResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `request` | `UpdateAccountPreferencesRequest` | required | - | Validated typed request body. |
| `request.trailing_stops_enabled` | `bool | None` | default: `None` | - | Whether trailing stops are enabled for the account. |
| `request.hedging_mode` | `str | None` | default: `None` | - | Provider account hedging preference. |

### Sync example

```python
from ig_trading_lib.operations.accounts import UpdateAccountPreferencesRequest

result = ig.operations.accounts.update_preferences(request=UpdateAccountPreferencesRequest(trailing_stops_enabled=True))
```

### Async example

```python
from ig_trading_lib.operations.accounts import UpdateAccountPreferencesRequest

result = await ig.operations.accounts.update_preferences(request=UpdateAccountPreferencesRequest(trailing_stops_enabled=True))
```

### Response shape: `UpdateAccountPreferencesResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `trailing_stops_enabled` | `bool | None` | default: `None` |
| `hedging_mode` | `str | None` | default: `None` |

### Response example

```json
{
  "trailing_stops_enabled": true,
  "hedging_mode": "example"
}
```

### Limitations

- Live calls require an explicit `TradingPermit`; demo calls do not.
- Mutations are sent once and are never automatically retried after an uncertain outcome.
- Only fields supported by the account type can be changed.

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
