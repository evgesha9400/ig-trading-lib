# Client sentiment

`client.sentiment` is the typed client-sentiment resource. Use `get()` with the appropriate provider suffix for a market or related-market request. Response fields remain IG-controlled and are normalised to `snake_case`.

```python
with IGClient(config) as client:
    sentiment = client.sentiment.get("/MARKET_ID")
    related = client.sentiment.get("/related/MARKET_ID")
```

Client sentiment is observational data, not an execution signal or suitability assessment. Confirm market availability and account permissions independently.

--8<-- "docs/rest-api-reference/.client-sentiment-endpoints.md"
