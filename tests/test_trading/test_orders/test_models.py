from ig_trading_lib.trading.orders.models import WorkingOrders


def test_working_orders_validation(working_orders):
    working_order = WorkingOrders.model_validate(working_orders)
    assert working_order is not None

