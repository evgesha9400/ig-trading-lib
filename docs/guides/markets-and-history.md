# Markets and history

Use the typed market search façade for discovery. Use the typed resource façades for linked account history. Use the raw version façades only when an IG-specific version, path, or payload is required.

## Market discovery

`client.markets.search(search_term)` is the dedicated v1 market-search operation. `client.markets.get("/EPIC")` is a typed v4 market lookup. Neither method validates whether a returned market is tradeable for the current account.

```python
with IGClient(config) as client:
    matches = client.markets.search("EURUSD")
    for market in matches.items:
        print(market.epic, market.market_status)
```

## Account history

`client.activity` uses v3 and `client.transactions` uses v2 for their high-level resource façades. `iter_pages()` follows only the continuation path returned by IG, so consume it lazily and retain any cursor state your application needs.

```python
with IGClient(config) as client:
    for activity in client.activity.iter_pages(item_key="activities"):
        print(activity)
```

For date-range, period, and price-history forms that require exact endpoint versions, use `client.v1` through `client.v4` as described in [version façades](version-facades.md). Those facades preserve raw provider payloads and do not provide endpoint-specific schema validation.
