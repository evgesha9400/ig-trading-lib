# Accounts and preferences

`client.accounts` is the typed v1 account façade. It normalises provider keys to `snake_case` and returns `Page` or `IGModel` values.

## Read accounts and preferences

`accounts.list()` returns one page. Its `items` contain the accounts available to the authenticated session. `accounts.preferences()` reads the active account's preferences.

```python
with IGClient(config) as client:
    for account in client.accounts.list().items:
        print(account.account_id)

    preferences = client.accounts.preferences()
    print(preferences.trailing_stops_enabled)
```

## Change preferences deliberately

`accounts.update_preferences(body)` is a guarded mutation. The body remains an IG provider-defined mapping; the library does not invent or validate provider preference fields. On a live account, construct the client with an explicit `TradingPermit()` before calling it.

Use [the endpoint matrix](../reference/endpoint-matrix.md) when an exact provider route or version matters. The maintained matrix is a library compatibility catalog, not a live check that a provider operation is currently available to an account.
