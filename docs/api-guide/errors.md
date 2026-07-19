# Errors

All operational REST failures derive from `IGError`; `LiveTradingPermissionError` is a separate `PermissionError` raised before a protected live mutation reaches authentication or the network.

## Handle typed failures

| Failure | Meaning | Next action |
| --- | --- | --- |
| `AuthenticationError` | Session credentials or token refresh failed. | Repair credentials or authentication state. |
| `AuthorizationError` | The authenticated session lacks resource access. | Check account and application permissions. |
| `RateLimitError` | IG rejected a request for quota. | Schedule a later read using `retry_after_seconds` when present. |
| `ResourceNotFoundError` | The route or resource was not found or accessible. | Verify IDs and access scope. |
| `ProviderRejectionError` | IG rejected a provider request. | Inspect safe provider diagnostics when available. |
| `TransportError` | A read did not complete. | Let a caller-owned retry policy decide. |
| `AmbiguousExecutionError` | A mutation may have reached IG. | Verify its outcome; do not blindly retry. |

`status_code`, `error_code`, `request_id`, `operation_id`, `retry_after_seconds`, and redacted `details` are optional diagnostics. Their absence does not change the failure type. Sensitive values in retained details are redacted.

## Successful response logs

The standard-library logger is `ig_trading_lib.transport`. On successful HTTP responses it emits the message `ig.http.response` with structured fields including method, path, status code, provider request ID, operation ID, and retry count. It is not a log event for failed responses. Configure this logger in your application and avoid recording credentials or raw provider tokens in surrounding logs.

## Rate limits and retry decisions

For retriable reads, catch `RateLimitError` or `TransportError` and let a caller-owned scheduler choose whether and when to retry. `RateLimitError.retry_after_seconds` is optional and is only set when IG supplies a usable `Retry-After` header.

Never reuse this read-recovery pattern for a mutation after `AmbiguousExecutionError`. Verify with a confirmation or relevant read first. The [error recovery recipe](../recipes/index.md#error-recovery) makes one retry decision signal and intentionally does not send another request.
