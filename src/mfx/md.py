"""``client.md`` — the market-data subscriptions a stream's price channels depend on.

**Subscribing on the stream is not enough.** ``md:{server_id}:{symbol}`` answers
``not_subscribed: subscribe to the symbol first`` until the symbol has a subscription here: the
stream carries what the platform is already fanning out, and this is what asks for it to be fanned
out. A tenant reading only :mod:`mfx.streaming` has no way to discover that, which is why this
surface exists rather than leaving the generated call to be found.

The order is always the same:

.. code-block:: python

    await client.md.subscribe(server_id, "EURUSD.sd", idempotency_key=key)
    async with client.stream() as stream:
        await stream.subscribe(Channel.md(server_id, "EURUSD.sd"))

A subscription outlives the stream. It is the tenant's standing request for that symbol on that
server, counted against the plan, and it stays until :meth:`unsubscribe` — closing a connection
does not drop it, and a reconnect does not need to re-create it.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import AsyncIterator
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Final
from uuid import UUID

from mfx._generated.api.md import (
    create_subscription as _create_subscription,
)
from mfx._generated.api.md import (
    delete_subscription as _delete_subscription,
)
from mfx._generated.api.md import (
    get_candles as _get_candles,
)
from mfx._generated.api.md import (
    get_ticks as _get_ticks,
)
from mfx._generated.api.md import (
    list_subscriptions as _list_subscriptions,
)
from mfx._generated.models.get_candles_tf import GetCandlesTf
from mfx._generated.models.md_subscription import MdSubscription
from mfx._generated.models.md_subscription_create import MdSubscriptionCreate
from mfx._generated.models.md_subscription_create_delivery import MdSubscriptionCreateDelivery
from mfx._generated.models.md_subscription_create_timeframes_item import (
    MdSubscriptionCreateTimeframesItem,
)
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of

if TYPE_CHECKING:  # pragma: no cover - typing only
    from collections.abc import Mapping

    from mfx._generated.models.candle_list import CandleList
    from mfx._generated.models.tick import Tick
    from mfx._generated.models.tick_list import TickList
    from mfx.client import MfxClient
    from mfx.streaming import StreamMessage

__all__ = [
    "Book",
    "MarketData",
    "SubscriptionDegraded",
    "SubscriptionRecovered",
    "book_of",
    "subscription_event",
]

#: The two messages on ``events`` that say a subscription stopped delivering and delivers again
#:.
DEGRADED: Final = "md.subscription_degraded"
RECOVERED: Final = "md.subscription_recovered"
#: The message on ``book:{server_id}:{symbol}``.
BOOK: Final = "md.book"

#: Ids are uuids on the wire; a caller holding a string from its own database should not have to
#: know that. The same rule as `mfx.terminals.Id`.
Id = str | UUID


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


@dataclass(frozen=True, slots=True)
class SubscriptionDegraded:
    """A subscription whose symbol cannot tick, or should be ticking and is not.

    Sent once, when it becomes degraded. A closed market is not a degradation, and neither is a
    terminal that restarts and is back inside a few minutes. ``reason`` is the platform's own
    word and is text, not a closed list: ``symbol_removed``, ``subscription_refused``,
    ``terminal_disconnected``, ``report_stale`` and ``no_ticks_in_session`` today, and a
    platform that learns another will send it. A reason that gives way to another while the
    subscription stays degraded sends nothing; read the subscription for the one that holds.
    """

    subscription_id: UUID
    broker_id: UUID
    server_id: UUID
    symbol: str
    reason: str
    since: dt.datetime
    #: The symbol's last tick, or None when it has never ticked.
    last_tick_at: dt.datetime | None


@dataclass(frozen=True, slots=True)
class SubscriptionRecovered:
    """A degraded subscription that is delivering again. Sent once.

    ``reason`` is what it recovered from and ``since`` when it had become degraded, so the two
    together with ``recovered_at`` are the whole gap, without the first message being kept.
    """

    subscription_id: UUID
    broker_id: UUID
    server_id: UUID
    symbol: str
    reason: str
    since: dt.datetime
    recovered_at: dt.datetime
    last_tick_at: dt.datetime | None


@dataclass(frozen=True, slots=True)
class Book:
    """A symbol's whole order book as one terminal read it. Replace yours with every one.

    Prices and volumes are :class:`~decimal.Decimal`, exact as the platform sent them. ``levels``
    is the most a side the platform reads, so a side shorter than it is the broker's whole side.
    Not a reconstruction: MFX Hub builds no book from ticks or from several terminals.
    """

    channel: str
    seq: int | None
    #: Buy orders, highest price first: ``(price, volume)``.
    bids: tuple[tuple[Decimal, Decimal], ...]
    #: Sell orders, lowest price first.
    asks: tuple[tuple[Decimal, Decimal], ...]
    #: When the terminal read it, on the broker's clock, as a tick's ``broker_ts``.
    broker_ts: str
    levels: int

    @property
    def best_bid(self) -> Decimal | None:
        """The highest buy price, or None when the book has no bids."""
        return self.bids[0][0] if self.bids else None

    @property
    def best_ask(self) -> Decimal | None:
        """The lowest sell price, or None when the book has no asks."""
        return self.asks[0][0] if self.asks else None


def _side(raw: Any) -> tuple[tuple[Decimal, Decimal], ...]:  # noqa: ANN401 - the message's list
    if not isinstance(raw, list):
        raise ValueError("a book side is a list of [price, volume]")
    return tuple((Decimal(str(level[0])), Decimal(str(level[1]))) for level in raw)


def book_of(message: StreamMessage) -> Book | None:
    """A message from a ``book:`` channel as the :class:`Book` it is, or None for any other.

    .. code-block:: python

        await stream.subscribe(Channel.book(server_id, "XAUUSD"))
        async for message in stream:
            book = book_of(message)
            if book is not None:
                spread = book.best_ask - book.best_bid

    The first message after a subscribe is the newest book the platform holds; each later one is
    a change. A gap in ``seq`` is a book superseded before it reached you, not a lost fact.
    """
    if getattr(message, "type", None) != BOOK:
        return None
    data: Mapping[str, Any] = message.data
    return Book(
        channel=message.channel,
        seq=message.seq,
        bids=_side(data.get("bids")),
        asks=_side(data.get("asks")),
        broker_ts=str(data["broker_ts"]),
        levels=int(data["levels"]),
    )


def _instant(raw: Any) -> dt.datetime | None:  # noqa: ANN401 - whatever the message carried
    return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")) if isinstance(raw, str) else None


def subscription_event(
    message: StreamMessage,
) -> SubscriptionDegraded | SubscriptionRecovered | None:
    """A message from ``events`` as the subscription-health event it is, or None for any other.

    .. code-block:: python

        async for message in stream:
            health = subscription_event(message)
            if isinstance(health, SubscriptionDegraded):
                pause(health.symbol, why=health.reason)

    A subscription keeps its stream while it is degraded: nothing needs subscribing again when
    it recovers. The same two facts are on the subscription itself (``state``,
    ``degraded_reason``, ``degraded_since``) for a caller that was not listening.
    """
    kind = getattr(message, "type", None)
    if kind not in (DEGRADED, RECOVERED):
        return None
    data: Mapping[str, Any] = message.data
    since = _instant(data["since"])
    if since is None:
        raise ValueError(f"{kind} carries no `since`")
    subscription_id = UUID(str(data["subscription_id"]))
    broker_id, server_id = UUID(str(data["broker_id"])), UUID(str(data["server_id"]))
    symbol, reason = str(data["symbol"]), str(data["reason"])
    last_tick_at = _instant(data.get("last_tick_at"))
    if kind == DEGRADED:
        return SubscriptionDegraded(
            subscription_id=subscription_id,
            broker_id=broker_id,
            server_id=server_id,
            symbol=symbol,
            reason=reason,
            since=since,
            last_tick_at=last_tick_at,
        )
    recovered_at = _instant(data["recovered_at"])
    if recovered_at is None:
        raise ValueError(f"{kind} carries no `recovered_at`")
    return SubscriptionRecovered(
        subscription_id=subscription_id,
        broker_id=broker_id,
        server_id=server_id,
        symbol=symbol,
        reason=reason,
        since=since,
        recovered_at=recovered_at,
        last_tick_at=last_tick_at,
    )


class MarketData:
    """``client.md`` — what this tenant has asked to be streamed."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def subscribe(
        self,
        server_id: Id,
        symbol: str,
        *,
        idempotency_key: str,
        timeframes: list[str] | None = None,
    ) -> MdSubscription:
        """Ask for a symbol's ticks on one broker server, and optionally its candles.

        ``symbol`` is the broker's own name, exactly as the tenant's catalogue lists it
        (``EURUSD.sd``, not ``EURUSD``): a broker's suffix is part of the name, and the platform
        matches what the terminal reports rather than guessing.

        ``timeframes`` names the candles to build; none means ticks only. Candles arrive on their
        own channel, ``candles:{server_id}:{symbol}:{tf}``.

        Subscribing twice with the same ``idempotency_key`` returns the same subscription rather
        than a second one.
        """
        subscription = await self._client.write(
            lambda: _create_subscription.asyncio_detailed(
                client=self._client.generated,
                body=MdSubscriptionCreate(
                    server_id=_uuid(server_id),
                    symbol=symbol,
                    timeframes=(
                        [MdSubscriptionCreateTimeframesItem(t) for t in timeframes]
                        if timeframes
                        else UNSET
                    ),
                    delivery=MdSubscriptionCreateDelivery.WS,
                ),
                idempotency_key=idempotency_key,
            ),
            "POST /md/subscriptions",
        )
        return subscription  # type: ignore[no-any-return]

    async def subscriptions(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[MdSubscription]:
        """One page of what this tenant has subscribed, newest first."""
        parsed = await self._client.read(
            lambda: _list_subscriptions.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            "GET /md/subscriptions",
        )
        return page_of(parsed)

    async def all_subscriptions(self) -> AsyncIterator[MdSubscription]:
        """Every subscription, following the cursor."""
        cursor: str | None = None
        while True:
            page = await self.subscriptions(cursor=cursor)
            for subscription in page.items:
                yield subscription
            if not page.next_cursor:
                return
            cursor = page.next_cursor

    async def unsubscribe(self, subscription_id: Id, *, idempotency_key: str) -> None:
        """Stop streaming this symbol. The channel stops; nothing else is affected."""
        await self._client.write(
            lambda: _delete_subscription.asyncio_detailed(
                id=_uuid(subscription_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"DELETE /md/subscriptions/{subscription_id}",
        )

    async def candles(
        self,
        broker: Id,
        symbol: str,
        timeframe: str,
        *,
        from_: dt.datetime,
        to: dt.datetime,
        limit: int | None = None,
        server_id: Id | None = None,
    ) -> CandleList:
        """A symbol's bars for a window, oldest first: at most 1,000 a call.

        The bars are the ones the broker's server shows the tenant's own account, read through
        one of its ACTIVE terminals on that server. When the window
        holds more than ``limit`` bars the answer is the **newest** of them, so a chart asking
        for "up to now" gets the bars nearest now; ask again with an earlier ``to`` for the
        ones before. The bar still forming is included when the window reaches it: its close
        is the last price.

        ``timeframe`` is one of M1, M5, M15, M30, H1, H4, D1, W1, MN1; any other is a
        ``ValueError`` here, before the wire. Each bar's ``ts`` is its open time as a true
        instant: a daily bar opens at the broker's midnight, which is not UTC midnight.
        ``symbol`` is the broker's own name. With terminals on more than one of the broker's
        servers, name ``server_id``. No bar in the window is an empty answer, not an error.
        """
        tf = GetCandlesTf(timeframe)
        parsed = await self._client.read(
            lambda: _get_candles.asyncio_detailed(
                client=self._client.generated,
                broker=str(broker),
                symbol=symbol,
                tf=tf,
                from_=from_,
                to=to,
                limit=limit if limit is not None else UNSET,
                server_id=str(server_id) if server_id is not None else UNSET,
            ),
            "GET /md/candles",
        )
        return parsed  # type: ignore[no-any-return]

    async def ticks(
        self,
        broker: Id,
        symbol: str,
        *,
        from_: dt.datetime,
        to: dt.datetime | None = None,
        limit: int | None = None,
        server_id: Id | None = None,
    ) -> TickList:
        """One read of tick history: the first ``limit`` ticks at or after ``from_``, oldest first.

        The ticks are the ones the broker's server keeps for the tenant's own account, read
        through one of its ACTIVE terminals on that server; MFX keeps no tick
        store of its own, so how far back they go is the broker's to say. At most 1,000 a call,
        which is also the default. ``to`` leaves out ticks after it. ``more`` on the answer is true
        when the window holds ticks beyond the ones returned - :meth:`all_ticks` follows it.

        ``symbol`` is the broker's own name. With terminals on more than one of the broker's
        servers, name ``server_id``.
        """
        parsed = await self._client.read(
            lambda: _get_ticks.asyncio_detailed(
                client=self._client.generated,
                broker=str(broker),
                symbol=symbol,
                from_=from_,
                to=to if to is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                server_id=str(server_id) if server_id is not None else UNSET,
            ),
            "GET /md/ticks",
        )
        return parsed  # type: ignore[no-any-return]

    async def all_ticks(
        self,
        broker: Id,
        symbol: str,
        *,
        from_: dt.datetime,
        to: dt.datetime | None = None,
        page_size: int | None = None,
        server_id: Id | None = None,
    ) -> AsyncIterator[Tick]:
        """Every tick of a window, in order, each once, a call at a time.

        The contract's way to continue is to ask again from the last tick's time, and several
        ticks can share one millisecond, so the next answer begins with ticks already held. This
        drops exactly those and yields the rest, which is easy to get subtly wrong by hand: drop
        by time alone and ticks are lost, drop nothing and they are doubled.

        Every call is a round trip to a cell (a busy symbol passes 100,000 ticks a day): this is
        for reading history. The stream is the way to follow ticks as they happen.
        """
        start = from_
        held: list[tuple[object, ...]] = []
        while True:
            answer = await self.ticks(
                broker, symbol, from_=start, to=to, limit=page_size, server_id=server_id
            )
            fresh = []
            for tick in answer.items:
                key = (tick.ts, tick.bid, tick.ask, tick.last, tick.volume)
                if tick.ts == start and key in held:
                    held.remove(key)
                    continue
                fresh.append(tick)
            for tick in fresh:
                yield tick
            if not answer.more or not fresh:
                # Nothing new with more promised is one millisecond holding more ticks than a
                # call returns; asking again would return the same ones for ever.
                return
            start = answer.items[-1].ts
            held = [
                (tick.ts, tick.bid, tick.ask, tick.last, tick.volume)
                for tick in answer.items
                if tick.ts == start
            ]
