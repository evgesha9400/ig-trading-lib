# Watchlists

`client.watchlists` is the typed watchlist resource. It exposes `list()` for one page, `get()` for one watchlist, and generic `create()`, `update()`, and `delete()` methods for provider-defined watchlist operations.

## Mutation boundary

Watchlist mutations are guarded on live accounts. Construct the client with `TradingPermit()` only when the mutation is intentional. Preserve provider identifiers and validate request bodies against IG's current requirements.

```python
with IGClient(config, trading_permit=TradingPermit()) as client:
    watchlists = client.watchlists.list()
    response = client.watchlists.create(provider_request)
```

Consult [Trading safety](../api-guide/trading-safety.md) before changing a live watchlist.

--8<-- "docs/rest-api-reference/.watchlists-endpoints.md"
