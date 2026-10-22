"""Market depth and an expert's telemetry on the stream."""

from __future__ import annotations

from decimal import Decimal

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import ValidationError
from mfx.md import Book, book_of
from mfx.streaming import Channel, StreamMessage, _replayable

from .conftest import SERVER_ID, TERMINAL_ID, FakeMfx, body_of, terminal_body


def test_the_book_and_ea_channels_are_keyed_as_the_platform_keys_them() -> None:
    """Given a server, a symbol and a terminal
    When a caller builds the book and ea channel keys
    Then they are book:{server_id}:{symbol} and ea:{terminal_id}, a name in place of an id or a
    colon in the symbol is refused here, ea replays on resume as events does, and a book is not
    resumed because the platform answers every subscribe with the newest book."""
    assert Channel.book(SERVER_ID, "XAUUSD") == f"book:{SERVER_ID}:XAUUSD"
    assert Channel.ea(TERMINAL_ID) == f"ea:{TERMINAL_ID}"
    for bad in (lambda: Channel.book("Pepperstone-Demo", "XAUUSD"),
                lambda: Channel.book(SERVER_ID, "XAU:USD"), lambda: Channel.ea("t1")):  # fmt: skip
        with pytest.raises(ValueError, match="not a channel key"):
            bad()
    assert _replayable(Channel.ea(TERMINAL_ID))
    assert not _replayable(Channel.book(SERVER_ID, "XAUUSD"))


def test_a_book_message_reads_as_exact_decimals_best_first_and_nothing_else_is_a_book() -> None:
    """Given an md.book message as the platform sends it, prices and volumes as strings
    When the caller reads it with book_of
    Then it is a Book with both sides exact as Decimal, in the order sent (bids highest first, asks
    lowest first), the best bid and ask, the broker's time and the levels; an empty side has no
    best price; and a tick or an event is not a book."""
    channel = Channel.book(SERVER_ID, "XAUUSD")
    message = StreamMessage(channel=channel, seq=12, type="md.book", data={
        "schema_version": "1", "levels": 5, "broker_ts": "2026-10-16T13:00:00.123",
        "bids": [["2400.10", "1.5"], ["2400.00", "2"]], "asks": [["2400.20", "0.5"]]})  # fmt: skip
    book = book_of(message)
    best, second = (Decimal("2400.10"), Decimal("1.5")), (Decimal("2400.00"), Decimal("2"))
    assert book == Book(channel=channel, seq=12, bids=(best, second),
                        asks=((Decimal("2400.20"), Decimal("0.5")),),
                        broker_ts="2026-10-16T13:00:00.123", levels=5)  # fmt: skip
    assert (book.best_bid, book.best_ask) == (Decimal("2400.10"), Decimal("2400.20"))
    empty = book_of(StreamMessage(channel=channel, seq=13, type="md.book", data={
        "levels": 5, "broker_ts": "t", "bids": [], "asks": []}))  # fmt: skip
    assert empty is not None and (empty.best_bid, empty.best_ask) == (None, None)
    assert book_of(StreamMessage(channel="md:x:XAUUSD", seq=None, type=None, data={})) is None
    assert book_of(StreamMessage(channel="events", seq=1, type="md.subscription_degraded",
                                 data={})) is None  # fmt: skip
    with pytest.raises(ValueError, match="a book side"):
        bad = {"levels": 1, "broker_ts": "t", "bids": "x", "asks": []}
        book_of(StreamMessage(channel=channel, seq=14, type="md.book", data=bad))


async def test_a_terminals_instruments_are_replaced_with_the_depth_symbols_it_should_read(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal
    When the tenant replaces its instruments, once naming the symbols whose book it reads, once
    stopping depth with an empty list, and once leaving depth out
    Then one PUT /terminals/{id}/instruments goes out each time with the idempotency key and the
    whole lists as sent, depth left out of the body when not given (the terminal keeps what it
    has), and the answer is the terminal."""
    for _ in range(3):
        mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    terminal = await client.terminals.replace_instruments(
        TERMINAL_ID, ["XAUUSD", "EURUSD"], depth_instruments=["XAUUSD"], idempotency_key="k1"
    )
    request = mfx.last
    assert (request.method, request.url.path) == ("PUT", f"/v1/terminals/{TERMINAL_ID}/instruments")
    assert request.headers["Idempotency-Key"] == "k1"
    assert body_of(request) == {
        "instruments": ["XAUUSD", "EURUSD"],
        "depth_instruments": ["XAUUSD"],
    }
    assert str(terminal.id) == TERMINAL_ID
    await client.terminals.replace_instruments(
        TERMINAL_ID, ["XAUUSD"], depth_instruments=[], idempotency_key="k2"
    )
    assert body_of(mfx.last) == {"instruments": ["XAUUSD"], "depth_instruments": []}
    await client.terminals.replace_instruments(TERMINAL_ID, ["XAUUSD"], idempotency_key="k3")
    assert body_of(mfx.last) == {"instruments": ["XAUUSD"]}


async def test_a_farm_that_offers_no_depth_is_a_validation_error_carrying_the_platforms_code(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal on a farm whose depth limit is 0
    When the tenant asks for a symbol's depth
    Then the SDK raises the platform's 422 as a ValidationError carrying depth_not_offered and its
    details, so a caller can tell 'this farm offers none' from a wrong list."""
    mfx.responses.append(httpx.Response(422, json={"error": {
        "code": "depth_not_offered", "message": "this farm offers no market depth",
        "details": {"depth_max": 0}}}))  # fmt: skip
    with pytest.raises(ValidationError) as raised:
        await client.terminals.replace_instruments(
            TERMINAL_ID, ["XAUUSD"], depth_instruments=["XAUUSD"], idempotency_key="k4"
        )
    assert raised.value.code == "depth_not_offered"
    assert raised.value.details == {"depth_max": 0}
