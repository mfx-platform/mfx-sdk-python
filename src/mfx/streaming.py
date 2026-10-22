"""``client.stream()`` — the multiplexed WebSocket.

One connection carries every channel a tenant is watching: ticks, closed candles, platform events
and execution results. The caller writes one loop::

    async with client.stream() as stream:
        await stream.subscribe(Channel.md(server_id, "EURUSD.sd"))
        await stream.subscribe(Channel.results(terminal_id))
        async for event in stream:
            ...

Four things this module is opinionated about, each because the alternative loses data quietly:

* **Channels are keyed by id, never by display name**. Brokers rename servers and
  symbols, and a subscription keyed on a name silently stops matching when they do. :class:`Channel`
  builds the keys so a caller never formats one by hand, and refuses a key the platform would.

* **A reconnect resumes what can be resumed and says so about the rest.** Events and results carry
  a per-channel ``seq`` and are replayed from up to 15 minutes back, so the stream re-subscribes
  with ``resume`` and the caller misses nothing. Ticks and candles are *not* replayed, by design —
  a stale tick is worse than none — so those channels simply re-subscribe and the gap is counted
  rather than papered over.

* **Nothing is buffered on the caller's behalf.** The iterator reads from the socket directly, so a
  slow consumer applies real backpressure and is eventually dropped by the server with close code
  4008, which this reports. An internal unbounded queue would turn that into a memory leak and a
  consumer reading minutes-old prices believing they are live.

* **Gaps are counted, not hidden.** ``seq`` increases per channel; anything missing is arithmetic,
  and :attr:`MfxStream.stats` carries the total. A stream that cannot say what it missed cannot be
  reconciled against anything.

Authentication is the same Ed25519 signature as every REST call, over ``GET /v1/stream``, sent as
headers on the upgrade. (The spec's one-line summary for this path still says "HMAC at upgrade",
which predates request signing; the signed-request scheme is what the security scheme itself
defines.)
"""

from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from dataclasses import dataclass, field, replace
from types import TracebackType
from typing import TYPE_CHECKING, Any, Final, Literal, Protocol, Self
from uuid import UUID

from mfx.errors import AuthError, MfxError, error_for

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = [
    "Channel",
    "ChannelRefused",
    "MfxStream",
    "Resync",
    "StreamClosed",
    "StreamConnection",
    "StreamMessage",
    "StreamStats",
    "Timeframe",
]

Timeframe = Literal["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]

#: Exactly the platform's own pattern for a channel key (`StreamChannel`). Kept here as one string
#: so a key this SDK builds and a key the platform accepts cannot diverge.
#:
#: `account:` matches the published `StreamChannel`.
_CHANNEL_RE: Final = re.compile(
    r"^(md:[0-9a-f-]{36}:[^:]+"
    r"|candles:[0-9a-f-]{36}:[^:]+:(M1|M5|M15|M30|H1|H4|D1|W1|MN1)"
    r"|events"
    r"|results:[0-9a-f-]{36}"
    r"|account:[0-9a-f-]{36}"
    r"|ea:[0-9a-f-]{36}"
    r"|book:[0-9a-f-]{36}:[^:]+)$"
)

#: These replay on `resume`. Ticks and candles are deliberately not replayed.
#:
#: `ea:` replays up to 15 minutes, as `events` does (ea-telemetry.md). `book:` is not here: a book
#: is a state, and the platform answers every subscribe with the newest one, so subscribing again
#: after a reconnect loses nothing a resume would have given.
#:
#: `account:` is here for a different reason from the other two: resuming it replays nothing, it
#: answers with a current snapshot (the stream's resume rule). Resuming is still the right thing to
#: do — it is the documented remedy for a gap — so the channel belongs on this list; what it must
#: not do is be left off it and silently resubscribed from nothing after a reconnect.
_REPLAYABLE: Final = ("events", "results:", "account:", "ea:")

#: The server says why it hung up. 4001 is the one that reconnecting cannot fix.
CLOSE_REAUTHENTICATE: Final = 4001
CLOSE_SLOW_CONSUMER: Final = 4008
CLOSE_LIFETIME: Final = 4009


class StreamClosed(MfxError):  # noqa: N818 - it is a condition, not a failure of the caller's
    """The connection ended. ``code`` is the WebSocket close code, ``reason`` the server's words."""

    def __init__(self, code: int, reason: str = "") -> None:
        super().__init__(f"stream closed {code}: {reason}" if reason else f"stream closed {code}")
        self.code = code
        self.reason = reason


class StreamConnection(Protocol):
    """What this module needs of a WebSocket, and nothing more.

    Narrow on purpose: it keeps the library choice out of every other module, and it lets the
    reconnect and gap logic — the part that is easy to get wrong — be tested against a socket that
    closes exactly when the test says to.
    """

    async def send(self, message: str) -> None:
        """Send one text frame."""
        ...

    async def recv(self) -> str:
        """The next frame, or raise :class:`StreamClosed` when the connection has ended."""
        ...

    async def close(self) -> None:
        """Close the connection."""
        ...


#: Opens one connection: given the url and the signed upgrade headers, return a live socket.
Connector = Callable[[str, Mapping[str, str]], Awaitable[StreamConnection]]


@dataclass(frozen=True, slots=True)
class StreamMessage:
    """One message on one channel."""

    channel: str
    seq: int | None
    #: The event type on ``events`` and ``results`` (``command.completed``, ``feed.degraded`` …).
    #: None on a tick or a candle, which are the channel's only payload.
    type: str | None
    data: Mapping[str, Any]
    #: ``account:{terminal_id}`` only: the ``seq`` of the snapshot this message applies to, a
    #: snapshot's being its own (the stream's resume rule). None on every other channel, and on an
    #: account message from a platform that does not stamp it yet. :class:`mfx.LiveAccount` is
    #: what this is for — it is the whole of rule 2, and applying a mark without checking it
    #: silently merges a delta into a position set it was never measured against.
    base: int | None = None

    # There is deliberately no `replayed` flag. A `resume` replays messages the caller never saw
    # and the protocol marks no end to the replay, so the SDK cannot say where catching up stops
    # and live begins. `seq` is the ground truth a caller reconciles against; a flag that guessed
    # would be trusted exactly as if it knew.


@dataclass(frozen=True, slots=True)
class Resync:
    """The requested position is older than the replay window: read current state over REST.

    Delivered rather than raised, because it is not an error — it is the platform being honest that
    it cannot replay this far back, and the remedy is a read, not a retry.
    """

    channel: str


@dataclass(frozen=True, slots=True)
class ChannelRefused:
    """The platform refused one channel. Every other channel on this stream is unaffected.

    Delivered rather than raised. A refusal is about one channel, and raising it out of
    ``async for message in stream`` ended the whole connection: a tenant following hundreds of
    terminals lost every one of them because a single terminal had been retired since it last
    subscribed. That is the common case, not an exotic one - ``not_found`` is exactly what the
    platform answers for a terminal that is gone, or was never this tenant's.

    The subscription is dropped when this arrives, so a reconnect does not ask for it again and
    collect the same refusal for the life of the process. A caller that believes the channel should
    exist subscribes again and finds out again.

    An error that names no channel is about the connection itself and is still raised.
    """

    channel: str
    #: The platform's own code - ``not_found``, ``forbidden``, ``not_subscribed``.
    code: str
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)


StreamEvent = StreamMessage | Resync | ChannelRefused


@dataclass(frozen=True, slots=True)
class StreamStats:
    """What the stream missed and how often it had to come back."""

    #: Connections opened after the first one.
    reconnects: int = 0
    #: Messages the sequence numbers prove were not delivered, summed over every channel. On md and
    #: candles this is the server dropping oldest-first for a slow client; on events and results it
    #: is what `resume` could not reach.
    dropped: int = 0
    #: Channels told to resync because the replay window had passed.
    resyncs: int = 0
    #: Times the server closed us for falling behind (4008).
    slow_consumer_drops: int = 0
    #: Times the 24 h connection lifetime was reached (4009). Expected, not a fault.
    lifetime_reconnects: int = 0
    #: Channels the platform refused. Each one cost its own channel and nothing else.
    refused: int = 0


@dataclass(frozen=True, slots=True)
class _Subscription:
    channel: str
    last_seq: int | None = None


@dataclass
class _State:
    subscriptions: dict[str, _Subscription] = field(default_factory=dict)
    stats: StreamStats = field(default_factory=StreamStats)


class Channel:
    """Builds the channel keys the platform accepts, from ids rather than names."""

    #: Every platform event for this tenant. One channel, because they are not per-object.
    EVENTS: Final = "events"

    @staticmethod
    def md(server_id: str | UUID, symbol: str) -> str:
        """Ticks for one symbol on one server, in the broker's own name for it."""
        return _checked(f"md:{server_id}:{symbol}")

    @staticmethod
    def candles(server_id: str | UUID, symbol: str, timeframe: Timeframe) -> str:
        """Closed candles. Only closed ones are published — a forming candle is not a fact yet."""
        return _checked(f"candles:{server_id}:{symbol}:{timeframe}")

    @staticmethod
    def results(terminal_id: str | UUID) -> str:
        """Execution results for one terminal: where a 202 command_id is finally answered."""
        return _checked(f"results:{terminal_id}")

    @staticmethod
    def account(terminal_id: str | UUID) -> str:
        """One terminal's live account: a snapshot, then marks.

        Account *state* has its own channel per terminal rather than riding ``events``, because
        state is latest-wins and events may not be lost: at thousands of terminals, snapshots
        competing with fills for one 15-minute replay window turns that window over in seconds.
        Use :class:`mfx.LiveAccount` to merge what arrives; ``position.opened``/``closed`` still
        arrive on ``events``, which is where notifications and history belong.
        """
        return _checked(f"account:{terminal_id}")

    @staticmethod
    def ea(terminal_id: str | UUID) -> str:
        """What the tenant's own expert on this terminal writes (ea-telemetry.md): batches of its
        records as ``expert_advisor.telemetry``, and ``expert_advisor.telemetry_lost`` when the
        cell had to discard some. Needs ``ea:read``. Replayed up to 15 minutes on resume."""
        return _checked(f"ea:{terminal_id}")

    @staticmethod
    def book(server_id: str | UUID, symbol: str) -> str:
        """The symbol's order book as one of the tenant's terminals reads it: an
        ``md.book`` message with the whole book each time it changes; read it with
        :func:`mfx.md.book_of`. Granted as :meth:`md` is - ``md:read`` and a live subscription to
        the symbol - and it carries nothing until a terminal on that server reads the symbol's
        depth (``depth_instruments``, :meth:`mfx.terminals.Terminals.replace_instruments`)."""
        return _checked(f"book:{server_id}:{symbol}")


def _checked(channel: str) -> str:
    if not _CHANNEL_RE.match(channel):
        raise ValueError(
            f"{channel!r} is not a channel key the platform accepts. Ids are uuids and a symbol "
            "carries no colon; see StreamChannel in the spec."
        )
    return channel


def _replayable(channel: str) -> bool:
    return channel.startswith(_REPLAYABLE)


class MfxStream:
    """The multiplexed stream. Opened with ``async with client.stream() as stream``."""

    def __init__(
        self,
        client: MfxClient,
        *,
        connect: Connector,
        url: str | None = None,
        max_reconnects: int | None = None,
    ) -> None:
        self._client = client
        self._connect = connect
        self._url = url or _ws_url(client.base_url)
        self._max_reconnects = max_reconnects
        self._state = _State()
        self._connection: StreamConnection | None = None

    @property
    def stats(self) -> StreamStats:
        """What has been missed so far. A snapshot; it never mutates under the caller."""
        return self._state.stats

    @property
    def channels(self) -> tuple[str, ...]:
        """The channels currently subscribed, in the order they were asked for."""
        return tuple(self._state.subscriptions)

    async def subscribe(self, channel: str) -> None:
        """Subscribe to one channel. The platform acknowledges it on the stream.

        Subscribing twice is not an error: the channel is already being watched, and a caller
        re-asserting its subscriptions after its own restart should not have to remember.
        """
        _checked(channel)
        if channel not in self._state.subscriptions:
            self._state.subscriptions[channel] = _Subscription(channel)
        await self._send({"op": "subscribe", "ch": channel})

    async def resume(self, channel: str) -> None:
        """Ask the platform to bring one channel back up to date, from the last seq seen.

        The SDK does this for you across a reconnect. This is for the other case: the caller has
        noticed, from the data itself, that its own view is behind — which only it can know. On
        ``account:{terminal_id}`` that is the documented remedy for a `seq` gap or an unapplicable
        marks message (the stream's resume rule), and the answer there is a fresh snapshot rather
        than a replay.

        On a channel that does not replay, and on one never subscribed, this subscribes instead of
        resuming. Both are the honest request: there is no position to resume from, so asking to
        carry on from one would be asking for something the platform cannot give, and a caller
        would be left with a silent channel rather than a current one.
        """
        _checked(channel)
        subscription = self._state.subscriptions.get(channel)
        if subscription is None or not _replayable(channel) or subscription.last_seq is None:
            await self.subscribe(channel)
            return
        await self._send({"op": "resume", "ch": channel, "after_seq": subscription.last_seq})

    async def unsubscribe(self, channel: str) -> None:
        """Stop watching a channel, and stop resubscribing to it after a reconnect."""
        self._state.subscriptions.pop(channel, None)
        await self._send({"op": "unsubscribe", "ch": channel})

    async def __aenter__(self) -> Self:
        await self._open()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the stream's connection, if one is open. ``async with`` does this for you."""
        connection, self._connection = self._connection, None
        if connection is not None:
            await connection.close()

    def __aiter__(self) -> AsyncIterator[StreamEvent]:
        return self._events()

    async def _events(self) -> AsyncIterator[StreamEvent]:
        while True:
            event = await self._next()
            if event is None:
                return
            yield event

    async def _next(self) -> StreamEvent | None:
        """The next event the caller cares about, reconnecting underneath as needed.

        Returns None when the stream is done: the server closed normally and there is nothing left
        to reconnect for.
        """
        while True:
            connection = self._connection
            if connection is None:
                return None
            try:
                raw = await connection.recv()
            except StreamClosed as closed:
                if not await self._reopen(closed):
                    return None
                continue
            event = self._interpret(raw)
            if event is not None:
                return event

    def _interpret(self, raw: str) -> StreamEvent | None:
        """One server frame. Returns None for a frame the caller has no use for (an ack)."""
        message = json.loads(raw)
        op = message.get("op")
        channel = str(message.get("ch") or "")
        if op == "error":
            body = message.get("error") or {}
            code = str(body.get("code") or "stream_error")
            text = str(body.get("message") or f"stream error on {channel or 'the connection'}")
            raw_details = body.get("details")
            details: dict[str, Any] = raw_details if isinstance(raw_details, dict) else {}
            if channel:
                # One channel's refusal costs that channel. Dropped from the state so a
                # reconnect does not re-ask and be refused again for the life of the process.
                self._state.subscriptions.pop(channel, None)
                self._bump(refused=1)
                return ChannelRefused(channel, code, text, details)
            # Typed by the platform's code, as a call's answer is: a tenant the
            # operator disabled meets TenantDisabledError here too. Status 0: no HTTP answer.
            raise error_for(code, text, status=0, details=details)
        if op == "resync":
            self._bump(resyncs=1)
            # The replay window has passed, so there is no position to resume from any more.
            # Forgetting it here is what stops the next reconnect asking for the same dead seq.
            self._forget(channel)
            return Resync(channel)
        if op == "ack":
            return None  # protocol, not data
        if op != "msg":
            return None  # an op added after this SDK shipped; ignored rather than fatal
        seq = message.get("seq")
        seq = int(seq) if isinstance(seq, int) else None
        base = message.get("base")
        self._account_for(channel, seq)
        data = message.get("data")
        return StreamMessage(
            channel=channel,
            seq=seq,
            type=str(message["type"]) if message.get("type") is not None else None,
            data=data if isinstance(data, dict) else {},
            base=int(base) if isinstance(base, int) else None,
        )

    def _account_for(self, channel: str, seq: int | None) -> None:
        """Count what the sequence numbers prove was not delivered."""
        subscription = self._state.subscriptions.get(channel)
        if subscription is None or seq is None:
            return
        last = subscription.last_seq
        if last is not None and seq > last + 1:
            self._bump(dropped=seq - last - 1)
        self._state.subscriptions[channel] = replace(subscription, last_seq=seq)

    def _forget(self, channel: str) -> None:
        subscription = self._state.subscriptions.get(channel)
        if subscription is not None:
            self._state.subscriptions[channel] = replace(subscription, last_seq=None)

    def _bump(self, **counts: int) -> None:
        current = self._state.stats
        self._state.stats = replace(
            current, **{name: getattr(current, name) + n for name, n in counts.items()}
        )

    async def _open(self) -> None:
        headers = self._client.signature.headers_for("GET", _path_of(self._url))
        self._connection = await self._connect(self._url, headers)

    async def _reopen(self, closed: StreamClosed) -> bool:
        """Come back after a close, or say the stream is over. Raises when reconnecting cannot help.

        4001 is re-authenticate: the key was rotated, expired or revoked, and every reconnect would
        meet the same wall. It is raised rather than retried, because a client silently spinning on
        a revoked key is indistinguishable from an outage.
        """
        if closed.code == CLOSE_REAUTHENTICATE:
            self._connection = None
            raise AuthError(
                closed.reason or "the stream's credentials were rotated, expired or revoked",
                status=401,
                code="auth_error",
            )
        if closed.code == CLOSE_SLOW_CONSUMER:
            self._bump(slow_consumer_drops=1)
        elif closed.code == CLOSE_LIFETIME:
            self._bump(lifetime_reconnects=1)
        if (
            self._max_reconnects is not None
            and self._state.stats.reconnects >= self._max_reconnects
        ):
            self._connection = None
            return False
        self._bump(reconnects=1)
        # The client's own jittered backoff, so the stream and the read path cannot disagree about
        # how hard this tenant leans on MFX while it is unwell.
        await self._client.pause(self._client.backoff_for(self._state.stats.reconnects))
        await self._open()
        await self._resubscribe()
        return True

    async def _resubscribe(self) -> None:
        """Ask for everything again — resuming what replays, plain subscribing what does not."""
        for subscription in list(self._state.subscriptions.values()):
            if _replayable(subscription.channel) and subscription.last_seq is not None:
                await self._send(
                    {
                        "op": "resume",
                        "ch": subscription.channel,
                        "after_seq": subscription.last_seq,
                    }
                )
            else:
                # Ticks and candles are never replayed, so the position is meaningless across a
                # reconnect; dropping it stops the next gap being counted against a stale seq.
                if not _replayable(subscription.channel):
                    self._forget(subscription.channel)
                await self._send({"op": "subscribe", "ch": subscription.channel})

    async def _send(self, message: Mapping[str, Any]) -> None:
        connection = self._connection
        if connection is None:
            raise StreamClosed(1006, "the stream is not open")
        await connection.send(json.dumps(message, separators=(",", ":")))

    def __repr__(self) -> str:
        return f"MfxStream({self._url!r}, channels={len(self._state.subscriptions)})"


def _ws_url(base_url: str) -> str:
    """The stream url beside the REST base: ``api.dev.mfxhub.com`` → ``ws.dev.mfxhub.com``.

    Derived rather than configured, so a caller that has pointed the client at dev cannot leave its
    stream pointed at production.
    """
    url = base_url.rstrip("/")
    url = url.replace("https://", "wss://", 1).replace("http://", "ws://", 1)
    url = url.replace("://api.", "://ws.", 1)
    return f"{url}/stream" if not url.endswith("/stream") else url


def _path_of(url: str) -> str:
    """The path the signature covers, which is the path only — never the host."""
    without_scheme = url.split("://", 1)[-1]
    slash = without_scheme.find("/")
    return without_scheme[slash:] if slash >= 0 else "/"


async def websockets_connector(url: str, headers: Mapping[str, str]) -> StreamConnection:
    """The default transport, over ``websockets``.

    Imported here rather than at module load so the rest of the SDK — and anyone supplying their
    own connector — does not pay for it.
    """
    from websockets.asyncio.client import connect as ws_connect  # noqa: PLC0415 - see docstring
    from websockets.exceptions import ConnectionClosed  # noqa: PLC0415

    socket = await ws_connect(url, additional_headers=dict(headers))

    class _Connection:
        async def send(self, message: str) -> None:
            await socket.send(message)

        async def recv(self) -> str:
            try:
                frame = await socket.recv()
            except ConnectionClosed as closed:
                raise StreamClosed(
                    closed.rcvd.code if closed.rcvd else 1006,
                    closed.rcvd.reason if closed.rcvd else "",
                ) from closed
            return frame if isinstance(frame, str) else frame.decode("utf-8")

        async def close(self) -> None:
            await socket.close()

    return _Connection()
