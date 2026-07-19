# Paging

High-level resource reads return `Page[IGModel]`. A page has immutable `items` and an optional `next_path` supplied by IG.

## Consume pages lazily

`list()` returns one page; `iter_pages()` follows the provider continuation path one page at a time. Pass `item_key` only when the provider's payload stores its items under a non-default key such as `activities`.

```python
with IGClient(config) as client:
    page = client.activity.list(item_key="activities")
    print(page.next_path)

    for activity in client.activity.iter_pages(item_key="activities"):
        process(activity)
```

The asynchronous equivalent is `async for item in client.activity.iter_pages(...)`. The library follows the path supplied by IG; it does not create stable cursors or persist a resume checkpoint for you.

Read [Errors](errors.md) for rate-limit recovery and the rule that a mutation outcome must be verified rather than retried.
