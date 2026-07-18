import threading
from collections.abc import AsyncIterator, Callable
from typing import Any

import pytest

from ig_trading_lib.core import StreamingSession
from ig_trading_lib.streaming import StreamingClient, StreamSubscription


class FakeUpdate:
    def getItemName(self) -> str:
        return "MARKET:CS.D.EURUSD.TODAY.IP"

    def getItemPos(self) -> int:
        return 1

    def isSnapshot(self) -> bool:
        return False

    def getFields(self) -> dict[str, str]:
        return {"BID": "1.0800", "OFFER": "1.0802"}

    def getChangedFields(self) -> dict[str, str]:
        return {"BID": "1.0800"}


class FakeSubscription:
    def __init__(self, mode: str, items: list[str], fields: list[str]) -> None:
        self.mode = mode
        self.items = items
        self.fields = fields
        self.listener: Any = None
        self.data_adapter: str | None = None
        self.snapshot: bool | None = None

    def addListener(self, listener: Any) -> None:
        self.listener = listener

    def setDataAdapter(self, value: str) -> None:
        self.data_adapter = value

    def setRequestedSnapshot(self, value: bool) -> None:
        self.snapshot = value


class FakeConnectionDetails:
    def __init__(self) -> None:
        self.user: str | None = None
        self.password: str | None = None

    def setUser(self, value: str) -> None:
        self.user = value

    def setPassword(self, value: str) -> None:
        self.password = value


class FakeLightstreamerClient:
    def __init__(self, emit: Callable[[Any], None]) -> None:
        self.connectionDetails = FakeConnectionDetails()
        self._emit = emit
        self.connected = False
        self.connect_calls = 0
        self.disconnected = False
        self.subscriptions: list[FakeSubscription] = []
        self.unsubscribed: list[FakeSubscription] = []
        self.listeners: list[Any] = []

    def connect(self) -> None:
        self.connected = True
        self.connect_calls += 1

    def addListener(self, listener: Any) -> None:
        self.listeners.append(listener)

    def disconnect(self) -> None:
        self.disconnected = True

    def subscribe(self, subscription: FakeSubscription) -> None:
        self.subscriptions.append(subscription)
        self._emit(subscription.listener)

    def unsubscribe(self, subscription: FakeSubscription) -> None:
        self.unsubscribed.append(subscription)


def _subscription() -> StreamSubscription:
    return StreamSubscription(
        key="prices",
        mode="MERGE",
        items=("MARKET:CS.D.EURUSD.TODAY.IP",),
        fields=("BID", "OFFER"),
        data_adapter="DEFAULT",
    )


def _session() -> StreamingSession:
    return StreamingSession(
        endpoint="https://stream.example.test",
        account_id="ABC123",
        cst="cst",
        security_token="security",
    )


def test_streaming_bridge_yields_updates_and_closes_its_sdk_subscription() -> None:
    sdk_clients: list[FakeLightstreamerClient] = []

    def client_factory(_: str, __: str | None) -> FakeLightstreamerClient:
        client = FakeLightstreamerClient(lambda listener: listener.onItemUpdate(FakeUpdate()))
        sdk_clients.append(client)
        return client

    stream = StreamingClient(
        session_provider=_session,
        client_factory=client_factory,
        subscription_factory=FakeSubscription,
    )
    updates = stream.iter_updates(_subscription())

    update = next(updates)
    updates.close()

    client = sdk_clients[0]
    assert update.item_name == "MARKET:CS.D.EURUSD.TODAY.IP"
    assert update.fields == {"BID": "1.0800", "OFFER": "1.0802"}
    assert update.changed_fields == {"BID": "1.0800"}
    assert client.connectionDetails.user == "ABC123"
    assert client.connectionDetails.password == "CST-cst|XST-security"
    assert client.subscriptions[0].data_adapter == "DEFAULT"
    assert client.unsubscribed == client.subscriptions


@pytest.mark.asyncio
async def test_async_streaming_bridge_delivers_sdk_callbacks_to_the_event_loop() -> None:
    thread: threading.Thread | None = None

    def client_factory(_: str, __: str | None) -> FakeLightstreamerClient:
        def emit(listener: Any) -> None:
            nonlocal thread
            thread = threading.Thread(target=lambda: listener.onItemUpdate(FakeUpdate()))
            thread.start()

        return FakeLightstreamerClient(emit)

    stream = StreamingClient(
        session_provider=_session,
        client_factory=client_factory,
        subscription_factory=FakeSubscription,
    )

    updates: AsyncIterator[Any] = stream.aiter_updates(_subscription())
    update = await anext(updates)
    await updates.aclose()
    if thread is not None:
        thread.join()

    assert update.changed_fields == {"BID": "1.0800"}


def test_terminal_stream_error_refreshes_credentials_without_duplicate_subscriptions() -> None:
    refreshed = threading.Event()
    sdk_clients: list[FakeLightstreamerClient] = []

    def client_factory(_: str, __: str | None) -> FakeLightstreamerClient:
        client = FakeLightstreamerClient(lambda listener: listener.onItemUpdate(FakeUpdate()))
        sdk_clients.append(client)
        return client

    def refresh_session() -> StreamingSession:
        refreshed.set()
        return StreamingSession(
            endpoint="https://stream.example.test",
            account_id="ABC123",
            cst="new-cst",
            security_token="new-security",
        )

    stream = StreamingClient(
        session_provider=_session,
        refresh_session_provider=refresh_session,
        client_factory=client_factory,
        subscription_factory=FakeSubscription,
    )
    updates = stream.iter_updates(_subscription())
    next(updates)

    client = sdk_clients[0]
    client.listeners[0].onServerError(20, "session expired")

    assert refreshed.wait(timeout=1)
    assert client.connect_calls == 2
    assert client.connectionDetails.password == "CST-new-cst|XST-new-security"
    assert len(client.subscriptions) == 1
    updates.close()
