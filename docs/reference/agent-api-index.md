# Agent API index

[`public-api-index.json`](public-api-index.json) is generated from the checked
[public API contract](../contracts/public-api.yml) and private source-evidence manifest. Do not
hand-edit it.

Its `entry_points` are the only construction routes. Its `operations` and `workflows` map every
public path back to the checked contract.

For a compact entry point, use the deployed [`/llms.txt`](../llms.txt). Before constructing a call, an agent should re-read the public contract and the relevant conceptual guide.
