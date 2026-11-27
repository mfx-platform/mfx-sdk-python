"""The order, position, terminal, candle, Risk Management and copy events, as typed values.

The platform sends the order, position, terminal and candle events with every value as text, and
the copy events in the contract's own shape: nested objects, numbers as numbers, decimals as
text and nulls as null. :func:`event_of` reads one message as the event it is, or None for any
other:

.. code-block:: python

    async for message in stream:
        event = mfx.event_of(message)
        if isinstance(event, mfx.OrderClosed) and event.reason == "filled":
            print("order", event.ticket, "became position", event.position_ticket)

Ids are UUIDs, tickets and magic numbers integers, prices, volumes and money Decimals, and times
aware UTC datetimes. The platform's own words (``side``, ``order_type``, ``reason``,
``close_reason``, a terminal's states, a candle's ``timeframe``) stay text: they are not a closed
list, and a word the platform adds later reads as it was written instead of failing the read.

The copy events (``copy.copied``, ``copy.refused``, ``copy.stopout``, ``copy.drift`` and
``copy.state_changed``) name accounts by ``account_id`` with their ``venue``, never a terminal or a
ticket. A refusal's ``reason`` is one of :data:`mfx.copy_trading.REFUSAL_REASONS`, with the venue's
own code beside ``broker`` as ``venue_code``. Stage timings and latencies are milliseconds, as
floats: they are measurements, not money.

A message keeps its ``data`` whatever this returns, so nothing is lost by a type this version
does not know.
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, ClassVar, Final
from uuid import UUID

from mfx.errors import RiskRefusal
from mfx.streaming import StreamMessage

__all__ = [
    "EVENT_KINDS",
    "CandleClosed",
    "CopyAs",
    "CopyClosed",
    "CopyClosedEvent",
    "CopyCopied",
    "CopyDeal",
    "CopyDrift",
    "CopyNotClosed",
    "CopyRefused",
    "CopyStateChanged",
    "CopyStopoutEvent",
    "Event",
    "OrderClosed",
    "OrderModified",
    "OrderPlaced",
    "PositionClosed",
    "PositionModified",
    "PositionOpened",
    "RiskCoverageChanged",
    "RiskPeriodClosed",
    "RiskProgrammeResult",
    "RiskRuleEvent",
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

    def blank_none(self, key: str) -> str | None:
        """Text, where the platform sends an empty string for none (a flat event's field)."""
        value = self._raw(key, False)
        return None if value is None or value == "" else str(value)

    def json(self, key: str) -> Any:  # noqa: ANN401 - the contract's object or list
        """A nested part: the stream carries it as JSON text, a webhook body as JSON itself."""
        value = self._raw(key, False)
        if isinstance(value, str):
            return json.loads(value) if value else None
        return value

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

    def uuid_or_none(self, key: str) -> UUID | None:
        value = self._raw(key, False)
        return None if value is None else UUID(str(value))

    def number_or_none(self, key: str) -> float | None:
        value = self._raw(key, False)
        return None if value is None else float(str(value))

    def part(self, key: str) -> _Data:
        """A nested object the contract requires, read by the same rules."""
        value = self._raw(key, True)
        if not isinstance(value, Mapping):
            raise ValueError(f"{self._kind} `{key}` is not an object")
        return _Data(f"{self._kind} `{key}`", value)

    def parts(self, key: str) -> list[_Data]:
        """A list of nested objects; absent or null is an empty list."""
        value = self._raw(key, False) or []
        return [_Data(f"{self._kind} `{key}`", item) for item in value]

    def timings(self, key: str) -> dict[str, float]:
        """A nested object of milliseconds by name; absent or null is empty, as is a null one."""
        value = self._raw(key, False) or {}
        return {str(name): float(str(ms)) for name, ms in value.items() if ms is not None}


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


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskRuleEvent:
    """``risk.rule_warning``, ``risk.rule_breached`` or ``risk.rule_cleared``: a rule of a policy
    (``policy_id``) or of a challenge (``challenge_id``) reached its warning or action level, or
    cleared. Figures stay as the platform wrote them, in the account's currency."""

    KINDS: ClassVar[frozenset[str]] = frozenset(
        {"risk.rule_warning", "risk.rule_breached", "risk.rule_cleared"}
    )
    kind: str
    schema_version: str
    account_id: UUID
    rule: str
    policy_id: UUID | None
    challenge_id: UUID | None
    version: int | None
    used: Decimal | None
    limit: Decimal | None
    #: ``warn``, ``act`` or ``cleared``.
    level: str
    #: What the rule authorised: ``notify``, ``block_entries``, ``cancel_pending``,
    #: ``close_positions``.
    actions: tuple[str, ...]
    #: ``reset``, ``override`` or ``below_warn`` on a clear; None otherwise.
    cleared_by: str | None
    at: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskCoverageChanged:
    """``risk.coverage_changed``: one kind of an account's coverage changed state."""

    KIND: ClassVar[str] = "risk.coverage_changed"
    schema_version: str
    account_id: UUID
    #: ``monitoring``, ``pre_trade``, ``broker_held`` or ``managed_actions``.
    coverage: str
    #: The contract's ``from`` and ``to``: ``healthy``, ``degraded``, ``disconnected``,
    #: ``unknown``.
    from_state: str
    to_state: str
    reason: str | None
    at: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskProgrammeResult:
    """``risk.programme_result``: a challenge account passed, failed or ended. Once only."""

    KIND: ClassVar[str] = "risk.programme_result"
    schema_version: str
    challenge_id: UUID
    version: int
    account_id: UUID
    #: ``passed``, ``failed`` or ``ended``.
    result: str
    #: The rule it failed on; None on a pass or an end.
    rule: str | None
    at: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskPeriodClosed:
    """``risk.period_closed``: one period of a challenge account closed, with its statistics
    (the contract's ``RiskPeriod``, as a mapping: figures as text)."""

    KIND: ClassVar[str] = "risk.period_closed"
    schema_version: str
    challenge_id: UUID
    account_id: UUID
    period: Mapping[str, Any]
    at: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyDeal:
    """The leader's deal a copy event is about."""

    #: ``open``, ``modify``, ``close``, ``close_part``, ``pending_place``, ``pending_modify`` or
    #: ``pending_cancel``.
    action: str
    #: ``buy`` or ``sell``.
    side: str
    #: The leader's volume in base units.
    units: Decimal
    price: Decimal | None
    #: The venue-neutral instrument key (``fx:EURUSD``), when the leader's symbol has one.
    instrument_key: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyAs:
    """What a copy became on the follower account."""

    symbol: str
    side: str
    #: In the follower venue's unit.
    volume: Decimal
    price: Decimal | None


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyClosed:
    """Copied volume a stop-out or a requested close closed."""

    symbol: str
    volume: Decimal
    command_id: UUID | None


@dataclass(frozen=True, slots=True, kw_only=True)
class _CopyFollowerEvent:
    schema_version: str
    follower_id: UUID
    leader_id: UUID
    #: The follower account.
    account_id: UUID
    #: ``mt5`` or ``ctrader`` today.
    venue: str
    at: dt.datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyCopied(_CopyFollowerEvent):
    """``copy.copied``: one follower's copy filled."""

    KIND: ClassVar[str] = "copy.copied"
    #: MFX Hub's id for the signal; the copy log names it.
    signal_id: UUID
    command_id: UUID
    deal: CopyDeal
    #: The contract's ``as``.
    as_: CopyAs
    #: MFX Hub's part, in milliseconds (the log row's ``mfx_ms``).
    latency_ms: float | None
    slippage: Decimal | None
    #: Milliseconds by stage (``detect_ms``, ``sign_ms``, ``deliver_ms``, ``expand_ms``,
    #: ``queue_ms``, ``hand_ms``, ``broker_ms``): the ones measured.
    stages: dict[str, float]


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyRefused(_CopyFollowerEvent):
    """``copy.refused``: one follower's copy did not fill: refused, skipped, or a stop-out's
    close."""

    KIND: ClassVar[str] = "copy.refused"
    signal_id: UUID
    deal: CopyDeal
    #: ``refused``, ``skipped`` or ``stopout``.
    outcome: str
    #: One of :data:`mfx.copy_trading.REFUSAL_REASONS`.
    reason: str
    #: The venue's own code beside ``broker``.
    venue_code: str | None
    #: The reason in words, for a person.
    why: str | None
    #: When Risk Management refused the copy (``reason`` ``risk_rule``): the rule, the policy or
    #: challenge with its version, and the figures as text. None otherwise.
    risk: RiskRefusal | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyNotClosed:
    """A copied position a requested close did not close."""

    symbol: str
    volume: Decimal | None
    #: ``netting``, ``not_copied``, ``copy_mismatch`` or ``gave_up``; None when not known.
    why: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyClosedEvent(_CopyFollowerEvent):
    """``copy.closed``: a requested close of copied positions stopped being pending. Sent once."""

    KIND: ClassVar[str] = "copy.closed"
    close_id: UUID
    #: ``unfollowed``, ``leader_retired`` or ``group_close``.
    cause: str
    #: ``done``, ``incomplete`` or ``superseded``.
    state: str
    closed: tuple[CopyClosed, ...]
    not_closed: tuple[CopyNotClosed, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyStopoutEvent(_CopyFollowerEvent):
    """``copy.stopout``: a follower reached a copy limit and is stopped out."""

    KIND: ClassVar[str] = "copy.stopout"
    stopout_id: UUID
    #: ``daily``, ``monthly`` or ``lifetime``.
    limit: str
    #: In the follower account's currency.
    used: Decimal
    #: The copied volume closed, when the follower closes on a stop-out.
    closed: tuple[CopyClosed, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyDrift(_CopyFollowerEvent):
    """``copy.drift``: the follower's copied positions differ from what the leader's positions and
    the mandate say, found when they were healed from the account. MFX Hub trades nothing to close
    the gap."""

    KIND: ClassVar[str] = "copy.drift"
    #: How far the copied exposure is from the expected, as a percentage of the expected.
    drift_pct: Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class CopyStateChanged(_CopyFollowerEvent):
    """``copy.state_changed``: a follower's state changed."""

    KIND: ClassVar[str] = "copy.state_changed"
    #: The contract's ``from``: ``copying``, ``paused``, ``stopped_out`` or ``unfollowed``.
    from_state: str
    #: The contract's ``to``.
    to_state: str
    #: ``paused``, ``resumed``, ``stopout``, ``unfollowed``, ``leader_retired`` and others; a word
    #: added later reads as written.
    why: str


Event = (
    OrderPlaced
    | OrderModified
    | OrderClosed
    | PositionOpened
    | PositionModified
    | PositionClosed
    | TerminalStateChanged
    | CandleClosed
    | RiskRuleEvent
    | RiskCoverageChanged
    | RiskProgrammeResult
    | RiskPeriodClosed
    | CopyCopied
    | CopyRefused
    | CopyStopoutEvent
    | CopyDrift
    | CopyStateChanged
    | CopyClosedEvent
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


def _risk_uuid(d: _Data, key: str) -> UUID | None:
    value = d.blank_none(key)
    return None if value is None else UUID(value)


def _risk_rule(d: _Data) -> RiskRuleEvent:
    version, used, limit = d.blank_none("version"), d.blank_none("used"), d.blank_none("limit")
    actions = d.json("actions") or []
    return RiskRuleEvent(
        kind=d._kind,  # noqa: SLF001 - the reader's own record of the type
        schema_version=d.text("schema_version"),
        account_id=d.uuid("account_id"),
        rule=d.text("rule"),
        policy_id=_risk_uuid(d, "policy_id"),
        challenge_id=_risk_uuid(d, "challenge_id"),
        version=None if version is None else int(version),
        used=None if used is None else Decimal(used),
        limit=None if limit is None else Decimal(limit),
        level=d.text("level"),
        actions=tuple(str(a) for a in actions),
        cleared_by=d.blank_none("cleared_by"),
        at=d.instant("at"),
    )


def _risk_coverage(d: _Data) -> RiskCoverageChanged:
    return RiskCoverageChanged(
        schema_version=d.text("schema_version"),
        account_id=d.uuid("account_id"),
        coverage=d.text("kind"),
        from_state=d.text("from"),
        to_state=d.text("to"),
        reason=d.blank_none("reason"),
        at=d.instant("at"),
    )


def _risk_result(d: _Data) -> RiskProgrammeResult:
    return RiskProgrammeResult(
        schema_version=d.text("schema_version"),
        challenge_id=d.uuid("challenge_id"),
        version=d.integer("version"),
        account_id=d.uuid("account_id"),
        result=d.text("result"),
        rule=d.blank_none("rule"),
        at=d.instant("at"),
    )


def _risk_period(d: _Data) -> RiskPeriodClosed:
    period = d.json("period")
    if not isinstance(period, Mapping):
        raise ValueError("risk.period_closed carries no `period`")
    return RiskPeriodClosed(
        schema_version=d.text("schema_version"),
        challenge_id=d.uuid("challenge_id"),
        account_id=d.uuid("account_id"),
        period=period,
        at=d.instant("at"),
    )


def _copy_fields(d: _Data) -> dict[str, Any]:
    return {
        "schema_version": d.text("schema_version"),
        "follower_id": d.uuid("follower_id"),
        "leader_id": d.uuid("leader_id"),
        "account_id": d.uuid("account_id"),
        "venue": d.text("venue"),
        "at": d.instant("at"),
    }


def _copy_deal(d: _Data) -> CopyDeal:
    return CopyDeal(
        action=d.text("action"),
        side=d.text("side"),
        units=d.decimal("units"),
        price=d.decimal_or_none("price"),
        instrument_key=d.text_or_none("instrument_key"),
    )


def _copy_copied(d: _Data) -> CopyCopied:
    became = d.part("as")
    return CopyCopied(
        **_copy_fields(d),
        signal_id=d.uuid("signal_id"),
        command_id=d.uuid("command_id"),
        deal=_copy_deal(d.part("deal")),
        as_=CopyAs(
            symbol=became.text("symbol"),
            side=became.text("side"),
            volume=became.decimal("volume"),
            price=became.decimal_or_none("price"),
        ),
        latency_ms=d.number_or_none("latency_ms"),
        slippage=d.decimal_or_none("slippage"),
        stages=d.timings("stages"),
    )


def _copy_refused(d: _Data) -> CopyRefused:
    return CopyRefused(
        **_copy_fields(d),
        signal_id=d.uuid("signal_id"),
        deal=_copy_deal(d.part("deal")),
        outcome=d.text("outcome"),
        reason=d.text("reason"),
        venue_code=d.text_or_none("venue_code"),
        why=d.text_or_none("why"),
        risk=_copy_risk(d),
    )


def _copy_risk(d: _Data) -> RiskRefusal | None:
    """A copy refusal's Risk Management detail: the contract's fields, figures as text."""
    value = d.json("risk")
    if not isinstance(value, Mapping):
        return None
    r = _Data("copy.refused `risk`", value)
    version, challenge_version = (
        r.integer_or_none("version"),
        r.integer_or_none("challenge_version"),
    )
    return RiskRefusal(
        reason=r.text("reason"),
        rule=r.text_or_none("rule"),
        policy_id=r.text_or_none("policy_id"),
        version=version,
        challenge_id=r.text_or_none("challenge_id"),
        challenge_version=challenge_version,
        used=r.text_or_none("used"),
        limit=r.text_or_none("limit"),
        would_be=r.text_or_none("would_be"),
    )


def _copy_closed(d: _Data) -> CopyClosedEvent:
    return CopyClosedEvent(
        **_copy_fields(d),
        close_id=d.uuid("close_id"),
        cause=d.text("cause"),
        state=d.text("state"),
        closed=tuple(
            CopyClosed(
                symbol=item.text("symbol"),
                volume=item.decimal("volume"),
                command_id=item.uuid_or_none("command_id"),
            )
            for item in d.parts("closed")
        ),
        not_closed=tuple(
            CopyNotClosed(
                symbol=item.text("symbol"),
                volume=item.decimal_or_none("volume"),
                why=item.text_or_none("why"),
            )
            for item in d.parts("not_closed")
        ),
    )


def _copy_stopout(d: _Data) -> CopyStopoutEvent:
    return CopyStopoutEvent(
        **_copy_fields(d),
        stopout_id=d.uuid("stopout_id"),
        limit=d.text("limit"),
        used=d.decimal("used"),
        closed=tuple(
            CopyClosed(
                symbol=item.text("symbol"),
                volume=item.decimal("volume"),
                command_id=item.uuid_or_none("command_id"),
            )
            for item in d.parts("closed")
        ),
    )


def _copy_drift(d: _Data) -> CopyDrift:
    return CopyDrift(**_copy_fields(d), drift_pct=d.decimal("drift_pct"))


def _copy_state_changed(d: _Data) -> CopyStateChanged:
    return CopyStateChanged(
        **_copy_fields(d),
        from_state=d.text("from"),
        to_state=d.text("to"),
        why=d.text("why"),
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
    **dict.fromkeys(RiskRuleEvent.KINDS, _risk_rule),
    RiskCoverageChanged.KIND: _risk_coverage,
    RiskProgrammeResult.KIND: _risk_result,
    RiskPeriodClosed.KIND: _risk_period,
    CopyCopied.KIND: _copy_copied,
    CopyRefused.KIND: _copy_refused,
    CopyStopoutEvent.KIND: _copy_stopout,
    CopyDrift.KIND: _copy_drift,
    CopyStateChanged.KIND: _copy_state_changed,
    CopyClosedEvent.KIND: _copy_closed,
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
