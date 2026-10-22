"""Planned maintenance and a drained terminal, as the platform serves them since 20-21 Oct:
a 403 that says until when, an order that may be sent again, the two reads that are
always answered, and a terminal that is kept while it holds no cell."""

from __future__ import annotations

import datetime as dt
import json

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import (
    DependencyUnavailableError,
    EdgeError,
    ForbiddenError,
    MaintenanceError,
    UpstreamError,
)
from mfx.results import CommandState, ExecutionResult, Reason

from .conftest import TERMINAL_ID, FakeMfx, page, terminal_body

WINDOW_ID = "0192aaaa-bbbb-7ccc-8ddd-000000000031"
ENDS_AT = "2026-10-22T02:38:00Z"


def _paused(service: str = "order_placement") -> httpx.Response:
    return httpx.Response(
        403,
        json={
            "error": {
                "code": "maintenance",
                "message": "Paused for planned maintenance until 02:38 UTC.",
                "details": {
                    "window_id": WINDOW_ID,
                    "window": "MW-0031",
                    "ends_at": ENDS_AT,
                    "service": service,
                    "suspended": ["order_placement", "market_data"],
                },
            }
        },
    )


async def test_a_maintenance_refusal_names_its_window_and_end_and_an_order_may_be_sent_again(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a maintenance window that suspends order placement and market data for the tenant
    When a read is refused with 403 maintenance, an order is refused the same way, and a command
    queued before the window comes back with the result maintenance
    Then the read raises a MaintenanceError (still a ForbiddenError) naming the window, its label,
    its end as an aware time, the service that refused and every service suspended; the order is a
    result with reason maintenance that is retryable at the window's end; and the queued command's
    result is retryable too, whatever its flag says, because it never ran."""
    mfx.responses.append(_paused("market_data"))
    with pytest.raises(MaintenanceError) as paused:
        await client.terminals.get(TERMINAL_ID)
    said = paused.value
    assert isinstance(said, ForbiddenError) and said.status == 403
    assert (said.code, said.window_id, said.window, said.service) == (
        "maintenance", WINDOW_ID, "MW-0031", "market_data",
    )  # fmt: skip
    assert said.ends_at == dt.datetime(2026, 10, 22, 2, 38, tzinfo=dt.UTC)
    assert said.suspended == ["order_placement", "market_data"]
    assert said.message == "Paused for planned maintenance until 02:38 UTC."

    mfx.responses.append(_paused())
    order = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.10", idempotency_key="o-1"
    )
    assert order.ok is False and order.reason is Reason.MAINTENANCE
    assert order.retryable is True and order.final is True
    assert order.retry_at == dt.datetime(2026, 10, 22, 2, 38, tzinfo=dt.UTC)
    assert order.detail is not None and "02:38" in order.detail

    queued = ExecutionResult.from_command(
        {
            "command_id": "c-1",
            "state": "REJECTED",
            "result": {"ok": False, "reason": "maintenance", "retryable": False, "attempts": 0},
        },
        idempotency_key="o-2",
        client_rtt_ms=1.0,
    )
    assert queued.state is CommandState.REJECTED and queued.reason is Reason.MAINTENANCE
    assert queued.retryable is True, "refused before it ran: nothing reached the broker"

    bare = MaintenanceError("paused", status=403, code="maintenance", details={"suspended": "x"})
    assert (bare.window_id, bare.window, bare.ends_at, bare.service, bare.suspended) == (
        None, None, None, None, [],
    )  # fmt: skip


async def test_a_503_is_told_apart_by_its_code_and_an_edge_page_is_an_edge_error(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given the platform answering 503 upstream_error, 503 dependency_unavailable with
    Retry-After, and the edge in between answering 502 or 504 with a page of its own
    When the caller reads a terminal
    Then upstream_error is an UpstreamError and nothing narrower, dependency_unavailable is a
    DependencyUnavailableError carrying its Retry-After, and each edge page is an EdgeError that
    says it came from the edge; all three are still caught as UpstreamError."""
    body = {"error": {"code": "upstream_error", "message": "no answer", "details": {}}}
    mfx.responses.append(httpx.Response(503, json=body))
    with pytest.raises(UpstreamError) as upstream:
        await client.terminals.get(TERMINAL_ID)
    assert type(upstream.value) is UpstreamError

    body = {"error": {"code": "dependency_unavailable", "message": "store", "details": {}}}
    mfx.responses.append(httpx.Response(503, json=body, headers={"Retry-After": "3"}))
    with pytest.raises(DependencyUnavailableError) as store:
        await client.terminals.get(TERMINAL_ID)
    assert store.value.retry_after_s == 3.0 and store.value.from_edge is False

    for status in (502, 504):
        mfx.responses.append(httpx.Response(status, text="<html>bad gateway</html>"))
        with pytest.raises(EdgeError) as edge:
            await client.terminals.get(TERMINAL_ID)
        assert edge.value.status == status and edge.value.from_edge is True


async def test_a_terminal_is_drained_with_a_reason_and_resumed_and_reads_drained_in_between(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an ACTIVE terminal with positions open
    When it is drained with a reason and confirm_open_positions, read once its cell has stopped it,
    and resumed
    Then the drain sends the reason and the confirmation under its idempotency key and answers
    DRAINING, the read says DRAINED and the terminal is not usable, a drain with no reason sends
    no reason, and the resume is a POST to its own route that answers REQUESTED."""
    from mfx.terminals import is_usable

    mfx.responses.append(httpx.Response(202, json=terminal_body("DRAINING")))
    draining = await client.terminals.drain(
        TERMINAL_ID, reason="month end", confirm_open_positions=True, idempotency_key="d-1"
    )
    request = mfx.last
    assert request.url.path == f"/v1/terminals/{TERMINAL_ID}/drain"
    assert request.headers["Idempotency-Key"] == "d-1"
    assert json.loads(request.content) == {"reason": "month end", "confirm_open_positions": True}
    assert draining.state.value == "DRAINING"

    mfx.responses.append(httpx.Response(200, json=terminal_body("DRAINED")))
    drained = await client.terminals.get(TERMINAL_ID)
    assert drained.state.value == "DRAINED" and not is_usable(drained)

    mfx.responses.append(httpx.Response(202, json=terminal_body("DRAINING")))
    await client.terminals.drain(TERMINAL_ID, idempotency_key="d-2")
    assert json.loads(mfx.last.content) == {"confirm_open_positions": False}

    mfx.responses.append(httpx.Response(202, json=terminal_body("REQUESTED")))
    resumed = await client.terminals.resume(TERMINAL_ID, idempotency_key="r-1")
    assert mfx.last.method == "POST"
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/resume"
    assert mfx.last.headers["Idempotency-Key"] == "r-1"
    assert resumed.state.value == "REQUESTED"


def _window(label: str) -> dict[str, object]:
    return {
        "id": WINDOW_ID,
        "label": label,
        "state": "in_progress",
        "starts_at": "2026-10-22T01:00:00Z",
        "ends_at": ENDS_AT,
        "expected_minutes": 98,
        "started_at": "2026-10-22T01:00:00Z",
        "ended_at": None,
        "message": None,
        "suspended": ["order_placement"],
        "terminals": 2,
        "console": "read_only",
    }


async def test_the_windows_and_a_windows_terminals_are_read_following_the_cursor(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given two pages of maintenance windows and one page of the tenant's terminals in a window
    When the windows are listed by state and the window's terminals are listed
    Then the windows come from GET /maintenance with the state asked for, following the cursor to
    the last page, and the terminals come from the window's own route, each with its state and
    expected time back."""
    mfx.responses.append(page([_window("MW-0031")], "c2"))
    mfx.responses.append(page([_window("MW-0032")], None))
    windows = [w async for w in client.maintenance.list(state="in_progress")]
    assert [w.label for w in windows] == ["MW-0031", "MW-0032"]
    assert windows[0].ends_at == dt.datetime(2026, 10, 22, 2, 38, tzinfo=dt.UTC)
    first, second = mfx.requests[-2:]
    assert first.url.path == "/v1/maintenance" and first.url.params["state"] == "in_progress"
    assert second.url.params["cursor"] == "c2"

    member = {"terminal_id": TERMINAL_ID, "state": "migrating", "since": None, "eta_at": ENDS_AT}
    mfx.responses.append(page([member], None))
    terminals = [t async for t in client.maintenance.terminals(WINDOW_ID, limit=10)]
    assert mfx.last.url.path == f"/v1/maintenance/{WINDOW_ID}/terminals"
    assert mfx.last.url.params["limit"] == "10"
    assert [(str(t.terminal_id), t.state.value) for t in terminals] == [(TERMINAL_ID, "migrating")]
