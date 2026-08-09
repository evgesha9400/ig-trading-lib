<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Client Sentiment methods

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.client_sentiment.list()`

List client sentiment, optionally restricted to market identifiers.

Official IG reference: [https://labs.ig.com/reference/client-sentiment.html](https://labs.ig.com/reference/client-sentiment.html)

### Signatures

- Sync: `(market_ids: 'tuple[str, ...] | None' = None) -> 'ClientSentimentsResponse'`
- Async: `(market_ids: 'tuple[str, ...] | None' = None) -> 'ClientSentimentsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `market_ids` | `tuple[str, ...] | None` | None | - | Optional collection of IG client-sentiment market identifiers. |

### Sync example

```python
result = ig.operations.client_sentiment.list(market_ids=("EURUSD", "GBPUSD"))
```

### Async example

```python
result = await ig.operations.client_sentiment.list(market_ids=("EURUSD", "GBPUSD"))
```

### Response shape: `ClientSentimentsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `client_sentiments[]` | `tuple[ClientSentiment, ...]` | default: `()` |
| `client_sentiments[].market_id` | `str | None` | default: `None` |
| `client_sentiments[].long_position_percentage` | `float | None` | default: `None` |
| `client_sentiments[].short_position_percentage` | `float | None` | default: `None` |

### Response example

```json
{
  "client_sentiments": [
    {
      "market_id": "EURUSD",
      "long_position_percentage": 1.0,
      "short_position_percentage": 1.0
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- At most 500 identifiers are accepted; each must be 1-30 letters, digits, spaces, underscores, or hyphens.

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
| `ValueError` | The collection exceeds 500 items or an identifier violates IG's character and length rules. | Correct the argument before calling IG again. |

## `ig.operations.client_sentiment.get()`

Read client sentiment for one market identifier.

Official IG reference: [https://labs.ig.com/reference/client-sentiment-market-id.html](https://labs.ig.com/reference/client-sentiment-market-id.html)

### Signatures

- Sync: `(market_id: 'str') -> 'ClientSentimentResponse'`
- Async: `(market_id: 'str') -> 'ClientSentimentResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `market_id` | `str` | required | - | IG client-sentiment market identifier. |

### Sync example

```python
result = ig.operations.client_sentiment.get(market_id="EURUSD")
```

### Async example

```python
result = await ig.operations.client_sentiment.get(market_id="EURUSD")
```

### Response shape: `ClientSentimentResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `market_id` | `str | None` | default: `None` |
| `long_position_percentage` | `float | None` | default: `None` |
| `short_position_percentage` | `float | None` | default: `None` |

### Response example

```json
{
  "market_id": "EURUSD",
  "long_position_percentage": 1.0,
  "short_position_percentage": 1.0
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Sentiment is available only for markets exposed by IG's sentiment service.

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

## `ig.operations.client_sentiment.related()`

List sentiment for markets related to one market identifier.

Official IG reference: [https://labs.ig.com/reference/client-sentiment-related-market-id.html](https://labs.ig.com/reference/client-sentiment-related-market-id.html)

### Signatures

- Sync: `(market_id: 'str') -> 'ClientSentimentsResponse'`
- Async: `(market_id: 'str') -> 'ClientSentimentsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `market_id` | `str` | required | - | IG client-sentiment market identifier. |

### Sync example

```python
result = ig.operations.client_sentiment.related(market_id="EURUSD")
```

### Async example

```python
result = await ig.operations.client_sentiment.related(market_id="EURUSD")
```

### Response shape: `ClientSentimentsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `client_sentiments[]` | `tuple[ClientSentiment, ...]` | default: `()` |
| `client_sentiments[].market_id` | `str | None` | default: `None` |
| `client_sentiments[].long_position_percentage` | `float | None` | default: `None` |
| `client_sentiments[].short_position_percentage` | `float | None` | default: `None` |

### Response example

```json
{
  "client_sentiments": [
    {
      "market_id": "EURUSD",
      "long_position_percentage": 1.0,
      "short_position_percentage": 1.0
    }
  ]
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Related markets are selected by IG and may be empty.

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
