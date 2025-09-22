import logging
import time

import pytest

from ig_trading_lib.trading import CreateWorkingOrder, UpdateWorkingOrder, get_deal_confirmation

logger = logging.getLogger(__name__)


def test_orders_service_crud(order_service, tradeable_market_data):
    """
    Tests the full CRUD lifecycle of working orders.
    """
    throttle_seconds = 0.5

    def sleep_if_needed():
        if throttle_seconds > 0:
            time.sleep(throttle_seconds)

    # CREATE
    order = CreateWorkingOrder(
        currencyCode="USD",
        direction=tradeable_market_data["direction"],
        epic=tradeable_market_data["epic"],
        expiry="DFB",
        forceOpen=False,
        goodTillDate=None,
        level=tradeable_market_data["level"],
        size=0.5,
        type=tradeable_market_data["order_type"],
        guaranteedStop=False,
        timeInForce="GOOD_TILL_CANCELLED",
    )
    deal_reference = order_service.create_order(order=order)

    deal_confirmation = get_deal_confirmation(order_service.client, deal_reference)
    logger.info(f"Deal confirmation:\n{deal_confirmation.model_dump_json(indent=4)}")
    assert deal_confirmation.dealStatus == "ACCEPTED"
    sleep_if_needed()

    # RETRIEVE and assert created order present
    orders = order_service.get_orders()
    logger.info(f"Orders:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 1
    created_order = orders.workingOrders[0]
    sleep_if_needed()

    # UPDATE
    level_value = tradeable_market_data["level_value"]
    points = tradeable_market_data["points"]
    if tradeable_market_data["order_type"] == "LIMIT" and tradeable_market_data["direction"] == "BUY":
        updated_level_value = level_value - points
    elif tradeable_market_data["order_type"] == "LIMIT" and tradeable_market_data["direction"] == "SELL":
        updated_level_value = level_value + points
    elif tradeable_market_data["order_type"] == "STOP" and tradeable_market_data["direction"] == "BUY":
        updated_level_value = level_value + points
    else:
        updated_level_value = level_value - points
    updated_level = f"{updated_level_value:.2f}"

    deal_reference_update = order_service.update_order(
        deal_id=created_order.workingOrderData.dealId,
        order=UpdateWorkingOrder(
            level=updated_level, type=tradeable_market_data["order_type"], timeInForce="GOOD_TILL_CANCELLED"
        ),
    )
    deal_confirmation_update = get_deal_confirmation(order_service.client, deal_reference_update)
    logger.info(f"Update confirmation:\n{deal_confirmation_update.model_dump_json(indent=4)}")
    assert deal_confirmation_update.dealStatus == "ACCEPTED"
    sleep_if_needed()

    # VERIFY update
    orders = order_service.get_orders()
    logger.info(f"Orders after update:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 1
    provider_level = float(orders.workingOrders[0].workingOrderData.orderLevel)
    assert provider_level == pytest.approx(float(updated_level), abs=0.2)

    # DELETE
    order_service.delete_order(deal_id=orders.workingOrders[0].workingOrderData.dealId)

    # VERIFY deletion
    orders = order_service.get_orders()
    logger.info(f"Orders after deletion:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 0
