"""``SyncMfxClient`` — the facade for scripts that are not async.

The interesting assertions here are not "it returns the same thing". They are the two failures a
naive sync wrapper ships with: a fresh event loop per call, which kills the connection pool on the
*second* call, and a silent deadlock when it is used from inside someone's running loop.
"""

from __future__ import annotations

import asyncio
import datetime as dt
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx.errors import NotFoundError
from mfx.secrets import Secret
from mfx.sync import SyncMfxClient

from .conftest import (
    BASE_URL,
    BROKER_ID,
    FARM_ID,
    KEY_ID,
    SERVER_ID,
    TERMINAL_ID,
    FakeMfx,
    accepted,
    error,
    page,
    terminal_body,
)

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.


@pytest.fixture
def sync_client(mfx: FakeMfx, private_key: Ed25519PrivateKey) -> Any:
    client = SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    yield client
    client.close()


def test_a_script_with_no_event_loop_can_use_mfx_and_keep_one_connection_pool(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """Given ordinary synchronous code / When it makes several MFX calls in a row / Then each one
    works, and the second does not fail on a connection pool left behind by the first.

    This is the failure a per-call `anyio.run` ships with: a new event loop each time, a pool
    opened under the first one, and `Event loop is closed` on call two — in a cron job, at 3am.
    One long-lived loop on one worker thread keeps the pool, the retry policy and the budget
    counter intact."""
    mfx.responses.extend(
        [
            accepted("REQUESTED"),
            httpx.Response(200, json=terminal_body("ACTIVE")),
            httpx.Response(200, json=terminal_body("ACTIVE")),
        ]
    )

    created = sync_client.create_terminal(
        farm_id=FARM_ID,
        broker_id=BROKER_ID,
        server_id=SERVER_ID,
        idempotency_key="script-1",
    )
    first = sync_client.get_terminal(TERMINAL_ID)
    second = sync_client.get_terminal(TERMINAL_ID)

    assert created.state.value == "REQUESTED"
    assert first.state.value == second.state.value == "ACTIVE"
    assert len(mfx.requests) == 3, "three calls, one client"
    assert sync_client.budget is not None, "the budget counter survives across calls"


def test_calling_it_from_inside_a_running_loop_is_refused_with_the_remedy(
    sync_client: Any,
) -> None:
    """Waiting on the worker thread would block the caller's own loop and everything else on it.
    The message names the client to use instead, because this is the mistake the facade invites."""

    async def from_inside_a_loop() -> None:
        with pytest.raises(RuntimeError, match="MfxClient and await"):
            sync_client.get_terminal(TERMINAL_ID)

    asyncio.run(from_inside_a_loop())


def test_a_list_is_an_ordinary_iterator_that_follows_the_cursor(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """A script wants `for terminal in mfx.terminals()`. The cursor is followed a page at a time,
    so a script that stops early has not paid for the rest."""
    mfx.responses.extend(
        [
            page([terminal_body("ACTIVE", id="0191f0c2-0000-7000-8000-000000000001")], "cursor-2"),
            page([terminal_body("ACTIVE", id="0191f0c2-0000-7000-8000-000000000002")], None),
        ]
    )

    seen = [str(terminal.id) for terminal in sync_client.terminals()]

    assert seen == [
        "0191f0c2-0000-7000-8000-000000000001",
        "0191f0c2-0000-7000-8000-000000000002",
    ]
    assert mfx.requests[1].url.params.get("cursor") == "cursor-2"


def test_stopping_early_does_not_fetch_the_next_page(sync_client: Any, mfx: FakeMfx) -> None:
    mfx.responses.append(
        page([terminal_body("ACTIVE"), terminal_body("ACTIVE")], "cursor-2"),
    )

    first = next(iter(sync_client.terminals()))

    assert str(first.id) == TERMINAL_ID
    assert len(mfx.requests) == 1, "one page was enough"


def test_reads_raise_the_same_typed_errors_the_async_client_raises(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """The error hierarchy crosses the facade unchanged — a script catches `NotFoundError`, not a
    wrapped `concurrent.futures` exception from the thread the call happened to run on."""
    mfx.responses.append(error(404, "not_found", "no such terminal"))

    with pytest.raises(NotFoundError):
        sync_client.get_terminal(TERMINAL_ID)


def test_execution_returns_a_result_here_too_rather_than_raising(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """Execution never raising does not stop at the facade. A script that treated an exception
    as "it did not happen" would read a refusal as a network fault and retry an order that was
    already filled."""
    mfx.responses.append(error(409, "state_error", "terminal is DRAINING"))

    result = sync_client.place_order(
        TERMINAL_ID,
        symbol="EURUSD.sd",
        side="buy",
        volume="0.10",
        idempotency_key="order-1",
    )

    assert result.ok is False
    assert result.reason is not None


def test_the_whole_execution_surface_is_present_and_none_of_it_raises(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """Every execution method mirrors its async twin, including cancel_order first-class (gap G1)
    and modify_order. A script reconciling orders needs the same verbs the async client
    has, or it reaches past the facade for raw HTTP — which is the thing the SDK exists to stop."""
    command_id = "0191f0c2-0000-7000-8000-0000000000c1"
    mfx.responses.extend(
        httpx.Response(
            202, json={"command_id": command_id, "state": "ACCEPTED", "duplicate": False}
        )
        for _ in range(9)
    )
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "command_id": command_id,
                "terminal_id": TERMINAL_ID,
                "kind": "order_place",
                "state": "ACCEPTED",
                "final": False,
                "created_at": "2026-09-25T09:00:00Z",
                "updated_at": "2026-09-25T09:00:01Z",
                "result": None,
            },
        )
    )

    results = [
        sync_client.cancel_order(TERMINAL_ID, ticket=8811, idempotency_key="k1"),
        sync_client.modify_order(TERMINAL_ID, ticket=8811, price="1.20500", idempotency_key="k1b"),
        sync_client.modify_position(TERMINAL_ID, ticket=8811, sl="1.09", idempotency_key="k2"),
        sync_client.close_position(TERMINAL_ID, ticket=8811, idempotency_key="k3"),
        sync_client.close_position_by(TERMINAL_ID, 8811, 8812, idempotency_key="k3b"),
        sync_client.close_position_partial(
            TERMINAL_ID, ticket=8811, volume="0.05", idempotency_key="k4"
        ),
        sync_client.place_order(
            TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="0.10", idempotency_key="k5"
        ),
        sync_client.set_trailing_stop(TERMINAL_ID, 8811, distance="0.0020", idempotency_key="k6"),
        sync_client.clear_trailing_stop(TERMINAL_ID, 8811, idempotency_key="k7"),
        sync_client.get_command("0191f0c2-0000-7000-8000-0000000000c1"),
    ]

    assert len(results) == 10
    assert all(result.command_id is not None for result in results)
    assert len(mfx.requests) == 10


def test_credentials_and_the_rest_of_the_write_surface_reach_the_wire(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """The sync surface mirrors the async one method for method, so moving a script to async is
    deleting `Sync` and adding `await` rather than relearning the API."""
    mfx.responses.extend(
        [
            httpx.Response(
                202,
                json={
                    "credential_ref_id": "00000000-0000-4000-8000-000000000001",
                    "terminal_id": TERMINAL_ID,
                    "cred_type": "master",
                    "execution_disabled": False,
                    "rotated": False,
                    "takes_effect": "first_login",
                    "operation_id": None,
                },
            ),
            httpx.Response(202, json=terminal_body("DRAINING")),
            httpx.Response(202, json=terminal_body("DRAINING")),
            httpx.Response(202, json=terminal_body("REQUESTED")),
        ]
    )

    sync_client.submit_credentials(
        TERMINAL_ID,
        login=61587349,
        password=Secret("s3cret"),
        server="EquitiSecurities-Demo",
        idempotency_key="cred-1",
    )
    assert sync_client.drain_terminal(TERMINAL_ID, idempotency_key="d-1").state.value == "DRAINING"
    assert sync_client.retire_terminal(TERMINAL_ID, idempotency_key="r-1").state.value == "DRAINING"
    assert (
        sync_client.resume_terminal(TERMINAL_ID, idempotency_key="u-1").state.value == "REQUESTED"
    )
    assert [r.method for r in mfx.requests] == ["POST", "POST", "DELETE", "POST"]


def test_the_read_surface_is_all_here(sync_client: Any, mfx: FakeMfx) -> None:
    """Catalogue, account and usage, so a reconciliation script never needs the async client."""
    symbol_body = {
        "symbol": "EURUSD.sd",
        "description": "Euro vs US Dollar",
        "server_id": BROKER_ID,
        "account_type": "sd",
        "digits": 5,
        "contract_size": "100000",
        "volume_min": "0.01",
        "volume_max": "100",
        "volume_step": "0.01",
        "trade_mode": "full",
        "margin_currency": "USD",
        "pip_value_per_lot": None,
        "spec_hash": "b3f1",
        "trade_sessions": [],
        "refreshed_at": "2026-09-25T09:00:00Z",
        "status": {
            "state": "open",
            "reason": None,
            "since": "2026-09-25T08:00:00Z",
            "next_open": None,
            "last_tick_age_s": 0.4,
            "quote_watched": True,
            "as_of": "2026-09-25T09:00:00Z",
        },
    }
    mfx.responses.extend(
        [
            page(
                [{"id": BROKER_ID, "code": "equiti", "display_name": "Equiti", "status": "active"}],
                None,
            ),
            page(
                [
                    {
                        "id": BROKER_ID,
                        "server_name": "EquitiSecurities-Demo",
                        "kind": "demo",
                        "enabled": True,
                        "disabled_reason": None,
                    }
                ],
                None,
            ),
            page([symbol_body], None),
            httpx.Response(200, json=symbol_body),
            httpx.Response(
                200,
                json={
                    "symbol": "EURUSD.sd",
                    "server_id": BROKER_ID,
                    "account_type": "sd",
                    "bid": "1.09431",
                    "ask": "1.09445",
                    "tick_time": "2026-09-25T09:59:59Z",
                    "broker_time": "2026-09-25 12:59:59",
                    "age_s": 0.8,
                    "state": "open",
                },
            ),
            httpx.Response(
                200,
                json={
                    "terminal_id": TERMINAL_ID,
                    "snapshot": None,
                    "profile": None,
                    "stale": True,
                },
            ),
            httpx.Response(200, json={"as_of": "2026-09-25T10:00:00Z", "stale": True, "items": []}),
            httpx.Response(200, json={"as_of": "2026-09-25T10:00:00Z", "stale": True, "items": []}),
            page([], None),
            httpx.Response(
                200,
                json={"terminal_id": TERMINAL_ID, "as_of": "2026-09-25T10:00:00Z", "items": []},
            ),
            httpx.Response(
                200,
                json={
                    "items": [],
                    "limits": {"commands_per_s": 5, "md_msgs_per_s": None, "ws_conns": 2},
                    "budget_remaining": 900,
                    "budget_source": "configured",
                    "as_of": "2026-09-25T10:00:00Z",
                },
            ),
        ]
    )

    assert [b.code for b in sync_client.brokers()] == ["equiti"]
    assert [s.server_name for s in sync_client.servers(BROKER_ID)] == ["EquitiSecurities-Demo"]
    assert [s.symbol for s in sync_client.symbols(BROKER_ID)] == ["EURUSD.sd"]
    assert sync_client.symbol(BROKER_ID, "EURUSD.sd").digits == 5
    assert sync_client.quote(BROKER_ID, "EURUSD.sd").age_s == 0.8
    account = sync_client.account(TERMINAL_ID)
    assert account.snapshot is None
    assert account.stale is True, "nothing has arrived from the cell, and the answer says so"
    assert sync_client.positions(TERMINAL_ID).items == []
    assert sync_client.pending_orders(TERMINAL_ID).items == []
    window = dt.datetime(2026, 9, 24, tzinfo=dt.UTC), dt.datetime(2026, 9, 25, tzinfo=dt.UTC)
    assert list(sync_client.deals(TERMINAL_ID, from_=window[0], to=window[1])) == []
    assert sync_client.spread(TERMINAL_ID).items == []
    assert sync_client.usage().budget_remaining == 900


def test_closing_is_idempotent_and_a_closed_client_says_so(
    mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """A script exiting must not hang on a worker thread, and a call after close must name the
    reason rather than blocking forever on a stopped loop."""
    client = SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    with client:
        pass
    client.close()  # twice is harmless

    with pytest.raises(RuntimeError, match="closed"):
        client.get_terminal(TERMINAL_ID)


def test_it_names_itself_usefully(sync_client: Any) -> None:
    assert repr(sync_client).startswith("SyncMfxClient(MfxClient(")


def test_a_script_reads_bars_and_ticks_without_an_event_loop(
    sync_client: Any, mfx: FakeMfx
) -> None:
    """Given ordinary synchronous code that backfills a chart
    When it reads a window of bars and a page of ticks
    Then each is the one call the async client makes, to the same path with the same parameters,
    and the answer comes back as the same model: a script that fetches history is the plainest use
    of the sync client, and it should not have to reach past it for raw HTTP."""
    import datetime as dt

    start = dt.datetime(2026, 10, 13, 9, 0, tzinfo=dt.UTC)
    mfx.responses.extend(
        [
            httpx.Response(200, json={"items": []}),
            httpx.Response(200, json={"items": [], "more": False}),
        ]
    )

    bars = sync_client.candles(
        BROKER_ID, "EURUSD.sd", "H1", from_=start, to=start + dt.timedelta(hours=1)
    )
    ticks = sync_client.ticks(BROKER_ID, "EURUSD.sd", from_=start, limit=50)

    assert bars.items == [] and (ticks.items, ticks.more) == ([], False)
    assert [r.url.path for r in mfx.requests] == ["/v1/md/candles", "/v1/md/ticks"]
    assert mfx.requests[0].url.params["tf"] == "H1"
    assert mfx.requests[1].url.params["limit"] == "50"
