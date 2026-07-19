<section class="ig-docs-hero" aria-labelledby="ig-docs-title">
  <p class="ig-docs-eyebrow">IG API · Python SDK</p>
  <h1 id="ig-docs-title">IG Trading Library</h1>
  <p class="ig-docs-lede">Safe, typed synchronous and asynchronous IG REST and streaming clients.</p>
  <div class="ig-docs-actions">
    <a class="ig-docs-primary-action" href="getting-started/">Start with a demo</a>
    <a class="ig-docs-secondary-action" href="reference/public-api/">Explore the API</a>
  </div>
  <p class="ig-docs-disclaimer">Independent open-source documentation. This project is not affiliated with IG.</p>
</section>

The library supports demo and live IG environments, canonical snake-case response models, typed provider failures, and Lightstreamer subscriptions. It does not store credentials or tokens on disk.

## Use it safely

- Start with a demo account.
- Keep credentials outside source control.
- Pass `TradingPermit()` only when a live mutation is intentional.
- Treat `AmbiguousExecutionError` as an outcome that needs verification, not a signal to retry blindly.

## Find the right guide

- [Credentials and environments](guides/credentials.md)
- [Markets and history](guides/markets-and-history.md)
- [Positions and working orders](guides/positions-and-working-orders.md)
- [Streaming](guides/streaming.md)
- [Sync and async recipes](recipes/index.md)
- [Agent API index](reference/agent-api-index.md)
