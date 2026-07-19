"""The documented IG REST reference, grouped in IG's published order."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HttpMethod = Literal["DELETE", "GET", "POST", "PUT"]
RestReferenceCategory = Literal[
    "account",
    "dealing",
    "markets",
    "watchlists",
    "client-sentiment",
    "login",
    "indicative-costs-and-charges",
    "general",
]


@dataclass(frozen=True, slots=True)
class RestReferenceSection:
    """One official IG REST reference section and its documentation path."""

    slug: RestReferenceCategory
    title: str


REST_REFERENCE_SECTIONS: tuple[RestReferenceSection, ...] = (
    RestReferenceSection("account", "Account"),
    RestReferenceSection("dealing", "Dealing"),
    RestReferenceSection("markets", "Markets"),
    RestReferenceSection("watchlists", "Watchlists"),
    RestReferenceSection("client-sentiment", "Client sentiment"),
    RestReferenceSection("login", "Login"),
    RestReferenceSection("indicative-costs-and-charges", "Indicative costs and charges"),
    RestReferenceSection("general", "General"),
)


@dataclass(frozen=True, slots=True)
class EndpointSpec:
    """One operation listed in IG's REST API reference."""

    name: str
    path_template: str
    method: HttpMethod
    versions: tuple[int, ...]
    category: RestReferenceCategory


DOCUMENTED_ENDPOINTS: tuple[EndpointSpec, ...] = (
    EndpointSpec("accounts", "/accounts", "GET", (1,), "account"),
    EndpointSpec("account_preferences", "/accounts/preferences", "GET", (1,), "account"),
    EndpointSpec("account_preferences", "/accounts/preferences", "PUT", (1,), "account"),
    EndpointSpec("activity", "/history/activity", "GET", (2, 3), "account"),
    EndpointSpec(
        "activity_date_range", "/history/activity/{from_date}/{to_date}", "GET", (1,), "account"
    ),
    EndpointSpec("activity_period", "/history/activity/{last_period}", "GET", (1,), "account"),
    EndpointSpec("transactions", "/history/transactions", "GET", (2,), "account"),
    EndpointSpec(
        "transactions_date_range",
        "/history/transactions/{transaction_type}/{from_date}/{to_date}",
        "GET",
        (1,),
        "account",
    ),
    EndpointSpec(
        "transactions_period",
        "/history/transactions/{transaction_type}/{last_period}",
        "GET",
        (1,),
        "account",
    ),
    EndpointSpec("confirmation", "/confirms/{deal_reference}", "GET", (1,), "dealing"),
    EndpointSpec("positions", "/positions", "GET", (1, 2), "dealing"),
    EndpointSpec("position", "/positions/{deal_id}", "GET", (1, 2), "dealing"),
    EndpointSpec("otc_position", "/positions/otc", "POST", (1, 2), "dealing"),
    EndpointSpec("otc_position", "/positions/otc", "DELETE", (1,), "dealing"),
    EndpointSpec("otc_position_by_deal", "/positions/otc/{deal_id}", "PUT", (1, 2), "dealing"),
    EndpointSpec("working_orders", "/working-orders", "GET", (1, 2), "dealing"),
    EndpointSpec("otc_working_order", "/working-orders/otc", "POST", (1, 2), "dealing"),
    EndpointSpec(
        "otc_working_order_by_deal", "/working-orders/otc/{deal_id}", "DELETE", (1, 2), "dealing"
    ),
    EndpointSpec(
        "otc_working_order_by_deal", "/working-orders/otc/{deal_id}", "PUT", (1, 2), "dealing"
    ),
    EndpointSpec("repeat_dealing_window", "/repeat-dealing-window", "GET", (1,), "dealing"),
    EndpointSpec("categories", "/categories", "GET", (1,), "markets"),
    EndpointSpec(
        "category_instruments", "/categories/{category_id}/instruments", "GET", (1,), "markets"
    ),
    EndpointSpec("markets", "/markets", "GET", (1, 2), "markets"),
    EndpointSpec("market", "/markets/{epic}", "GET", (1, 2, 3, 4), "markets"),
    EndpointSpec("market_search", "/markets", "GET", (1,), "markets"),
    EndpointSpec("prices", "/prices/{epic}", "GET", (3,), "markets"),
    EndpointSpec(
        "prices_points", "/prices/{epic}/{resolution}/{num_points}", "GET", (1, 2), "markets"
    ),
    EndpointSpec(
        "prices_date_range",
        "/prices/{epic}/{resolution}/{start_date}/{end_date}",
        "GET",
        (1, 2),
        "markets",
    ),
    EndpointSpec("watchlists", "/watchlists", "GET", (1,), "watchlists"),
    EndpointSpec("watchlists", "/watchlists", "POST", (1,), "watchlists"),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "GET", (1,), "watchlists"),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "PUT", (1,), "watchlists"),
    EndpointSpec("watchlist", "/watchlists/{watchlist_id}", "DELETE", (1,), "watchlists"),
    EndpointSpec(
        "watchlist_market", "/watchlists/{watchlist_id}/{epic}", "DELETE", (1,), "watchlists"
    ),
    EndpointSpec("client_sentiment", "/client-sentiment", "GET", (1,), "client-sentiment"),
    EndpointSpec(
        "client_sentiment_market", "/client-sentiment/{market_id}", "GET", (1,), "client-sentiment"
    ),
    EndpointSpec(
        "client_sentiment_related",
        "/client-sentiment/related/{market_id}",
        "GET",
        (1,),
        "client-sentiment",
    ),
    EndpointSpec("session", "/session", "GET", (1,), "login"),
    EndpointSpec("session", "/session", "DELETE", (1,), "login"),
    EndpointSpec("session", "/session", "POST", (1, 2, 3), "login"),
    EndpointSpec("session", "/session", "PUT", (1,), "login"),
    EndpointSpec("encryption_key", "/session/encryptionKey", "GET", (1,), "login"),
    EndpointSpec("refresh_token", "/session/refresh-token", "POST", (1,), "login"),
    EndpointSpec(
        "indicative_costs_close",
        "/indicativecostsandcharges/close",
        "POST",
        (1,),
        "indicative-costs-and-charges",
    ),
    EndpointSpec(
        "indicative_costs_durable_medium",
        "/indicativecostsandcharges/durablemedium/{indicative_quote_reference}",
        "GET",
        (1,),
        "indicative-costs-and-charges",
    ),
    EndpointSpec(
        "indicative_costs_edit",
        "/indicativecostsandcharges/edit",
        "POST",
        (1,),
        "indicative-costs-and-charges",
    ),
    EndpointSpec(
        "indicative_costs_history",
        "/indicativecostsandcharges/history/from/{from_date}/to/{to_date}",
        "GET",
        (1,),
        "indicative-costs-and-charges",
    ),
    EndpointSpec(
        "indicative_costs_open",
        "/indicativecostsandcharges/open",
        "POST",
        (1,),
        "indicative-costs-and-charges",
    ),
    EndpointSpec("applications", "/operations/application", "GET", (1,), "general"),
    EndpointSpec("applications", "/operations/application", "PUT", (1,), "general"),
    EndpointSpec("application_disable", "/operations/application/disable", "PUT", (1,), "general"),
)
