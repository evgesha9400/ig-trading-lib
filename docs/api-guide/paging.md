# Paging

Paged IG responses retain typed items and typed paging metadata. Supply an operation-specific
query model instead of constructing provider URLs.

```python
from ig_trading_lib.operations.accounts import ActivityQuery

with IG(config) as ig:
    page = ig.operations.activity.list(ActivityQuery(page_size=100))
    while (next_query := page.next_query()) is not None:
        page = ig.operations.activity.list(next_query)
```

`ActivityResponse.next_query()` converts IG's continuation URL into a validated `ActivityQuery`.
It discards the provider's protocol-version parameter, keeping paths and versions private.

Transaction history uses numbered pages through `TransactionsQuery(page_number=..., page_size=...)`.
