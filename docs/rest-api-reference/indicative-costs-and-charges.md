# Indicative costs and charges

`client.costs` is the typed resource for IG's indicative-cost and charge operations. Provider request shapes and the returned quote fields vary by operation and market, so pass a reviewed mapping and retain the provider reference where supplied.

## Mutation boundary

Cost and charge requests that create or amend an indicative quote are guarded for live accounts. A `TradingPermit()` expresses intent; it does not validate provider request fields or make a quote executable.

Use the exact compatibility table below before choosing an operation. For an IG version or path not represented by the high-level resource, use a version façade.

--8<-- "docs/rest-api-reference/.indicative-costs-and-charges-endpoints.md"
