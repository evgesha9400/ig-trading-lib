# Public Python API

The source-checked contract is [public-api.yml](../contracts/public-api.yml). The composition roots
expose exactly two layers.

For copyable sync and async examples, every parameter and nested request field, recursive response
shapes, limitations, and exception recovery rules, use the
[library reference](index.md).

--8<-- "docs/reference/.client-entry-points.md"

## Composition roots

::: ig_trading_lib.api

## Core configuration and safety

::: ig_trading_lib.core

## Public failures

::: ig_trading_lib.errors

## Account operations

::: ig_trading_lib.operations.accounts

## Dealing operations

::: ig_trading_lib.operations.dealing

## Market operations

::: ig_trading_lib.operations.markets

## Watchlist operations

::: ig_trading_lib.operations.watchlists

## Session and application operations

::: ig_trading_lib.operations.session

::: ig_trading_lib.operations.applications

## Sentiment and cost operations

::: ig_trading_lib.operations.sentiment

::: ig_trading_lib.operations.costs

## Streaming operations

::: ig_trading_lib.operations.streaming

## Workflows

::: ig_trading_lib.workflows.discovery

::: ig_trading_lib.workflows.dealing

::: ig_trading_lib.workflows.portfolio
