# Types and exceptions

Use this section after choosing an [operation](../operations/index.md) or
[workflow](../workflows/index.md). It documents the objects that cross those interfaces without
repeating the methods themselves.

| Category | Use it to understand |
| --- | --- |
| [Client and configuration](client-and-configuration.md) | How to construct the sync or async client and permit live mutations. |
| [Requests and responses](requests-and-responses.md) | Where request validation and typed results belong. |
| [Streaming](streaming.md) | How subscriptions are declared and updates are delivered. |
| [Exceptions](exceptions.md) | What failures mean and whether an operation is safe to retry. |

The supported convenience imports are exported from `ig_trading_lib`. Operation-specific request
and response types remain in their resource modules and are linked from the method that consumes or
returns them.

The checked [`public-api.yml`](../../contracts/public-api.yml) contract and
[`public-api-index.json`](../public-api-index.json) remain the machine-readable sources for tooling.
They are not a second human-facing method hierarchy.
