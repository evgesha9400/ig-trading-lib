from __future__ import annotations

import inspect
import re
from types import UnionType
from typing import get_args, get_origin, get_type_hints
from urllib.parse import quote

import httpx
import pytest

from ig_trading_lib import (
    IG,
    AsyncIG,
    Environment,
    IGConfig,
    LiveTradingPermissionError,
    OAuthCredentials,
    SessionCredentials,
)
from ig_trading_lib._protocol.manifest import (
    OPERATION_MANIFEST,
    PUBLIC_OPERATION_MANIFEST,
    SOURCE_EXCLUSIONS,
)
from ig_trading_lib.models import IGModel, IGRequest
from ig_trading_lib.operations.dealing import CreatePositionRequest


def _config(environment: Environment = Environment.DEMO) -> IGConfig:
    return IGConfig(
        environment=environment,
        credentials=SessionCredentials(api_key="key", identifier="user", password="pass"),
    )


EXPECTED_NAMESPACES = {
    "accounts",
    "activity",
    "applications",
    "categories",
    "client_sentiment",
    "confirmations",
    "indicative_costs",
    "markets",
    "positions",
    "prices",
    "repeat_dealing_window",
    "session",
    "streaming",
    "transactions",
    "watchlists",
    "working_orders",
}

TRANSPORT_MANAGED_OPERATION_IDS = {
    "session.create",
    "session.refresh_token",
}


def test_manifest_is_the_complete_source_evidence_and_protocol_boundary() -> None:
    assert len(OPERATION_MANIFEST) >= 50
    assert SOURCE_EXCLUSIONS
    assert {spec.operation_id for spec in OPERATION_MANIFEST.values()} == set(OPERATION_MANIFEST)
    for spec in OPERATION_MANIFEST.values():
        assert spec.path.startswith("/")
        assert spec.version in {1, 2, 3, 4}
        assert spec.evidence.url == "https://labs.ig.com/rest-trading-api-reference.html"
        assert spec.evidence.retrieved_on == "2026-08-09"
        assert len(spec.evidence.sha256) == 64
        assert spec.schema_provenance


def test_protocol_versions_are_private_including_authentication() -> None:
    assert "version" not in inspect.signature(SessionCredentials).parameters
    assert "version" not in inspect.signature(OAuthCredentials).parameters


def test_transport_manages_authentication_without_duplicate_public_operations() -> None:
    assert set(PUBLIC_OPERATION_MANIFEST) == (
        set(OPERATION_MANIFEST) - TRANSPORT_MANAGED_OPERATION_IDS
    )
    assert all(
        not OPERATION_MANIFEST[operation_id].public
        for operation_id in TRANSPORT_MANAGED_OPERATION_IDS
    )
    assert any("authentication lifecycle" in exclusion for exclusion in SOURCE_EXCLUSIONS)

    root = IG(_config())
    try:
        assert not hasattr(root.operations.session, "create")
        assert not hasattr(root.operations.session, "refresh_token")
        assert hasattr(root.operations.session, "delete")
    finally:
        root.close()


def test_logout_clears_local_authentication_and_accepts_an_empty_response() -> None:
    session_creations = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal session_creations
        if request.method == "POST" and request.url.path == "/gateway/deal/session":
            session_creations += 1
            return httpx.Response(
                200,
                headers={"CST": f"cst-{session_creations}", "X-SECURITY-TOKEN": "security"},
            )
        if request.method == "DELETE" and request.url.path == "/gateway/deal/session":
            return httpx.Response(200)
        return httpx.Response(200, json={"markets": []})

    root = IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    try:
        root.operations.session.delete()
        root.operations.markets.search("EURUSD")
    finally:
        root.close()

    assert session_creations == 2


def test_roots_expose_exactly_two_layers_with_symmetric_operation_namespaces() -> None:
    sync = IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(lambda _: None)))
    async_root = AsyncIG(_config())
    try:
        assert set(vars(sync)) >= {"operations", "workflows"}
        assert set(sync.operations.__dataclass_fields__) == EXPECTED_NAMESPACES
        assert set(async_root.operations.__dataclass_fields__) == EXPECTED_NAMESPACES
        assert set(sync.workflows.__dataclass_fields__) == set(
            async_root.workflows.__dataclass_fields__
        )
        assert not hasattr(sync, "v1")
        assert not hasattr(sync.operations, "request")
    finally:
        sync.close()


def test_every_mutation_uses_one_live_permission_boundary_before_network_io() -> None:
    called = False

    def reject_network(_: httpx.Request) -> httpx.Response:
        nonlocal called
        called = True
        return httpx.Response(200, json={"dealReference": "should-not-run"})

    root = IG(
        _config(Environment.LIVE),
        http_client=httpx.Client(transport=httpx.MockTransport(reject_network)),
    )
    try:
        with pytest.raises(LiveTradingPermissionError):
            root.operations.positions.create(
                CreatePositionRequest(
                    epic="CS.D.EURUSD.CFD.IP",
                    direction="BUY",
                    size=1,
                    order_type="MARKET",
                    currency_code="GBP",
                )
            )
        assert called is False
    finally:
        root.close()


def test_sync_and_async_public_methods_have_matching_parameters() -> None:
    sync_root = IG(_config())
    async_root = AsyncIG(_config())
    try:
        for namespace in EXPECTED_NAMESPACES - {"streaming"}:
            sync_service = getattr(sync_root.operations, namespace)
            async_service = getattr(async_root.operations, namespace)
            sync_methods = {
                name
                for name, value in inspect.getmembers(sync_service, inspect.ismethod)
                if not name.startswith("_")
            }
            async_methods = {
                name
                for name, value in inspect.getmembers(async_service, inspect.ismethod)
                if not name.startswith("_")
            }
            assert sync_methods == async_methods
            for method in sync_methods:
                assert inspect.signature(getattr(sync_service, method)) == inspect.signature(
                    getattr(async_service, method)
                )
    finally:
        sync_root.close()


class _SyncRecorder:
    def __init__(self) -> None:
        self.operation_ids: set[str] = set()

    def execute(self, operation_id: str, *_: object, **__: object) -> object:
        self.operation_ids.add(operation_id)
        return object()


class _AsyncRecorder:
    def __init__(self) -> None:
        self.operation_ids: set[str] = set()

    async def execute(self, operation_id: str, *_: object, **__: object) -> object:
        self.operation_ids.add(operation_id)
        return object()


def _required_arguments(method: object) -> list[object]:
    signature = inspect.signature(method)
    hints = get_type_hints(method)
    arguments: list[object] = []
    for parameter in signature.parameters.values():
        if parameter.default is not inspect.Parameter.empty:
            continue
        annotation = hints.get(parameter.name)
        if inspect.isclass(annotation) and issubclass(annotation, IGRequest):
            arguments.append(annotation.model_construct())
            continue
        if get_origin(annotation) is tuple:
            arguments.append(("value",))
            continue
        arguments.append(1 if parameter.name in {"num_points"} else "value")
    return arguments


def test_every_sync_operation_method_binds_to_the_manifest() -> None:
    root = IG(_config())
    recorder = _SyncRecorder()
    try:
        for namespace in EXPECTED_NAMESPACES - {"streaming"}:
            service = getattr(root.operations, namespace).__class__(recorder)
            for name, method in inspect.getmembers(service, inspect.ismethod):
                if name.startswith("_"):
                    continue
                method(*_required_arguments(method))
        assert recorder.operation_ids == set(PUBLIC_OPERATION_MANIFEST)
    finally:
        root.close()


@pytest.mark.asyncio
async def test_every_async_operation_method_binds_to_the_same_manifest() -> None:
    root = AsyncIG(_config())
    recorder = _AsyncRecorder()
    for namespace in EXPECTED_NAMESPACES - {"streaming"}:
        service = getattr(root.operations, namespace).__class__(recorder)
        for name, method in inspect.getmembers(service, inspect.ismethod):
            if name.startswith("_"):
                continue
            await method(*_required_arguments(method))
    assert recorder.operation_ids == set(PUBLIC_OPERATION_MANIFEST)
    await root.close()


def test_every_sync_operation_reaches_its_manifest_bound_wire_contract() -> None:
    payload: dict[str, object] = {}
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/gateway/deal/session":
            return httpx.Response(
                200,
                headers={"CST": "cst", "X-SECURITY-TOKEN": "security"},
            )
        requests.append(request)
        return httpx.Response(200, json=payload)

    root = IG(_config(), http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    try:
        for namespace in EXPECTED_NAMESPACES - {"streaming"}:
            service = getattr(root.operations, namespace)
            for name, method in inspect.getmembers(service, inspect.ismethod):
                if name.startswith("_"):
                    continue
                operation_id = _operation_id(namespace, name)
                spec = PUBLIC_OPERATION_MANIFEST[operation_id]
                response_type = get_type_hints(method)["return"]
                payload = _required_payload(response_type)
                arguments = _required_arguments(method)

                method(*arguments)

                request = requests[-1]
                assert request.method == spec.method
                assert request.headers["Version"] == str(spec.version)
                assert request.url.path == f"/gateway/deal{_expected_path(spec.path, arguments)}"
                if request.content:
                    request.read()
    finally:
        root.close()

    assert len(requests) == len(PUBLIC_OPERATION_MANIFEST)


def _operation_id(namespace: str, method_name: str) -> str:
    expected = {
        operation_id
        for operation_id in PUBLIC_OPERATION_MANIFEST
        if operation_id.startswith(f"{namespace}.") and operation_id.endswith(f".{method_name}")
    }
    assert len(expected) == 1
    return expected.pop()


def _required_payload(model_type: type[IGModel]) -> dict[str, object]:
    return {
        name: _sample_value(field.annotation)
        for name, field in model_type.model_fields.items()
        if field.is_required()
    }


def _sample_value(annotation: object) -> object:
    origin = get_origin(annotation)
    if origin in (tuple, list):
        return []
    if origin is UnionType:
        return _sample_value(next(item for item in get_args(annotation) if item is not type(None)))
    if inspect.isclass(annotation) and issubclass(annotation, IGModel):
        return _required_payload(annotation)
    if annotation is str:
        return "value"
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is bool:
        return False
    raise AssertionError(f"No sample value for {annotation!r}")


def _expected_path(template: str, arguments: list[object]) -> str:
    values = iter(arguments)
    return re.sub(r"\{[^}]+\}", lambda _: quote(str(next(values)), safe=""), template)
