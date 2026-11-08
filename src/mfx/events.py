"""The order, position, terminal and candle events, as typed values.

The platform sends these on the stream with every value as text. :func:`event_of` reads one
message as the event it is, or None for any other:

.. code-block:: python

    async for message in stream:
        event = mfx.event_of(message)
        if isinstance(event, mfx.OrderClosed) and event.reason == "filled":
            print("order", event.ticket, "became position", event.position_ticket)

Ids are UUIDs, tickets and magic numbers integers, prices, volumes and money Decimals, and times
aware UTC datetimes. The platform's own words (``side``, ``order_type``, ``reason``,
``close_reason``, a terminal's states, a candle's ``timeframe``) stay text: they are not a closed
list, and a word the platform adds later reads as it was written instead of failing the read.

A message keeps its ``data`` whatever this returns, so nothing is lost by a type this version
does not know.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, Final
from uuid import UUID

from mfx.streaming import StreamMessage

__all__ = [
    "EVENT_KINDS",
    "CandleClosed",
    "Event",
    "OrderClosed",
    "OrderModified",
    "OrderPlaced",
    "PositionClosed",
    "PositionModified",
    "PositionOpened",
    "TerminalStateChanged",
    "event_of",
]


class _Data:
    """One message's ``data``, read by the contract's rules: a required field that is missing is a
    ValueError naming it; an optional one that is absent or null is None."""

    __slots__ = ("_data", "_kind")

    def __init__(self, kind: str, data: Mapping[str, Any]) -> None:
        self._kind, self._data = kind, data

    def _raw(self, key: str, required: bool) -> Any:  # noqa: ANN401 - whatever the message carried
        value = self._data.get(key)
        if value is None and required:
            raise ValueError(f"{self._kind} carries no `{key}`")
        return value

    def text(self, key: str) -> str:
        return str(self._raw(key, True))

    def text_or_none(self, key: str) -> str | None:
        value = self._raw(key, False)
        return None if value is None else str(value)

    def uuid(self, key: str) -> UUID:
        return UUID(str(self._raw(key, True)))

    def integer(self, key: str) -> int:
        return int(str(self._raw(key, True)))

    def integer_or_none(self, key: str) -> int | None:
        value = self._raw(key, False)
        return None if value is None else int(str(value))

    def decimal(self, key: str) -> Decimal:
        return Decimal(str(self._raw(key, True)))

    def decimal_or_none(self, key: str) -> Decimal | None:
        value = self._raw(key, False)
        return None if value is None else Decimal(str(value))

    def instant(self, key: str) -> dt.datetime:
        return _instant(str(self._raw(key, True)))

    def instant_or_none(self, key: str) -> dt.datetime | None:
        value = self._raw(key, False)
        return None if value is None else _instant(str(value))


def _instant(raw: str) -> dt.datetime:
    moment = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=dt.UTC)


@dataclass(frozen=True, slots=True, kw_only=True)
class _Order:
    """A pending order (a buy or sell limit, stop or stop-limit order), as its events carry it."""

    schema_version: str
    terminal_id: UUID
    #: The same for a replay of the same change: drop one you have seen.
    event_id: str
    ticket: int
    symbol: str
    #: ``buy`` or ``sell``.
    side: str
    #: ``limit``, ``stop`` or ``stop_limit``.
    order_type: str
    #: Lots still to fill.
    volume: Decimal
    #: On a stop-limit order, the stop price.
    price: Decimal
    #: A stop-limit order's limit, placed when the market reaches ``price``.
    stop_limit_price: Decimal | None
    sl: Decimal | None
    tp: Decimal | None
    placed_time: dt.datetime
    #: None when good till cancelled.
    expires_at: dt.datetime | None
    magic: int
    comment: str
    ts: dt.datetime
    #: The Idempotency-Key of the platform command that made this change; None for a change the
    #: platform did not make.
    idempotency_key: str | None


def _order_fields(d: _Data) -> dict[str, Any]:
    return {
        "schema_version": d.text("schema_version"),
        "terminal_id": d.uuid("terminal_id"),
        "event_id": d.text("event_id"),
        "ticket": d.integer("ticket"),
        "symbol": d.text("symbol"),
        "side": d.text("side"),
        "order_type": d.text("order_type"),
        "volume": d.decimal("volume"),
        "price": d.decimal("price"),
        "stop_limit_price": d.decimal_or_none("stop_limit_price"),
        "sl": d.decimal_or_none("sl"),
        "tp": d.decimal_or_none("tp"),
        "placed_time": d.instant("placed_time"),
        "expires_at": d.instant_or_none("expires_at"),
        "magic": d.integer("magic"),
        "comment": d.text("comment"),
        "ts": d.instant("ts"),
        "idempotency_key": d.text_or_none("idempotency_key"),
    }


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderPlaced(_Order):
    """``order.placed``: a pending order appeared on the account, placed by anyone."""

    KIND: ClassVar[str] = "order.placed"


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderModified(_Order):
    """``order.modified``: a pending order's price, stops, expiry or volume changed."""

    KIND: ClassVar[str] = "order.modified"


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderClosed(_Order):
    """``order.closed``: a pending order left the account. On ``filled``, ``position_ticket`` is
    the position it became (also on that position's ``order_ticket``)."""

    KIND: ClassVar[str] = "order.closed"
    #: ``filled``, ``cancelled``, ``expired``, ``rejected`` or ``unknown`` today.
    reason: str
    #: MetaTrader's own word for the order's last state, when the reason was read from it.
    order_state_raw: str | None
    position_ticket: int | None


@dataclass(frozen=True, slots=True, kw_only=True)
class _Position:
    schema_version: str
    terminal_id: UUID
    event_id: str
    ticket: int
    symbol: str
    #: ``buy`` or ``sell``.
    side: str
    volume: Decimal
    open_price: Decimal
    price_current: Decimal | None
    sl: Decimal | None
    tp: Decimal | None
    profit: Decimal | None
    swap: Decimal | None
    open_time: dt.datetime
    magic: int
    comment: str
    ts: dt.datetime
    idempotency_key: str | None


def _position_fields(d: _Data) -> dict[str, Any]:
    return {
        "schema_version": d.text("schema_version"),
        "terminal_id": d.uuid("terminal_id"),
        "event_id": d.text("event_id"),
        "ticket": d.integer("ticket"),
        "symbol": d.text("symbol"),
        "side": d.text("side"),
        "volume": d.decimal("volume"),
        "open_price": d.decimal("open_price"),
        "price_current": d.decimal_or_none("price_current"),
        "sl": d.decimal_or_none("sl"),
        "tp": d.decimal_or_none("tp"),
        "profit": d.decimal_or_none("profit"),
        "swap": d.decimal_or_none("swap"),
        "open_time": d.instant("open_time"),
        "magic": d.integer("magic"),
        "comment": d.text("comment"),
        "ts": d.instant("ts"),
        "idempotency_key": d.text_or_none("idempotency_key"),
    }


@dataclass(frozen=True, slots=True, kw_only=True)
class PositionOpened(_Position):
    """``position.opened``: a position appeared on the account."""

    KIND: ClassVar[str] = "position.opened"
    #: The pending order it filled from; None for a market order.
    order_ticket: int | None


@dataclass(frozen=True, slots=True, kw_only=True)
class PositionModified(_Position):
    """``position.modified``: a position's stops or volume changed."""

    KIND: ClassVar[str] = "position.modified"


@dataclass(frozen=True, slots=True, kw_only=True)
class PositionClosed(_Position):
    """``position.closed``: a position left the account."""

    KIND: ClassVar[str] = "position.closed"
    close_price: Decimal | None
    #: ``client``, ``mobile``, ``web``, ``expert``, ``sl``, ``tp``, ``stop_out``, ``rollover``,
    #: ``vmargin``, ``split`` or ``unknown`` today.
    close_reason: str
    #: MetaTrader's own word for the closing deal's reason.
    deal_reason_raw: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class TerminalStateChanged:
    """``terminal.state_changed``: a terminal moved from one state to another."""

    KIND: ClassVar[str] = "terminal.state_changed"
    schema_version: str
    terminal_id: UUID
    #: The contract's ``from``: ``ACTIVE``, ``OFFLINE``, ``RETIRED`` and the rest, as text.
    from_state: str
    #: The contract's ``to``.
    to_state: str
    reason: str
    transition_id: UUID
    ts: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class CandleClosed:
    """``md.candle_closed`` on ``candles:{server_id}:{symbol}:{tf}``: a closed bar, sent once and
    never replayed. ``prev_ts`` is the bar before it: if it is not the last one you have, you
    missed one."""

    KIND: ClassVar[str] = "md.candle_closed"
    schema_version: str
    server_id: UUID
    symbol: str
    timeframe: str
    ts: dt.datetime
    o: Decimal
    h: Decimal
    l: Decimal  # noqa: E741 - the contract's name for the low
    c: Decimal
    #: Tick volume.
    v: int
    prev_ts: dt.datetime


Event = (
    OrderPlaced
    | OrderModified
    | OrderClosed
    | PositionOpened
    | PositionModified
    | PositionClosed
    | TerminalStateChanged
    | CandleClosed
)


def _order_placed(d: _Data) -> OrderPlaced:
    return OrderPlaced(**_order_fields(d))


def _order_modified(d: _Data) -> OrderModified:
    return OrderModified(**_order_fields(d))


def _order_closed(d: _Data) -> OrderClosed:
    return OrderClosed(
        **_order_fields(d),
        reason=d.text("reason"),
        order_state_raw=d.text_or_none("order_state_raw"),
        position_ticket=d.integer_or_none("position_ticket"),
    )


def _position_opened(d: _Data) -> PositionOpened:
    return PositionOpened(**_position_fields(d), order_ticket=d.integer_or_none("order_ticket"))


def _position_modified(d: _Data) -> PositionModified:
    return PositionModified(**_position_fields(d))


def _position_closed(d: _Data) -> PositionClosed:
    return PositionClosed(
        **_position_fields(d),
        close_price=d.decimal_or_none("close_price"),
        close_reason=d.text("close_reason"),
        deal_reason_raw=d.text_or_none("deal_reason_raw"),
    )


def _terminal_state_changed(d: _Data) -> TerminalStateChanged:
    return TerminalStateChanged(
        schema_version=d.text("schema_version"),
        terminal_id=d.uuid("terminal_id"),
        from_state=d.text("from"),
        to_state=d.text("to"),
        reason=d.text("reason"),
        transition_id=d.uuid("transition_id"),
        ts=d.instant("ts"),
    )


def _candle_closed(d: _Data) -> CandleClosed:
    return CandleClosed(
        schema_version=d.text("schema_version"),
        server_id=d.uuid("server_id"),
        symbol=d.text("symbol"),
        timeframe=d.text("timeframe"),
        ts=d.instant("ts"),
        o=d.decimal("o"),
        h=d.decimal("h"),
        l=d.decimal("l"),
        c=d.decimal("c"),
        v=d.integer("v"),
        prev_ts=d.instant("prev_ts"),
    )


_READERS: Final[Mapping[str, Callable[[_Data], Event]]] = {
    OrderPlaced.KIND: _order_placed,
    OrderModified.KIND: _order_modified,
    OrderClosed.KIND: _order_closed,
    PositionOpened.KIND: _position_opened,
    PositionModified.KIND: _position_modified,
    PositionClosed.KIND: _position_closed,
    TerminalStateChanged.KIND: _terminal_state_changed,
    CandleClosed.KIND: _candle_closed,
}

#: The event types :func:`event_of` reads. Any other type is None, never an error.
EVENT_KINDS: Final = frozenset(_READERS)


def event_of(message: StreamMessage) -> Event | None:
    """A stream message as the typed event it is, or None for a message of any other type.

    A candle is read by its channel: ``candles:`` messages carry the bar and no event type. A
    message of one of these types that lacks a field the contract requires is a ValueError naming
    the field.
    """
    kind = message.type
    if kind is None:
        if not message.channel.startswith("candles:"):
            return None
        kind = CandleClosed.KIND
    reader = _READERS.get(kind)
    if reader is None:
        return None
    return reader(_Data(kind, message.data))
