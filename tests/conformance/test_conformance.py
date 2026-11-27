"""The Python SDK passes the shared SDK test suite: every case, played back by the suite's fake MFX
Hub on localhost, through this SDK's public surface.

This file is the Python runner. It holds no rule: it starts the fake hub, asks it for each case,
turns the case's neutral operation into the Python call, and checks what came back against the
case and against the hub's verdict on what was sent. The rules are the suite's
(``suite/cases``), vendored at the version in ``suite-version.txt``.
"""

from __future__ import annotations

import asyncio
import base64
import datetime as dt
import json
import logging
import os
import subprocess
import sys
from collections.abc import Iterator
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pytest

import mfx
from mfx import errors
from mfx.signing import SigningKey, signing_message
from mfx.streaming import StreamMessage

SUITE = Path(__file__).resolve().parent / "suite"
VOCABULARY = json.loads((SUITE / "vocabulary.json").read_text(encoding="utf-8"))
#: Cases this SDK does not pass yet, each with the reason. Empty at 1.0 (the suite's rule).
NOT_YET: dict[str, str] = json.loads(
    (Path(__file__).resolve().parent / "not-yet.json").read_text(encoding="utf-8")
)
#: The suite's neutral error kinds, as this SDK's classes.
KINDS: dict[str, type[Exception]] = {
    "ApiError": errors.MfxApiError,
    "TransportError": errors.MfxTransportError,
    "Timeout": errors.MfxTimeout,
    **{name: getattr(errors, name) for name in VOCABULARY["errors"] if hasattr(errors, name)},
    # The suite's kinds end in Error; these two keep the names the SDKs share, without it.
    "ServiceAgreementNotAcceptedError": errors.ServiceAgreementNotAccepted,
    "TermsNotAcceptedError": errors.TermsNotAccepted,
}


def _case_ids() -> list[str]:
    ids: list[str] = []
    for path in sorted((SUITE / "cases").glob("*.json")):
        ids += [case["id"] for case in json.loads(path.read_text(encoding="utf-8"))]
    return ids


@pytest.fixture(scope="module")
def hub() -> Iterator[str]:
    """The suite's fake hub, on a free local port, for this module; its base URL."""
    env = {**os.environ, "PYTHONPATH": str(SUITE)}
    process = subprocess.Popen(  # noqa: S603 - fixed argv, this interpreter
        [sys.executable, "-m", "mfx_fake_hub", "--cases", str(SUITE / "cases")],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert process.stdout is not None
    line = process.stdout.readline().strip()
    assert line.startswith("listening "), line
    yield line.removeprefix("listening ")
    process.terminate()
    process.wait(timeout=10)


def _value(raw: Any) -> Any:  # noqa: ANN401 - a case's JSON value
    """A case argument as Python: ``$decimal`` is a Decimal, ``$float`` a float."""
    if isinstance(raw, dict) and "$decimal" in raw:
        return Decimal(raw["$decimal"])
    if isinstance(raw, dict) and "$float" in raw:
        return float(raw["$float"])
    return raw


async def _call(client: mfx.MfxClient, op: str, args: dict[str, Any]) -> dict[str, Any]:
    """Make the case's call through this SDK and describe what came back in the suite's names."""
    a = {name: _value(value) for name, value in args.items()}
    if op == "signing.sign":
        key = SigningKey(base64.b64encode(bytes.fromhex(VOCABULARY["key"]["seed_hex"])).decode())
        message = signing_message(
            a["timestamp"], a["nonce"], a["method"], a["path_with_query"], a["body"].encode()
        )
        return {"signature": key.sign(message)}
    if op == "terminals.get":
        terminal = await client.terminals.get(a["terminal_id"])
        return {"id": str(terminal.id), "state": str(terminal.state)}
    if op == "terminals.page":
        page = await client.terminals.page(cursor=a.get("cursor"), limit=a.get("limit"))
        return {"count": len(page), "next_cursor": page.next_cursor}
    if op == "terminals.list":
        return {"ids": [str(t.id) async for t in client.terminals.list()]}
    if op == "terminals.create":
        terminal = await client.terminals.create(**a)
        return {"id": str(terminal.id), "state": str(terminal.state)}
    if op == "execution.place_order":
        result = await client.execution.place_order(a.pop("terminal_id"), **a)
        return {
            "ok": result.ok,
            "state": str(result.state) if result.state else None,
            "command_id": result.command_id,
            "duplicate": result.duplicate,
            "retryable": result.retryable,
            "exec_price": result.exec_price,
            "position": result.tickets.position,
            "comment_raw": result.comment_raw,
        }
    if op == "catalog.quote":
        quote = await client.catalog.quote(a["broker_id"], a["symbol"])
        return {"bid": quote.bid, "ask": quote.ask, "age_s": quote.age_s, "state": str(quote.state)}
    if op == "stream.read":
        return await asyncio.wait_for(_read_stream(client, a["channels"], a["count"]), timeout=15)
    if op == "stream.close_waiting":
        return await asyncio.wait_for(_close_waiting(client, a["channels"]), timeout=15)
    if op == "md.subscribe_account":
        subscription = await client.md.subscribe_account(
            a["account_id"], a["symbol"], idempotency_key=a["idempotency_key"]
        )
        return {
            "id": str(subscription.id),
            "account_id": str(subscription.account_id),
            "symbol": subscription.symbol,
            "state": str(subscription.state),
        }
    if op == "md.account_subscriptions":
        return {
            "symbols": [
                s.symbol async for s in client.md.all_account_subscriptions(a["account_id"])
            ]
        }
    if op == "md.account_candles":
        bars = await client.md.account_candles(
            a["account_id"],
            a["symbol"],
            a["timeframe"],
            from_=dt.datetime.fromisoformat(a["from"]),
            to=dt.datetime.fromisoformat(a["to"]),
        )
        return {
            "count": len(bars.items),
            "first_open": bars.items[0].o if bars.items else None,
            "last_close": bars.items[-1].c if bars.items else None,
        }
    if op == "tenant.service_agreement":
        agreement = await client.tenant.service_agreement()
        change = agreement.plan_change
        return {
            "due": agreement.due,
            "held": agreement.held,
            "plan": agreement.plan,
            "plan_change_state": _word(change.state) if change is not None else None,
            "plan_change_to": change.to if change is not None else None,
            "documents": [d.document for d in agreement.documents],
            "accept_url": agreement.accept_url,
        }
    if op == "agreement.due_warnings":
        return {"warnings": await _due_warnings(client, a["terminal_id"], a["clients"], a["calls"])}
    if op == "risk.check":
        order = {"symbol": a["symbol"], "side": a["side"], "type": "market", "volume": a["volume"]}
        checked = await client.risk.check(a["account_id"], order)
        return {"verdict": str(checked.verdict)}
    if op == "risk.create_plan":
        order = {"symbol": a["symbol"], "side": a["side"], "type": "market", "volume": a["volume"]}
        step = {"trigger": {"kind": "r", "value": "1"},
                "action": {"kind": "close_part", "pct": "50"}, "held_by": "mfx"}  # fmt: skip
        plan = await client.risk.create_plan(
            {"account_id": a["account_id"], "order": order, "steps": [step]},
            idempotency_key=a["idempotency_key"],
        )
        return {"id": str(plan.id)}
    if op == "risk.create_policy":
        policy = await client.risk.create_policy(
            a["name"], a["rules"], reset=a["reset"], idempotency_key=a["idempotency_key"]
        )
        return {"id": str(policy.id), "version": policy.current_version.version}
    if op == "risk.challenge_accounts":
        accounts = client.risk.challenge_accounts(
            a["challenge_id"], state=a.get("state"), sort=a.get("sort", "daily_loss_used")
        )
        return {"ids": [str(x.account_id) async for x in accounts]}
    if op.startswith("copy."):
        return await _copy(client, op, a)
    raise AssertionError(f"this runner does not know the operation {op!r}")


def _word(value: Any) -> Any:  # noqa: ANN401 - a generated enum, a string or None
    """A generated enum as the word the API sent; anything else as it is."""
    return getattr(value, "value", value)


def _instant(raw: str | None) -> dt.datetime | None:
    return None if raw is None else dt.datetime.fromisoformat(raw)


async def _copy(client: mfx.MfxClient, op: str, a: dict[str, Any]) -> dict[str, Any]:  # noqa: C901, PLR0911
    """The Copy Trading operations, through ``client.copy``."""
    copy = client.copy
    if op == "copy.create_leader":
        leader = await copy.create_leader(**a)
        return {"id": str(leader.id), "source": _word(leader.source), "state": _word(leader.state)}
    if op == "copy.leaders":
        ids: list[str] = []
        stats: Any = None
        cursor: str | None = None
        while True:
            page = await copy.leaders(cursor=cursor, state=a.get("state"))
            ids += [str(leader.id) for leader in page]
            stats = stats or page.stats
            cursor = page.next_cursor
            if cursor is None:
                break
        return {"ids": ids, "stats_leaders": stats.leaders if stats else None}
    if op == "copy.send_open_signal":
        accepted = await copy.send_open_signal(a.pop("leader_id"), id_=a.pop("id"), **a)
        return {"signal_id": str(accepted.signal_id), "duplicate": accepted.duplicate}
    if op == "copy.create_follower":
        follower = await copy.create_follower(**a)
        return {
            "id": str(follower.id),
            "state": _word(follower.state),
            "mandate_version": follower.mandate_version,
        }
    if op == "copy.preview_follower":
        preview = await copy.preview_follower(**a)
        return {
            "refusal": None if preview.refusal is None else preview.refusal.to_dict(),
            "follower_volumes": [row.follower_volume for row in preview.rows],
            "reasons": [_word(row.reason) for row in preview.rows],
        }
    if op == "copy.unfollow":
        follower = await copy.unfollow(a.pop("follower_id"), **a)
        return {"state": _word(follower.state)}
    if op == "copy.reset_stopouts":
        follower = await copy.reset_stopouts(a.pop("follower_id"), **a)
        return {"state": _word(follower.state)}
    if op == "copy.log":
        log = await copy.log(
            outcome=a.get("outcome"),
            reason=a.get("reason"),
            from_=_instant(a.get("from")),
            to=_instant(a.get("to")),
        )
        return {
            "count": len(log),
            "reasons": [_word(row.reason) for row in log],
            "stats_refused": log.stats.refused if log.stats else None,
        }
    if op == "copy.add_group_followers":
        result = await copy.add_group_followers(
            a["group_id"], a["follower_ids"], idempotency_key=a["idempotency_key"]
        )
        return {
            "outcomes": [_word(item.outcome) for item in result.results],
            "reasons": [item.reason for item in result.results],
        }
    if op == "copy.close_group":
        closed = await copy.close_group(a.pop("group_id"), **a)
        return {
            "batch_id": str(closed.batch_id),
            "paused": closed.paused,
            "closes": [str(c) for c in closed.closes],
        }
    if op == "copy.rollover_group":
        rolled = await copy.rollover_group(a.pop("group_id"), **a)
        return {
            "outcomes": [_word(item.outcome) for item in rolled.results],
            "reasons": [item.reason for item in rolled.results],
            "next_after": None if rolled.next_after is None else str(rolled.next_after),
        }
    if op == "copy.closes":
        rows: list[Any] = []
        stats, cursor = None, None
        while True:
            page = await copy.closes(
                cursor=cursor, batch_id=a.get("batch_id"), state=a.get("state")
            )
            rows += list(page)
            stats = stats or page.stats
            cursor = page.next_cursor
            if cursor is None:
                break
        return {
            "ids": [str(c.id) for c in rows],
            "states": [_word(c.state) for c in rows],
            "stats_incomplete": stats.incomplete if stats else None,
        }
    if op == "copy.read_events":
        return await asyncio.wait_for(_copy_events(client, a["count"]), timeout=15)
    raise AssertionError(f"this runner does not know the operation {op!r}")


async def _copy_events(client: mfx.MfxClient, count: int) -> dict[str, Any]:
    """Read ``count`` messages on the events channel as the SDK's typed copy events."""
    events: list[Any] = []
    async with client.stream(max_reconnects=3) as stream:
        await stream.subscribe("events")
        async for message in stream:
            if isinstance(message, StreamMessage):
                events.append(mfx.event_of(message))
                if len(events) >= count:
                    break
    return {
        "types": [event.KIND for event in events],
        "accounts": [str(event.account_id) for event in events],
        "venues": [event.venue for event in events],
        "reasons": [
            event.reason if isinstance(event, mfx.CopyRefused) else None for event in events
        ],
    }


async def _close_waiting(client: mfx.MfxClient, channels: list[str]) -> dict[str, Any]:
    """Leave a read waiting on a quiet stream, close the stream, and see whether the read ended.

    The read has ended when it finishes within 2 s with nothing: no message, no error."""
    async with client.stream(max_reconnects=3) as stream:
        for channel in channels:
            await stream.subscribe(channel)
        waiting = asyncio.ensure_future(anext(aiter(stream)))
        await asyncio.sleep(0.1)
        await stream.aclose()
        try:
            await asyncio.wait_for(waiting, timeout=2)
            ended = False  # it brought back something: that is not the end
        except StopAsyncIteration:
            ended = True
        except (TimeoutError, Exception):
            ended = False
        stats = stream.stats
    return {"ended": ended, "reconnects": stats.reconnects}


async def _read_stream(client: mfx.MfxClient, channels: list[str], count: int) -> dict[str, Any]:
    """Subscribe in order, read ``count`` data messages, and report them with the stream's counters.

    A few reconnects are allowed, enough for any case; the client's sleep is a no-op, so a
    reconnect is decided by the stream and not waited for."""
    seqs: list[int | None] = []
    types: list[str | None] = []
    async with client.stream(max_reconnects=3) as stream:
        for channel in channels:
            await stream.subscribe(channel)
        async for event in stream:
            if isinstance(event, StreamMessage):
                seqs.append(event.seq)
                types.append(event.type)
                if len(seqs) >= count:
                    break
        stats = stream.stats
    return {
        "seqs": seqs,
        "types": types,
        "dropped": stats.dropped,
        "reconnects": stats.reconnects,
        "lifetime_reconnects": stats.lifetime_reconnects,
        "slow_consumer_drops": stats.slow_consumer_drops,
        "resyncs": stats.resyncs,
        "refused": stats.refused,
    }


class _Count(logging.Handler):
    """Counts the Service Agreement warnings the SDK logs."""

    def __init__(self) -> None:
        super().__init__(logging.WARNING)
        self.warnings = 0

    def emit(self, record: logging.LogRecord) -> None:
        if record.getMessage() == mfx.SERVICE_AGREEMENT_WARNING:
            self.warnings += 1


async def _due_warnings(client: mfx.MfxClient, terminal_id: str, clients: int, calls: int) -> int:
    """``clients`` clients, one after another, each reading the terminal ``calls`` times; the
    warnings they logged that a Service Agreement is due."""
    seed = base64.b64encode(bytes.fromhex(VOCABULARY["key"]["seed_hex"])).decode()
    counted = _Count()
    logger = logging.getLogger("mfx")
    logger.addHandler(counted)
    try:
        for _ in range(clients):
            async with mfx.MfxClient(client.base_url, client.key_id, seed, sleep=_noop) as each:
                for _ in range(calls):
                    await each.terminals.get(terminal_id)
    finally:
        logger.removeHandler(counted)
    return counted.warnings


def _same(got: Any, want: Any) -> bool:  # noqa: ANN401 - JSON values
    if isinstance(want, dict) and "$decimal" in want:
        return got is not None and Decimal(str(got)) == Decimal(want["$decimal"])
    return bool(got == want)


async def _noop(_: float) -> None:
    """The client's sleep: a retry is decided as the server said, without waiting for it."""


@pytest.mark.parametrize("case_id", _case_ids())
async def test_the_sdk_passes_every_case_of_the_shared_suite(hub: str, case_id: str) -> None:
    """Given a case of the shared SDK test suite, played back by the suite's fake MFX Hub
    When this SDK makes the case's call, signed with the suite's test key
    Then it returns, raises or refuses exactly as the case observes, and the hub's verdict is that
    every request the case expects arrived in order, signed and shaped as the case says, and
    nothing else did. A case listed in not-yet.json is expected to fail, for the reason given."""
    if case_id in NOT_YET:
        pytest.xfail(NOT_YET[case_id])
    control = httpx.AsyncClient(base_url=hub.removesuffix("/v1"))
    case = (await control.post("/_hub/case", json={"id": case_id})).json()
    seed = base64.b64encode(bytes.fromhex(VOCABULARY["key"]["seed_hex"])).decode()
    observe = case["observe"]
    async with mfx.MfxClient(hub, VOCABULARY["key"]["id"], seed, sleep=_noop) as client:
        if "raises" in observe:
            with pytest.raises(KINDS[observe["raises"]]) as raised:
                await _call(client, case["call"]["op"], case["call"]["args"])
            for name, want in observe.get("fields", {}).items():
                assert getattr(raised.value, name) == want, name
        elif "refuses" in observe:
            assert observe["refuses"] == "invalid_argument"
            with pytest.raises((TypeError, ValueError)):
                await _call(client, case["call"]["op"], case["call"]["args"])
        else:
            got = await _call(client, case["call"]["op"], case["call"]["args"])
            for name, want in observe["returns"].items():
                assert _same(got[name], want), f"{name}: {got[name]!r}, the case wants {want!r}"
    verdict = (await control.get("/_hub/verdict")).json()
    await control.aclose()
    assert verdict["ok"], "\n".join(verdict["problems"])
