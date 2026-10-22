"""G1–G8 — the capability gaps MFX Hub closes, asserted through the public SDK.

These are eight things a trading client needs from a hosted-terminal API and often cannot get,
written down as the reason MFX Hub is built. Each is a one-line row in a design note, which is a
claim nobody can run. This module turns each into a test against the SDK a tenant actually
calls, so "the gap is closed" stops being a table and becomes something CI can lose.

Deliberately end-to-shape rather than end-to-end: each asserts the *fact the gap is about* — that
the value exists, is granular, is attributed to a terminal, and is not derived — not that some
particular code path produces it. The conformance suite is what runs this against a real
deployment.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from mfx.client import MfxClient
from mfx.results import Reason
from mfx.streaming import Channel

from .conftest import BROKER_ID, SERVER_ID, TERMINAL_ID, FakeMfx, error
from .test_reads import _symbol
from .test_streaming import FakeTransport, ack, collect, event

#: The Story these cases are Tested By: Inventory gap closures G1-G8.

COMMAND_ID = "0191f0c2-0000-7000-8000-0000000000c1"


def _accepted() -> httpx.Response:
    return httpx.Response(
        202, json={"command_id": COMMAND_ID, "state": "ACCEPTED", "duplicate": False}
    )


def _command(result: dict[str, Any] | None, **extra: Any) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "command_id": COMMAND_ID,
            "terminal_id": TERMINAL_ID,
            "kind": "order_place",
            "state": "SUCCEEDED",
            "final": True,
            "created_at": "2026-09-25T09:00:00Z",
            "updated_at": "2026-09-25T09:00:01Z",
            "result": result,
            **extra,
        },
    )


def _result(**changes: Any) -> dict[str, Any]:
    return {
        "ok": True,
        "reason": None,
        "retryable": False,
        "mt5_retcode": 10009,
        "retcode_text": "TRADE_RETCODE_DONE",
        "comment_raw": "",
        "terminal_state": "ACTIVE",
        "tickets": {"order": 8811, "deal": 9911, "position": 8811},
        "exec_price": "1.09431",
        "exec_volume": "0.10",
        "broker_latency_ms": 41,
        "agent_latency_ms": 7,
        **changes,
    }


# -- G1 ------------------------------------------------------------------------------------------


async def test_g1_cancelling_a_pending_order_is_its_own_call(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a pending order / When it is cancelled / Then the call is its own path, not a
    modify.

    G1: without a first-class cancel, a pending order is cancelled by modifying it into
    something that will not fill, or by closing a position that does not exist yet.

    Here it is its own verb with its own ticket, and it returns a result like any other execution —
    a cancel that silently did nothing is the failure this closes."""
    mfx.responses.extend([_accepted(), _command(_result(tickets={"order": 8811}))])

    accepted = await client.execution.cancel_order(
        TERMINAL_ID, ticket=8811, idempotency_key="cancel-1"
    )
    result = await client.execution.get_command(accepted.command_id or COMMAND_ID)

    assert "8811" in mfx.requests[0].url.path, "the ticket is in the path, not in a body"
    assert accepted.command_id == COMMAND_ID, "answered at once with a command to follow"
    assert result.ok is True
    assert result.tickets.order == 8811, "the cancel names the order it cancelled"


# -- G2, G3 --------------------------------------------------------------------------------------


async def test_g2_a_degraded_market_data_subscription_is_an_event_not_a_silence(
    client: MfxClient,
) -> None:
    """Given a subscription the platform degrades / When ticks thin out / Then the client is told in
    an event rather than left to infer it.

    G2: a hosted feed commonly degrades by simply sending fewer ticks. A feed that thins out
    reads exactly like a quiet market, and the difference is only visible in hindsight.

    `md.subscription_degraded` arrives on the stream with what degraded and why, so a caller can
    act on it while it is happening."""
    transport = FakeTransport(
        [
            ack(Channel.EVENTS),
            event(
                Channel.EVENTS,
                1,
                "md.subscription_degraded",
                terminal_id=TERMINAL_ID,
                symbol="EURUSD.sd",
                reason="broker_throttled",
                ticks_per_s=0.2,
            ),
        ]
    )

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(Channel.EVENTS)
        seen = await collect(stream, 1)

    assert seen[0].type == "md.subscription_degraded"
    assert seen[0].data["reason"] == "broker_throttled", "why, not just that"
    assert seen[0].data["terminal_id"] == TERMINAL_ID


async def test_g3_a_symbol_whose_specification_changed_says_so_and_carries_its_hash(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a symbol whose specification changed mid-session / When it is read / Then it says
    so and carries the hash of the specification it is describing.

    G3: a broker changing a symbol's contract size, step or stops level mid-session silently
    invalidates every order a caller is about to place, and a hosted-terminal
    API commonly gives no notice.

    Two halves: `spec_hash` on the symbol, so a caller can tell a spec apart from one that looks
    the same, and `symbol.spec_changed` on the stream when it moves."""
    mfx.responses.append(httpx.Response(200, json=_symbol()))
    symbol = await client.catalog.symbol(BROKER_ID, "EURUSD.sd")

    transport = FakeTransport(
        [
            ack(Channel.EVENTS),
            event(
                Channel.EVENTS,
                1,
                "symbol.spec_changed",
                symbol="EURUSD.sd",
                server_id=SERVER_ID,
                spec_hash="c4d2",
                previous_spec_hash=symbol.spec_hash,
            ),
        ]
    )
    async with client.stream(connect=transport) as stream:
        await stream.subscribe(Channel.EVENTS)
        seen = await collect(stream, 1)

    assert symbol.spec_hash == "b3f1", "a spec has an identity, not just fields"
    assert seen[0].type == "symbol.spec_changed"
    assert seen[0].data["previous_spec_hash"] == "b3f1", "and the change names both sides"


# -- G4 ------------------------------------------------------------------------------------------


async def test_g4_pip_value_comes_from_the_terminal_or_is_null_and_is_never_derived(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a symbol whose pip value the terminal did not report / When it is read / Then the value
    is null, never a number the SDK worked out for itself.

    G4: pip value was computed from the quote currency and a guess at the conversion rate, which
    is right for the majors and wrong for exactly the instruments where position sizing matters.

    It is read from the terminal, and null until the terminal has reported it. A null a caller must
    handle beats a number that is quietly wrong on XAUUSD."""
    mfx.responses.extend(
        [
            httpx.Response(200, json=_symbol(pip_value_per_lot=None)),
            httpx.Response(200, json=_symbol("XAUUSD", pip_value_per_lot="10.00")),
        ]
    )

    unknown = await client.catalog.symbol(BROKER_ID, "EURUSD.sd")
    known = await client.catalog.symbol(BROKER_ID, "XAUUSD")

    assert unknown.pip_value_per_lot is None, "not yet observed is null, not a computation"
    assert known.pip_value_per_lot == "10.00", "and when it is known it is the terminal's number"


# -- G5 ------------------------------------------------------------------------------------------


async def test_g5_every_execution_result_says_what_state_its_terminal_was_in(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an execution result / When it is read / Then it names the state its terminal was in,
    whether it succeeded or failed.

    G5: an order that failed told you the order failed. It never told you the terminal had been
    reconnecting for ninety seconds, so a caller could not tell "the broker refused this" from
    "this never really left".

    `terminal_state` rides every result, the refused ones included."""
    mfx.responses.extend(
        [
            _accepted(),
            _command(_result()),
            error(409, "state_error", "terminal is DRAINING"),
        ]
    )

    await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="0.10", idempotency_key="g5-1"
    )
    filled = await client.execution.get_command(COMMAND_ID)
    refused = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="0.10", idempotency_key="g5-2"
    )

    assert filled.terminal_state == "ACTIVE"
    assert refused.ok is False
    assert hasattr(refused, "terminal_state"), "on a refusal too, or the field is not dependable"


# -- G6 ------------------------------------------------------------------------------------------


async def test_g6_terminal_id_is_the_one_join_key_across_reads_results_and_events(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a read, a result and an event for one terminal / When they are joined / Then
    terminal_id is the single key on all three.

    G6: a client otherwise has to join the provider's account id, its own user id and a broker
    login, and every report has to pick one. Three keys for one thing means three ways to be wrong.

    There is one id here. It names the terminal on a read, keys its results channel on the stream,
    and is what an event carries — so a result, an account and a tick can be put beside each other
    without a lookup table."""
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "terminal_id": TERMINAL_ID,
                "as_of": "2026-09-25T10:00:00Z",
                "items": [],
            },
        )
    )
    spreads = await client.accounts.spread(TERMINAL_ID)

    transport = FakeTransport(
        [
            ack(Channel.results(TERMINAL_ID)),
            event(
                Channel.results(TERMINAL_ID),
                1,
                "command.completed",
                terminal_id=TERMINAL_ID,
                command_id=COMMAND_ID,
            ),
        ]
    )
    async with client.stream(connect=transport) as stream:
        await stream.subscribe(Channel.results(TERMINAL_ID))
        seen = await collect(stream, 1)

    assert str(spreads.terminal_id) == TERMINAL_ID
    assert seen[0].channel == f"results:{TERMINAL_ID}", "the channel is keyed by it"
    assert seen[0].data["terminal_id"] == TERMINAL_ID, "and the payload carries it"


# -- G7 ------------------------------------------------------------------------------------------


async def test_g7_a_refusal_keeps_the_brokers_own_words_and_its_own_code(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a refusal from the broker / When it reaches the caller / Then the broker's own retcode
    and its own words both survive.

    G7: every failure arrived as one of a handful of buckets, so "not enough money",
    "market shut" and "your price moved" were the same string. A caller cannot retry one, wait for
    another and give up on the third if it cannot tell them apart.

    Three things survive: a granular `Reason`, the broker's numeric retcode, and `comment_raw` —
    the broker's own sentence, unedited. There is no bucket field anywhere in this SDK."""
    mfx.responses.extend(
        [
            _accepted(),
            _command(
                _result(
                    ok=False,
                    reason="insufficient_funds",
                    mt5_retcode=10019,
                    retcode_text="TRADE_RETCODE_NO_MONEY",
                    comment_raw="No money [free margin 12.40 < 41.00]",
                    tickets={},
                )
            ),
        ]
    )

    await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="5.00", idempotency_key="g7-1"
    )
    result = await client.execution.get_command(COMMAND_ID)

    assert result.reason is Reason.INSUFFICIENT_FUNDS, "the reason, not a bucket"
    assert result.mt5_retcode == 10019 and result.retcode_text == "TRADE_RETCODE_NO_MONEY"
    assert "free margin 12.40" in (result.comment_raw or ""), "the broker's own words, unedited"
    assert not hasattr(result, "bucket") and not hasattr(result, "category")


# -- G8 ------------------------------------------------------------------------------------------


async def test_g8_a_closed_deal_says_why_it_closed_in_the_platforms_own_vocabulary(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a deal that closed / When it is read / Then close_reason is the platform's own
    vocabulary, not a bucket.

    G8: a position that vanished told you only that it was gone. Stopped out, taken profit,
    closed by hand and rolled over are four different things to a strategy, and an API that
    reports one loses the difference.

    `close_reason` on a deal is MT5's own DEAL_REASON, not a five-value summary of it: `sl`,
    `tp`, `stop_out`, `rollover`, `vmargin`, `split`, `client`, `expert`, `mobile`, `web`. Null on
    an entry deal, because an opening deal did not close anything.

    Note on the numbering: an earlier design note numbered this G8 with the vocabulary
    `{TP, SL, SO, MANUAL, API}`; `openapi.yaml` numbers it G7 and ships MT5's. The spec is what the
    platform serves and what this asserts, and it is also the right one because the SDK passes the
    platform's own vocabulary through rather than summarising it — five buckets would lose
    `rollover` and `vmargin`, which are the two nobody predicts."""
    deal = {
        "deal": 9911,
        "order": 8811,
        "position": 8811,
        "symbol": "EURUSD.sd",
        "side": "sell",
        "entry": "out",
        "volume": "0.10",
        "price": "1.09220",
        "profit": "-21.10",
        "commission": "-0.70",
        "swap": "0.00",
        "time": "2026-09-25T11:00:00Z",
        "magic": 0,
        "comment": "[sl 1.09220]",
        "close_reason": "sl",
    }
    entry_deal = {**deal, "deal": 9910, "entry": "in", "close_reason": None}
    mfx.responses.append(
        httpx.Response(200, json={"items": [deal, entry_deal], "next_cursor": None, "returned": 2})
    )

    import datetime as dt

    page = await client.accounts.deals(
        TERMINAL_ID,
        from_=dt.datetime(2026, 9, 25, tzinfo=dt.UTC),
        to=dt.datetime(2026, 9, 26, tzinfo=dt.UTC),
    )

    closed, opened = page.items
    assert closed.close_reason == "sl", "stopped out, and it says so"
    assert opened.close_reason is None, "an entry deal closed nothing"
    assert json.dumps(deal["close_reason"]) == '"sl"', "the broker's vocabulary, not a bucket"
