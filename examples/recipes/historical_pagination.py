"""Walk historical activity pages without manually parsing continuation paths."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from ig_trading_lib import AsyncIGClient, IGClient, IGModel


def list_activity(client: IGClient) -> Iterator[IGModel]:
    """Yield all linked activity entries from the typed history facade."""
    yield from client.activity.iter_pages(item_key="activities")


async def list_activity_async(client: AsyncIGClient) -> AsyncIterator[IGModel]:
    """Yield all linked activity entries from the asynchronous history facade."""
    async for activity in client.activity.iter_pages(item_key="activities"):
        yield activity
