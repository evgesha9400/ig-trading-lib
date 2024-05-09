import logging
import time

from trading.positions import CreatePosition, ClosePosition, UpdatePosition

logger = logging.getLogger(__name__)


def test_position_service_crud(position_service):
    # Create a position
    create = CreatePosition(
        epic="CS.D.EURGBP.TODAY.IP",
        expiry="DFB",
        direction="BUY",
        size=0.5,
        orderType="MARKET",
        currencyCode="GBP",
        forceOpen=False,
        guaranteedStop=False,
        trailingStop=False,
        dealReference=None,
        level=None,
        limitDistance=None,
        limitLevel=None,
        quoteId=None,
        stopDistance=None,
        stopLevel=None,
        trailingStopIncrement=None
    )
    deal_reference = position_service.create_position(create)
    assert deal_reference is not None
    logger.info(f"Create Deal reference:\n{deal_reference.model_dump_json(indent=2)}")

    time.sleep(1)

    # Get open positions
    open_positions = position_service.get_open_positions()
    assert open_positions is not None
    assert len(open_positions.positions) == 1
    deal_id = open_positions.positions[0].position.dealId
    logger.info(f"Open positions:\n{open_positions.model_dump_json(indent=2)}")

    # Get open position by deal ID
    open_position = position_service.get_open_position_by_deal_id(deal_id=deal_id)
    assert open_position is not None
    assert open_position.position.dealId == deal_id
    logger.info(f"Open position by deal ID:\n{open_position.model_dump_json(indent=2)}")

    # Update the position
    update = UpdatePosition(
        stopLevel=open_position.market.low - 1,
        limitLevel=open_position.market.high + 1,
    )
    deal_reference = position_service.update_position(deal_id, update)
    assert deal_reference is not None
    logger.info(f"Update Deal reference:\n{deal_reference.model_dump_json(indent=2)}")

    # Close the position
    close = ClosePosition(
        direction="SELL",
        orderType="MARKET",
        size=0.5,
        dealId=deal_id,
    )
    deal_reference = position_service.close_position(close)
    assert deal_reference is not None
    logger.info(f"Close Deal reference:\n{deal_reference.model_dump_json(indent=2)}")

