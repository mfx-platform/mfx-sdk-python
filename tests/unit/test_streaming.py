"""``client.stream()`` — the multiplexed WebSocket (gap G2).

These drive the socket rather than the network: a fake connection hands over exactly the frames the
test names, and closes on cue. What is being asserted is the part that is easy to get wrong and
impossible to observe once it ships — what the stream asks for again after a reconnect, and what it
admits it missed.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

import pytest

from mfx.client import MfxClient
from mfx.errors import AuthError, MfxApiError
from mfx.streaming import (
    Channel,
    ChannelRefused,
    MfxStream,
    Resync,
    StreamClosed,
    StreamMessage,
)

from .conftest import BROKER_ID, SERVER_ID, TERMINAL_ID

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

SYMBOL = "EURUSD.sd"


class FakeSocket:
    """One connection's worth of frames, then whatever ending the test asked for."""

    def __init__(self, frames: list[Any]) -> None:
        self._frames = list(frames)
        self.sent: list[dict[str, Any]] = []
        self.closed = False

    async def send(self, message: str) -> None:
        self.sent.append(json.loads(message))

    async def recv(self) -> str:
        if not self._frames:
            raise StreamClosed(1000, "no more frames")
        frame = self._frames.pop(0)
        if isinstance(frame, StreamClosed):
            raise frame
        return json.dumps(frame)

    async def close(self) -> None:
        self.closed = True


class FakeTransport:
    """Hands out one FakeSocket per connection, so a reconnect is visible as a second socket."""

    def __init__(self, *connections: list[Any]) -> None:
        self._pending = list(connections)
        self.sockets: list[FakeSocket] = []
        self.headers: list[Mapping[str, str]] = []
        self.urls: list[str] = []

    async def __call__(self, url: str, headers: Mapping[str, str]) -> FakeSocket:
        self.urls.append(url)
        self.headers.append(dict(headers))
        frames = self._pending.pop(0) if self._pending else []
        socket = FakeSocket(frames)
        self.sockets.append(socket)
        return socket

    @property
    def last(self) -> FakeSocket:
        return self.sockets[-1]


def tick(channel: str, seq: int, bid: str = "1.09431") -> dict[str, Any]:
    return {"op": "msg", "ch": channel, "seq": seq, "data": {"bid": bid, "ask": "1.09445"}}


def event(channel: str, seq: int, type_: str, **data: Any) -> dict[str, Any]:
    return {"op": "msg", "ch": channel, "seq": seq, "type": type_, "data": data}


def ack(channel: str) -> dict[str, Any]:
    return {"op": "ack", "ch": channel}


async def collect(stream: MfxStream, count: int) -> list[Any]:
    """The next `count` events, so a test never waits on a stream that has more to give."""
    seen: list[Any] = []
    async for message in stream:
        seen.append(message)
        if len(seen) == count:
            return seen
    return seen


def test_a_channel_is_keyed_by_id_and_a_key_the_platform_would_refuse_is_refused_here() -> None:
    """Keys are ids, never display names, because brokers rename servers and symbols and
    a subscription keyed on a name stops matching the day they do.

    The pattern is the platform's own. Refusing locally turns "the stream is silent" — which looks
    exactly like a quiet market — into a ValueError at the call."""
    assert Channel.md(SERVER_ID, SYMBOL) == f"md:{SERVER_ID}:{SYMBOL}"
    assert Channel.candles(SERVER_ID, SYMBOL, "M5") == f"candles:{SERVER_ID}:{SYMBOL}:M5"
    assert Channel.results(TERMINAL_ID) == f"results:{TERMINAL_ID}"
    assert Channel.account(TERMINAL_ID) == f"account:{TERMINAL_ID}"
    assert Channel.EVENTS == "events"

    with pytest.raises(ValueError, match="not a channel key"):
        Channel.account("not-a-uuid")

    with pytest.raises(ValueError, match="not a channel key"):
        Channel.md("EquitiSecurities-Demo", SYMBOL)  # a name, not an id
    with pytest.raises(ValueError, match="not a channel key"):
        Channel.md(SERVER_ID, "EUR:USD")  # a colon would move the key's own boundaries


async def test_the_upgrade_is_signed_like_every_other_request_and_points_at_the_streams_own_host(
    client: MfxClient,
) -> None:
    """The stream carries the same Ed25519 signature as a REST call, over GET /v1/stream, and its
    host is derived from the client's rather than configured twice — a client pointed at dev cannot
    leave its stream pointed at prod."""
    transport = FakeTransport([])

    async with client.stream(connect=transport):
        pass

    assert transport.urls == ["wss://ws.dev.mfxhub.com/v1/stream"]
    signed = transport.headers[0]
    assert set(signed) == {"X-MFX-Key", "X-MFX-Timestamp", "X-MFX-Nonce", "X-MFX-Signature"}
    assert signed["X-MFX-Key"] == client.key_id
    assert transport.last.closed, "leaving the block closes the socket"


async def test_one_connection_carries_every_channel_and_an_ack_is_not_the_callers_business(
    client: MfxClient,
) -> None:
    """Multiplexed: ticks, events and results arrive interleaved on one socket, each tagged with
    its channel. The acks that confirm the subscriptions are protocol, not data, and never reach
    the caller's loop."""
    md = Channel.md(SERVER_ID, SYMBOL)
    results = Channel.results(TERMINAL_ID)
    transport = FakeTransport(
        [
            ack(md),
            ack(results),
            tick(md, 1),
            event(results, 1, "command.completed", command_id="c-1"),
            tick(md, 2, "1.09440"),
        ]
    )

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        await stream.subscribe(results)
        seen = await collect(stream, 3)

    assert [m.channel for m in seen] == [md, results, md]
    assert isinstance(seen[1], StreamMessage) and seen[1].type == "command.completed"
    assert seen[0].type is None, "a tick is its payload; it has no event type"
    assert seen[0].data["bid"] == "1.09431"
    assert stream.channels == (md, results)
    assert transport.last.sent == [
        {"op": "subscribe", "ch": md},
        {"op": "subscribe", "ch": results},
    ]


async def test_a_reconnect_resumes_what_replays_subscribes_what_does_not_and_counts_the_gaps(
    client: MfxClient, sleeps: list[float]
) -> None:
    """Given a stream watching ticks and results / When the connection is dropped and comes back /
    Then it waits a jittered backoff, resumes the results channel from the last seq it saw, plainly
    re-subscribes the tick channel, and reports what the sequence numbers prove it missed.

    The asymmetry is the platform's and it is deliberate: results and events replay for 15 minutes,
    ticks and candles never do, because a stale tick is worse than none. A stream that resumed
    ticks would hand a caller minutes-old prices that look live."""
    md = Channel.md(SERVER_ID, SYMBOL)
    results = Channel.results(TERMINAL_ID)
    transport = FakeTransport(
        [ack(md), ack(results), tick(md, 1), event(results, 7, "command.completed")],
        [
            ack(results),
            ack(md),
            # seq 9 after resuming from 7: one result the replay window could not reach.
            event(results, 9, "command.failed"),
            # The tick channel restarts its own numbering; it is not a gap.
            tick(md, 1, "1.09500"),
        ],
    )

    async with client.stream(connect=transport, max_reconnects=1) as stream:
        await stream.subscribe(md)
        await stream.subscribe(results)
        first = await collect(stream, 2)
        transport.sockets[0]._frames.append(StreamClosed(4009, "lifetime"))
        after = await collect(stream, 2)

    assert [m.seq for m in first] == [1, 7]
    assert transport.sockets[1].sent == [
        {"op": "subscribe", "ch": md},
        {"op": "resume", "ch": results, "after_seq": 7},
    ], "results resumes from where it was, md just re-subscribes"

    assert stream.stats.reconnects == 1
    assert stream.stats.lifetime_reconnects == 1, "4009 is expected, not a fault"
    assert stream.stats.dropped == 1, "seq 8 never arrived and the stream says so"
    assert sleeps, "the reconnect waited"
    assert [m.seq for m in after] == [9, 1], "the replay arrives, and the tick starts over"


async def test_a_slow_consumer_that_the_server_drops_is_reported_not_swallowed(
    client: MfxClient,
) -> None:
    """Close 4008 means this client fell too far behind and was dropped. Nothing is buffered on the
    caller's behalf — an internal queue would turn backpressure into a memory leak and feed the
    caller minutes-old prices — so the honest thing is to reconnect and say it happened."""
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport(
        [ack(md), tick(md, 1), StreamClosed(4008, "slow consumer")],
        [ack(md), tick(md, 1, "1.09600")],
    )

    async with client.stream(connect=transport, max_reconnects=1) as stream:
        await stream.subscribe(md)
        seen = await collect(stream, 2)

    assert len(seen) == 2
    assert stream.stats.slow_consumer_drops == 1
    assert stream.stats.reconnects == 1


async def test_a_revoked_key_stops_the_stream_rather_than_reconnecting_against_a_wall(
    client: MfxClient,
) -> None:
    """Close 4001 is re-authenticate. Every reconnect would meet the same refusal, and a client
    silently spinning on a revoked key is indistinguishable from an outage."""
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport([ack(md), StreamClosed(4001, "key revoked")], [ack(md)])

    with pytest.raises(AuthError, match="revoked"):
        async with client.stream(connect=transport) as stream:
            await stream.subscribe(md)
            await collect(stream, 1)

    assert len(transport.sockets) == 1, "it did not come back for more"


async def test_a_resync_is_delivered_as_news_not_raised_as_a_failure(client: MfxClient) -> None:
    """`resync` means the requested position is older than the replay window. That is the platform
    being honest, not an error: the remedy is to read current state over REST, and a raised
    exception would push a caller towards retrying instead."""
    results = Channel.results(TERMINAL_ID)
    transport = FakeTransport(
        [ack(results), event(results, 4, "command.completed"), {"op": "resync", "ch": results}],
        [ack(results)],
    )

    async with client.stream(connect=transport, max_reconnects=1) as stream:
        await stream.subscribe(results)
        seen = await collect(stream, 2)
        transport.sockets[0]._frames.append(StreamClosed(1006, ""))
        await collect(stream, 0)

    assert isinstance(seen[1], Resync) and seen[1].channel == results
    assert stream.stats.resyncs == 1
    assert transport.sockets[1].sent == [{"op": "subscribe", "ch": results}], (
        "after a resync there is no live position left to resume from"
    )


async def test_a_refused_channel_carries_the_platforms_own_code_to_the_caller(
    client: MfxClient,
) -> None:
    """A stream refusal is an MFX refusal. It carries the platform's own code, so a caller writes
    the same handling for both surfaces rather than parsing a string here and a status there.

    It arrives as a :class:`~mfx.streaming.ChannelRefused` rather than an exception: the
    code is the same, and the connection survives. An error naming no channel is still raised.
    """
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport(
        [
            ack(md),
            {
                "op": "error",
                "ch": md,
                "error": {"code": "forbidden", "message": "md:read is not in this key's scopes"},
            },
        ]
    )

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        [refusal] = await collect(stream, 1)

    assert isinstance(refusal, ChannelRefused)
    assert refusal.code == "forbidden"
    assert "md:read" in refusal.message


async def test_unsubscribing_stops_it_coming_back_after_the_next_reconnect(
    client: MfxClient,
) -> None:
    """The subscription set is what a reconnect replays. Dropping a channel has to drop it from
    that set too, or unsubscribe would last exactly until the next disconnection."""
    md = Channel.md(SERVER_ID, SYMBOL)
    candles = Channel.candles(SERVER_ID, SYMBOL, "M5")
    transport = FakeTransport([ack(md), ack(candles), StreamClosed(1006, "")], [ack(candles)])

    async with client.stream(connect=transport, max_reconnects=1) as stream:
        await stream.subscribe(md)
        await stream.subscribe(candles)
        await stream.unsubscribe(md)
        await collect(stream, 0)

    assert stream.channels == (candles,)
    assert {"op": "unsubscribe", "ch": md} in transport.sockets[0].sent
    assert transport.sockets[1].sent == [{"op": "subscribe", "ch": candles}]


async def test_subscribing_twice_is_not_an_error_and_an_unknown_op_is_not_fatal(
    client: MfxClient,
) -> None:
    """A caller re-asserting its subscriptions after its own restart should not have to remember
    what it already asked for. And an `op` added to the protocol after this SDK shipped is ignored
    rather than fatal — a new message type must not take a tenant's stream down."""
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport([ack(md), {"op": "invented_later", "ch": md}, tick(md, 1)])

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        await stream.subscribe(md)
        seen = await collect(stream, 1)

    assert stream.channels == (md,), "asked for twice, watched once"
    assert seen[0].seq == 1


async def test_a_message_on_a_channel_nobody_asked_for_is_delivered_without_being_counted(
    client: MfxClient,
) -> None:
    """Gap counting is per subscription, so a frame for a channel this stream does not track — an
    unsubscribe still in flight, or a server sending more than was asked for — has no baseline to
    be a gap against. It reaches the caller; it just does not invent a number."""
    md = Channel.md(SERVER_ID, SYMBOL)
    other = Channel.md(BROKER_ID, "XAUUSD")
    transport = FakeTransport(
        [ack(md), tick(other, 99), {"op": "msg", "ch": md, "data": {"bid": "1.1"}}]
    )

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        seen = await collect(stream, 2)

    assert [m.channel for m in seen] == [other, md]
    assert seen[1].seq is None, "a message without a seq is not given one"
    assert stream.stats.dropped == 0


async def test_iterating_a_closed_stream_ends_rather_than_reaching_for_a_dead_socket(
    client: MfxClient,
) -> None:
    """Closing is final. The loop finishes instead of raising from inside the SDK, so `async with`
    followed by a late iteration is untidy rather than a crash."""
    stream = client.stream(connect=FakeTransport([]))
    async with stream:
        pass

    assert [message async for message in stream] == []


async def test_sending_on_a_stream_that_was_never_opened_says_so(client: MfxClient) -> None:
    """A subscribe before the `async with` is a mistake worth naming, not an AttributeError from
    somewhere inside the SDK."""
    stream = client.stream(connect=FakeTransport([]))

    with pytest.raises(StreamClosed):
        await stream.subscribe(Channel.EVENTS)


async def test_a_stream_that_ends_for_good_stops_the_loop_rather_than_hanging(
    client: MfxClient,
) -> None:
    """When reconnecting is exhausted the iterator finishes. A stream that quietly stopped yielding
    while still awaiting would read, from the caller's side, as a market that had gone quiet."""
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport([ack(md), tick(md, 1)])

    async with client.stream(connect=transport, max_reconnects=0) as stream:
        await stream.subscribe(md)
        seen = [message async for message in stream]

    assert [m.seq for m in seen] == [1]
    assert stream.stats.reconnects == 0
    assert repr(stream).startswith("MfxStream('wss://ws.dev.mfxhub.com/v1/stream'")


async def test_a_stream_url_is_derived_from_whatever_base_the_client_was_given(
    private_key: Any, mfx: Any
) -> None:
    """Including bases that are not the `api.` host — a local or proxied deployment keeps its host
    and only its scheme changes, rather than being silently rewritten to something that does not
    exist."""
    transport = FakeTransport([])
    local = MfxClient("http://localhost:8080/v1", "key", private_key, transport=mfx.transport)

    async with local.stream(connect=transport):
        pass

    assert transport.urls == ["ws://localhost:8080/v1/stream"]
    await local.aclose()


async def test_the_default_transport_speaks_websockets_and_turns_a_close_into_a_stream_closed(
    client: MfxClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The one place the `websockets` library is touched. What matters is that a library close
    becomes this SDK's StreamClosed carrying the code, because every reconnect decision is made on
    that code — 4001 stop, 4009 expected, anything else back off and try."""
    import websockets.asyncio.client as ws_client
    from websockets.exceptions import ConnectionClosedError
    from websockets.frames import Close

    class LibrarySocket:
        def __init__(self) -> None:
            self.sent: list[str] = []
            self.closed = False
            self.frames: list[Any] = [b"{}", ConnectionClosedError(Close(4009, "bye"), None)]

        async def send(self, message: str) -> None:
            self.sent.append(message)

        async def recv(self) -> Any:
            frame = self.frames.pop(0)
            if isinstance(frame, Exception):
                raise frame
            return frame

        async def close(self) -> None:
            self.closed = True

    library_socket = LibrarySocket()
    seen_headers: dict[str, Any] = {}

    async def fake_connect(url: str, **kwargs: Any) -> LibrarySocket:
        seen_headers.update(kwargs.get("additional_headers") or {})
        return library_socket

    monkeypatch.setattr(ws_client, "connect", fake_connect)

    from mfx.streaming import websockets_connector

    connection = await websockets_connector("wss://ws.dev.mfxhub.com/v1/stream", {"X-MFX-Key": "k"})

    assert seen_headers == {"X-MFX-Key": "k"}
    assert await connection.recv() == "{}", "bytes and text frames both arrive as text"
    await connection.send("ping")
    assert library_socket.sent == ["ping"]

    with pytest.raises(StreamClosed) as closed:
        await connection.recv()
    assert closed.value.code == 4009 and closed.value.reason == "bye"

    await connection.close()
    assert library_socket.closed


async def test_a_caller_that_knows_it_is_behind_can_ask_for_one_channel_again(
    client: MfxClient,
) -> None:
    """Given a subscribed account channel
    When the caller resumes it before any message, after one, and resumes a channel it never
    subscribed to
    Then the first and last send subscribe, and the middle one sends resume with the seq it saw.

    The stream resumes for you across a *reconnect*; this is the
    other case, where nothing about the connection went wrong and only the caller can tell that its
    own view has fallen behind — a marks message it could not apply. The fallbacks matter as much
    as the happy path: resuming from a position that does not exist asks the platform for something
    it cannot answer, and leaves the caller holding a silent channel while believing it asked for a
    current one."""
    account = Channel.account(TERMINAL_ID)
    transport = FakeTransport([ack(account), event(account, 41, "account.snapshot", balance="10")])

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(account)
        await stream.resume(account)
        assert transport.last.sent[-1] == {"op": "subscribe", "ch": account}, (
            "nothing seen on it yet, so there is no position to resume from"
        )

        await collect(stream, 1)
        await stream.resume(account)
        assert transport.last.sent[-1] == {"op": "resume", "ch": account, "after_seq": 41}

        never = Channel.account(BROKER_ID)
        await stream.resume(never)
        assert transport.last.sent[-1] == {"op": "subscribe", "ch": never}


def error_frame(channel: str, code: str, message: str) -> dict[str, Any]:
    return {"op": "error", "ch": channel, "error": {"code": code, "message": message}}


async def test_one_refused_channel_costs_that_channel_and_not_the_connection(
    client: MfxClient,
) -> None:
    """Given a stream carrying three channels, one of which the platform refuses
    When the refusal arrives
    Then it is delivered as a ChannelRefused naming the channel and the reason, the subscription is
    dropped, and every other channel keeps flowing on the same connection.

    This is how it failed before: the refusal was raised out of
    ``async for message in stream`` and ended the connection. A tenant following hundreds of
    terminals would lose all of them because one terminal had been retired since it subscribed -
    and ``not_found`` is exactly what the platform answers for a terminal that is gone or was never
    this tenant's, so it is the common case, not an exotic one.
    """
    md = Channel.md(SERVER_ID, SYMBOL)
    gone = Channel.account(TERMINAL_ID)
    events = Channel.EVENTS
    transport = FakeTransport(
        [
            ack(md),
            ack(gone),
            ack(events),
            tick(md, 1),
            error_frame(gone, "not_found", "no such terminal"),
            tick(md, 2, "1.09440"),
            event(events, 1, "terminal.state_changed", state="ACTIVE"),
        ]
    )

    async with client.stream(connect=transport) as stream:
        for channel in (md, gone, events):
            await stream.subscribe(channel)
        seen = await collect(stream, 4)

        refusal = seen[1]
        assert isinstance(refusal, ChannelRefused)
        assert (refusal.channel, refusal.code) == (gone, "not_found")
        assert refusal.message == "no such terminal"

        assert [m.channel for m in seen] == [md, gone, md, events]
        assert seen[2].data["bid"] == "1.09440", "the healthy channel kept flowing"
        assert isinstance(seen[3], StreamMessage)
        assert stream.stats.refused == 1
        # Dropped, so a reconnect does not ask again and collect the same refusal for ever.
        assert stream.channels == (md, events)


async def test_an_error_about_the_connection_is_still_raised(client: MfxClient) -> None:
    """Given an error frame that names no channel
    When it arrives
    Then it is raised, because it is not about one channel and there is nothing left to deliver.

    The narrowness is the point: a refusal naming a channel costs that channel, and
    anything else - an authentication failure, a protocol error - still ends the stream, because
    continuing to read a connection the platform has disowned would be pretending.
    """
    md = Channel.md(SERVER_ID, SYMBOL)
    transport = FakeTransport(
        [ack(md), tick(md, 1), {"op": "error", "error": {"code": "auth_error", "message": "gone"}}]
    )

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        with pytest.raises(MfxApiError, match="gone") as raised:
            await collect(stream, 3)
    assert raised.value.code == "auth_error"
