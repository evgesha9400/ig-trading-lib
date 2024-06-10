import logging

from trading.orders import CreateWorkingOrder

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
        stopLevel=None
    )
    deal_reference = order_service.create_order(order=order)

    # Retrieve order
    orders = order_service.get_orders()
    logger.info(f"Orders:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 1

    # Delete order
    order_service.delete_order(deal_id=orders.workingOrders[0].workingOrderData.dealId)

    orders = order_service.get_orders()
    logger.info(f"Orders:\n{orders.model_dump_json(indent=4)}")
    assert len(orders.workingOrders) == 0
