# Markets

Use the typed market search service for discovery and the typed resources for market snapshots and historical prices.

## Market discovery

`client.markets.search(search_term)` discovers markets. `client.markets.get("/EPIC")` retrieves one market. Neither method validates whether a returned market is tradeable for the current account.

```python
with IGClient(config) as client:
    matches = client.markets.search("EURUSD")
    for market in matches.items:
        print(market.epic, market.market_status)
```

## Market navigation and prices

`client.categories` reads instrument categories. `client.prices` retrieves historical price data.

```python
with IGClient(config) as client:
    categories = client.categories.list()
    prices = client.prices.get("/CS.D.EURUSD.TODAY.IP")
```

--8<-- "docs/rest-api-reference/.markets-endpoints.md"
