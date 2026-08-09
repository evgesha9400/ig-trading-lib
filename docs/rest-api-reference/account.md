# Account operations

Use `ig.operations.accounts` for accounts and preferences, `ig.operations.activity` for account
activity, and `ig.operations.transactions` for transaction history.

```python
from ig_trading_lib.operations.accounts import ActivityQuery, TransactionsQuery

with IG(config) as ig:
    accounts = ig.operations.accounts.list()
    activity = ig.operations.activity.list(ActivityQuery(page_size=100))
    transactions = ig.operations.transactions.list(
        TransactionsQuery(transaction_type="ALL", page_number=1, page_size=100)
    )
```

Preference changes accept `UpdateAccountPreferencesRequest` and cross the shared mutation guard.

--8<-- "docs/rest-api-reference/.account-endpoints.md"
