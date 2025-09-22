import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def cleanup_working_orders(order_service):
    """
    Fixture to ensure no working orders exist before a test run.
    """
    logger.info("Cleaning up working orders before test.")
    orders = order_service.get_orders()
    if len(orders.workingOrders) > 0:
        for wo in orders.workingOrders:
            order_service.delete_order(deal_id=wo.workingOrderData.dealId)

    orders_after_cleanup = order_service.get_orders()
    logger.info(f"Orders after cleanup:\n{orders_after_cleanup.model_dump_json(indent=4)}")
    assert len(orders_after_cleanup.workingOrders) == 0
    logger.info("Cleanup complete. No working orders.")


@pytest.fixture
def tradeable_market_data(order_service):
    """
    Provides data for a tradeable market, skipping the test if the market is closed.
    """
    epic = "CS.D.EURUSD.TODAY.IP"
    order_type = "LIMIT"
    direction = "BUY"

    # Fetch current market snapshot and dealing rules to compute a safe level
    headers = order_service.client.build_headers(override_version="3")
    url = f"{order_service.client.base_url}/gateway/deal/markets/{epic}"
    resp = order_service.client.http.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    snapshot = data.get("snapshot", {})
    bid = float(snapshot.get("bid"))
    offer = float(snapshot.get("offer"))
    market_status = snapshot.get("marketStatus")
    if market_status not in {"TRADEABLE", "EDITS_ONLY"}:
        pytest.skip(f"Market {epic} is not tradeable right now: {market_status}")
    mid = (bid + offer) / 2.0

    # Determine minimum stop/limit distance if provided; otherwise use a conservative default
    default_points = 100.0
    dealing_rules = data.get("dealingRules", {}) or data.get("instrument", {}).get("dealingRules", {})
    min_dist = None
    if isinstance(dealing_rules, dict):
        normal = dealing_rules.get("minNormalStopOrLimitDistance") or dealing_rules.get("minNormalStopLimitDistance")
        if isinstance(normal, dict) and normal.get("value") is not None:
            try:
                min_dist = float(normal.get("value"))
            except Exception:
                min_dist = None
    points = min_dist if (min_dist and min_dist > 0) else default_points

    # Choose a far-away level that respects direction/type and avoids immediate fill
    if order_type == "LIMIT" and direction == "BUY":
        level_value = mid - 20 * points
    elif order_type == "LIMIT" and direction == "SELL":
        level_value = mid + 20 * points
    elif order_type == "STOP" and direction == "BUY":
        level_value = mid + 20 * points
    else:  # STOP and SELL
        level_value = mid - 20 * points

    return {
        "epic": epic,
        "order_type": order_type,
        "direction": direction,
        "level": f"{level_value:.5f}",
        "points": points,
        "level_value": level_value,
    }
