# Agent API index

[`public-api-index.json`](public-api-index.json) is generated from the checked [public API contract](../contracts/public-api.yml) and the maintained source endpoint catalog. Do not hand-edit it.

Its `entry_points` are the only application-client construction routes. Their `namespaces` map every client-owned service path and operation back to the checked contract. Use `complete_reference` for exhaustive type, method, error, and model coverage; it is not a list of constructors to invoke.

For a compact entry point, use the deployed [`/llms.txt`](../llms.txt). Before constructing a call, an agent should re-read the public contract and the relevant conceptual guide. In particular, raw `v1` through `v4` resources are generic helpers and must not be treated as provider-schema validation.
