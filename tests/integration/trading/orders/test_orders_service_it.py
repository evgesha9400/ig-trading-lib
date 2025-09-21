import logging

from ig_trading_lib.trading.orders import CreateWorkingOrder

logger = logging.getLogger(__name__)


def test_orders_service_crud(order_service):
    orders = order_service.get_orders()
    logger.info(f"Orders:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 0

    # Create order
    order = CreateWorkingOrder(
        currencyCode="GBP",
        direction="BUY",
        epic="CS.D.EURGBP.TODAY.IP",
        expiry="DFB",
        forceOpen=False,
        goodTillDate=None,
        level="8452.0",
        size=0.5,
        type="STOP",
        guaranteedStop=False,
        timeInForce="GOOD_TILL_CANCELLED",
        dealReference=None,
        limitDistance=None,
        limitLevel=None,
        stopDistance=None,
        stopLevel=None,
    )
    deal_reference = order_service.create_order(order=order)

    deal_confirmation = order_service.confirms(deal_reference=deal_reference)
    logger.info(f"Deal confirmation:\n{deal_confirmation.model_dump_json(indent=4)}")

    if deal_confirmation.affectedDeals:
        logger.info("Order was accepted, proceeding with retrieval and deletion")
        orders = order_service.get_orders()
        logger.info(f"Orders:\n{orders.model_dump_json(indent=4)}")
        assert len(orders.workingOrders) == 1

        order_service.delete_order(
            deal_id=orders.workingOrders[0].workingOrderData.dealId
        )

        orders = order_service.get_orders()
        logger.info(f"Orders after deletion:\n{orders.model_dump_json(indent=4)}")
        assert len(orders.workingOrders) == 0
    else:
        logger.info(f"Order was rejected with reason: {deal_confirmation.reason}")
        orders = order_service.get_orders()
        logger.info(f"Orders after rejection:\n{orders.model_dump_json(indent=4)}")
        assert len(orders.workingOrders) == 0
