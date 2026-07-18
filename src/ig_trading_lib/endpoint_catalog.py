"""The documented IG REST operation and version compatibility matrix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HttpMethod = Literal["DELETE", "GET", "POST", "PUT"]


@dataclass(frozen=True, slots=True)
class EndpointSpec:
    """One operation listed in IG's REST API reference."""

    name: str
    path_template: str
    method: HttpMethod
    versions: tuple[int, ...]


DOCUMENTED_ENDPOINTS: tuple[EndpointSpec, ...] = (
    EndpointSpec("accounts", "/accounts", "GET", (1,)),
    EndpointSpec("account_preferences", "/accounts/preferences", "GET", (1,)),
    EndpointSpec("account_preferences", "/accounts/preferences", "PUT", (1,)),
    EndpointSpec("activity", "/history/activity", "GET", (2, 3)),
    EndpointSpec("activity_date_range", "/history/activity/{from_date}/{to_date}", "GET", (1,)),
    EndpointSpec("activity_period", "/history/activity/{last_period}", "GET", (1,)),
    EndpointSpec("transactions", "/history/transactions", "GET", (2,)),
    EndpointSpec(
        "transactions_date_range",
        "/history/transactions/{transaction_type}/{from_date}/{to_date}",
        "GET",
        (1,),
    ),
    EndpointSpec(
        "transactions_period",
        "/history/transactions/{transaction_type}/{last_period}",
        "GET",
        (1,),
    ),
    EndpointSpec("confirmation", "/confirms/{deal_reference}", "GET", (1,)),
    EndpointSpec("positions", "/positions", "GET", (1, 2)),
    EndpointSpec("position", "/positions/{deal_id}", "GET", (1, 2)),
    EndpointSpec("otc_position", "/positions/otc", "POST", (1, 2)),
    EndpointSpec("otc_position", "/positions/otc", "DELETE", (1,)),
    EndpointSpec("otc_position_by_deal", "/positions/otc/{deal_id}", "PUT", (1, 2)),
    EndpointSpec("working_orders", "/working-orders", "GET", (1, 2)),
    EndpointSpec("otc_working_order", "/working-orders/otc", "POST", (1, 2)),
    EndpointSpec("otc_working_order_by_deal", "/working-orders/otc/{deal_id}", "DELETE", (1, 2)),
    EndpointSpec("otc_working_order_by_deal", "/working-orders/otc/{deal_id}", "PUT", (1, 2)),
    EndpointSpec("repeat_dealing_window", "/repeat-dealing-window", "GET", (1,)),
    EndpointSpec("categories", "/categories", "GET", (1,)),
    EndpointSpec("category_instruments", "/categories/{category_id}/instruments", "GET", (1,)),
    EndpointSpec("markets", "/markets", "GET", (1, 2)),
    EndpointSpec("market", "/markets/{epic}", "GET", (1, 2, 3, 4)),
    EndpointSpec("market_search", "/markets", "GET", (1,)),
    EndpointSpec("prices", "/prices/{epic}", "GET", (3,)),
    EndpointSpec("prices_points", "/prices/{epic}/{resolution}/{num_points}", "GET", (1, 2)),
    EndpointSpec(
        "prices_date_range",
        "/prices/{epic}/{resolution}/{start_date}/{end_date}",
        "GET",
        (1, 2),
    ),
    EndpointSpec("watchlists", "/watchlists", "GET", (1,)),
    EndpointSpec("watchlists", "/watchlists", "POST", (1,)),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "GET", (1,)),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "PUT", (1,)),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "DELETE", (1,)),
    EndpointSpec("watchlist_market", "/watchlists/{watchlist_id}/{epic}", "DELETE", (1,)),
    EndpointSpec("client_sentiment", "/client-sentiment", "GET", (1,)),
    EndpointSpec("client_sentiment_market", "/client-sentiment/{market_id}", "GET", (1,)),
    EndpointSpec("client_sentiment_related", "/client-sentiment/related/{market_id}", "GET", (1,)),
    EndpointSpec("session", "/session", "GET", (1,)),
    EndpointSpec("session", "/session", "DELETE", (1,)),
    EndpointSpec("session", "/session", "POST", (1, 2, 3)),
    EndpointSpec("session", "/session", "PUT", (1,)),
    EndpointSpec("encryption_key", "/session/encryptionKey", "GET", (1,)),
    EndpointSpec("refresh_token", "/session/refresh-token", "POST", (1,)),
    EndpointSpec("indicative_costs_close", "/indicativecostsandcharges/close", "POST", (1,)),
    EndpointSpec(
        "indicative_costs_durable_medium",
        "/indicativecostsandcharges/durablemedium/{indicative_quote_reference}",
        "GET",
        (1,),
    ),
    EndpointSpec("indicative_costs_edit", "/indicativecostsandcharges/edit", "POST", (1,)),
    EndpointSpec(
        "indicative_costs_history",
        "/indicativecostsandcharges/history/from/{from_date}/to/{to_date}",
        "GET",
        (1,),
    ),
    EndpointSpec("indicative_costs_open", "/indicativecostsandcharges/open", "POST", (1,)),
    EndpointSpec("applications", "/operations/application", "GET", (1,)),
    EndpointSpec("applications", "/operations/application", "PUT", (1,)),
    EndpointSpec("application_disable", "/operations/application/disable", "PUT", (1,)),
)
