# General

`client.applications` is the typed v1 resource for client-owned application operations. It lists or changes application metadata and can disable the current application key through the provider's documented route.

Application mutations are guarded on live accounts. Treat a request that fails ambiguously as a state that must be verified before another mutation.

--8<-- "docs/rest-api-reference/.general-endpoints.md"
