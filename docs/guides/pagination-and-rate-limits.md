# Pagination and rate limits

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

## Rate-limit reads safely

For retriable read failures, catch `RateLimitError` or `TransportError` and let a caller-owned scheduler choose whether and when to retry. `RateLimitError.retry_after_seconds` is optional and is only set when IG provides a usable `Retry-After` header.

Never reuse this read-recovery pattern for a mutation after `AmbiguousExecutionError`. Verify with a confirmation or relevant read first. The [error recovery recipe](../recipes/index.md#error-recovery) makes one retry decision signal and intentionally does not send another request.
