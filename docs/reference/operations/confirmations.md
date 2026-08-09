<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Confirmations operations

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.confirmations.get()`

Retrieve the final confirmation for a deal reference.

Official IG reference: [https://labs.ig.com/reference/confirms-deal-reference.html](https://labs.ig.com/reference/confirms-deal-reference.html)

### Signatures

- Sync: `(deal_reference: 'str') -> 'DealConfirmationResponse'`
- Async: `(deal_reference: 'str') -> 'DealConfirmationResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `deal_reference` | `str` | required | - | Client or provider reference used to correlate a deal. |

### Sync example

```python
result = ig.operations.confirmations.get(deal_reference="ABC123")
```

### Async example

```python
result = await ig.operations.confirmations.get(deal_reference="ABC123")
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

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Confirmations are retained only for the provider-defined availability window.

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
