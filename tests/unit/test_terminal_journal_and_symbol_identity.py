"""The terminal journal, the label and state filters, broker words on a refused login, the broker
catalogue hashes, a symbol's identity fields and the maintenance window event: the reads the
platform added in November 2026, asserted through the public SDK."""

from __future__ import annotations

import datetime as dt
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx import maintenance
from mfx._generated.models.symbol_spec_changed import SymbolSpecChanged
from mfx._generated.models.terminal_condition_changed import TerminalConditionChanged
from mfx.client import MfxClient
from mfx.errors import StateError, UpstreamError
from mfx.streaming import Channel, StreamMessage
from mfx.sync import SyncMfxClient

from .conftest import (
    BASE_URL,
    BROKER_ID,
    KEY_ID,
    SERVER_ID,
    TERMINAL_ID,
    FakeMfx,
    error,
    page,
    terminal_body,
)
from .test_reads import _symbol
from .test_streaming import FakeTransport, ack, collect, event

WINDOW_ID = "5b1d7e0a-2c44-4f0e-9a51-7d3b8c6e1f20"


def _journal(source: str = "live", stopped: str | None = None) -> dict[str, Any]:
    return {
        "terminal_id": TERMINAL_ID,
        "from": source,
        "read_at": "2026-11-04T09:30:00Z",
        "stopped": stopped,
        "lines": [
            {"ts": "2026-11-04T09:29:58Z", "source": "Trades", "message": "order #1 sent"},
            {"ts": "2026-11-04T09:29:01Z", "source": "Network", "message": "authorized ****1234"},
        ],
    }


def _catalogue(account_type: str = "sd", source: str = "live") -> dict[str, Any]:
    return {
        "server_id": SERVER_ID,
        "account_type": account_type,
        "source": source,
        "catalogue_hash": "9f2c",
        "symbols": 412,
        "refreshed_at": "2026-11-04T09:00:00Z",
    }


def _window_data(**changes: str) -> dict[str, str]:
    data = {
        "schema_version": "1",
        "window_id": WINDOW_ID,
        "label": "MW-0031",
        "state": "in_progress",
        "starts_at": "2026-11-05T10:00:00Z",
        "ends_at": "2026-11-05T12:00:00Z",
        "message": "Planned maintenance on 3 of your terminals until about 12:00 UTC",
        "terminals": "3",
        "change": "eta_moved",
    }
    return {**data, **changes}


async def test_a_running_terminals_journal_is_read_live_newest_first_with_the_lines_asked_for(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a running terminal whose cell answers with its journal
    When the journal is read with lines=20
    Then the request is GET /terminals/{id}/journal?lines=20, and the answer says it was read live
    with its lines as typed values, newest first, and no stop reason."""
    mfx.responses.append(httpx.Response(200, json=_journal()))
    journal = await client.terminals.journal(TERMINAL_ID, lines=20)
    assert mfx.last.method == "GET"
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/journal"
    assert mfx.last.url.params["lines"] == "20"
    assert journal.from_.value == "live" and journal.stopped is None
    assert [line.source for line in journal.lines] == ["Trades", "Network"]
    assert journal.lines[0].ts == dt.datetime(2026, 11, 4, 9, 29, 58, tzinfo=dt.UTC)
    assert journal.lines[1].message == "authorized ****1234"


async def test_a_stopped_terminals_last_words_say_why_and_a_bad_lines_count_is_refused_here(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a stopped terminal whose cell kept its last lines, and one that is not running and
    holds none
    When the journal is read without lines, then with lines=0 and lines=201, then for the second
    Then the first answers from last_words with the reason it stopped and sends no lines
    parameter; 0 and 201 are a ValueError before any request; and the second raises StateError,
    and a cell that does not answer raises UpstreamError."""
    mfx.responses.append(httpx.Response(200, json=_journal("last_words", "failed")))
    journal = await client.terminals.journal(TERMINAL_ID)
    assert "lines" not in mfx.last.url.params
    assert journal.from_.value == "last_words" and journal.stopped is not None
    assert journal.stopped.value == "failed"

    sent = len(mfx.requests)
    for bad in (0, 201):
        with pytest.raises(ValueError, match="1 to 200"):
            await client.terminals.journal(TERMINAL_ID, lines=bad)
    assert len(mfx.requests) == sent, "a bad count never reaches the platform"

    mfx.responses.append(error(409, "state_error", "not running"))
    with pytest.raises(StateError) as refused:
        await client.terminals.journal(TERMINAL_ID)
    assert refused.value.status == 409

    mfx.responses.append(error(503, "upstream_error", "the cell did not answer"))
    with pytest.raises(UpstreamError):
        await client.terminals.journal(TERMINAL_ID)


async def test_the_terminal_list_filters_by_every_label_and_by_state_on_every_page(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant with more terminals than one page
    When the list is walked with label={team: fx, env: prod} and state=ACTIVE
    Then each page request repeats label as key:value, once per pair, and carries state, so the
    platform narrows before it cuts the page; and a list without either sends neither."""
    mfx.responses.append(page([terminal_body("ACTIVE")], "c2"))
    mfx.responses.append(page([terminal_body("ACTIVE")], None))
    seen = [
        t async for t in client.terminals.list(label={"team": "fx", "env": "prod"}, state="ACTIVE")
    ]
    assert len(seen) == 2
    first, second = mfx.requests[-2], mfx.requests[-1]
    assert first.url.params.get_list("label") == ["team:fx", "env:prod"]
    assert first.url.params["state"] == "ACTIVE" and "cursor" not in first.url.params
    assert second.url.params["cursor"] == "c2"
    assert second.url.params.get_list("label") == ["team:fx", "env:prod"]

    mfx.responses.append(page([], None))
    await client.terminals.page(state=["ACTIVE", "OFFLINE"])
    assert mfx.last.url.params.get_list("state") == ["ACTIVE,OFFLINE"], "one comma-separated value"
    with pytest.raises(ValueError, match="BOGUS"):
        await client.terminals.page(state=["ACTIVE", "BOGUS"])  # type: ignore[list-item]
    mfx.responses.append(page([], None))
    _ = [f async for f in client.webhooks.failures(WINDOW_ID, state=["retrying", "dead"])]
    assert mfx.last.url.params["state"] == "retrying,dead"
    with pytest.raises(ValueError, match="nope"):
        _ = [f async for f in client.webhooks.failures(WINDOW_ID, state=["nope"])]  # type: ignore[list-item]
    mfx.responses.append(page([], None))
    await client.maintenance.page(state=("scheduled", "in_progress"))
    assert mfx.last.url.params["state"] == "scheduled,in_progress"

    mfx.responses.append(page([], None))
    await client.terminals.page(state=[])
    await_none = mfx.last.url.params
    assert "label" not in await_none and "state" not in await_none


async def test_a_refused_login_carries_the_brokers_words_and_a_servers_kind_is_known_before_login(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal whose login the broker refused, on a server recorded as demo
    When the terminal is read
    Then its server_kind is demo, and its BrokerConnected condition carries the broker's own words
    and a refusal_kind of invalid_account; and a terminal with no kind reads None."""
    condition = {
        "status": "failed",
        "reason": "login_refused",
        "since": "2026-11-04T09:00:00Z",
        "broker_words": "Invalid account",
        "refusal_kind": "invalid_account",
    }
    mfx.responses.append(
        httpx.Response(
            200,
            json=terminal_body(
                "FAILED", server_kind="demo", conditions={"BrokerConnected": condition}
            ),
        )
    )
    terminal = await client.terminals.get(TERMINAL_ID)
    assert terminal.server_kind is not None and str(terminal.server_kind.value) == "demo"
    seen = terminal.conditions["BrokerConnected"]  # type: ignore[index]
    assert seen.broker_words == "Invalid account"
    assert seen.refusal_kind.value == "invalid_account"  # type: ignore[union-attr]

    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE", server_kind=None)))
    plain = await client.terminals.get(TERMINAL_ID)
    assert plain.server_kind is None


def test_the_condition_changed_event_carries_the_brokers_words_as_text() -> None:
    """Given a terminal.condition_changed event for a refused login, as the stream carries it
    When its data is read as the generated event model
    Then the broker's words and the refusal kind are there, and an event without them (another
    reason) still reads, with both left unset."""
    data = {
        "schema_version": "1",
        "terminal_id": TERMINAL_ID,
        "condition": "BrokerConnected",
        "status": "failed",
        "reason": "login_refused",
        "since": "2026-11-04T09:00:00Z",
        "attributed_to": "",
        "broker_words": "Invalid account",
        "refusal_kind": "invalid_account",
    }
    changed = TerminalConditionChanged.from_dict(data)
    assert changed.broker_words == "Invalid account"
    assert changed.refusal_kind.value == "invalid_account"  # type: ignore[union-attr]
    bare = TerminalConditionChanged.from_dict(
        {k: v for k, v in data.items() if k not in ("broker_words", "refusal_kind")}
    )
    assert not isinstance(bare.broker_words, str)


async def test_a_maintenance_window_change_is_a_typed_event_and_every_other_event_is_none(
    client: MfxClient,
) -> None:
    """Given the events channel carrying maintenance.window_changed and another event
    When each message is passed to maintenance.window_event
    Then the window change reads as a typed value with its change, label, state and aware times,
    and the other event reads None; the type name is the constant a webhook subscribes with."""
    transport = FakeTransport(
        [
            ack(Channel.EVENTS),
            event(Channel.EVENTS, 1, "maintenance.window_changed", **_window_data()),
            event(Channel.EVENTS, 2, "terminal.state_changed", terminal_id=TERMINAL_ID),
        ]
    )
    async with client.stream(connect=transport) as stream:
        await stream.subscribe(Channel.EVENTS)
        seen = await collect(stream, 2)
    changed = maintenance.window_event(seen[0])
    assert changed is not None
    assert (changed.label, changed.change.value, changed.state.value) == (
        "MW-0031",
        "eta_moved",
        "in_progress",
    )
    assert changed.ends_at == dt.datetime(2026, 11, 5, 12, 0, tzinfo=dt.UTC)
    assert changed.terminals == "3", "on the stream every value is text"
    assert maintenance.window_event(seen[1]) is None
    assert maintenance.WINDOW_CHANGED == "maintenance.window_changed"


async def test_a_webhook_subscribes_to_the_window_event_by_name_with_no_closed_list_in_the_way(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that wants maintenance windows pushed to its address
    When it registers an endpoint for maintenance.window_changed
    Then the type goes to the platform exactly as named, because the SDK keeps no closed list of
    event types that could drop a new one."""
    mfx.responses.append(httpx.Response(201, json={}))
    with pytest.raises(Exception):  # noqa: B017, PT011 - the answer's shape is not this case
        await client.webhooks.create(
            "https://hooks.example.com/m", [maintenance.WINDOW_CHANGED], idempotency_key="m-1"
        )
    assert mfx.last.method == "POST"
    assert b'"maintenance.window_changed"' in mfx.last.content


async def test_the_broker_catalogues_come_back_one_row_per_server_and_account_type(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a broker with two catalogues, one live and one last known
    When the catalogues are read, and again for a broker with none
    Then the request is GET /brokers/{id}/catalogues, each row carries its hash, symbol count,
    source and refreshed time, and a broker with none is an empty list, not an error."""
    mfx.responses.append(
        httpx.Response(200, json={"items": [_catalogue(), _catalogue("ecn", "last_known")]})
    )
    rows = await client.catalog.catalogues(BROKER_ID)
    assert mfx.last.url.path == f"/v1/brokers/{BROKER_ID}/catalogues"
    assert [(r.account_type, r.source.value, r.symbols) for r in rows] == [
        ("sd", "live", 412),
        ("ecn", "last_known", 412),
    ]
    assert rows[0].catalogue_hash == "9f2c"
    assert rows[0].refreshed_at == dt.datetime(2026, 11, 4, 9, 0, tzinfo=dt.UTC)

    mfx.responses.append(httpx.Response(200, json={"items": []}))
    assert await client.catalog.catalogues(BROKER_ID) == []


async def test_a_symbol_page_says_where_it_came_from_and_a_symbol_carries_its_identity(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a symbol list answered from the last report because no terminal runs there any more
    When the page is read, and a list that names no source
    Then the page says last_known, each symbol carries the broker's path, isin, exchange,
    category, base currency, basis and calc_mode (None where the broker leaves one empty), and a
    page without a source reads None."""
    identity = {
        "path": "Shares\\US\\NVDA",
        "isin": "US67066G1040",
        "exchange": "NASDAQ",
        "category": None,
        "currency_base": "USD",
        "basis": None,
        "calc_mode": "exch_stocks",
    }
    body = {"items": [_symbol("NVDA", **identity)], "next_cursor": None, "source": "last_known"}
    mfx.responses.append(httpx.Response(200, json=body))
    answer = await client.catalog.symbols(BROKER_ID)
    assert answer.source == "last_known"
    symbol = answer.items[0]
    assert (symbol.path, symbol.isin, symbol.exchange) == (
        "Shares\\US\\NVDA",
        "US67066G1040",
        "NASDAQ",
    )
    assert (symbol.currency_base, symbol.calc_mode) == ("USD", "exch_stocks")
    assert symbol.category is None and symbol.basis is None

    mfx.responses.append(page([_symbol()], None))
    assert (await client.catalog.symbols(BROKER_ID)).source is None


def test_symbol_spec_changed_names_the_four_new_changes() -> None:
    """Given symbol.spec_changed events for a symbol added, returned after a removal, changed in
    its long name and changed in its identity
    When each is read as the generated event model
    Then each change value reads, alongside the older ones."""
    base = {
        "schema_version": "1",
        "terminal_id": TERMINAL_ID,
        "broker_id": BROKER_ID,
        "server_id": SERVER_ID,
        "account_type": "sd",
        "symbol": "NVDA",
        "before": None,
        "after": None,
        "observed_at": "2026-11-04T09:00:00Z",
    }
    spec = {"digits": 5, "description": "Euro vs US Dollar"}
    sides = {  # added has no before, removed no after; the rest are specs on both sides
        "added": (None, spec),
        "removed": (spec, None),
        "came_back": (spec, spec),
        "description": (spec, spec),
        "identity": (spec, spec),
    }
    for change, (before, after) in sides.items():
        parsed = SymbolSpecChanged.from_dict(
            {**base, "change": change, "before": before, "after": after}
        )
        assert parsed.change.value == change
        assert (parsed.before is None, parsed.after is None) == (before is None, after is None)


def test_the_blocking_client_reads_the_journal_the_catalogues_and_a_filtered_list(
    mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given a script with no event loop
    When it reads a terminal's journal, a broker's catalogues and the list filtered by label and
    state
    Then each blocking form sends the same request as its async form and returns the same values."""
    sync = SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    try:
        mfx.responses.append(httpx.Response(200, json=_journal()))
        assert sync.terminal_journal(TERMINAL_ID, lines=5).lines[0].source == "Trades"
        assert mfx.last.url.params["lines"] == "5"

        mfx.responses.append(httpx.Response(200, json={"items": [_catalogue()]}))
        assert sync.catalogues(BROKER_ID)[0].catalogue_hash == "9f2c"

        mfx.responses.append(page([terminal_body("ACTIVE")], None))
        assert len(list(sync.terminals(label={"team": "fx"}, state="ACTIVE"))) == 1
        assert mfx.last.url.params.get_list("label") == ["team:fx"]
        assert mfx.last.url.params["state"] == "ACTIVE"
    finally:
        sync.close()


async def test_a_condition_changed_event_on_the_stream_reaches_the_caller_with_its_new_fields(
    client: MfxClient,
) -> None:
    """Given the events channel carrying a terminal.condition_changed for a refused login
    When the caller reads the stream
    Then the message arrives whole, broker_words and refusal_kind included, because the SDK passes
    an event's data through and does not filter its fields."""
    transport = FakeTransport(
        [
            ack(Channel.EVENTS),
            event(
                Channel.EVENTS,
                1,
                "terminal.condition_changed",
                terminal_id=TERMINAL_ID,
                condition="BrokerConnected",
                broker_words="Invalid account",
                refusal_kind="invalid_account",
            ),
        ]
    )
    async with client.stream(connect=transport) as stream:
        await stream.subscribe(Channel.EVENTS)
        seen = await collect(stream, 1)
    message: StreamMessage = seen[0]
    assert message.type == "terminal.condition_changed"
    assert message.data["broker_words"] == "Invalid account"
    assert message.data["refusal_kind"] == "invalid_account"
