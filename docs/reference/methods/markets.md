# Markets operations

## `ig.operations.markets.search()`

Search for markets by name or identifier.

Official IG reference: [https://labs.ig.com/reference/markets-searchterm.html](https://labs.ig.com/reference/markets-searchterm.html)

### Signatures

- Sync: `(search_term: 'str') -> 'MarketSearchResponse'`
- Async: use the same parameters and `await` the result.

### Parameters

| Name | Type | Required/default | Description |
| --- | --- | --- | --- |
| `search_term` | `str` | required | Text matched against IG market names and identifiers. |

### Sync example

```python
result = ig.operations.markets.search(search_term="EUR/USD")
```

### Async example

```python
result = await ig.operations.markets.search(search_term="EUR/USD")
```

### Response shape: `MarketSearchResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `markets[]` | `tuple[MarketSummary, Ellipsis]` | required |
| `markets[].bid` | `Decimal | NoneType` | default: `None` |
| `markets[].delay_time` | `int | NoneType` | default: `None` |
| `markets[].epic` | `str` | required |
| `markets[].expiry` | `str | NoneType` | default: `None` |
| `markets[].high` | `Decimal | NoneType` | default: `None` |
| `markets[].instrument_name` | `str | NoneType` | default: `None` |
| `markets[].instrument_type` | `str | NoneType` | default: `None` |
| `markets[].low` | `Decimal | NoneType` | default: `None` |
| `markets[].market_status` | `str | NoneType` | default: `None` |
| `markets[].net_change` | `Decimal | NoneType` | default: `None` |
| `markets[].offer` | `Decimal | NoneType` | default: `None` |
| `markets[].percentage_change` | `Decimal | NoneType` | default: `None` |
| `markets[].scaling_factor` | `Decimal | NoneType` | default: `None` |
| `markets[].streaming_prices_available` | `bool | NoneType` | default: `None` |
| `markets[].update_time` | `str | NoneType` | default: `None` |
| `markets[].update_time_utc` | `str | NoneType` | default: `None` |

### Response example

```json
{
  "markets": [
    {
      "epic": "CS.D.EURUSD.CFD.IP",
      "instrumentName": "EUR/USD",
      "marketStatus": "TRADEABLE",
      "bid": "1.08120",
      "offer": "1.08135"
    }
  ]
}
```

### Limitations

- `search_term` must contain at least one non-whitespace character.
- Results depend on the active account's permissions and market catalogue.

### Exceptions

| Exception | Trigger | Recovery |
| --- | --- | --- |
| `ValueError` | `search_term` is empty or contains only whitespace. | Correct the argument before calling IG again. |
| `AuthenticationError` | IG rejected the credentials or session refresh failed. | Re-authenticate with valid credentials before retrying. |
| `AuthorizationError` | The active account cannot access this resource. | Switch to an entitled account or request the required IG permission. |
| `RateLimitError` | IG rejected the request because an allowance was exhausted. | Wait for `retry_after_seconds` when present, then retry with backoff. |
| `ProviderRejectionError` | IG rejected an otherwise valid request. | Inspect `error_code` and correct the provider-specific input or account state. |
| `TransportError` | A network or timeout failure prevented a completed read request. | Retry the idempotent read with bounded backoff. |
