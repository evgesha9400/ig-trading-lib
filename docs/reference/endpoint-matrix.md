# Endpoint matrix

This checked table mirrors `DOCUMENTED_ENDPOINTS`. It records the documented IG REST operation name, HTTP method, path template, and supported provider API versions.

| Operation | Method | Path | Supported IG API versions |
| --- | --- | --- | --- |
| accounts | GET | `/accounts` | v1 |
| account_preferences | GET | `/accounts/preferences` | v1 |
| account_preferences | PUT | `/accounts/preferences` | v1 |
| activity | GET | `/history/activity` | v2, v3 |
| activity_date_range | GET | `/history/activity/{from_date}/{to_date}` | v1 |
| activity_period | GET | `/history/activity/{last_period}` | v1 |
| transactions | GET | `/history/transactions` | v2 |
| transactions_date_range | GET | `/history/transactions/{transaction_type}/{from_date}/{to_date}` | v1 |
| transactions_period | GET | `/history/transactions/{transaction_type}/{last_period}` | v1 |
| confirmation | GET | `/confirms/{deal_reference}` | v1 |
| positions | GET | `/positions` | v1, v2 |
| position | GET | `/positions/{deal_id}` | v1, v2 |
| otc_position | POST | `/positions/otc` | v1, v2 |
| otc_position | DELETE | `/positions/otc` | v1 |
| otc_position_by_deal | PUT | `/positions/otc/{deal_id}` | v1, v2 |
| working_orders | GET | `/working-orders` | v1, v2 |
| otc_working_order | POST | `/working-orders/otc` | v1, v2 |
| otc_working_order_by_deal | DELETE | `/working-orders/otc/{deal_id}` | v1, v2 |
| otc_working_order_by_deal | PUT | `/working-orders/otc/{deal_id}` | v1, v2 |
| repeat_dealing_window | GET | `/repeat-dealing-window` | v1 |
| categories | GET | `/categories` | v1 |
| category_instruments | GET | `/categories/{category_id}/instruments` | v1 |
| markets | GET | `/markets` | v1, v2 |
| market | GET | `/markets/{epic}` | v1, v2, v3, v4 |
| market_search | GET | `/markets` | v1 |
| prices | GET | `/prices/{epic}` | v3 |
| prices_points | GET | `/prices/{epic}/{resolution}/{num_points}` | v1, v2 |
| prices_date_range | GET | `/prices/{epic}/{resolution}/{start_date}/{end_date}` | v1, v2 |
| watchlists | GET | `/watchlists` | v1 |
| watchlists | POST | `/watchlists` | v1 |
| watchlist | GET | `/watchlists/{watchlist_id}` | v1 |
| watchlist | PUT | `/watchlists/{watchlist_id}` | v1 |
| watchlist | DELETE | `/watchlists/{watchlist_id}` | v1 |
| watchlist_market | DELETE | `/watchlists/{watchlist_id}/{epic}` | v1 |
| client_sentiment | GET | `/client-sentiment` | v1 |
| client_sentiment_market | GET | `/client-sentiment/{market_id}` | v1 |
| client_sentiment_related | GET | `/client-sentiment/related/{market_id}` | v1 |
| session | GET | `/session` | v1 |
| session | DELETE | `/session` | v1 |
| session | POST | `/session` | v1, v2, v3 |
| session | PUT | `/session` | v1 |
| encryption_key | GET | `/session/encryptionKey` | v1 |
| refresh_token | POST | `/session/refresh-token` | v1 |
| indicative_costs_close | POST | `/indicativecostsandcharges/close` | v1 |
| indicative_costs_durable_medium | GET | `/indicativecostsandcharges/durablemedium/{indicative_quote_reference}` | v1 |
| indicative_costs_edit | POST | `/indicativecostsandcharges/edit` | v1 |
| indicative_costs_history | GET | `/indicativecostsandcharges/history/from/{from_date}/to/{to_date}` | v1 |
| indicative_costs_open | POST | `/indicativecostsandcharges/open` | v1 |
| applications | GET | `/operations/application` | v1 |
| applications | PUT | `/operations/application` | v1 |
| application_disable | PUT | `/operations/application/disable` | v1 |
