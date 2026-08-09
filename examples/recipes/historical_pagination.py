"""Advance typed account-activity pages without handling provider URLs."""

from ig_trading_lib import IG, AsyncIG
from ig_trading_lib.operations.accounts import Activity, ActivityQuery


def list_activity(ig: IG, *, page_size: int = 100) -> tuple[Activity, ...]:
    page = ig.operations.activity.list(ActivityQuery(page_size=page_size))
    activities = page.activities
    while (next_query := page.next_query()) is not None:
        page = ig.operations.activity.list(next_query)
        activities += page.activities
    return activities


async def list_activity_async(ig: AsyncIG, *, page_size: int = 100) -> tuple[Activity, ...]:
    page = await ig.operations.activity.list(ActivityQuery(page_size=page_size))
    activities = page.activities
    while (next_query := page.next_query()) is not None:
        page = await ig.operations.activity.list(next_query)
        activities += page.activities
    return activities
