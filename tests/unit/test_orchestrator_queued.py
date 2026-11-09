"""The terminal orchestrator as a tenant meets it: QUEUED, the queued restart and bulk actions.

A cell starts terminals a few at a time, so a terminal or an operation can wait its turn in QUEUED.
These assert what goes on the wire and how the SDK waits, because a client that polls a queue
every two seconds only adds load to the thing it is waiting for.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

import httpx
import pytest

from mfx import terminals as terminals_module
from mfx.client import MfxClient
from mfx.terminals import ON_ITS_WAY, bulk_ask, next_wait_s

from .conftest import BROKER_ID, FARM_ID, TERMINAL_ID, FakeMfx, body_of, terminal_body

#: The Story these cases are Tested By: the terminal orchestrator.

BULK_ID = "4d2d3e4f-5a6b-7c8d-9e0f-102030405060"
OP_ID = "5d2d3e4f-5a6b-7c8d-9e0f-102030405060"
NOW = dt.datetime(2026, 11, 10, 6, 0, 0, tzinfo=dt.UTC)


def _queued(expected: str | None, position: int | None = 3) -> dict[str, Any]:
    return terminal_body(
        "QUEUED",
        queue={
            "queued_at": "2026-11-10T05:59:00Z",
            "position": position,
            "expected_start_at": expected,
            "reason": "cell_busy",
        },
    )


def _bulk(state: str = "RUNNING", **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": BULK_ID,
        "kind": "restart",
        "state": state,
        "requested_by": "tenant",
        "reason": "broker maintenance done",
        "requested_n": 3,
        "accepted_n": 2,
        "refused_n": 1,
        "refused": [{"terminal_id": TERMINAL_ID, "code": "positions_open"}],
        "counts": {"queued": 2, "running": 0, "succeeded": 0, "failed": 0, "cancelled": 0},
        "expected_finish_at": "2026-11-10T06:04:00Z",
        "late": False,
        "created_at": "2026-11-10T06:00:00Z",
        "finished_at": None,
    }
    body.update(overrides)
    return body


async def test_a_queued_terminal_is_waited_on_at_its_expected_start_not_on_a_fixed_beat(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Given a terminal QUEUED behind its cell's other starts, then LOGGING_IN, then ACTIVE / When
    the tenant waits until it is active / Then the SDK reads it again at the queue's expected start
    (clamped to between 2 s and a minute), backs off 2 s doubling for any other state on its way,
    and returns the first settled read; a restart asks to be queued unless told otherwise.

    A cell starts terminals a few at a time, so asking every two seconds tells nothing new and adds
    load to the cell being waited on."""
    monkeypatch.setattr(terminals_module, "_now", lambda: NOW)
    mfx.responses += [
        httpx.Response(200, json=_queued("2026-11-10T06:00:40Z")),
        httpx.Response(200, json=_queued("2026-11-10T06:30:00Z")),
        httpx.Response(200, json=_queued("2026-11-10T05:00:00Z")),
        httpx.Response(200, json=_queued(None, position=None)),
        httpx.Response(200, json=terminal_body("LOGGING_IN")),
        httpx.Response(200, json=terminal_body("ACTIVE")),
    ]

    terminal = await client.terminals.wait_until_active(TERMINAL_ID)

    assert terminal.state.value == "ACTIVE"
    # 40 s to the expected start; capped at 60; a start already past is 2; then backoff 16, 15.
    assert sleeps == [40.0, 60.0, 2.0, 15.0, 15.0]
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}"
    assert {"REQUESTED", "QUEUED", "PROVISIONING", "LOGGING_IN"} == ON_ITS_WAY

    mfx.responses.append(httpx.Response(200, json=_queued("2026-11-10T06:10:00Z")))
    mfx.responses.append(httpx.Response(200, json=_queued("2026-11-10T06:10:00Z")))
    late = await client.terminals.wait_until_active(TERMINAL_ID, timeout_s=5)
    assert late.state.value == "QUEUED" and sleeps[-1] == 5.0
    with pytest.raises(ValueError, match="timeout_s"):
        await client.terminals.wait_until_active(TERMINAL_ID, timeout_s=-1)

    naive = terminal_body("QUEUED")
    naive["queue"] = {"queued_at": "2026-11-10T05:59:00Z", "position": 1,
                      "expected_start_at": "2026-11-10T06:00:10", "reason": None}  # fmt: skip
    from mfx._generated.models.tenant_terminal import TenantTerminal  # noqa: PLC0415

    assert next_wait_s(TenantTerminal.from_dict(naive), 2.0, NOW) == 10.0

    mfx.responses.append(httpx.Response(202, json={"operation_id": OP_ID, "state": "QUEUED"}))
    accepted = await client.terminals.restart(TERMINAL_ID, reason="stuck", idempotency_key="r-1")
    assert body_of(mfx.last)["queue"] is True and accepted.state.value == "QUEUED"
    mfx.responses.append(httpx.Response(202, json={"operation_id": OP_ID, "state": "ACCEPTED"}))
    await client.terminals.restart(TERMINAL_ID, reason="stuck", idempotency_key="r-2", queue=False)
    assert body_of(mfx.last)["queue"] is False


async def test_a_bulk_restart_or_retire_goes_to_the_colon_route_and_reads_back_its_progress(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant restarting a farm's terminals, then retiring a list of them / When it asks,
    reads the action and cancels it / Then each is one call to the route as the contract names it
    (``/v1/terminals:restart``, colon and all, under the base path), carrying the idempotency key,
    and the answer is the action with what was refused and its expected finish."""
    mfx.responses.append(httpx.Response(202, json=_bulk()))
    action = await client.terminals.bulk_restart(
        farm_id=FARM_ID, reason="broker maintenance done", idempotency_key="b-1"
    )
    assert (mfx.last.method, mfx.last.url.path) == ("POST", "/v1/terminals:restart")
    assert mfx.last.headers["Idempotency-Key"] == "b-1"
    assert body_of(mfx.last) == {"reason": "broker maintenance done", "farm_id": FARM_ID,
                                 "confirm_open_positions": False}  # fmt: skip
    assert action.refused[0].code == "positions_open" and action.counts.queued == 2

    mfx.responses.append(httpx.Response(202, json=_bulk(kind="retire")))
    await client.terminals.bulk_retire(
        terminal_ids=[TERMINAL_ID],
        broker_id=BROKER_ID,
        reason="done with them",
        idempotency_key="b-2",
        confirm_open_positions=True,
    )
    assert mfx.last.url.path == "/v1/terminals:retire"
    assert body_of(mfx.last) == {"reason": "done with them", "broker_id": BROKER_ID,
                                 "terminal_ids": [TERMINAL_ID],
                                 "confirm_open_positions": True}  # fmt: skip

    mfx.responses.append(httpx.Response(200, json=_bulk("DONE")))
    read = await client.terminals.get_bulk_action(BULK_ID)
    assert (mfx.last.method, mfx.last.url.path) == ("GET", f"/v1/bulk-actions/{BULK_ID}")
    assert read.state.value == "DONE"

    mfx.responses.append(httpx.Response(200, json=_bulk("CANCELLED")))
    cancelled = await client.terminals.cancel_bulk_action(BULK_ID, idempotency_key="c-1")
    assert (mfx.last.method, mfx.last.url.path) == ("POST", f"/v1/bulk-actions/{BULK_ID}/cancel")
    assert mfx.last.headers["Idempotency-Key"] == "c-1"
    assert cancelled.state.value == "CANCELLED"


@pytest.mark.parametrize(
    ("ask", "message"),
    [
        ({"reason": "", "farm_id": FARM_ID}, "reason is 1 to 500"),
        ({"reason": "   ", "farm_id": FARM_ID}, "reason is 1 to 500"),
        ({"reason": "x" * 501, "farm_id": FARM_ID}, "reason is 1 to 500"),
        ({"reason": "why"}, "names farm_id, broker_id or terminal_ids"),
        ({"reason": "why", "terminal_ids": [TERMINAL_ID] * 1001}, "at most 1000"),
    ],
    ids=["empty-reason", "blank-reason", "long-reason", "no-filter", "too-many-ids"],
)
def test_a_bulk_ask_the_platform_would_refuse_is_refused_at_the_call(
    ask: dict[str, Any], message: str
) -> None:
    """Given a bulk ask with no reason, a reason over 500 characters, no filter, or over 1000 ids /
    When it is built / Then it is a ValueError naming the rule, before any request goes out."""
    full = {"farm_id": None, "broker_id": None, "terminal_ids": None,
            "confirm_open_positions": False, **ask}  # fmt: skip
    with pytest.raises(ValueError, match=message):
        bulk_ask(**full)
