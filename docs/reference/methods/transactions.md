<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Transactions methods

Examples assume an initialized synchronous or asynchronous client named `ig`.

## `ig.operations.transactions.list()`

List account transactions with v2 query controls.

Official IG reference: [https://labs.ig.com/reference/history-transactions.html](https://labs.ig.com/reference/history-transactions.html)

### Signatures

- Sync: `(query: 'TransactionsQuery | None' = None) -> 'TransactionsResponse'`
- Async: `(query: 'TransactionsQuery | None' = None) -> 'TransactionsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `query` | `TransactionsQuery | None` | None | - | Optional typed query controls; `None` uses provider defaults. |
| `query.transaction_type` | `Literal['ALL', 'ALL_DEAL', 'DEPOSIT', 'WITHDRAWAL']` | default: `'ALL'` | - | Provider transaction category filter. |
| `query.from_date` | `date | datetime | str | None` | default: `None` | - | Inclusive beginning of the requested time range. |
| `query.to_date` | `date | datetime | str | None` | default: `None` | - | Inclusive end of the requested time range. |
| `query.max_span_seconds` | `int | None` | default: `None` | >= `0` | Maximum transaction-history span in seconds. |
| `query.page_size` | `int | None` | default: `None` | >= `0` | Maximum records requested per provider page. |
| `query.page_number` | `int | None` | default: `None` | >= `1` | Provider page number. |

### Sync example

```python
from ig_trading_lib.operations.accounts import TransactionsQuery

result = ig.operations.transactions.list(query=TransactionsQuery(transaction_type="ALL", page_size=50))
```

### Async example

```python
from ig_trading_lib.operations.accounts import TransactionsQuery

result = await ig.operations.transactions.list(query=TransactionsQuery(transaction_type="ALL", page_size=50))
```

### Response shape: `TransactionsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `transactions[]` | `tuple[Transaction, ...]` | default: `()` |
| `transactions[].cash_transaction` | `bool | None` | default: `None` |
| `transactions[].close_level` | `str | None` | default: `None` |
| `transactions[].currency` | `str | None` | default: `None` |
| `transactions[].date` | `str | None` | default: `None` |
| `transactions[].date_utc` | `str | None` | default: `None` |
| `transactions[].instrument_name` | `str | None` | default: `None` |
| `transactions[].open_date_utc` | `str | None` | default: `None` |
| `transactions[].open_level` | `str | None` | default: `None` |
| `transactions[].period` | `str | None` | default: `None` |
| `transactions[].profit_and_loss` | `str | None` | default: `None` |
| `transactions[].reference` | `str | None` | default: `None` |
| `transactions[].size` | `str | None` | default: `None` |
| `transactions[].transaction_type` | `str | None` | default: `None` |
| `metadata` | `NumberedPageMetadata | None` | default: `None` |
| `metadata.page_data` | `PageData` | required |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |

### Response example

```json
{
  "transactions": [
    {
      "cash_transaction": true,
      "close_level": "example",
      "currency": "GBP",
      "date": "example",
      "date_utc": "example",
      "instrument_name": "EUR/USD",
      "open_date_utc": "example",
      "open_level": "example",
      "period": "example",
      "profit_and_loss": "example",
      "reference": "example",
      "size": "example",
      "transaction_type": "example"
    }
  ],
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "size": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- IG restricts transaction history to provider-defined date and page windows.

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

## `ig.operations.transactions.list_by_date_range()`

List transactions of one type between two dates.

Official IG reference: [https://labs.ig.com/reference/history-transactions-dates.html](https://labs.ig.com/reference/history-transactions-dates.html)

### Signatures

- Sync: `(transaction_type: 'TransactionType', from_date: 'date | datetime | str', to_date: 'date | datetime | str') -> 'TransactionsResponse'`
- Async: `(transaction_type: 'TransactionType', from_date: 'date | datetime | str', to_date: 'date | datetime | str') -> 'TransactionsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `transaction_type` | `Literal['ALL', 'ALL_DEAL', 'DEPOSIT', 'WITHDRAWAL']` | required | - | Provider transaction category filter. |
| `from_date` | `date | datetime | str` | required | - | Inclusive beginning of the requested time range. |
| `to_date` | `date | datetime | str` | required | - | Inclusive end of the requested time range. |

### Sync example

```python
result = ig.operations.transactions.list_by_date_range(transaction_type="ALL", from_date="2026-08-01", to_date="2026-08-08")
```

### Async example

```python
result = await ig.operations.transactions.list_by_date_range(transaction_type="ALL", from_date="2026-08-01", to_date="2026-08-08")
```

### Response shape: `TransactionsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `transactions[]` | `tuple[Transaction, ...]` | default: `()` |
| `transactions[].cash_transaction` | `bool | None` | default: `None` |
| `transactions[].close_level` | `str | None` | default: `None` |
| `transactions[].currency` | `str | None` | default: `None` |
| `transactions[].date` | `str | None` | default: `None` |
| `transactions[].date_utc` | `str | None` | default: `None` |
| `transactions[].instrument_name` | `str | None` | default: `None` |
| `transactions[].open_date_utc` | `str | None` | default: `None` |
| `transactions[].open_level` | `str | None` | default: `None` |
| `transactions[].period` | `str | None` | default: `None` |
| `transactions[].profit_and_loss` | `str | None` | default: `None` |
| `transactions[].reference` | `str | None` | default: `None` |
| `transactions[].size` | `str | None` | default: `None` |
| `transactions[].transaction_type` | `str | None` | default: `None` |
| `metadata` | `NumberedPageMetadata | None` | default: `None` |
| `metadata.page_data` | `PageData` | required |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |

### Response example

```json
{
  "transactions": [
    {
      "cash_transaction": true,
      "close_level": "example",
      "currency": "GBP",
      "date": "example",
      "date_utc": "example",
      "instrument_name": "EUR/USD",
      "open_date_utc": "example",
      "open_level": "example",
      "period": "example",
      "profit_and_loss": "example",
      "reference": "example",
      "size": "example",
      "transaction_type": "example"
    }
  ],
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "size": 1
  }
}
```

### Limitations

- Returned resources and fields depend on the active account, environment, entitlements, and current IG catalogue.
- IG can change account-specific allowances and availability independently of this library.
- Date strings and transaction types must be accepted by the provider endpoint.

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

## `ig.operations.transactions.list_by_period()`

List recent transactions of one type for a provider period.

Official IG reference: [https://labs.ig.com/reference/history-transactions-period.html](https://labs.ig.com/reference/history-transactions-period.html)

### Signatures

- Sync: `(transaction_type: 'TransactionType', period: 'str') -> 'TransactionsResponse'`
- Async: `(transaction_type: 'TransactionType', period: 'str') -> 'TransactionsResponse'`

### Parameters

| Name | Type | Required/default | Constraints | Description |
| --- | --- | --- | --- | --- |
| `transaction_type` | `Literal['ALL', 'ALL_DEAL', 'DEPOSIT', 'WITHDRAWAL']` | required | - | Provider transaction category filter. |
| `period` | `str` | required | - | ISO-8601-style provider period such as `P7D`. |

### Sync example

```python
result = ig.operations.transactions.list_by_period(transaction_type="ALL", period="P7D")
```

### Async example

```python
result = await ig.operations.transactions.list_by_period(transaction_type="ALL", period="P7D")
```

### Response shape: `TransactionsResponse`

| Field | Type | Required/default |
| --- | --- | --- |
| `transactions[]` | `tuple[Transaction, ...]` | default: `()` |
| `transactions[].cash_transaction` | `bool | None` | default: `None` |
| `transactions[].close_level` | `str | None` | default: `None` |
| `transactions[].currency` | `str | None` | default: `None` |
| `transactions[].date` | `str | None` | default: `None` |
| `transactions[].date_utc` | `str | None` | default: `None` |
| `transactions[].instrument_name` | `str | None` | default: `None` |
| `transactions[].open_date_utc` | `str | None` | default: `None` |
| `transactions[].open_level` | `str | None` | default: `None` |
| `transactions[].period` | `str | None` | default: `None` |
| `transactions[].profit_and_loss` | `str | None` | default: `None` |
| `transactions[].reference` | `str | None` | default: `None` |
| `transactions[].size` | `str | None` | default: `None` |
| `transactions[].transaction_type` | `str | None` | default: `None` |
| `metadata` | `NumberedPageMetadata | None` | default: `None` |
| `metadata.page_data` | `PageData` | required |
| `metadata.page_data.page_number` | `int` | required |
| `metadata.page_data.page_size` | `int` | required |
| `metadata.page_data.total_pages` | `int` | required |
| `metadata.size` | `int | None` | default: `None` |

### Response example

```json
{
  "transactions": [
    {
      "cash_transaction": true,
      "close_level": "example",
      "currency": "GBP",
      "date": "example",
      "date_utc": "example",
      "instrument_name": "EUR/USD",
      "open_date_utc": "example",
      "open_level": "example",
      "period": "example",
      "profit_and_loss": "example",
      "reference": "example",
      "size": "example",
      "transaction_type": "example"
    }
  ],
  "metadata": {
    "page_data": {
      "page_number": 1,
      "page_size": 1,
      "total_pages": 1
    },
    "size": 1
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
