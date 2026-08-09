# Exceptions

Catch the narrowest exception that changes your recovery decision. All library transport and
provider failures inherit from `IGError`; request and response validation uses
`pydantic.ValidationError`.

```python
from ig_trading_lib import AmbiguousExecutionError, ProviderRejectionError

try:
    confirmation = ig.operations.positions.create(request)
except AmbiguousExecutionError:
    # Reconcile account state. Replaying could duplicate the trade.
    raise
except ProviderRejectionError as error:
    print(error.error_code)
```

## Failure hierarchy

```text
Exception
├── PermissionError
│   └── LiveTradingPermissionError
└── RuntimeError
    └── IGError
        ├── AuthenticationError
        ├── AuthorizationError
        ├── RateLimitError
        ├── ProviderRejectionError
        ├── ResourceNotFoundError
        ├── TransportError
        ├── AmbiguousExecutionError
        ├── DealConfirmationError
        ├── StreamingSubscriptionError
        └── StreamingDataLossError
```

## Recovery decisions

| Exception | Meaning | Recovery |
| --- | --- | --- |
| `AuthenticationError` | Credentials, session creation, or token refresh failed. | Correct credentials or re-authenticate before retrying. |
| `AuthorizationError` | The active account lacks permission. | Switch account or obtain entitlement. |
| `RateLimitError` | An IG allowance was exhausted. | Honour `retry_after_seconds` and use bounded backoff. |
| `ProviderRejectionError` | IG rejected a well-formed request. | Inspect `error_code`; correct input or account state. |
| `ResourceNotFoundError` | The resource is absent or inaccessible. | Verify the identifier and active account. |
| `TransportError` | A read did not complete because of network or timeout failure. | Retry only when the method page says the call is safe to repeat. |
| `AmbiguousExecutionError` | A mutation may have reached IG, but its outcome is unknown. | Reconcile account state; never replay automatically. |
| `DealConfirmationError` | IG accepted a mutation, but confirmation retrieval failed. | Retrieve confirmation using `deal_reference`; never replay the mutation. |
| `LiveTradingPermissionError` | A live mutation lacked an explicit `TradingPermit`. | Construct the client with a deliberate permit. |
| `StreamingSubscriptionError` | IG or Lightstreamer rejected the subscription. | Correct the item, field, mode, adapter, or entitlement. |
| `StreamingDataLossError` | IG reported lost updates or the local buffer overflowed. | Rebuild state from a fresh snapshot before resubscribing. |
| `pydantic.ValidationError` | Request construction or response validation failed. | Correct request fields or report provider schema drift. |

## Safe diagnostics

`IGError` provides `status_code`, `error_code`, `request_id`, `operation_id`,
`retry_after_seconds`, and redacted `details`. Credential-like values are removed from retained
provider details.

::: ig_trading_lib.errors.IGError

::: ig_trading_lib.errors.DealConfirmationError

::: ig_trading_lib.core.LiveTradingPermissionError
