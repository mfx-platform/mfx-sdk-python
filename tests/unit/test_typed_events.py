"""The order, position, terminal and candle events, typed from the stream.

The platform sends these on the stream and the SDK left them as dictionaries of text, so every
caller wrote its own parser. These tests hold the typed form to the contract: each event reads from
the contract's own example, a word the platform adds later still reads, and a field the contract
gains fails here before a caller misses it.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
import yaml

from mfx import events
from mfx.streaming import StreamMessage

#: The Story these cases are Tested By: typed order, position, terminal and candle events.

SPEC = Path(__file__).resolve().parents[2] / "spec" / "openapi.yaml"
SERVER = "3c2d3e4f-5a6b-7c8d-9e0f-102030405060"

#: Each typed event: the contract's schema, the type the platform names it by, its class.
TYPED = {
    "OrderPlaced": ("order.placed", events.OrderPlaced),
    "OrderModified": ("order.modified", events.OrderModified),
    "OrderClosed": ("order.closed", events.OrderClosed),
    "PositionOpened": ("position.opened", events.PositionOpened),
    "PositionModified": ("position.modified", events.PositionModified),
    "PositionClosed": ("position.closed", events.PositionClosed),
    "TerminalStateChanged": ("terminal.state_changed", events.TerminalStateChanged),
    "MdCandleClosed": ("md.candle_closed", events.CandleClosed),
}
#: The contract's `from` is a Python keyword; the class says `from_state` (and `to_state`).
RENAMED = {"from": "from_state", "to": "to_state"}


def _schemas() -> dict[str, Any]:
    spec: dict[str, Any] = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    schemas: dict[str, Any] = spec["components"]["schemas"]
    return schemas


def _message(kind: str, data: dict[str, Any]) -> StreamMessage:
    if kind == "md.candle_closed":
        return StreamMessage(f"candles:{SERVER}:EURUSD:H1", 7, None, data)
    return StreamMessage("events", 7, kind, data)


#: The two schemas the contract gives no example; written here in the contract's own words.
LOCAL_EXAMPLES: dict[str, dict[str, Any]] = {
    "PositionClosed": {
        "schema_version": "1",
        "terminal_id": "0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101",
        "event_id": "0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101:58190241:closed",
        "ticket": "58190241",
        "symbol": "EURUSD",
        "side": "buy",
        "volume": "0.10",
        "open_price": "1.08000",
        "open_time": "2026-10-23T09:20:00Z",
        "sl": None,
        "tp": "1.08600",
        "magic": "0",
        "comment": "",
        "close_price": "1.08600",
        "profit": "60.00",
        "close_reason": "tp",
        "ts": "2026-10-23T11:02:13Z",
    },
    "MdCandleClosed": {
        "schema_version": "1",
        "server_id": SERVER,
        "symbol": "EURUSD",
        "timeframe": "H1",
        "ts": "2026-10-23T09:00:00Z",
        "o": "1.08010",
        "h": "1.08120",
        "l": "1.07950",
        "c": "1.08100",
        "v": 1834,
        "prev_ts": "2026-10-23T08:00:00Z",
    },
}


def _example(name: str) -> dict[str, Any]:
    example = _schemas()[name].get("example") or LOCAL_EXAMPLES.get(name)
    assert isinstance(example, dict), f"{name} has no example"
    return dict(example)


@pytest.mark.parametrize("name", list(TYPED))
def test_each_event_reads_from_the_contracts_own_example_as_typed_values(name: str) -> None:
    """Given the contract's example of an order, position, terminal or candle event
    When the stream delivers it and the caller asks for the typed event
    Then it is that event's class; ids are UUIDs, tickets integers, prices and volumes Decimals and
    times aware datetimes; and a field the example leaves out reads None."""
    kind, cls = TYPED[name]
    data = _example(name)
    event = events.event_of(_message(kind, data))
    assert isinstance(event, cls)
    for field in dataclasses.fields(event):
        value = getattr(event, field.name)
        if field.name in ("terminal_id", "server_id", "transition_id"):
            assert isinstance(value, UUID)
        elif field.name in ("ticket", "order_ticket", "position_ticket", "magic", "v"):
            assert value is None or isinstance(value, int)
        elif field.name.endswith(("_time", "_at")) or field.name in ("ts", "prev_ts"):
            assert value is None or (isinstance(value, dt.datetime) and value.tzinfo is not None)
    raw = {RENAMED.get(k, k): v for k, v in data.items()}
    for key in ("volume", "price", "open_price", "close_price", "sl", "tp", "o", "c"):
        if raw.get(key) is not None and hasattr(event, key):
            assert getattr(event, key) == Decimal(str(raw[key]))
    absent = [f.name for f in dataclasses.fields(event) if f.name not in raw]
    assert all(getattr(event, f) is None for f in absent if f != "kind"), absent


def test_a_word_the_platform_adds_later_still_reads_and_other_messages_are_none() -> None:
    """Given events whose side, order type, close reason or terminal state is a word this version
    does not know, a message of another type, one of a type nobody knows, and one missing a field
    the contract requires
    When the caller asks for the typed event
    Then the new words are kept as the platform wrote them, the other messages are None, and the
    one missing a required field is a ValueError naming that field."""
    order = _example("OrderClosed") | {"side": "sell_short", "reason": "withdrawn_by_broker"}
    closed = events.event_of(_message("order.closed", order))
    assert isinstance(closed, events.OrderClosed)
    assert (closed.side, closed.reason) == ("sell_short", "withdrawn_by_broker")

    moved = _example("TerminalStateChanged") | {"to": "HIBERNATING"}
    state = events.event_of(_message("terminal.state_changed", moved))
    assert isinstance(state, events.TerminalStateChanged) and state.to_state == "HIBERNATING"

    assert events.event_of(StreamMessage("events", 1, "feed.degraded", {})) is None
    assert events.event_of(StreamMessage("events", 1, "order.teleported", {})) is None
    assert events.event_of(StreamMessage(f"md:{SERVER}:EURUSD", 1, None, {"bid": "1"})) is None

    broken = _example("PositionOpened")
    del broken["open_price"]
    with pytest.raises(ValueError, match="open_price"):
        events.event_of(_message("position.opened", broken))


@pytest.mark.parametrize("name", list(TYPED))
def test_every_field_the_contract_gives_an_event_has_a_place_in_its_class(name: str) -> None:
    """Given an event's schema in the vendored contract
    When it is compared with the event's class
    Then every property has a field of the same name (`from` and `to` as `from_state` and
    `to_state`), the class has none the contract does not, and the type names agree, so a field
    the contract gains fails here instead of being dropped where a caller cannot see it."""
    kind, cls = TYPED[name]
    schema = _schemas()[name]
    contract = {RENAMED.get(k, k) for k in schema["properties"]}
    fields = {f.name for f in dataclasses.fields(cls)} - {"kind"}
    assert fields == contract, (sorted(contract - fields), sorted(fields - contract))
    assert kind == cls.KIND
    assert kind in events.EVENT_KINDS
