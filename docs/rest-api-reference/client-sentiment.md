# Client sentiment operations

```python
with IG(config) as ig:
    sentiment = ig.operations.client_sentiment.get("MARKET_ID")
    related = ig.operations.client_sentiment.related("MARKET_ID")
```

Client sentiment is observational data, not an execution signal or suitability assessment.

--8<-- "docs/rest-api-reference/.client-sentiment-endpoints.md"
