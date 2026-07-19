# Markets

Use the typed market search façade for discovery. Use the typed resource façades for market snapshots and historical prices. Use the raw version façades only when an IG-specific version, path, or payload is required.

## Market discovery

`client.markets.search(search_term)` is the dedicated v1 market-search operation. `client.markets.get("/EPIC")` is a typed v4 market lookup. Neither method validates whether a returned market is tradeable for the current account.

```python
with IGClient(config) as client:
    matches = client.markets.search("EURUSD")
    for market in matches.items:
        print(market.epic, market.market_status)
```

## Market navigation and prices

`client.categories` reads instrument categories. `client.prices` exposes the v3 price resource. Use a version façade for the provider's resolution, point-count, and date-range variants.

```python
with IGClient(config) as client:
    categories = client.categories.list()
    prices = client.prices.get("/CS.D.EURUSD.TODAY.IP")
```

For date-range, period, and price-history forms that require exact endpoint versions, use `client.v1` through `client.v4` as described in [version compatibility](../reference/version-compatibility.md). Those facades preserve raw provider payloads and do not provide endpoint-specific schema validation.

--8<-- "docs/rest-api-reference/.markets-endpoints.md"
