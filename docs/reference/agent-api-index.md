# Agent API index

[`public-api-index.json`](public-api-index.json) is generated from the checked [public API contract](../contracts/public-api.yml) and the maintained source endpoint catalog. Do not hand-edit it.

It is intended for tool-using agents that need to discover supported imports, checked signatures, typed errors, safety rules, and the library's endpoint/version compatibility catalog. The catalog is maintained source data, not a live assertion that IG currently enables an operation for a particular account.

For a compact entry point, use the deployed [`/llms.txt`](../llms.txt). Before constructing a call, an agent should re-read the public contract and the relevant conceptual guide. In particular, raw `v1` through `v4` resources are generic helpers and must not be treated as provider-schema validation.
