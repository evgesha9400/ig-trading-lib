# Account

`client.accounts` is the typed account service. It normalises provider keys to `snake_case` and returns `Page` or `IGModel` values.

## Accounts and preferences

`accounts.list()` returns one page. Its `items` contain the accounts available to the authenticated session. `accounts.preferences()` reads the active account's preferences.

```python
with IGClient(config) as client:
    for account in client.accounts.list().items:
        print(account.account_id)

    preferences = client.accounts.preferences()
    print(preferences.trailing_stops_enabled)
```

## Activity and transaction history

`client.activity` and `client.transactions` both expose `list()` for one page and `iter_pages()` for IG's next-link sequence.

```python
with IGClient(config) as client:
    for activity in client.activity.iter_pages(item_key="activities"):
        print(activity)
```

## Change preferences deliberately

`accounts.update_preferences(body)` is a guarded mutation. The body remains an IG provider-defined mapping; the library does not invent or validate provider preference fields. On a live account, construct the client with an explicit `TradingPermit()` before calling it.

Use the operation table below to find the supported account routes. It is not a live check that a provider operation is currently available to an account.

--8<-- "docs/rest-api-reference/.account-endpoints.md"
