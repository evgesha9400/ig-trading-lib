"""Authoritative IG operation manifest.

Protocol versions are implementation details. Public operation methods bind to one
maintained specification so users never choose HTTP methods, paths, or versions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HttpMethod = Literal["DELETE", "GET", "POST", "PUT"]


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    """Immutable evidence for the provider operation catalog."""

    url: str
    retrieved_on: str
    sha256: str


@dataclass(frozen=True, slots=True)
class OperationSpec:
    """Private wire contract for one IG operation."""

    operation_id: str
    method: HttpMethod
    path: str
    version: int
    mutation: bool
    public: bool
    invalidates_session: bool
    schema_provenance: str
    evidence: SourceEvidence


OFFICIAL_REST_EVIDENCE = SourceEvidence(
    url="https://labs.ig.com/rest-trading-api-reference.html",
    retrieved_on="2026-08-09",
    sha256="083d97999fe05bb88087cd6390ab880c4a4a29e6172bf9db09d66064dd52c083",
)

SOURCE_EXCLUSIONS = (
    "Client-controlled REST paths and protocol-version selection are intentionally unsupported.",
    "Credentialed provider integration calls are excluded from automated verification.",
    "Deprecated endpoint variants are excluded when a current documented variant exists.",
    "Session creation and OAuth refresh belong to the transport authentication lifecycle, "
    "not the authenticated public operation layer.",
)


def _spec(
    operation_id: str,
    method: HttpMethod,
    path: str,
    version: int,
    *,
    mutation: bool = False,
    public: bool = True,
    invalidates_session: bool = False,
    schema: str = "IG REST reference response schema with provider extras preserved",
) -> OperationSpec:
    return OperationSpec(
        operation_id=operation_id,
        method=method,
        path=path,
        version=version,
        mutation=mutation,
        public=public,
        invalidates_session=invalidates_session,
        schema_provenance=schema,
        evidence=OFFICIAL_REST_EVIDENCE,
    )


_SPECS = (
    _spec("accounts.list", "GET", "/accounts", 1),
    _spec("accounts.get_preferences", "GET", "/accounts/preferences", 1),
    _spec("accounts.update_preferences", "PUT", "/accounts/preferences", 1, mutation=True),
    _spec("activity.list", "GET", "/history/activity", 3),
    _spec("activity.list_by_date_range", "GET", "/history/activity/{from_date}/{to_date}", 1),
    _spec("activity.list_by_period", "GET", "/history/activity/{period}", 1),
    _spec("transactions.list", "GET", "/history/transactions", 2),
    _spec(
        "transactions.list_by_date_range",
        "GET",
        "/history/transactions/{transaction_type}/{from_date}/{to_date}",
        1,
    ),
    _spec(
        "transactions.list_by_period",
        "GET",
        "/history/transactions/{transaction_type}/{period}",
        1,
    ),
    _spec("confirmations.get", "GET", "/confirms/{deal_reference}", 1),
    _spec("positions.list", "GET", "/positions", 2),
    _spec("positions.get", "GET", "/positions/{deal_id}", 2),
    _spec("positions.create", "POST", "/positions/otc", 2, mutation=True),
    _spec("positions.amend", "PUT", "/positions/otc/{deal_id}", 2, mutation=True),
    _spec("positions.close", "DELETE", "/positions/otc", 1, mutation=True),
    _spec("working_orders.list", "GET", "/working-orders", 2),
    _spec("working_orders.create", "POST", "/working-orders/otc", 2, mutation=True),
    _spec("working_orders.amend", "PUT", "/working-orders/otc/{deal_id}", 2, mutation=True),
    _spec(
        "working_orders.delete",
        "DELETE",
        "/working-orders/otc/{deal_id}",
        2,
        mutation=True,
    ),
    _spec("repeat_dealing_window.get", "GET", "/repeat-dealing-window", 1),
    _spec("categories.list", "GET", "/categories", 1),
    _spec("categories.list_instruments", "GET", "/categories/{category_id}/instruments", 1),
    _spec("markets.list", "GET", "/markets", 2),
    _spec("markets.search", "GET", "/markets", 1),
    _spec("markets.get", "GET", "/markets/{epic}", 4),
    _spec("prices.list", "GET", "/prices/{epic}", 3),
    _spec("prices.list_points", "GET", "/prices/{epic}/{resolution}/{num_points}", 2),
    _spec(
        "prices.list_date_range",
        "GET",
        "/prices/{epic}/{resolution}/{start_date}/{end_date}",
        2,
    ),
    _spec("watchlists.list", "GET", "/watchlists", 1),
    _spec("watchlists.create", "POST", "/watchlists", 1, mutation=True),
    _spec("watchlists.get", "GET", "/watchlists/{watchlist_id}", 1),
    _spec("watchlists.update", "PUT", "/watchlists/{watchlist_id}", 1, mutation=True),
    _spec("watchlists.delete", "DELETE", "/watchlists/{watchlist_id}", 1, mutation=True),
    _spec(
        "watchlists.remove_market",
        "DELETE",
        "/watchlists/{watchlist_id}/{epic}",
        1,
        mutation=True,
    ),
    _spec("client_sentiment.list", "GET", "/client-sentiment", 1),
    _spec("client_sentiment.get", "GET", "/client-sentiment/{market_id}", 1),
    _spec("client_sentiment.related", "GET", "/client-sentiment/related/{market_id}", 1),
    _spec("session.get", "GET", "/session", 1),
    _spec("session.create", "POST", "/session", 3, mutation=True, public=False),
    _spec("session.switch_account", "PUT", "/session", 1, mutation=True),
    _spec(
        "session.delete",
        "DELETE",
        "/session",
        1,
        mutation=True,
        invalidates_session=True,
    ),
    _spec("session.get_encryption_key", "GET", "/session/encryptionKey", 1),
    _spec(
        "session.refresh_token",
        "POST",
        "/session/refresh-token",
        1,
        mutation=True,
        public=False,
    ),
    _spec(
        "indicative_costs.quote_open",
        "POST",
        "/indicativecostsandcharges/open",
        1,
        mutation=True,
    ),
    _spec(
        "indicative_costs.quote_close",
        "POST",
        "/indicativecostsandcharges/close",
        1,
        mutation=True,
    ),
    _spec(
        "indicative_costs.quote_edit",
        "POST",
        "/indicativecostsandcharges/edit",
        1,
        mutation=True,
    ),
    _spec(
        "indicative_costs.get_durable_medium",
        "GET",
        "/indicativecostsandcharges/durablemedium/{quote_reference}",
        1,
    ),
    _spec(
        "indicative_costs.history",
        "GET",
        "/indicativecostsandcharges/history/from/{from_date}/to/{to_date}",
        1,
    ),
    _spec("applications.list", "GET", "/operations/application", 1),
    _spec("applications.update", "PUT", "/operations/application", 1, mutation=True),
    _spec("applications.disable", "PUT", "/operations/application/disable", 1, mutation=True),
)

OPERATION_MANIFEST = {spec.operation_id: spec for spec in _SPECS}
PUBLIC_OPERATION_MANIFEST = {
    operation_id: spec for operation_id, spec in OPERATION_MANIFEST.items() if spec.public
}
