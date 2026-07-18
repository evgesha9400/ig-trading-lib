# IG Trading Library

Safe, typed synchronous and asynchronous IG REST and streaming clients.

The library supports demo and live IG environments, canonical snake-case response models, typed provider failures, and Lightstreamer subscriptions. It does not store credentials or tokens on disk.

## Use it safely

- Start with a demo account.
- Keep credentials outside source control.
- Pass `TradingPermit()` only when a live mutation is intentional.
- Treat `AmbiguousExecutionError` as an outcome that needs verification, not a signal to retry blindly.

## Documentation contract

The checked [public API contract](contracts/public-api.yml) records the exported API, source signatures, errors, model fields, examples, live-mutation rules, and every endpoint-matrix row. Continuous integration validates it before the documentation build.

## Find the right guide

- [Credentials and environments](guides/credentials.md)
- [Markets and history](guides/markets-and-history.md)
- [Positions and working orders](guides/positions-and-working-orders.md)
- [Streaming](guides/streaming.md)
- [Sync and async recipes](recipes/index.md)
- [Agent API index](reference/agent-api-index.md)
