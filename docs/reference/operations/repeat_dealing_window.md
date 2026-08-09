<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Repeat Dealing Window operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.repeat_dealing_window.get()`

Read repeat-dealing window availability, optionally for one epic.

Official IG reference: [https://labs.ig.com/reference/repeat-deal-window.html](https://labs.ig.com/reference/repeat-deal-window.html)

### Signatures

- Sync: `(*, epic: 'str | None' = None) -> 'RepeatDealingWindowResponse'`
- Async: `(*, epic: 'str | None' = None) -> 'RepeatDealingWindowResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `epic` | `str | None` | None | - | IG market epic. |

### Sync example

```python
result = ig.operations.repeat_dealing_window.get(epic="CS.D.EURUSD.CFD.IP")
```

### Async example

```python
result = await ig.operations.repeat_dealing_window.get(epic="CS.D.EURUSD.CFD.IP")
```

### Response shape: `RepeatDealingWindowResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `account_id` | `str` | required |
| `request_start_time` | `int` | required |
| `repeat_dealing_entry_list[]` | `tuple[RepeatDealingEntry, ...]` | default: `()` |
| `repeat_dealing_entry_list[].instrument_source` | `str` | required |
| `repeat_dealing_entry_list[].instrument_value` | `str` | required |
| `repeat_dealing_entry_list[].currency_list[]` | `tuple[RepeatDealingCurrency, ...]` | default: `()` |
| `repeat_dealing_entry_list[].currency_list[].currency` | `str` | required |
| `repeat_dealing_entry_list[].currency_list[].buy[]` | `tuple[RepeatDealingExecution, ...]` | default: `()` |
| `repeat_dealing_entry_list[].currency_list[].buy[].size` | `Decimal` | required |
| `repeat_dealing_entry_list[].currency_list[].buy[].expiry` | `int` | required |
| `repeat_dealing_entry_list[].currency_list[].sell[]` | `tuple[RepeatDealingExecution, ...]` | default: `()` |
| `repeat_dealing_entry_list[].currency_list[].sell[].size` | `Decimal` | required |
| `repeat_dealing_entry_list[].currency_list[].sell[].expiry` | `int` | required |

### Response example

```json
{
  "account_id": "ABC123",
  "request_start_time": 1,
  "repeat_dealing_entry_list": [
    {
      "instrument_source": "example",
      "instrument_value": "example",
      "currency_list": [
        {
          "currency": "GBP",
          "buy": [
            {
              "size": "1.0",
              "expiry": 1
            }
          ],
          "sell": [
            {
              "size": "1.0",
              "expiry": 1
            }
          ]
        }
      ]
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Repeat-dealing eligibility and expiry are determined by IG in real time.

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
