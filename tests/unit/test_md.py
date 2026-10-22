"""``client.md`` — the market-data subscriptions price channels depend on."""

from __future__ import annotations

import datetime as dt

import httpx
import pytest

from mfx.client import MfxClient
from mfx.md import SubscriptionDegraded, SubscriptionRecovered, subscription_event
from mfx.streaming import Channel, StreamMessage

from .conftest import BROKER_ID, SERVER_ID, FakeMfx, body_of, page

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

SYMBOL = "EURUSD.sd"


def subscription(
    symbol: str = SYMBOL, sub_id: str = "06abfa00-0000-7000-8000-000000000001"
) -> dict:
    """One subscription as the platform answers it: ids resolved to refs, never a second fetch."""
    return {
        "id": sub_id,
        "broker": {"id": str(BROKER_ID), "label": "Equiti"},
        "server": {"id": str(SERVER_ID), "label": "EquitiSecurities-Demo"},
        "symbol": symbol,
        "timeframes": [],
        "delivery": "ws",
        "state": "pending",
        "created_at": "2026-10-02T13:00:00Z",
    }


async def test_market_data_is_subscribed_before_its_channel_carries_anything(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that wants a symbol's prices
    When it subscribes through the SDK and then opens the channel
    Then the subscription names the server and the broker's own symbol, candles are asked for only
    when named, and the channel key is the one the subscription made live.

    Subscribing on the stream is not enough and the failure is quiet in the worst way:
    `md:{server_id}:{symbol}` answers `not_subscribed: subscribe to the symbol first`, which a
    caller watching an empty channel reads as a quiet market. The two calls belong together, which
    is why this surface exists rather than leaving the generated call to be discovered.
    """
    mfx.responses.extend(
        [
            httpx.Response(201, json=subscription()),
            httpx.Response(201, json=subscription("XAUUSD.sd")),
        ]
    )

    await client.md.subscribe(SERVER_ID, SYMBOL, idempotency_key="k1")
    sent = body_of(mfx.requests[-1])
    assert sent["server_id"] == str(SERVER_ID)
    assert sent["symbol"] == SYMBOL, "the broker's own name, suffix and all"
    assert "timeframes" not in sent, "no candles unless asked for; ticks only"
    assert mfx.requests[-1].headers["Idempotency-Key"] == "k1"
    assert mfx.requests[-1].url.path.endswith("/md/subscriptions")

    await client.md.subscribe(SERVER_ID, "XAUUSD.sd", idempotency_key="k2", timeframes=["M1", "H1"])
    assert body_of(mfx.requests[-1])["timeframes"] == ["M1", "H1"]

    # The key the subscription made live is the key the stream takes.
    assert Channel.md(SERVER_ID, SYMBOL) == f"md:{SERVER_ID}:{SYMBOL}"


async def test_subscriptions_are_listed_across_pages_and_dropped_by_id(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given more subscriptions than one page holds
    When the tenant lists them and then drops one
    Then every page is followed to the end, and the drop is a write like any other.

    A subscription outlives the stream: it is the standing request, counted against the
    plan, and closing a connection does not drop it. A tenant reconciling what it is paying for
    needs the whole list, not the first page.
    """
    mfx.responses.extend(
        [
            page(
                [
                    subscription("EURUSD.sd"),
                    subscription("XAUUSD.sd", "06abfa00-0000-7000-8000-000000000002"),
                ],
                "cursor-2",
            ),
            page([subscription("GBPUSD.sd", "06abfa00-0000-7000-8000-000000000003")], None),
            httpx.Response(204),
        ]
    )

    symbols = [s.symbol async for s in client.md.all_subscriptions()]
    assert symbols == ["EURUSD.sd", "XAUUSD.sd", "GBPUSD.sd"]
    assert "cursor=cursor-2" in str(mfx.requests[-1].url), "the second page followed the cursor"

    await client.md.unsubscribe("06abfa00-0000-7000-8000-000000000001", idempotency_key="k3")
    assert mfx.requests[-1].method == "DELETE"
    assert mfx.requests[-1].headers["Idempotency-Key"] == "k3"


def _ticks(*rows: tuple[str, str, str], more: bool) -> httpx.Response:
    """A TickList as the platform answers it: (time, bid, ask) rows, oldest first."""
    return httpx.Response(
        200,
        json={
            "items": [
                {"ts": ts, "bid": bid, "ask": ask, "last": None, "volume": None}
                for ts, bid, ask in rows
            ],
            "more": more,
        },
    )


async def test_tick_history_is_read_forward_from_a_moment_through_the_tenants_own_terminal(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that wants a symbol's past ticks
    When it reads them through the SDK, once with only a start and once with every bound
    Then each is one GET /md/ticks naming the broker, the broker's own symbol and `from`; `to`,
    `limit` and `server_id` go only when given; and the answer is the ticks oldest first with
    prices as decimal strings and `more` saying whether the window holds further ticks."""
    start = dt.datetime(2026, 10, 13, 9, 0, tzinfo=dt.UTC)
    mfx.responses.extend(
        [
            _ticks(("2026-10-13T09:00:00.120Z", "1.15801", "1.15809"), more=True),
            _ticks(more=False),
        ]
    )

    first = await client.md.ticks(BROKER_ID, SYMBOL, from_=start)

    sent = mfx.last.url
    assert sent.path == "/v1/md/ticks"
    assert (sent.params["broker"], sent.params["symbol"]) == (str(BROKER_ID), SYMBOL)
    assert sent.params["from"].startswith("2026-10-13T09:00:00")
    assert "to" not in sent.params and "server_id" not in sent.params
    assert (first.items[0].bid, first.items[0].ask, first.more) == ("1.15801", "1.15809", True)

    empty = await client.md.ticks(
        BROKER_ID,
        SYMBOL,
        from_=start,
        to=start + dt.timedelta(minutes=5),
        limit=200,
        server_id=SERVER_ID,
    )
    sent = mfx.last.url
    assert sent.params["to"].startswith("2026-10-13T09:05:00")
    assert (sent.params["limit"], sent.params["server_id"]) == ("200", str(SERVER_ID))
    assert (empty.items, empty.more) == ([], False), "nothing in the window is an empty answer"


async def test_a_window_of_ticks_is_followed_call_by_call_and_each_tick_comes_once(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a window that holds more ticks than one call returns, with three ticks sharing the
    millisecond a call ended on, two of them identical
    When the SDK follows the window to its end
    Then each further call starts from the last tick's time, as the contract says; the ticks of
    that millisecond already held are dropped and the one not yet held is kept, so every tick comes
    once and in order; and it stops when the platform says there are no more. A call that brings
    nothing new while promising more ends the read instead of asking for ever."""
    start = dt.datetime(2026, 10, 13, 9, 0, tzinfo=dt.UTC)
    same_ms = "2026-10-13T09:00:01.500Z"
    mfx.responses.extend(
        [
            _ticks(
                ("2026-10-13T09:00:00.120Z", "1.15801", "1.15809"),
                (same_ms, "1.15802", "1.15810"),
                (same_ms, "1.15802", "1.15810"),
                more=True,
            ),
            _ticks(
                (same_ms, "1.15802", "1.15810"),
                (same_ms, "1.15802", "1.15810"),
                (same_ms, "1.15803", "1.15811"),
                ("2026-10-13T09:00:02.000Z", "1.15804", "1.15812"),
                more=True,
            ),
            _ticks(("2026-10-13T09:00:02.000Z", "1.15804", "1.15812"), more=True),
        ]
    )

    seen = [t.bid async for t in client.md.all_ticks(BROKER_ID, SYMBOL, from_=start, page_size=3)]

    assert seen == ["1.15801", "1.15802", "1.15802", "1.15803", "1.15804"]
    asked = [r.url.params["from"] for r in mfx.requests]
    assert asked[0].startswith("2026-10-13T09:00:00")
    assert asked[1].startswith("2026-10-13T09:00:01.5"), "from the last tick's own millisecond"
    assert asked[2].startswith("2026-10-13T09:00:02")
    assert len(mfx.requests) == 3, "nothing new with more promised ends the read"
    assert all(r.url.params["limit"] == "3" for r in mfx.requests)


async def test_bars_are_read_for_a_window_through_the_tenants_own_terminal(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that wants a symbol's bars
    When it reads a window through the SDK, once with only the window and once with a limit and a
    server, and once with a timeframe the contract does not name
    Then each read is one GET /md/candles naming the broker, the broker's own symbol, the timeframe
    and the window; `limit` and `server_id` go only when given; the answer is the bars oldest first
    with open, high, low and close as decimal strings and each bar's time as an instant; and the
    unknown timeframe is a ValueError at the call, before anything reaches MFX."""
    start = dt.datetime(2026, 10, 13, 9, 0, tzinfo=dt.UTC)
    end = start + dt.timedelta(hours=2)
    bar = {
        "ts": "2026-10-13T09:00:00Z",
        "o": "1.158",
        "h": "1.1592",
        "l": "1.1575",
        "c": "1.159",
        "v": 812,
    }
    mfx.responses.extend(
        [httpx.Response(200, json={"items": [bar]}), httpx.Response(200, json={"items": []})]
    )

    bars = await client.md.candles(BROKER_ID, SYMBOL, "H1", from_=start, to=end)

    sent = mfx.last.url
    assert sent.path == "/v1/md/candles"
    assert (sent.params["broker"], sent.params["symbol"], sent.params["tf"]) == (
        str(BROKER_ID),
        SYMBOL,
        "H1",
    )
    assert sent.params["from"].startswith("2026-10-13T09:00:00")
    assert sent.params["to"].startswith("2026-10-13T11:00:00")
    assert "server_id" not in sent.params
    first = bars.items[0]
    assert (first.o, first.h, first.l, first.c, first.v) == (
        "1.158",
        "1.1592",
        "1.1575",
        "1.159",
        812,
    )
    assert first.ts == start

    empty = await client.md.candles(
        BROKER_ID, SYMBOL, "M5", from_=start, to=end, limit=300, server_id=SERVER_ID
    )
    sent = mfx.last.url
    assert (sent.params["tf"], sent.params["limit"], sent.params["server_id"]) == (
        "M5",
        "300",
        str(SERVER_ID),
    )
    assert empty.items == [], "no bar in the window is an empty answer"

    with pytest.raises(ValueError, match="M2"):
        await client.md.candles(BROKER_ID, SYMBOL, "M2", from_=start, to=end)
    assert len(mfx.requests) == 2, "the unknown timeframe never reached MFX"


def _health(kind: str, **data: object) -> StreamMessage:
    body = {
        "schema_version": "1.0",
        "subscription_id": "06abfb31-cf99-791e-8000-73d40c66805a",
        "broker_id": str(BROKER_ID),
        "server_id": str(SERVER_ID),
        "symbol": SYMBOL,
        "reason": "report_stale",
        "since": "2026-10-12T21:15:09Z",
        **data,
    }
    return StreamMessage(channel="events", seq=7, type=kind, data=body)


def test_a_subscription_that_stops_delivering_and_delivers_again_are_two_typed_events() -> None:
    """Given the messages a tenant's `events` channel carries when a subscription degrades and when
    it recovers, a degradation of a symbol that has never ticked, one with a reason this SDK was
    not built knowing, and a message about something else
    When each is read through the SDK
    Then the first two come back as SubscriptionDegraded and SubscriptionRecovered with ids as
    uuids, the times as instants, the reason in the platform's own word and the whole gap on the
    recovery; a symbol that never ticked has no last tick rather than an invented one; a new reason
    is passed on as text, not refused; and any other message is None, so a caller can ask of every
    message it reads."""
    degraded = subscription_event(
        _health("md.subscription_degraded", last_tick_at="2026-10-12T21:10:02.250Z")
    )
    assert isinstance(degraded, SubscriptionDegraded)
    assert (degraded.symbol, degraded.reason) == (SYMBOL, "report_stale")
    assert str(degraded.server_id) == str(SERVER_ID) and str(degraded.broker_id) == str(BROKER_ID)
    assert degraded.since == dt.datetime(2026, 10, 12, 21, 15, 9, tzinfo=dt.UTC)
    assert degraded.last_tick_at == dt.datetime(2026, 10, 12, 21, 10, 2, 250000, tzinfo=dt.UTC)

    recovered = subscription_event(
        _health("md.subscription_recovered", recovered_at="2026-10-12T21:16:10Z")
    )
    assert isinstance(recovered, SubscriptionRecovered)
    assert recovered.subscription_id == degraded.subscription_id
    assert (recovered.recovered_at - recovered.since).total_seconds() == 61
    assert recovered.last_tick_at is None

    never = subscription_event(_health("md.subscription_degraded", reason="a_reason_from_later"))
    assert isinstance(never, SubscriptionDegraded)
    assert (never.reason, never.last_tick_at) == ("a_reason_from_later", None)

    other = StreamMessage(channel="events", seq=8, type="terminal.state_changed", data={})
    assert subscription_event(other) is None
    tick = StreamMessage(channel="md:x:EURUSD", seq=None, type=None, data={"bid": "1.1"})
    assert subscription_event(tick) is None

    for kind, missing in (
        ("md.subscription_degraded", "since"),
        ("md.subscription_recovered", "recovered_at"),
    ):
        broken = _health(kind, recovered_at="2026-10-12T21:16:10Z")
        with pytest.raises(ValueError, match=missing):
            subscription_event(
                StreamMessage(
                    channel="events", seq=9, type=kind, data={**broken.data, missing: None}
                )
            )


async def test_a_subscription_says_on_itself_why_it_is_degraded_and_since_when(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that was not listening when a subscription degraded
    When it lists its subscriptions
    Then the degraded one says so in its state and carries the reason and the moment, and a
    delivering one carries neither: the stream's two events and this read tell the same story."""
    held = {**subscription(), "state": "degraded", "degraded_reason": "no_ticks_in_session",
            "degraded_since": "2026-10-12T21:15:09Z"}  # fmt: skip
    fine = {
        **subscription("XAUUSD.sd", "06abfa00-0000-7000-8000-000000000002"),
        "state": "streaming",
        "degraded_reason": None,
        "degraded_since": None,
    }
    mfx.responses.append(page([held, fine], None))

    listed = (await client.md.subscriptions()).items

    assert (listed[0].state.value, listed[0].degraded_reason) == ("degraded", "no_ticks_in_session")
    assert listed[0].degraded_since == dt.datetime(2026, 10, 12, 21, 15, 9, tzinfo=dt.UTC)
    assert (listed[1].state.value, listed[1].degraded_reason, listed[1].degraded_since) == (
        "streaming",
        None,
        None,
    )
