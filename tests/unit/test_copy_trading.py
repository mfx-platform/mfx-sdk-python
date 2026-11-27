"""``client.copy`` — Copy Trading over ``/v1/copy/*``, and the ``copy.*`` events.

These assert what goes on the wire (the path, the body in the contract's names, the
Idempotency-Key on every write and on nothing else, each filter in the form the platform reads)
and that nothing is sent when an argument is wrong.
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Iterator
from decimal import Decimal
from typing import Any
from uuid import UUID

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import mfx
from mfx._generated.models.copy_follower_state import CopyFollowerState
from mfx._generated.models.copy_leader_state import CopyLeaderState
from mfx._generated.models.copy_reason import CopyReason
from mfx.client import MfxClient
from mfx.copy_trading import REFUSAL_REASONS, CopyPage
from mfx.errors import ConflictError, RiskRefusal, StateError, ValidationError
from mfx.events import (
    CopyClosedEvent,
    CopyCopied,
    CopyDrift,
    CopyRefused,
    CopyStateChanged,
    CopyStopoutEvent,
    event_of,
)
from mfx.streaming import StreamMessage
from mfx.sync import SyncMfxClient

from .conftest import BASE_URL, KEY_ID, FakeMfx, body_of, error

ACCOUNT = "4c2d3e4f-5a6b-7c8d-9e0f-102030405060"
FOLLOWER_ACCOUNT = "4c2d3e4f-5a6b-7c8d-9e0f-102030405061"
LEADER = "06abfa00-0000-7000-8000-0000000000c1"
FOLLOWER = "06abfa00-0000-7000-8000-0000000000f1"
GROUP = "06abfa00-0000-7000-8000-0000000000e1"
SIGNAL = "06abfa00-0000-7000-8000-0000000000d1"
STOPOUT = "06abfa00-0000-7000-8000-0000000000b1"
COMMAND = "0191f0c2-bbbb-7ccc-8ddd-000000000001"
AT = "2026-11-13T09:00:00Z"


def leader(state: str = "active", **more: Any) -> dict[str, Any]:
    return {
        "id": LEADER,
        "source": "account",
        "account_id": ACCOUNT,
        "venue": "mt5",
        "filters": {"symbols": [], "tag": None, "side": "both"},
        "copies": {},
        "signal_lifetime_s": 30,
        "limits": {},
        "who_may_join": {"accounts": "any"},
        "state": state,
        "followers_live": 0,
        "created_at": AT,
        "updated_at": AT,
        **more,
    }


def follower(state: str = "copying", follower_id: str = FOLLOWER, **more: Any) -> dict[str, Any]:
    return {
        "id": follower_id,
        "account_id": FOLLOWER_ACCOUNT,
        "venue": "ctrader",
        "leader_id": LEADER,
        "scaling": {"mode": "fixed_multiplier", "multiplier": "0.5"},
        "bounds": {},
        "symbol_map": {},
        "options": {},
        "risk_limits": {},
        "close_on_stopout": False,
        "group_id": None,
        "mandate_version": 1,
        "state": state,
        "stopouts": [],
        "created_at": AT,
        "updated_at": AT,
        **more,
    }


def group(state: str = "active") -> dict[str, Any]:
    return {
        "id": GROUP,
        "name": "Desk A",
        "template": {},
        "gross_exposure_cap": None,
        "placement_policy": None,
        "state": state,
        "followers_live": 2,
        "created_at": AT,
        "updated_at": AT,
    }


def stopout(state: str = "active") -> dict[str, Any]:
    return {
        "id": STOPOUT,
        "follower_id": FOLLOWER,
        "limit": "daily",
        "used": "5.2",
        "period_start": AT,
        "period_end": None,
        "closed": [],
        "state": state,
        "reset": None,
        "created_at": AT,
    }


def log_row(reason: str | None = "mapping", outcome: str = "refused") -> dict[str, Any]:
    return {
        "id": "06abfa00-0000-7000-8000-0000000000a9",
        "created_at": AT,
        "signal_id": SIGNAL,
        "leader_id": LEADER,
        "follower_id": FOLLOWER,
        "account_id": FOLLOWER_ACCOUNT,
        "venue": "ctrader",
        "action": "open",
        "side": "buy",
        "instrument_key": "fx:EURUSD",
        "outcome": outcome,
        "reason": reason,
        "venue_code": None,
        "command_id": None,
        "copied_volume": None,
        "price": None,
        "slippage": None,
        "stages": {"detect_ms": 2.5},
        "mfx_ms": 11.0,
        "signal_to_order_ms": 14.0,
        "deal": {
            "action": "open",
            "side": "buy",
            "units": "100000",
            "price": "1.0850",
            "instrument_key": "fx:EURUSD",
        },
        "symbol": "EURUSD" if reason is None else None,
        "risk": None,
    }


LEADER_STATS = {"leaders": 2, "active": 1, "paused": 1, "retired": 0}
FOLLOWER_STATS = {"followers": 1, "copying": 1, "paused": 0, "stopped_out": 0, "unfollowed": 0}
GROUP_STATS = {"groups": 1, "active": 1, "paused": 0}
LOG_STATS = {
    "copies": 3,
    "filled": 1,
    "refused": 2,
    "skipped": 0,
    "stopout": 0,
    "mfx_ms_p50": 11.0,
    "mfx_ms_p99": 40.0,
    "signal_to_order_ms_p50": 14.0,
    "broker_ms_p50": None,
    "mfx_ms_p95": 30.0,
    "signal_to_order_ms_p95": 35.0,
    "broker_ms_p95": None,
}


def copy_page(
    items: list[dict[str, Any]], next_cursor: str | None, stats: dict[str, Any] | None = None
) -> httpx.Response:
    body: dict[str, Any] = {"items": items, "next_cursor": next_cursor, "returned": len(items)}
    if stats is not None:
        body["stats"] = stats
    return httpx.Response(200, json=body)


def accepted(duplicate: bool = False, your_id: str = "s-1") -> dict[str, Any]:
    return {
        "signal_id": SIGNAL,
        "id": your_id,
        "leader_id": LEADER,
        "duplicate": duplicate,
        "iat": AT,
        "exp": "2026-11-13T09:00:30Z",
    }


def preview() -> dict[str, Any]:
    return {
        "account_id": FOLLOWER_ACCOUNT,
        "venue": "ctrader",
        "leader_id": LEADER,
        "refusal": None,
        "inputs": {
            "leader_currency": "USD",
            "follower_currency": "USD",
            "rate": None,
            "leader_balance": "10000",
            "leader_equity": "10000",
            "follower_balance": "5000",
            "follower_equity": "5000",
            "read_at": AT,
        },
        "rows": [
            {
                "leader_symbol": "EURUSD",
                "leader_volume": "1.00",
                "instrument_key": "fx:EURUSD",
                "follower_symbol": "EURUSD",
                "matched_by": "same_name",
                "follower_volume": "50000",
                "reason": None,
                "leader_contract_size": "100000",
                "follower_contract_size": "100000",
                "follower_volume_unit": "units",
            },
            {
                "leader_symbol": "US30",
                "leader_volume": "1.00",
                "instrument_key": None,
                "follower_symbol": None,
                "matched_by": None,
                "follower_volume": None,
                "reason": "mapping",
                "leader_contract_size": "1",
                "follower_contract_size": None,
                "follower_volume_unit": None,
            },
        ],
    }


CLOSE = "06abfa00-0000-7000-8000-0000000000a1"
BATCH = "06abfa00-0000-7000-8000-0000000000a2"
CLOSE_STATS = {"pending": 1, "done": 1, "incomplete": 0, "superseded": 0}
SIGNAL_STATS = {"signals": 1, "fill": 1, "external": 0}
STOPOUT_STATS = {"stopouts": 1, "active": 1, "reset": 0, "expired": 0}


def close_row(state: str = "pending") -> dict[str, Any]:
    return {
        "id": CLOSE,
        "follower_id": FOLLOWER,
        "leader_id": LEADER,
        "account_id": FOLLOWER_ACCOUNT,
        "group_id": GROUP,
        "batch_id": BATCH,
        "cause": "group_close",
        "reason": "desk closing",
        "cutoff_at": AT,
        "requested_by": "key:k-1",
        "attempt": 1,
        "next_attempt_at": None,
        "state": state,
        "created_at": AT,
        "finished_at": None,
        "entries": [
            {
                "position_id": None,
                "leader_position_ref": "L-1",
                "symbol": "EURUSD",
                "volume": "50000",
                "state": "not_closed",
                "why": "netting",
                "cut": False,
                "closed_volume": "0",
                "attempts": [
                    {
                        "close_id": CLOSE,
                        "attempt": 1,
                        "command_id": None,
                        "outcome": "refused",
                        "reason": "market_closed",
                        "venue_code": None,
                        "volume_closed": None,
                        "volume_after": "50000",
                        "at": AT,
                    }
                ],
            }
        ],
    }


def signal_row() -> dict[str, Any]:
    return {
        "id": SIGNAL,
        "leader_id": LEADER,
        "kind": "fill",
        "action": "open",
        "side": "buy",
        "volume_units": "100000",
        "price": "1.0850",
        "sl": None,
        "tp": None,
        "instrument_key": "fx:EURUSD",
        "leader_currency": "USD",
        "source_id": None,
        "iat": AT,
        "exp": "2026-11-13T09:00:30Z",
        "created_at": AT,
        "outcomes": {"filled": 2, "refused": 1, "skipped": 0},
    }


def members(*outcomes: tuple[str, str, str | None]) -> dict[str, Any]:
    return {
        "results": [
            {"follower_id": fid, "outcome": outcome, "reason": reason}
            for fid, outcome, reason in outcomes
        ]
    }


def ok(body: dict[str, Any], status: int = 200) -> httpx.Response:
    return httpx.Response(status, json=body)


def key_of(request: httpx.Request) -> str | None:
    value = request.headers.get("Idempotency-Key")
    return None if value is None else str(value)


async def test_a_leader_is_made_read_listed_changed_paused_resumed_and_retired(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an account the tenant wants to lead, and a second leader that is over the plan /
    When the SDK creates the leader, reads it, lists leaders across two pages with a state filter,
    changes it, pauses, resumes and retires it, and creates the second / Then each call is the
    contract's route with the body in the contract's names and the Idempotency-Key on every write
    and on no read; the list sends its states comma-separated and keeps the stats row; retire
    sends close_copied and the reason; and the plan's refusal is a ConflictError
    (quota_exceeded) sent once, never retried."""
    mfx.responses.extend(
        [
            ok(leader(), 201),
            ok(leader()),
            copy_page([leader()], "c2", LEADER_STATS),
            copy_page([leader("paused")], None, LEADER_STATS),
            ok(leader(signal_lifetime_s=60)),
            ok(leader("paused")),
            ok(leader()),
            ok(leader("retired")),
            httpx.Response(
                409,
                json={
                    "error": {
                        "code": "quota_exceeded",
                        "message": "over the plan",
                        "details": {"reason": "plan_limit", "limit": "copy_leaders"},
                    }
                },
            ),
        ]
    )
    made = await client.copy.create_leader(
        source="account",
        account_id=ACCOUNT,
        signal_lifetime_s=30,
        filters={"symbols": ["EURUSD"], "side": "buy"},
        copies={"pending": False},
        limits={"max_risk_pct": Decimal("2.5")},
        who_may_join={"accounts": "listed", "account_ids": [UUID(FOLLOWER_ACCOUNT)]},
        idempotency_key="lead-1",
    )
    assert made.state is CopyLeaderState.ACTIVE
    create = mfx.requests[0]
    assert (create.method, create.url.path) == ("POST", "/v1/copy/leaders")
    assert key_of(create) == "lead-1"
    assert body_of(create) == {
        "source": "account",
        "account_id": ACCOUNT,
        "signal_lifetime_s": 30,
        "filters": {"symbols": ["EURUSD"], "side": "buy"},
        "copies": {"pending": False},
        "limits": {"max_risk_pct": "2.5"},
        "who_may_join": {"accounts": "listed", "account_ids": [FOLLOWER_ACCOUNT]},
    }

    got = await client.copy.get_leader(LEADER)
    assert str(got.id) == LEADER
    assert mfx.requests[1].url.path == f"/v1/copy/leaders/{LEADER}"
    assert key_of(mfx.requests[1]) is None

    ids = [
        str(each.id)
        async for each in client.copy.all_leaders(
            state=["active", "paused"], source="account", account_id=ACCOUNT, limit=1
        )
    ]
    assert ids == [LEADER, LEADER]
    first, second = mfx.requests[2], mfx.requests[3]
    assert dict(first.url.params) == {
        "state": "active,paused",
        "source": "account",
        "account_id": ACCOUNT,
        "limit": "1",
    }
    assert second.url.params["cursor"] == "c2"

    await client.copy.update_leader(LEADER, signal_lifetime_s=60, idempotency_key="lead-2")
    assert mfx.requests[4].method == "PATCH"
    assert body_of(mfx.requests[4]) == {"signal_lifetime_s": 60}
    assert key_of(mfx.requests[4]) == "lead-2"

    paused = await client.copy.pause_leader(LEADER, idempotency_key="lead-3")
    assert paused.state is CopyLeaderState.PAUSED
    await client.copy.resume_leader(LEADER, idempotency_key="lead-4")
    retired = await client.copy.retire_leader(
        LEADER, close_copied=False, reason="desk closed", idempotency_key="lead-5"
    )
    assert retired.state is CopyLeaderState.RETIRED
    assert [r.url.path for r in mfx.requests[5:8]] == [
        f"/v1/copy/leaders/{LEADER}/pause",
        f"/v1/copy/leaders/{LEADER}/resume",
        f"/v1/copy/leaders/{LEADER}/retire",
    ]
    assert [key_of(r) for r in mfx.requests[5:8]] == ["lead-3", "lead-4", "lead-5"]
    assert body_of(mfx.requests[7]) == {"close_copied": False, "reason": "desk closed"}

    with pytest.raises(ConflictError) as over:
        await client.copy.create_leader(
            source="external", signal_lifetime_s=30, idempotency_key="lead-6"
        )
    assert over.value.code == "quota_exceeded"
    assert over.value.details["reason"] == "plan_limit"
    assert len(mfx.requests) == 9
    assert body_of(mfx.requests[8]) == {"source": "external", "signal_lifetime_s": 30}

    mfx.responses.append(copy_page([], None, LEADER_STATS))
    page = await client.copy.leaders()
    assert isinstance(page, CopyPage)
    assert dict(mfx.last.url.params) == {}


async def test_an_external_leader_sends_an_open_and_a_close_and_a_float_is_never_sent(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an external leader / When the SDK sends an open signal with a volume and stops, one
    with units, a close naming the open, a repeat the platform answers as a duplicate, and opens
    with both or neither of volume and units, a float volume, a float in a nested setting, a field
    the contract does not have and a word outside its list / Then each signal is POST
    /copy/leaders/{id}/signals with the contract's id, decimals as plain strings and the
    Idempotency-Key, a stop loss or take profit below zero sent signed as the contract's decimal
    allows; the duplicate comes back marked; and every wrong argument (a volume, units or
    exposure cap below zero among them) is refused before anything is sent."""
    mfx.responses.extend(
        [ok(accepted(), 202), ok(accepted(your_id="s-2"), 202), ok(accepted(True, "s-3"), 202)]
    )
    sent = await client.copy.send_open_signal(
        LEADER,
        id_="s-1",
        symbol="EURUSD",
        side="buy",
        volume=Decimal("1E+0"),
        sl="1.0800",
        tp=Decimal("1.1000"),
        instrument_key="fx:EURUSD",
        time=dt.datetime(2026, 11, 13, 9, tzinfo=dt.UTC),
        account={"balance": "10000"},
        idempotency_key="sig-1",
    )
    assert str(sent.signal_id) == SIGNAL
    assert sent.duplicate is False
    request = mfx.requests[0]
    assert request.url.path == f"/v1/copy/leaders/{LEADER}/signals"
    assert key_of(request) == "sig-1"
    assert body_of(request) == {
        "id": "s-1",
        "symbol": "EURUSD",
        "side": "buy",
        "volume": "1",
        "sl": "1.0800",
        "tp": "1.1000",
        "instrument_key": "fx:EURUSD",
        "time": "2026-11-13T09:00:00+00:00",
        "account": {"balance": "10000"},
    }

    await client.copy.send_open_signal(
        LEADER,
        id_="s-2",
        symbol="CL-SPREAD",
        side="sell",
        units=100000,
        sl="-1.25",
        tp=Decimal("-3.5E+0"),
        idempotency_key="sig-2",
    )
    assert body_of(mfx.requests[1]) == {
        "id": "s-2",
        "symbol": "CL-SPREAD",
        "side": "sell",
        "units": "100000",
        "sl": "-1.25",
        "tp": "-3.5",
    }

    closed = await client.copy.send_close_signal(
        LEADER, id_="s-3", close="s-1", idempotency_key="sig-3"
    )
    assert closed.duplicate is True
    assert body_of(mfx.requests[2]) == {"id": "s-3", "close": "s-1"}

    copy = client.copy
    with pytest.raises(ValueError, match="exactly one"):
        await copy.send_open_signal(
            LEADER, id_="x", symbol="EURUSD", side="buy", idempotency_key="k"
        )
    with pytest.raises(ValueError, match="exactly one"):
        await copy.send_open_signal(
            LEADER, id_="x", symbol="EURUSD", side="buy", volume=1, units=1, idempotency_key="k"
        )
    with pytest.raises(TypeError, match="float"):
        await copy.send_open_signal(
            LEADER,
            id_="x",
            symbol="EURUSD",
            side="buy",
            volume=0.1,  # type: ignore[arg-type]
            idempotency_key="k",
        )
    negative: list[dict[str, Any]] = [{"volume": "-1"}, {"units": -100}]
    for wrong in negative:
        with pytest.raises(ValueError, match="non-negative"):
            await copy.send_open_signal(
                LEADER, id_="x", symbol="EURUSD", side="buy", idempotency_key="k", **wrong
            )
    stops: list[dict[str, Any]] = [
        {"sl": -1.5},
        {"tp": "--1"},
        {"sl": "-"},
        {"tp": Decimal("-Infinity")},
    ]
    for stop in stops:
        with pytest.raises((TypeError, ValueError)):
            await copy.send_open_signal(
                LEADER, id_="x", symbol="EURUSD", side="buy", volume=1, idempotency_key="k", **stop
            )
    with pytest.raises(ValueError, match="non-negative"):
        await copy.create_group(name="g", gross_exposure_cap="-1", idempotency_key="k")
    with pytest.raises(TypeError, match="float"):
        await copy.create_leader(
            source="external",
            signal_lifetime_s=30,
            limits={"max_risk_pct": 2.5},
            idempotency_key="k",
        )
    with pytest.raises(ValueError, match="finite"):
        await copy.create_leader(
            source="external",
            signal_lifetime_s=30,
            limits={"max_risk_pct": Decimal("NaN")},
            idempotency_key="k",
        )
    with pytest.raises(ValueError, match="filters.sides is not a field"):
        await copy.create_leader(
            source="external", signal_lifetime_s=30, filters={"sides": "buy"}, idempotency_key="k"
        )
    with pytest.raises(ValueError, match="does not fit the contract"):
        await copy.create_leader(
            source="everyone",  # type: ignore[arg-type]
            signal_lifetime_s=30,
            idempotency_key="k",
        )
    with pytest.raises(TypeError, match="cannot be sent"):
        await copy.create_leader(
            source="external",
            signal_lifetime_s=30,
            filters={"symbols": {"EURUSD"}},
            idempotency_key="k",
        )
    assert len(mfx.requests) == 3


async def test_a_follower_is_made_read_listed_changed_paused_resumed_resynced_and_unfollowed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an account that will follow a leader / When the SDK creates the follower with its
    scaling, bounds, symbol map, options and limits, has one refused because it is an MT5 netting
    account, reads it, lists followers of a group across pages, changes its scaling,
    pauses, resumes, resyncs and unfollows it / Then each is the contract's route with the
    Idempotency-Key on every write; when_risk_unchecked goes in the options as given, refuse or
    copy, any other word is refused before sending, and a follower read back shows it; an MT5
    netting account's follow is a ValidationError naming not_on_this_venue and margin_mode; the
    list sends state, leader,
    account and group and keeps the stats row; unfollow sends close_copied; and nothing is
    retried."""
    mfx.responses.extend(
        [
            ok(follower(), 201),
            httpx.Response(
                422,
                json={
                    "error": {
                        "code": "unprocessable",
                        "message": "an MT5 netting account cannot follow",
                        "details": {"reason": "not_on_this_venue", "options": ["margin_mode"]},
                    }
                },
            ),
            ok(follower()),
            copy_page([follower()], "c2", FOLLOWER_STATS),
            copy_page([follower()], None, FOLLOWER_STATS),
            ok(follower(mandate_version=2)),
            ok(follower("paused")),
            ok(follower()),
            ok(follower(), 202),
            ok(follower("unfollowed")),
        ]
    )
    made = await client.copy.create_follower(
        account_id=FOLLOWER_ACCOUNT,
        leader_id=LEADER,
        scaling={"mode": "fixed_multiplier", "multiplier": Decimal("0.5")},
        bounds={"min_volume": "0.01", "max_volume": None, "max_open": 5},
        symbol_map={"US30": "DJ30.cash"},
        options={"reverse": False, "delay_ms": 0, "when_risk_unchecked": "copy"},
        risk_limits={"daily_pct": "3", "basis": "equity"},
        close_on_stopout=True,
        group_id=GROUP,
        idempotency_key="fol-1",
    )
    assert made.state is CopyFollowerState.COPYING
    assert key_of(mfx.requests[0]) == "fol-1"
    assert body_of(mfx.requests[0]) == {
        "account_id": FOLLOWER_ACCOUNT,
        "leader_id": LEADER,
        "scaling": {"mode": "fixed_multiplier", "multiplier": "0.5"},
        "bounds": {"min_volume": "0.01", "max_volume": None, "max_open": 5},
        "symbol_map": {"US30": "DJ30.cash"},
        "options": {"reverse": False, "delay_ms": 0, "when_risk_unchecked": "copy"},
        "risk_limits": {"daily_pct": "3", "basis": "equity"},
        "close_on_stopout": True,
        "group_id": GROUP,
    }

    with pytest.raises(ValidationError) as refused:
        await client.copy.create_follower(
            account_id=FOLLOWER_ACCOUNT,
            leader_id=LEADER,
            scaling={"mode": "balance_ratio"},
            idempotency_key="fol-2",
        )
    assert refused.value.details["reason"] == "not_on_this_venue"
    assert refused.value.details["options"] == ["margin_mode"]
    assert len(mfx.requests) == 2

    await client.copy.get_follower(FOLLOWER)
    assert mfx.requests[2].url.path == f"/v1/copy/followers/{FOLLOWER}"
    listed = [
        f.id
        async for f in client.copy.all_followers(
            state="copying",
            leader_id=LEADER,
            account_id=FOLLOWER_ACCOUNT,
            group_id=GROUP,
            out_of_step=True,
            sort="oldest",
        )
    ]
    assert len(listed) == 2
    assert dict(mfx.requests[3].url.params) == {
        "state": "copying",
        "leader_id": LEADER,
        "account_id": FOLLOWER_ACCOUNT,
        "group_id": GROUP,
        "sort": "oldest",
        "out_of_step": "true",
    }
    assert mfx.requests[4].url.params["cursor"] == "c2"
    assert mfx.requests[4].url.params["sort"] == "oldest"

    changed = await client.copy.update_follower(
        FOLLOWER, scaling={"mode": "fixed_volume", "volume": "0.10"}, idempotency_key="fol-3"
    )
    assert changed.mandate_version == 2
    assert body_of(mfx.requests[5]) == {"scaling": {"mode": "fixed_volume", "volume": "0.10"}}
    await client.copy.pause_follower(FOLLOWER, idempotency_key="fol-4")
    await client.copy.resume_follower(FOLLOWER, idempotency_key="fol-5")
    await client.copy.resync_follower(FOLLOWER, idempotency_key="fol-6")
    gone = await client.copy.unfollow(FOLLOWER, close_copied=True, idempotency_key="fol-7")
    assert gone.state is CopyFollowerState.UNFOLLOWED
    assert [r.url.path.rsplit("/", 1)[-1] for r in mfx.requests[6:10]] == [
        "pause",
        "resume",
        "resync",
        "unfollow",
    ]
    assert [key_of(r) for r in mfx.requests[5:10]] == ["fol-3", "fol-4", "fol-5", "fol-6", "fol-7"]
    assert body_of(mfx.requests[9]) == {"close_copied": True}
    with pytest.raises(ValueError, match="not a field"):
        await client.copy.update_follower(
            FOLLOWER, options={"reverse": True, "copy_tpp": True}, idempotency_key="fol-8"
        )
    for word in ("ignore", None, True):
        with pytest.raises(ValueError, match="not a valid CopyOptionsWhenRiskUnchecked"):
            await client.copy.update_follower(
                FOLLOWER, options={"when_risk_unchecked": word}, idempotency_key="fol-9"
            )
    assert len(mfx.requests) == 10

    mfx.responses.append(ok(follower(mandate_version=3, options={"when_risk_unchecked": "refuse"})))
    changed = await client.copy.update_follower(
        FOLLOWER, options={"when_risk_unchecked": "refuse"}, idempotency_key="fol-10"
    )
    assert body_of(mfx.last) == {"options": {"when_risk_unchecked": "refuse"}}
    assert changed.options.when_risk_unchecked == "refuse"


async def test_a_preview_is_a_read_with_no_key_and_names_each_rows_match_volume_or_reason(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """Given an account considering a follow and two leader symbols to try / When the SDK asks for
    the preview, the platform first answering 429, and asks again with no rows and with a float /
    Then the preview is POST /copy/followers/preview carrying the mandate and the rows, with no
    Idempotency-Key, retried after the 429 as a read; each row comes back with its follower
    symbol, how it was matched and its volume, or its refusal reason from the closed list; and
    an empty or float preview is refused before anything is sent."""
    mfx.responses.extend(
        [error(429, "rate_limited", "slow down", **{"Retry-After": "1"}), ok(preview())]
    )
    got = await client.copy.preview_follower(
        account_id=FOLLOWER_ACCOUNT,
        leader_id=LEADER,
        scaling={"mode": "equity_ratio"},
        rows=[{"symbol": "EURUSD", "volume": "1.00"}, {"symbol": "US30", "volume": Decimal("1")}],
        bounds={"max_volume": "5"},
        symbol_map={"XAUUSD": "GOLD"},
        options={"reverse": False},
    )
    assert len(mfx.requests) == 2
    assert sleeps == [1.0]
    request = mfx.requests[1]
    assert (request.method, request.url.path) == ("POST", "/v1/copy/followers/preview")
    assert key_of(request) is None
    assert body_of(request)["rows"] == [
        {"symbol": "EURUSD", "volume": "1.00"},
        {"symbol": "US30", "volume": "1"},
    ]
    assert got.refusal is None
    eurusd, us30 = got.rows
    assert (eurusd.follower_symbol, eurusd.follower_volume) == ("EURUSD", "50000")
    assert str(eurusd.matched_by) == "same_name"
    assert str(us30.reason) == "mapping"
    assert str(us30.reason) in REFUSAL_REASONS

    with pytest.raises(ValueError, match="at least one row"):
        await client.copy.preview_follower(
            account_id=FOLLOWER_ACCOUNT, leader_id=LEADER, scaling={"mode": "equity_ratio"}, rows=[]
        )
    with pytest.raises(TypeError, match="float"):
        await client.copy.preview_follower(
            account_id=FOLLOWER_ACCOUNT,
            leader_id=LEADER,
            scaling={"mode": "equity_ratio"},
            rows=[{"symbol": "EURUSD", "volume": 1.0}],
        )
    with pytest.raises(ValueError, match=r"rows\[0\].volumes is not a field"):
        await client.copy.preview_follower(
            account_id=FOLLOWER_ACCOUNT,
            leader_id=LEADER,
            scaling={"mode": "equity_ratio"},
            rows=[{"symbol": "EURUSD", "volume": "1", "volumes": "1"}],
        )
    assert len(mfx.requests) == 2


async def test_a_followers_stopouts_are_listed_and_reset_with_a_reason(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a follower stopped out by its daily limit / When the SDK lists its stop-outs across
    two pages filtered by state, one to a page, resets the daily one with a reason, and resets
    again when none is active / Then the list is GET /copy/followers/{id}/stopouts with the state
    filter, the page size and the cursor; the reset is POST .../stopouts/reset with the reason,
    the limit and the Idempotency-Key, answered with the follower; and no active stop-out is a
    StateError (no_active_stopout)."""
    mfx.responses.extend(
        [
            ok({"items": [stopout()], "next_cursor": "c2", "returned": 1}),
            ok({"items": [stopout("expired")], "next_cursor": None, "returned": 1}),
            ok(follower()),
            httpx.Response(
                409,
                json={
                    "error": {
                        "code": "state_error",
                        "message": "nothing to reset",
                        "details": {"reason": "no_active_stopout"},
                    }
                },
            ),
        ]
    )
    states = [
        s.state
        async for s in client.copy.all_stopouts(FOLLOWER, state=["active", "expired"], limit=1)
    ]
    assert [str(s) for s in states] == ["active", "expired"]
    assert mfx.requests[0].url.path == f"/v1/copy/followers/{FOLLOWER}/stopouts"
    assert dict(mfx.requests[0].url.params) == {"limit": "1", "state": "active,expired"}
    assert dict(mfx.requests[1].url.params) == {
        "limit": "1",
        "state": "active,expired",
        "cursor": "c2",
    }

    back = await client.copy.reset_stopouts(
        FOLLOWER, reason="limit raised", limit="daily", idempotency_key="reset-1"
    )
    assert back.state is CopyFollowerState.COPYING
    assert mfx.requests[2].url.path == f"/v1/copy/followers/{FOLLOWER}/stopouts/reset"
    assert body_of(mfx.requests[2]) == {"reason": "limit raised", "limit": "daily"}
    assert key_of(mfx.requests[2]) == "reset-1"

    with pytest.raises(StateError) as none:
        await client.copy.reset_stopouts(FOLLOWER, reason="again", idempotency_key="reset-2")
    assert none.value.details["reason"] == "no_active_stopout"
    assert body_of(mfx.requests[3]) == {"reason": "again"}
    assert len(mfx.requests) == 4


async def test_a_group_is_made_listed_changed_and_its_members_added_removed_paused_and_resumed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an Enterprise tenant with followers to manage together / When the SDK creates a group
    with a template and an exposure cap, reads it, lists groups across pages, changes its name and
    clears its cap, adds two followers (one in another group) and removes one, pauses and resumes
    the group, and adds none or more than 500 / Then each is the contract's route with the
    Idempotency-Key on every write; the template's when_risk_unchecked goes as given and another
    word is refused; every group is listed with the page size given; the cap goes as a plain
    decimal and a cleared one as null;
    each member's outcome is answered apart; and a member list of the wrong size is refused before
    anything is sent."""
    second = "06abfa00-0000-7000-8000-0000000000f2"
    mfx.responses.extend(
        [
            ok(group(), 201),
            ok(group()),
            copy_page([group()], "c2", GROUP_STATS),
            copy_page([group()], None, GROUP_STATS),
            ok(group()),
            ok(group()),
            ok(members((FOLLOWER, "done", None), (second, "refused", "in_another_group"))),
            ok(members((FOLLOWER, "done", None))),
            ok(group("paused")),
            ok(group()),
        ]
    )
    await client.copy.create_group(
        name="Desk A",
        template={
            "scaling": {"mode": "fixed_multiplier", "multiplier": "1"},
            "options": {"when_risk_unchecked": "refuse"},
        },
        gross_exposure_cap=Decimal("250000"),
        placement_policy="same_region",
        idempotency_key="grp-1",
    )
    assert body_of(mfx.requests[0]) == {
        "name": "Desk A",
        "template": {
            "scaling": {"mode": "fixed_multiplier", "multiplier": "1"},
            "options": {"when_risk_unchecked": "refuse"},
        },
        "gross_exposure_cap": "250000",
        "placement_policy": "same_region",
    }
    await client.copy.get_group(GROUP)
    assert mfx.requests[1].url.path == f"/v1/copy/groups/{GROUP}"
    assert len([g async for g in client.copy.all_groups(state="active", limit=1)]) == 2
    assert dict(mfx.requests[2].url.params) == {"state": "active", "limit": "1"}
    assert dict(mfx.requests[3].url.params) == {"state": "active", "limit": "1", "cursor": "c2"}

    await client.copy.update_group(
        GROUP, name="Desk B", gross_exposure_cap=None, idempotency_key="grp-2"
    )
    assert body_of(mfx.requests[4]) == {"name": "Desk B", "gross_exposure_cap": None}
    await client.copy.update_group(
        GROUP, gross_exposure_cap="1000", placement_policy=None, idempotency_key="grp-3"
    )
    assert body_of(mfx.requests[5]) == {"gross_exposure_cap": "1000", "placement_policy": None}

    added = await client.copy.add_group_followers(
        GROUP, [FOLLOWER, UUID(second)], idempotency_key="grp-4"
    )
    assert [(str(r.outcome), r.reason) for r in added.results] == [
        ("done", None),
        ("refused", "in_another_group"),
    ]
    assert mfx.requests[6].url.path == f"/v1/copy/groups/{GROUP}/followers"
    assert body_of(mfx.requests[6]) == {"follower_ids": [FOLLOWER, second]}
    await client.copy.remove_group_followers(GROUP, [FOLLOWER], idempotency_key="grp-5")
    assert mfx.requests[7].url.path == f"/v1/copy/groups/{GROUP}/followers/remove"
    await client.copy.pause_group(GROUP, idempotency_key="grp-6")
    await client.copy.resume_group(GROUP, idempotency_key="grp-7")
    assert [key_of(r) for r in mfx.requests] == [f"grp-{n}" for n in (1,)] + [None] * 3 + [
        f"grp-{n}" for n in range(2, 8)
    ]

    with pytest.raises(ValueError, match="not a valid CopyOptionsWhenRiskUnchecked"):
        await client.copy.update_group(
            GROUP, template={"options": {"when_risk_unchecked": "maybe"}}, idempotency_key="grp-8"
        )
    with pytest.raises(ValueError, match="1 to 500"):
        await client.copy.add_group_followers(GROUP, [], idempotency_key="grp-8")
    with pytest.raises(ValueError, match="1 to 500"):
        await client.copy.remove_group_followers(GROUP, [FOLLOWER] * 501, idempotency_key="grp-9")
    assert len(mfx.requests) == 10


async def test_the_copy_log_sends_its_filters_comma_joined_and_its_window_and_keeps_the_stats_row(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant reading what became of its copies / When the SDK reads the log by leader,
    follower, account and signal, with two outcomes, two refusal reasons, a venue, a window and
    the mfx_ms order, walks it across two pages, and asks with a reason outside the closed list or
    a window that ends before it starts or names a naive time / Then the read is GET /copy/log
    with each list sent as one
    comma-separated value and only the parameters given; every row keeps its outcome, reason and
    stage timings; the stats row is read from the page; and a wrong reason or window is refused
    before anything is sent."""
    mfx.responses.extend(
        [
            copy_page([log_row(), log_row("min_volume")], "c2", LOG_STATS),
            copy_page([log_row(None, "filled")], None, LOG_STATS),
        ]
    )
    since = dt.datetime(2026, 11, 12, tzinfo=dt.UTC)
    until = dt.datetime(2026, 11, 13, tzinfo=dt.UTC)
    rows = [
        row
        async for row in client.copy.all_log(
            leader_id=LEADER,
            follower_id=FOLLOWER,
            account_id=FOLLOWER_ACCOUNT,
            signal_id=SIGNAL,
            outcome=["refused", "filled"],
            reason=["mapping", "min_volume"],
            venue="ctrader",
            sort="mfx_ms",
            limit=2,
            from_=since,
            to=until,
        )
    ]
    assert [str(r.outcome) for r in rows] == ["refused", "refused", "filled"]
    assert [None if r.reason is None else str(r.reason) for r in rows] == [
        "mapping",
        "min_volume",
        None,
    ]
    assert rows[0].mfx_ms == 11.0
    first = mfx.requests[0]
    assert first.url.path == "/v1/copy/log"
    assert dict(first.url.params) == {
        "limit": "2",
        "leader_id": LEADER,
        "follower_id": FOLLOWER,
        "account_id": FOLLOWER_ACCOUNT,
        "signal_id": SIGNAL,
        "outcome": "refused,filled",
        "reason": "mapping,min_volume",
        "venue": "ctrader",
        "from": "2026-11-12T00:00:00+00:00",
        "to": "2026-11-13T00:00:00+00:00",
        "sort": "mfx_ms",
    }
    assert mfx.requests[1].url.params["cursor"] == "c2"

    mfx.responses.append(copy_page([log_row()], None, LOG_STATS))
    page = await client.copy.log()
    assert dict(mfx.last.url.params) == {}
    assert page.stats is not None
    assert (page.stats.copies, page.stats.refused, page.stats.broker_ms_p50) == (3, 2, None)
    assert len(page) == 1

    with pytest.raises(ValueError, match="terminal_not_active"):
        await client.copy.log(reason="terminal_not_active")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="ends before it starts"):
        await client.copy.log(from_=until, to=since)
    naive = dt.datetime(2026, 11, 12)  # noqa: DTZ001 - the point of the check
    windows: list[dict[str, Any]] = [
        {"from_": naive, "to": until},
        {"from_": since, "to": naive},
        {"to": naive},
    ]
    for window in windows:
        with pytest.raises(ValueError, match="naive datetime"):
            await client.copy.log(**window)
    with pytest.raises(ValueError, match="naive datetime"):
        [row async for row in client.copy.all_log(from_=naive)]
    assert len(mfx.requests) == 3
    assert REFUSAL_REASONS == (
        "mapping",
        "min_volume",
        "no_stop",
        "risk_rule",
        "plan_limit",
        "stopped_out",
        "signal_expired",
        "skip_pending",
        "close_only",
        "paused",
        "account_not_connected",
        "market_closed",
        "no_conversion",
        "not_on_this_venue",
        "venue_unavailable",
        "broker",
    )
    assert set(REFUSAL_REASONS) == {reason.value for reason in CopyReason}


def _message(kind: str, data: dict[str, Any]) -> StreamMessage:
    return StreamMessage(channel="events", seq=1, type=kind, data=data)


COPY_COMMON = {
    "schema_version": "1",
    "follower_id": FOLLOWER,
    "leader_id": LEADER,
    "account_id": FOLLOWER_ACCOUNT,
    "venue": "ctrader",
    "at": AT,
}
DEAL = {
    "action": "open",
    "side": "buy",
    "units": "100000",
    "price": "1.08512",
    "instrument_key": "fx:EURUSD",
}


def test_the_copy_events_are_read_as_typed_values() -> None:
    """Given the five copy events in the contract's shape (objects, numbers, nulls) / When each is
    read with event_of, and a copy event lacking its deal or with a deal that is not an object /
    Then copy.copied, copy.refused, copy.stopout, copy.drift and copy.state_changed come back as
    their typed values with ids as UUIDs, volumes and money as Decimals, times as aware UTC
    datetimes and timings as milliseconds; a refusal keeps its reason from the closed list and the
    venue's own code; and a missing or malformed part is a ValueError naming it."""
    copied = event_of(
        _message(
            "copy.copied",
            {
                **COPY_COMMON,
                "signal_id": SIGNAL,
                "command_id": COMMAND,
                "deal": DEAL,
                "as": {"symbol": "EURUSD", "side": "buy", "volume": "50000", "price": None},
                "latency_ms": 12.5,
                "slippage": "0.00002",
                "stages": {"detect_ms": 2, "broker_ms": 40.5},
            },
        )
    )
    assert isinstance(copied, CopyCopied)
    assert copied.KIND == "copy.copied"
    assert copied.account_id == UUID(FOLLOWER_ACCOUNT)
    assert copied.venue == "ctrader"
    assert copied.deal.units == Decimal("100000")
    assert copied.deal.price == Decimal("1.08512")
    assert copied.as_.volume == Decimal("50000")
    assert copied.as_.price is None
    assert copied.latency_ms == 12.5
    assert copied.slippage == Decimal("0.00002")
    assert copied.stages == {"detect_ms": 2.0, "broker_ms": 40.5}
    assert copied.at == dt.datetime(2026, 11, 13, 9, tzinfo=dt.UTC)

    refused = event_of(
        _message(
            "copy.refused",
            {
                **COPY_COMMON,
                "signal_id": SIGNAL,
                "deal": {**DEAL, "price": None, "instrument_key": None},
                "outcome": "refused",
                "reason": "broker",
                "venue_code": "MARKET_CLOSED",
                "why": "the broker refused it",
            },
        )
    )
    assert isinstance(refused, CopyRefused)
    assert refused.reason in REFUSAL_REASONS
    assert (refused.outcome, refused.venue_code) == ("refused", "MARKET_CLOSED")
    assert refused.deal.instrument_key is None

    stopped = event_of(
        _message(
            "copy.stopout",
            {
                **COPY_COMMON,
                "stopout_id": STOPOUT,
                "limit": "daily",
                "used": "312.40",
                "closed": [
                    {"symbol": "EURUSD", "volume": "50000", "command_id": COMMAND},
                    {"symbol": "XAUUSD", "volume": "10", "command_id": None},
                ],
            },
        )
    )
    assert isinstance(stopped, CopyStopoutEvent)
    assert stopped.used == Decimal("312.40")
    assert [c.command_id for c in stopped.closed] == [UUID(COMMAND), None]

    drift = event_of(_message("copy.drift", {**COPY_COMMON, "drift_pct": "4.5"}))
    assert isinstance(drift, CopyDrift)
    assert drift.drift_pct == Decimal("4.5")

    changed = event_of(
        _message(
            "copy.state_changed",
            {**COPY_COMMON, "from": "copying", "to": "stopped_out", "why": "stopout"},
        )
    )
    assert isinstance(changed, CopyStateChanged)
    assert (changed.from_state, changed.to_state, changed.why) == (
        "copying",
        "stopped_out",
        "stopout",
    )

    bare = event_of(
        _message(
            "copy.copied",
            {
                **COPY_COMMON,
                "signal_id": SIGNAL,
                "command_id": COMMAND,
                "deal": DEAL,
                "as": {"symbol": "EURUSD", "side": "buy", "volume": "1", "price": "1.1"},
                "latency_ms": None,
                "slippage": None,
                "stages": None,
            },
        )
    )
    assert isinstance(bare, CopyCopied)
    assert (bare.latency_ms, bare.stages) == (None, {})
    no_closed = event_of(
        _message(
            "copy.stopout",
            {
                **COPY_COMMON,
                "stopout_id": STOPOUT,
                "limit": "lifetime",
                "used": "1",
                "closed": None,
            },
        )
    )
    assert isinstance(no_closed, CopyStopoutEvent)
    assert no_closed.closed == ()

    with pytest.raises(ValueError, match="carries no `deal`"):
        event_of(_message("copy.refused", {**COPY_COMMON, "signal_id": SIGNAL}))
    with pytest.raises(ValueError, match="`deal` is not an object"):
        event_of(_message("copy.refused", {**COPY_COMMON, "signal_id": SIGNAL, "deal": "open"}))
    assert {"copy.copied", "copy.refused", "copy.stopout", "copy.drift"} <= mfx.events.EVENT_KINDS
    assert mfx.CopyStateChanged is CopyStateChanged


async def test_a_groups_close_needs_pause_its_rollover_a_key_once_applied_and_closes_are_followed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an Enterprise group whose members hold copied positions / When the SDK closes the
    group's copies with a reason and pause, rolls the group's template over as a dry run and then
    applied, lists the batch's requested closes by state across pages and reads one close / Then
    the close sends its reason and pause with the Idempotency-Key and answers the batch; the dry
    run sends no key and the applied one its key, each with the fields, the page and the limit;
    an applied rollover without a key, a dry run with one, or a naive or backward window is
    refused before anything is sent; the closes send their filters, the state comma-joined and
    the window as instants, and keep the stats row; and a close reads back each position and
    attempt."""
    mfx.responses.extend(
        [
            ok(
                {
                    "group_id": GROUP,
                    "batch_id": BATCH,
                    "paused": True,
                    "followers": 2,
                    "closes": [CLOSE],
                },
                202,
            ),  # fmt: skip
            ok(
                {
                    "group_id": GROUP,
                    "dry_run": True,
                    "fields": ["scaling"],
                    "next_after": None,
                    "results": [
                        {
                            "follower_id": FOLLOWER,
                            "outcome": "changed",
                            "reason": None,
                            "changes": {
                                "scaling": {
                                    "from": {"mode": "equity_ratio"},
                                    "to": {"mode": "balance_ratio"},
                                }
                            },
                        }
                    ],
                }
            ),  # fmt: skip
            ok(
                {
                    "group_id": GROUP,
                    "dry_run": False,
                    "fields": ["scaling"],
                    "next_after": None,
                    "results": [],
                }
            ),  # fmt: skip
            copy_page([close_row()], "c2", CLOSE_STATS),
            copy_page([close_row("done")], None, CLOSE_STATS),
            ok(close_row("incomplete")),
        ]
    )
    closed = await client.copy.close_group(
        GROUP, reason="desk closing", pause=True, idempotency_key="gc-1"
    )
    assert (closed.batch_id, closed.paused, closed.closes) == (UUID(BATCH), True, [UUID(CLOSE)])
    assert mfx.requests[0].url.path == f"/v1/copy/groups/{GROUP}/close"
    assert body_of(mfx.requests[0]) == {"reason": "desk closing", "pause": True}
    assert key_of(mfx.requests[0]) == "gc-1"

    dry = await client.copy.rollover_group(GROUP, dry_run=True, fields=["scaling"], limit=100)
    assert mfx.requests[1].url.path == f"/v1/copy/groups/{GROUP}/rollover"
    assert body_of(mfx.requests[1]) == {"dry_run": True, "fields": ["scaling"], "limit": 100}
    assert key_of(mfx.requests[1]) is None
    assert dry.results[0].outcome.value == "changed"
    await client.copy.rollover_group(GROUP, dry_run=False, after=FOLLOWER, idempotency_key="ro-1")
    assert body_of(mfx.requests[2]) == {"dry_run": False, "after": FOLLOWER}
    assert key_of(mfx.requests[2]) == "ro-1"
    with pytest.raises(ValueError, match="needs an idempotency_key"):
        await client.copy.rollover_group(GROUP, dry_run=False)
    with pytest.raises(ValueError, match="takes no key"):
        await client.copy.rollover_group(GROUP, dry_run=True, idempotency_key="ro-2")
    with pytest.raises(ValueError, match="does not fit the contract"):
        await client.copy.rollover_group(GROUP, dry_run=True, fields=["name"])  # type: ignore[list-item]
    assert len(mfx.requests) == 3

    start = dt.datetime(2026, 11, 12, tzinfo=dt.UTC)
    rows = [
        c
        async for c in client.copy.all_closes(
            batch_id=BATCH, group_id=GROUP, state=["pending", "incomplete"], from_=start
        )
    ]
    assert [r.state.value for r in rows] == ["pending", "done"]
    assert dict(mfx.requests[3].url.params) == {
        "batch_id": BATCH,
        "group_id": GROUP,
        "state": "pending,incomplete",
        "from": "2026-11-12T00:00:00+00:00",
    }
    assert mfx.requests[4].url.params["cursor"] == "c2"
    with pytest.raises(ValueError, match="naive datetime"):
        await client.copy.closes(to=dt.datetime(2026, 11, 12))  # noqa: DTZ001 - the point
    with pytest.raises(ValueError, match="ends before it starts"):
        await client.copy.closes(from_=start, to=start - dt.timedelta(days=1))
    with pytest.raises(ValueError):
        await client.copy.closes(state="open")  # type: ignore[arg-type]
    assert len(mfx.requests) == 5

    one = await client.copy.get_close(CLOSE)
    assert mfx.requests[5].url.path == f"/v1/copy/closes/{CLOSE}"
    (entry,) = one.entries
    assert (one.state.value, entry.state.value, entry.attempts[0].reason) == (
        "incomplete",
        "not_closed",
        "market_closed",
    )


async def test_signals_every_stopout_and_the_log_by_group_are_read_with_the_contracts_live_fields(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant reading its copying as a whole / When the SDK lists its leaders' signals by
    kind and action over a window, every stop-out of its followers by state and group, a follower
    read with its live figures, a group read with its exposure, and the copy log by group with a
    Risk refusal on a row / Then each is the contract's route with its filters comma-joined and its
    window as instants, stats kept on every page; a word outside a filter's list is refused
    before anything is sent; the follower reads back its drift, limits in use, today and
    requested close, the group its cap, its share, its leavers and the members it could not
    enforce on, and the log row the leader's deal, the follower's symbol and the Risk detail."""
    start = dt.datetime(2026, 11, 12, tzinfo=dt.UTC)
    live = follower(
        drift={"pct": "4.5", "at": AT},
        limits_use={
            "as_of": AT,
            "limits": [
                {
                    "limit": "daily",
                    "used": "12.5",
                    "allowed": "100",
                    "period_start": AT,
                    "as_of": AT,
                }
            ],  # fmt: skip
        },
        today={"copies": 3, "filled": 2, "mfx_ms_p50": 11.0},
        exposure={"used": "1200.50", "share": "5000"},
        close={
            "id": CLOSE,
            "state": "pending",
            "cause": "unfollowed",
            "positions": 2,
            "closed": 1,
            "attempt": 1,
            "created_at": AT,
        },  # fmt: skip
    )
    exposed = {
        **group(),
        "gross_exposure_cap": "10000",
        "out_of_step": 0,
        "exposure": {
            "cap": "10000",
            "used": "2400",
            "share": "5000",
            "members": 2,
            "unpriced": 0,
            "leavers": {"used": "300", "unpriced": 1},
            "unenforced": 1,
            "as_of": AT,
        },
    }
    risky = {
        **log_row(reason="risk_rule"),
        "risk": {
            "reason": "daily_loss",
            "rule": "daily_loss",
            "policy_id": None,
            "version": None,
            "used": "450",
            "limit": "500",
            "would_be": "520",
            "challenge_id": "06abfa00-0000-7000-8000-0000000000a3",
            "challenge_version": 2,
        },
    }
    mfx.responses.extend(
        [
            copy_page([signal_row()], "c2", SIGNAL_STATS),
            copy_page([signal_row()], None, SIGNAL_STATS),
            copy_page([stopout()], "c2", STOPOUT_STATS),
            copy_page([stopout()], None, STOPOUT_STATS),
            ok(live),
            ok(exposed),
            copy_page([risky], None, LOG_STATS),
        ]
    )
    signals = [
        x
        async for x in client.copy.all_signals(
            leader_id=LEADER, kind="fill", action=["open", "close"], from_=start
        )
    ]
    assert [x.outcomes.filled for x in signals] == [2, 2]
    assert dict(mfx.requests[0].url.params) == {
        "leader_id": LEADER,
        "kind": "fill",
        "action": "open,close",
        "from": "2026-11-12T00:00:00+00:00",
    }
    assert mfx.requests[1].url.params["cursor"] == "c2"
    stopouts = [
        x
        async for x in client.copy.all_tenant_stopouts(
            state=["active", "reset"], group_id=GROUP, follower_id=FOLLOWER, to=start
        )
    ]
    assert len(stopouts) == 2
    assert mfx.requests[2].url.path == "/v1/copy/stopouts"
    assert dict(mfx.requests[2].url.params) == {
        "state": "active,reset",
        "group_id": GROUP,
        "follower_id": FOLLOWER,
        "to": "2026-11-12T00:00:00+00:00",
    }
    with pytest.raises(ValueError):
        await client.copy.signals(kind="manual")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="naive datetime"):
        await client.copy.tenant_stopouts(from_=dt.datetime(2026, 11, 12))  # noqa: DTZ001
    assert len(mfx.requests) == 4

    read = await client.copy.get_follower(FOLLOWER)
    assert read.drift.pct == "4.5"  # type: ignore[union-attr]
    assert read.limits_use.limits[0].used == "12.5"  # type: ignore[union-attr]
    assert read.today.filled == 2  # type: ignore[union-attr]
    assert read.exposure.share == "5000"  # type: ignore[union-attr]
    assert read.close.state.value == "pending"  # type: ignore[union-attr]
    grp = await client.copy.get_group(GROUP)
    cap = grp.exposure
    assert (cap.share, cap.leavers.used, cap.unenforced) == ("5000", "300", 1)  # type: ignore[union-attr]

    page = await client.copy.log(group_id=GROUP, reason="risk_rule")
    assert dict(mfx.requests[6].url.params) == {"group_id": GROUP, "reason": "risk_rule"}
    (row,) = page.items
    assert (row.deal.units, row.symbol) == ("100000", None)
    assert (row.risk.limit, row.risk.would_be, row.risk.challenge_version) == ("500", "520", 2)  # type: ignore[union-attr]
    assert page.stats.mfx_ms_p95 == 30.0  # type: ignore[union-attr]


def test_a_finished_requested_close_and_a_risk_refusal_are_read_as_typed_copy_events() -> None:
    """Given copy.closed in the contract's shape and a copy.refused for risk_rule carrying the Risk
    detail / When each is read with event_of / Then copy.closed comes back as CopyClosedEvent with
    its close, cause and state, what it closed with each command, and what it did not close with
    why; a refusal's risk detail is a RiskRefusal with the figures as text, and a refusal without
    one reads risk as None."""
    closed = event_of(
        _message(
            "copy.closed",
            {
                **COPY_COMMON,
                "close_id": CLOSE,
                "cause": "unfollowed",
                "state": "incomplete",
                "closed": [{"symbol": "EURUSD", "volume": "50000", "command_id": COMMAND}],
                "not_closed": [
                    {"symbol": "XAUUSD", "volume": "10", "why": "netting"},
                    {"symbol": "US30", "volume": None, "why": None},
                ],
            },
        )
    )
    assert isinstance(closed, CopyClosedEvent)
    assert (closed.close_id, closed.cause, closed.state) == (
        UUID(CLOSE),
        "unfollowed",
        "incomplete",
    )
    assert [(c.symbol, c.volume, c.command_id) for c in closed.closed] == [
        ("EURUSD", Decimal("50000"), UUID(COMMAND))
    ]
    assert [(n.symbol, n.volume, n.why) for n in closed.not_closed] == [
        ("XAUUSD", Decimal("10"), "netting"),
        ("US30", None, None),
    ]
    refusal = {
        **COPY_COMMON,
        "signal_id": SIGNAL,
        "deal": DEAL,
        "outcome": "refused",
        "reason": "risk_rule",
        "venue_code": None,
        "why": "the daily loss rule",
    }
    risk = {
        "reason": "daily_loss",
        "rule": "daily_loss",
        "policy_id": "06abfa00-0000-7000-8000-0000000000a4",
        "version": 3,
        "used": "450",
        "limit": "500",
        "would_be": "520",
        "challenge_id": None,
        "challenge_version": None,
    }
    refused = event_of(_message("copy.refused", {**refusal, "risk": risk}))
    assert isinstance(refused, CopyRefused)
    assert refused.risk == RiskRefusal(
        reason="daily_loss",
        rule="daily_loss",
        policy_id="06abfa00-0000-7000-8000-0000000000a4",
        version=3,
        challenge_id=None,
        challenge_version=None,
        used="450",
        limit="500",
        would_be="520",
    )
    as_text = event_of(_message("copy.refused", {**refusal, "risk": json.dumps(risk)}))
    assert isinstance(as_text, CopyRefused)
    assert as_text.risk == refused.risk
    plain = event_of(_message("copy.refused", {**refusal, "risk": None}))
    assert isinstance(plain, CopyRefused)
    assert plain.risk is None
    assert "copy.closed" in mfx.events.EVENT_KINDS
    assert mfx.CopyClosedEvent is CopyClosedEvent


@pytest.fixture
def sync_client(mfx: FakeMfx, private_key: Ed25519PrivateKey) -> Iterator[SyncMfxClient]:
    client = SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    yield client
    client.close()


def test_the_blocking_client_offers_every_copy_method(
    sync_client: SyncMfxClient, mfx: FakeMfx
) -> None:
    """Given a script with no event loop / When it calls every Copy Trading method through
    SyncMfxClient.copy, walking each list to its end / Then each blocking method sends exactly what
    the async one sends, to the same route, and returns the same typed value; each all_* walk is an
    ordinary iterator that reads one page a request."""
    two_pages: list[tuple[str, dict[str, Any], dict[str, Any]]] = [
        ("leaders", leader(), LEADER_STATS),
        ("followers", follower(), FOLLOWER_STATS),
        ("groups", group(), GROUP_STATS),
        ("log", log_row(), LOG_STATS),
    ]
    sync = sync_client.copy
    mfx.responses.extend(
        [
            ok(leader(), 201),
            ok(leader()),
            copy_page([leader()], None, LEADER_STATS),
            ok(leader()),
            ok(leader("paused")),
            ok(leader()),
            ok(leader("retired")),
            ok(accepted(), 202),
            ok(accepted(), 202),
            ok(follower(), 201),
            ok(preview()),
            ok(follower()),
            copy_page([follower()], None, FOLLOWER_STATS),
            ok(follower()),
            ok(follower("paused")),
            ok(follower()),
            ok(follower(), 202),
            ok(follower("unfollowed")),
            ok({"items": [stopout()], "next_cursor": None, "returned": 1}),
            ok({"items": [stopout()], "next_cursor": None, "returned": 1}),
            ok(follower()),
            ok(group(), 201),
            ok(group()),
            copy_page([group()], None, GROUP_STATS),
            ok(group()),
            ok(members((FOLLOWER, "done", None))),
            ok(members((FOLLOWER, "done", None))),
            ok(group("paused")),
            ok(group()),
            copy_page([log_row()], None, LOG_STATS),
            ok(
                {
                    "group_id": GROUP,
                    "batch_id": BATCH,
                    "paused": False,
                    "followers": 0,
                    "closes": [],
                },
                202,
            ),  # fmt: skip
            ok(
                {
                    "group_id": GROUP,
                    "dry_run": True,
                    "fields": [],
                    "results": [],
                    "next_after": None,
                }
            ),  # fmt: skip
            copy_page([close_row()], None, CLOSE_STATS),
            ok(close_row()),
            copy_page([signal_row()], None, SIGNAL_STATS),
            copy_page([stopout()], None, STOPOUT_STATS),
        ]
        + [copy_page([item], None, stats) for _, item, stats in two_pages]
        + [
            copy_page([close_row()], None, CLOSE_STATS),
            copy_page([signal_row()], None, SIGNAL_STATS),
            copy_page([stopout()], None, STOPOUT_STATS),
        ]
    )
    k = {"idempotency_key": "k"}
    assert sync.create_leader(source="external", signal_lifetime_s=5, **k).state.value == "active"
    sync.get_leader(LEADER)
    assert sync.leaders(state="active").stats is not None
    sync.update_leader(LEADER, signal_lifetime_s=9, **k)
    sync.pause_leader(LEADER, **k)
    sync.resume_leader(LEADER, **k)
    sync.retire_leader(LEADER, close_copied=False, reason="r", **k)
    sync.send_open_signal(LEADER, id_="a", symbol="EURUSD", side="buy", volume="1", **k)
    sync.send_close_signal(LEADER, id_="b", close="a", **k)
    sync.create_follower(
        account_id=FOLLOWER_ACCOUNT, leader_id=LEADER, scaling={"mode": "equity_ratio"}, **k
    )
    assert (
        len(
            sync.preview_follower(
                account_id=FOLLOWER_ACCOUNT,
                leader_id=LEADER,
                scaling={"mode": "equity_ratio"},
                rows=[{"symbol": "EURUSD", "volume": "1"}],
            ).rows
        )
        == 2
    )
    sync.get_follower(FOLLOWER)
    sync.followers(group_id=GROUP)
    sync.update_follower(FOLLOWER, close_on_stopout=True, **k)
    sync.pause_follower(FOLLOWER, **k)
    sync.resume_follower(FOLLOWER, **k)
    sync.resync_follower(FOLLOWER, **k)
    sync.unfollow(FOLLOWER, close_copied=False, **k)
    assert len(sync.stopouts(FOLLOWER)) == 1
    assert len(list(sync.all_stopouts(FOLLOWER))) == 1
    sync.reset_stopouts(FOLLOWER, reason="r", **k)
    sync.create_group(name="G", **k)
    sync.get_group(GROUP)
    sync.groups()
    sync.update_group(GROUP, name="H", **k)
    sync.add_group_followers(GROUP, [FOLLOWER], **k)
    sync.remove_group_followers(GROUP, [FOLLOWER], **k)
    sync.pause_group(GROUP, **k)
    sync.resume_group(GROUP, **k)
    assert sync.log(reason="mapping").stats is not None
    assert sync.close_group(GROUP, reason="r", pause=False, **k).paused is False
    assert sync.rollover_group(GROUP, dry_run=True).dry_run is True
    assert sync.closes(batch_id=BATCH).stats is not None
    assert sync.get_close(CLOSE).id == UUID(CLOSE)
    assert sync.signals(kind="fill").stats is not None
    assert sync.tenant_stopouts(state="active").stats is not None
    assert len(list(sync.all_leaders(state="active"))) == 1
    assert len(list(sync.all_followers())) == 1
    assert len(list(sync.all_groups())) == 1
    assert len(list(sync.all_log(outcome="refused"))) == 1
    assert len(list(sync.all_closes(state="pending"))) == 1
    assert len(list(sync.all_signals())) == 1
    assert len(list(sync.all_tenant_stopouts())) == 1
    paths = [r.url.path for r in mfx.requests]
    assert paths[0] == "/v1/copy/leaders"
    assert paths[10] == "/v1/copy/followers/preview"
    assert paths[30:36] == [
        f"/v1/copy/groups/{GROUP}/close",
        f"/v1/copy/groups/{GROUP}/rollover",
        "/v1/copy/closes",
        f"/v1/copy/closes/{CLOSE}",
        "/v1/copy/signals",
        "/v1/copy/stopouts",
    ]
    assert paths[-4:] == [
        "/v1/copy/log",
        "/v1/copy/closes",
        "/v1/copy/signals",
        "/v1/copy/stopouts",
    ]
    assert len(mfx.requests) == 43
    assert json.loads(mfx.requests[7].content)["volume"] == "1"
