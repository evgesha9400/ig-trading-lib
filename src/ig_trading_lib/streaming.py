"""Thread-safe Lightstreamer adapters for IG stream subscriptions."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Mapping
from dataclasses import dataclass
from queue import Empty, Full, Queue
from threading import Lock, Thread
from typing import Any, Literal

from ig_trading_lib.core import StreamingSession
from ig_trading_lib.errors import (
    AuthenticationError,
    StreamingDataLossError,
    StreamingSubscriptionError,
)

StreamMode = Literal["MERGE", "DISTINCT"]
_Event = "StreamUpdate | Exception"


@dataclass(frozen=True, slots=True)
class StreamSubscription:
    """Declarative request for one IG Lightstreamer subscription."""

    key: str
    mode: StreamMode
    items: tuple[str, ...]
    fields: tuple[str, ...]
    data_adapter: str | None = None
    snapshot: bool = True
    max_frequency: str | float | None = None


@dataclass(frozen=True, slots=True)
class StreamUpdate:
    """A complete, immutable Lightstreamer update delivered to user code."""

    subscription_key: str
    item_name: str | None
    item_position: int
    fields: Mapping[str, str | None]
    changed_fields: Mapping[str, str | None]
    is_snapshot: bool


@dataclass(slots=True)
class _ActiveSubscription:
    subscription: Any
    sink: _Sink


class _Sink:
    def deliver(self, event: StreamUpdate | Exception) -> None:
        raise NotImplementedError

    def get(self) -> StreamUpdate | Exception:
        raise NotImplementedError


class _SyncSink(_Sink):
    def __init__(self, maxsize: int) -> None:
        self._queue: Queue[StreamUpdate | Exception] = Queue(maxsize=maxsize)
        self._failure: StreamingDataLossError | None = None

    def deliver(self, event: StreamUpdate | Exception) -> None:
        try:
            self._queue.put_nowait(event)
        except Full:
            self._failure = StreamingDataLossError(
                "Streaming consumer fell behind the configured local buffer."
            )

    def get(self) -> StreamUpdate | Exception:
        while True:
            if self._failure is not None:
                raise self._failure
            try:
                return self._queue.get(timeout=0.1)
            except Empty:
                continue


class _AsyncSink(_Sink):
    def __init__(self, loop: asyncio.AbstractEventLoop, maxsize: int) -> None:
        self._loop = loop
        self._queue: asyncio.Queue[StreamUpdate | Exception] = asyncio.Queue(maxsize=maxsize)
        self._failure: StreamingDataLossError | None = None

    def deliver(self, event: StreamUpdate | Exception) -> None:
        self._loop.call_soon_threadsafe(self._put, event)

    def _put(self, event: StreamUpdate | Exception) -> None:
        if self._queue.full():
            self._failure = StreamingDataLossError(
                "Streaming consumer fell behind the configured local buffer."
            )
            return
        self._queue.put_nowait(event)

    def get(self) -> StreamUpdate | Exception:
        raise RuntimeError("Async stream sinks must be awaited.")

    async def get_async(self) -> StreamUpdate | Exception:
        if self._failure is not None:
            raise self._failure
        event = await self._queue.get()
        if self._failure is not None:
            raise self._failure
        return event


class _SubscriptionListener:
    def __init__(self, specification: StreamSubscription, sink: _Sink) -> None:
        self._specification = specification
        self._sink = sink

    def onItemUpdate(self, update: Any) -> None:
        """Copy the SDK callback payload before returning to its event thread."""
        self._sink.deliver(
            StreamUpdate(
                subscription_key=self._specification.key,
                item_name=update.getItemName(),
                item_position=update.getItemPos(),
                fields=dict(update.getFields()),
                changed_fields=dict(update.getChangedFields()),
                is_snapshot=update.isSnapshot(),
            )
        )

    def onSubscriptionError(self, code: int, message: str) -> None:
        self._sink.deliver(
            StreamingSubscriptionError(f"IG rejected stream subscription {code}: {message}")
        )

    def onItemLostUpdates(self, item_name: str, item_position: int, lost_updates: int) -> None:
        self._sink.deliver(
            StreamingDataLossError(
                "IG reported "
                f"{lost_updates} lost updates for {item_name} at position {item_position}."
            )
        )


class _ConnectionListener:
    def __init__(self, owner: StreamingClient) -> None:
        self._owner = owner

    def onServerError(self, _: int, __: str) -> None:
        Thread(target=self._owner._recover_once, daemon=True).start()

    def onStatusChange(self, status: str) -> None:
        if status.startswith("CONNECTED"):
            self._owner._complete_recovery_epoch()


class StreamingClient:
    """Adapt Lightstreamer's callback API into synchronous and asynchronous iterators."""

    def __init__(
        self,
        *,
        session_provider: Callable[[], StreamingSession],
        refresh_session_provider: Callable[[], StreamingSession] | None = None,
        client_factory: Callable[[str, str | None], Any] | None = None,
        subscription_factory: Callable[[str, list[str], list[str]], Any] | None = None,
        queue_size: int = 1_000,
    ) -> None:
        self._session_provider = session_provider
        self._refresh_session_provider = refresh_session_provider or session_provider
        self._client_factory = client_factory or _default_client_factory
        self._subscription_factory = subscription_factory or _default_subscription_factory
        self._queue_size = queue_size
        self._client: Any | None = None
        self._active: list[_ActiveSubscription] = []
        self._lock = Lock()
        self._recovery_started = False

    def iter_updates(self, subscription: StreamSubscription) -> Iterator[StreamUpdate]:
        """Yield updates until the caller closes the iterator or a typed stream error occurs."""
        sink = _SyncSink(self._queue_size)
        active = self._start(subscription, sink)
        try:
            while True:
                event = sink.get()
                if isinstance(event, Exception):
                    raise event
                yield event
        finally:
            self._stop(active)

    async def aiter_updates(self, subscription: StreamSubscription) -> AsyncIterator[StreamUpdate]:
        """Yield updates on the current event loop without blocking the SDK callback thread."""
        sink = _AsyncSink(asyncio.get_running_loop(), self._queue_size)
        active = self._start(subscription, sink)
        try:
            while True:
                event = await sink.get_async()
                if isinstance(event, Exception):
                    raise event
                yield event
        finally:
            self._stop(active)

    def close(self) -> None:
        """Unsubscribe all active streams and close the Lightstreamer connection."""
        with self._lock:
            active = tuple(self._active)
        for entry in active:
            self._stop(entry, disconnect_when_idle=False)
        with self._lock:
            client = self._client
            self._client = None
        if client is not None:
            client.disconnect()

    def _start(self, specification: StreamSubscription, sink: _Sink) -> _ActiveSubscription:
        client = self._connect_if_needed()
        sdk_subscription = self._subscription_factory(
            specification.mode,
            list(specification.items),
            list(specification.fields),
        )
        listener = _SubscriptionListener(specification, sink)
        sdk_subscription.addListener(listener)
        if specification.data_adapter is not None:
            sdk_subscription.setDataAdapter(specification.data_adapter)
        sdk_subscription.setRequestedSnapshot(specification.snapshot)
        if specification.max_frequency is not None:
            sdk_subscription.setRequestedMaxFrequency(str(specification.max_frequency))
        active = _ActiveSubscription(sdk_subscription, sink)
        with self._lock:
            self._active.append(active)
        client.subscribe(sdk_subscription)
        return active

    def _stop(self, active: _ActiveSubscription, *, disconnect_when_idle: bool = True) -> None:
        with self._lock:
            if active not in self._active:
                return
            self._active.remove(active)
            client = self._client
            should_disconnect = disconnect_when_idle and not self._active
            if should_disconnect:
                self._client = None
        if client is not None:
            client.unsubscribe(active.subscription)
            if should_disconnect:
                client.disconnect()

    def _connect_if_needed(self) -> Any:
        with self._lock:
            if self._client is not None:
                return self._client
            session = self._session_provider()
            client = self._client_factory(session.endpoint, None)
            self._set_connection_credentials(client, session)
            if hasattr(client, "addListener"):
                client.addListener(_ConnectionListener(self))
            client.connect()
            self._client = client
            return client

    @staticmethod
    def _set_connection_credentials(client: Any, session: StreamingSession) -> None:
        client.connectionDetails.setUser(session.account_id)
        client.connectionDetails.setPassword(f"CST-{session.cst}|XST-{session.security_token}")

    def _recover_once(self) -> None:
        with self._lock:
            if self._client is None:
                return
            if self._recovery_started:
                active = tuple(self._active)
                failure = AuthenticationError("IG streaming recovery failed more than once.")
                for entry in active:
                    entry.sink.deliver(failure)
                return
            self._recovery_started = True
            client = self._client
        try:
            self._set_connection_credentials(client, self._refresh_session_provider())
            client.connect()
        except Exception as error:
            failure = AuthenticationError("IG streaming reauthentication failed.")
            failure.__cause__ = error
            with self._lock:
                active = tuple(self._active)
            for entry in active:
                entry.sink.deliver(failure)

    def _complete_recovery_epoch(self) -> None:
        with self._lock:
            self._recovery_started = False


def _default_client_factory(endpoint: str, adapter_set: str | None) -> Any:
    from lightstreamer.client import LightstreamerClient

    return LightstreamerClient(endpoint, adapter_set)


def _default_subscription_factory(mode: str, items: list[str], fields: list[str]) -> Any:
    from lightstreamer.client import Subscription

    return Subscription(mode, items, fields)


class AsyncStreamingClient:
    """Asynchronous streaming facade using the same callback bridge as the sync client."""

    def __init__(
        self,
        *,
        session_provider: Callable[[], Awaitable[StreamingSession]],
        refresh_session_provider: Callable[[], Awaitable[StreamingSession]],
        client_factory: Callable[[str, str | None], Any] | None = None,
        subscription_factory: Callable[[str, list[str], list[str]], Any] | None = None,
    ) -> None:
        self._session_provider = session_provider
        self._refresh_session_provider = refresh_session_provider
        self._client_factory = client_factory
        self._subscription_factory = subscription_factory
        self._delegates: list[StreamingClient] = []

    async def aiter_updates(self, subscription: StreamSubscription) -> AsyncIterator[StreamUpdate]:
        """Yield one subscription's updates without blocking the event loop."""
        loop = asyncio.get_running_loop()
        initial_session = await self._session_provider()
        delegate = StreamingClient(
            session_provider=lambda: initial_session,
            refresh_session_provider=lambda: asyncio.run_coroutine_threadsafe(
                self._refresh_session_provider(), loop
            ).result(),
            client_factory=self._client_factory,
            subscription_factory=self._subscription_factory,
        )
        self._delegates.append(delegate)
        try:
            async for update in delegate.aiter_updates(subscription):
                yield update
        finally:
            delegate.close()
            self._delegates.remove(delegate)

    async def close(self) -> None:
        """Close all Lightstreamer delegates created by this async facade."""
        for delegate in tuple(self._delegates):
            delegate.close()
