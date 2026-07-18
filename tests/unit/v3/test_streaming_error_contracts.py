import asyncio
from typing import Any

import pytest

from ig_trading_lib import AsyncStreamingClient, StreamingDataLossError, StreamSubscription
from ig_trading_lib.core import StreamingSession
from ig_trading_lib.errors import StreamingSubscriptionError
from ig_trading_lib.streaming import (
    StreamUpdate,
    _AsyncSink,
    _SubscriptionListener,
    _SyncSink,
)


def _subscription() -> StreamSubscription:
    return StreamSubscription("prices", "MERGE", ("MARKET:EPIC",), ("BID",))


def _session() -> StreamingSession:
    return StreamingSession("https://stream.example.test", "ABC123", "cst", "security")


def _update() -> StreamUpdate:
    return StreamUpdate("prices", "MARKET:EPIC", 1, {"BID": "1.0"}, {"BID": "1.0"}, False)


def test_streaming_sinks_expose_subscription_loss_and_backpressure_failures() -> None:
    sink = _SyncSink(maxsize=1)
    listener = _SubscriptionListener(_subscription(), sink)

    listener.onSubscriptionError(17, "invalid fields")
    with pytest.raises(StreamingSubscriptionError):
        event = sink.get()
        if isinstance(event, Exception):
            raise event

    listener.onItemLostUpdates("MARKET:EPIC", 1, 3)
    with pytest.raises(StreamingDataLossError):
        event = sink.get()
        if isinstance(event, Exception):
            raise event

    sink.deliver(_update())
    sink.deliver(_update())
    with pytest.raises(StreamingDataLossError):
        sink.get()


@pytest.mark.asyncio
async def test_async_streaming_sink_uses_the_event_loop_and_surfaces_backpressure() -> None:
    sink = _AsyncSink(asyncio.get_running_loop(), maxsize=1)
    sink.deliver(_update())
    await asyncio.sleep(0)
    assert await sink.get_async() == _update()
    sink.deliver(_update())
    sink.deliver(_update())
    await asyncio.sleep(0)
    with pytest.raises(StreamingDataLossError):
        await sink.get_async()


class _Details:
    def setUser(self, _: str) -> None:
        pass

    def setPassword(self, _: str) -> None:
        pass


class _Subscription:
    def __init__(self, *_: object) -> None:
        self.listener: Any = None

    def addListener(self, listener: Any) -> None:
        self.listener = listener

    def setRequestedSnapshot(self, _: bool) -> None:
        pass


class _Client:
    def __init__(self) -> None:
        self.connectionDetails = _Details()
        self.disconnect_calls = 0

    def addListener(self, _: Any) -> None:
        pass

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        self.disconnect_calls += 1

    def subscribe(self, subscription: _Subscription) -> None:
        subscription.listener._sink.deliver(_update())

    def unsubscribe(self, _: _Subscription) -> None:
        pass


@pytest.mark.asyncio
async def test_async_streaming_facade_owns_and_closes_its_delegate() -> None:
    clients: list[_Client] = []

    def client_factory(_: str, __: str | None) -> _Client:
        client = _Client()
        clients.append(client)
        return client

    stream = AsyncStreamingClient(
        session_provider=lambda: _session_async(),
        refresh_session_provider=lambda: _session_async(),
        client_factory=client_factory,
        subscription_factory=_Subscription,
    )

    updates = stream.aiter_updates(_subscription())
    assert await anext(updates) == _update()
    await updates.aclose()
    await stream.close()

    assert clients[0].disconnect_calls == 1


async def _session_async() -> StreamingSession:
    return _session()
