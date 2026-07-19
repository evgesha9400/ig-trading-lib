# HTTP requests

`IGClient` and `AsyncIGClient` own authentication, provider headers, finite timeouts, safe-read retry, rate-limit handling, and redacted response diagnostics. Create a client with `IGConfig`; use a context manager so owned transports close predictably.

## Read, create, update, and delete

High-level clients expose Pythonic read methods such as `list()`, `get()`, and `search()`. Generic resource clients expose `create()`, `update()`, and `delete()` when a provider-defined request body or route suffix is required.

The library safely retries only reads. A mutation is never blindly retried: retain its deal reference and handle `AmbiguousExecutionError` by reconciling the outcome.

## Typed service boundaries

Use the high-level client when it offers the operation you need. Typed service methods provide the stable application interface; provider request and response details remain behind those services.

Read [Authentication and authorisation](authentication-and-authorisation.md) before creating a configuration and [Errors](errors.md) before adding recovery logic.
