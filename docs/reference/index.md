<!-- Generated from docs/contracts/method-documentation.yml and live Python types. -->

# Library reference

The reference hierarchy mirrors the library interface. Choose the layer that matches your intent before choosing a namespace.

| Layer | Mental model | Namespaces | Methods |
| --- | --- | ---: | ---: |
| [Operations](operations/index.md) | One faithful typed IG call. | 16 | 51 |
| [Workflows](workflows/index.md) | A multi-operation journey composed from operations. | 4 | 8 |
| [Types and exceptions](types-and-exceptions/index.md) | Objects constructed, returned, streamed, or raised by those two layers. | 4 categories | - |

Every method documents its parameters, sync and async examples, recursive response shape, response example, limitations, and exceptions.

- Parameter and response tables use public Python field names.
- Nested request fields include Pydantic defaults and declared constraints.
- `ValidationError` is `pydantic.ValidationError`; all other named failures are exported by `ig_trading_lib`.
- Mutation workflows retain `DealConfirmationError.deal_reference`; reconcile it instead of replaying the mutation.
