"""``catalog``, ``accounts`` and ``usage`` — the read surface.

Reads raise the typed hierarchy rather than returning results: a caller asking what the balance is
either gets the balance or is told why not. The execution boundary is the opposite, and
test_execution.py is where that lives.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import NotFoundError

from .conftest import BROKER_ID, TERMINAL_ID, FakeMfx

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

SYMBOL = "EURUSD.sd"


def _page(items: list[dict[str, Any]], next_cursor: str | None = None) -> httpx.Response:
    return httpx.Response(
        200, json={"items": items, "next_cursor": next_cursor, "returned": len(items)}
    )


def _symbol(name: str = SYMBOL, **extra: Any) -> dict[str, Any]:
    """A Symbol as the API returns one: every required field, decimals as strings."""
    return {
        "symbol": name,
        "description": "Euro vs US Dollar",
        "server_id": BROKER_ID,
        "account_type": "sd",
        "digits": 5,
        "contract_size": "100000",
        "volume_min": "0.01",
        "volume_max": "100",
        "volume_step": "0.01",
        "trade_mode": "full",
        "margin_currency": "USD",
        "pip_value_per_lot": None,
        "spec_hash": "b3f1",
        "trade_sessions": [],
        "refreshed_at": "2026-09-25T09:00:00Z",
        # status is an object, not a word: a symbol is "open" or "closed" *for a reason*, and the
        # reason is what a caller acts on (SymbolStatus).
        "status": {
            "state": "open",
            "reason": None,
            "since": "2026-09-25T08:00:00Z",
            "next_open": None,
            "last_tick_age_s": 0.4,
            "quote_watched": True,
            "as_of": "2026-09-25T09:00:00Z",
        },
        **extra,
    }


def _broker(code: str, status: str = "active", **extra: Any) -> dict[str, Any]:
    return {
        "id": BROKER_ID,
        "code": code,
        "display_name": code.title(),
        "status": status,
        **extra,
    }


async def test_the_catalogue_names_brokers_servers_and_symbols_the_broker_itself_uses(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant choosing where to put a terminal / When it reads the catalogue / Then it gets
    the brokers MFX supports with each one's status, the servers each runs, and the symbols in the
    broker's own names.

    Those names are the point: MFX never renames an instrument on a tenant's behalf, so
    `BTCUSD.lv` is what a broker that calls it that will answer to — and what must be passed back
    to terminals.create and place_order."""
    mfx.responses.extend(
        [
            _page([_broker("equiti"), _broker("pepperstone", status="suspended")]),
            _page(
                [
                    {
                        "id": BROKER_ID,
                        "server_name": "EquitiSecurities-Demo",
                        "kind": "demo",
                        "enabled": True,
                        "disabled_reason": None,
                    }
                ]
            ),
            _page([_symbol("BTCUSD.lv", digits=2)]),
        ]
    )

    brokers = await client.catalog.brokers()
    assert [b.code for b in brokers] == ["equiti", "pepperstone"]
    assert [b.status.value for b in brokers.items] == ["active", "suspended"]
    assert mfx.last.url.path == "/v1/brokers"

    servers = await client.catalog.servers(BROKER_ID)
    assert servers.items[0].server_name == "EquitiSecurities-Demo"
    assert mfx.last.url.path == f"/v1/brokers/{BROKER_ID}/servers"

    symbols = await client.catalog.symbols(BROKER_ID)
    assert symbols.items[0].symbol == "BTCUSD.lv"
    assert len(symbols) == 1 and symbols.returned == 1


async def test_every_broker_is_reachable_by_following_the_cursor(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """There is no total and no page number in this API, by design (guardrail 7), so the cursor is
    the only way through."""
    mfx.responses.extend(
        [_page([_broker("equiti")], "cursor-2"), _page([_broker("pepperstone")], None)]
    )

    codes = [broker.code async for broker in client.catalog.all_brokers()]

    assert codes == ["equiti", "pepperstone"]
    assert mfx.requests[1].url.params.get("cursor") == "cursor-2"


async def test_a_symbol_carries_what_a_caller_needs_before_trading_it(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Gap G4: pip_value_per_lot comes from the terminal and is never derived, so it is null until
    a terminal has reported it rather than computed from something that looks close."""
    mfx.responses.append(httpx.Response(200, json=_symbol()))

    symbol = await client.catalog.symbol(BROKER_ID, SYMBOL)

    assert symbol.symbol == SYMBOL
    assert symbol.pip_value_per_lot is None, "unknown, not guessed"
    assert mfx.last.url.path == f"/v1/brokers/{BROKER_ID}/symbols/{SYMBOL}"


async def test_a_quote_is_never_returned_without_saying_how_old_it_is(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A stale quote reads exactly like a live one and gets acted on, so age_s and the symbol's
    state ride with every reading rather than being available somewhere else."""
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "symbol": SYMBOL,
                "server_id": BROKER_ID,
                "account_type": "sd",
                "bid": "1.09431",
                "ask": "1.09445",
                "tick_time": "2026-09-25T09:59:59Z",
                "broker_time": "2026-09-25 12:59:59",
                "age_s": 0.8,
                "state": "open",
            },
        )
    )

    quote = await client.catalog.quote(BROKER_ID, SYMBOL)

    assert mfx.last.url.path == f"/v1/brokers/{BROKER_ID}/symbols/{SYMBOL}/quote"
    assert quote.age_s == 0.8
    assert quote.state.value == "open"


async def test_the_spread_comes_from_the_tenants_own_terminal_and_says_how_old_it_is(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant asking for a symbol's spread / When the client reads it / Then it comes from
    that tenant's own terminal and carries its age.

    A pool cannot answer this: the spread a user trades against is the one their broker gives
    *their* account. And it is never returned without its age, because a stale spread reads exactly
    like a live one and gets acted on. This is the client half;
    the endpoint has its own test."""
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "terminal_id": TERMINAL_ID,
                "as_of": "2026-09-25T10:00:00Z",
                "items": [
                    {
                        "symbol": SYMBOL,
                        "bid": "1.09431",
                        "ask": "1.09445",
                        "spread_points": 14,
                        "digits": 5,
                        "tick_time": "2026-09-25T09:59:59Z",
                        "age_s": 1.2,
                    }
                ],
            },
        )
    )

    spreads = await client.accounts.spread(TERMINAL_ID)

    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/spread"
    assert spreads.items[0].age_s == 1.2
    assert spreads.items[0].spread_points == 14


async def test_an_account_reports_each_half_with_when_it_was_observed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """The fast numerics and the slow profile are two halves with their own timestamps, and a half
    never observed is null rather than zero — a zero balance is a fact, not a gap."""
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "terminal_id": TERMINAL_ID,
                "snapshot": {
                    "ts": "2026-09-25T10:00:00Z",
                    "balance": "10000.00",
                    "equity": "10012.40",
                    "margin": "120.00",
                    "margin_free": "9892.40",
                    "margin_level": None,
                },
                "profile": None,
                "stale": False,
            },
        )
    )

    account = await client.accounts.account(TERMINAL_ID)

    assert account.snapshot is not None and account.snapshot.balance == "10000.00"
    assert account.profile is None, "never observed is null, not an empty profile"
    assert account.stale is False, (
        "whether these numbers are still arriving is part of the answer, not something a caller "
        "infers from `snapshot.ts` and a clock it has to guess the tolerance for"
    )


async def test_live_lists_are_snapshots_and_history_is_paged(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Positions and pending orders come back whole with their as_of — a cursor over a
    set that changes while you page skips or repeats rows. Deals are history, so they page."""
    mfx.responses.extend(
        [
            httpx.Response(
                200,
                json={
                    "as_of": "2026-09-25T10:00:00Z",
                    "stale": False,
                    "items": [
                        {
                            "ticket": 8811,
                            "symbol": SYMBOL,
                            "side": "buy",
                            "volume": "0.10",
                            "open_price": "1.09431",
                            "sl": None,
                            "tp": None,
                            "profit": "1.20",
                            "swap": "0.00",
                            "open_time": "2026-09-25T09:00:00Z",
                            "magic": 0,
                            "comment": "",
                        }
                    ],
                },
            ),
            httpx.Response(
                200, json={"as_of": "2026-09-25T10:00:00Z", "stale": False, "items": []}
            ),
            _page([], None),
        ]
    )

    positions = await client.accounts.positions(TERMINAL_ID)
    assert positions.items[0].ticket == 8811
    assert "cursor" not in mfx.last.url.params, "a snapshot is not paged"

    assert (await client.accounts.pending_orders(TERMINAL_ID)).items == []

    window = dt.datetime(2026, 9, 24, tzinfo=dt.UTC), dt.datetime(2026, 9, 25, tzinfo=dt.UTC)
    deals = await client.accounts.deals(TERMINAL_ID, from_=window[0], to=window[1])
    assert deals.items == []
    assert mfx.last.url.params.get("from") or mfx.last.url.params.get("from_"), "the window is sent"


async def test_usage_reports_this_keys_ceilings_and_whether_the_budget_is_measured(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a key with its own ceilings / When usage is read / Then the limits reported are that
    key's and budget_source says whether the number was measured or configured.

    The limits are the calling key's, not the tenant's, so one runaway integration cannot starve a
    tenant's production traffic. A ceiling read as a reading is how a quota surprises someone."""
    mfx.responses.append(
        httpx.Response(
            200,
            json={
                "items": [
                    {
                        "metric": "commands",
                        "quantity": "41",
                        "period_start": "2026-09-25T09:00:00Z",
                        "period_end": "2026-09-25T10:00:00Z",
                    }
                ],  # fmt: skip
                "limits": {"commands_per_s": 5, "md_msgs_per_s": None, "ws_conns": 2},
                "budget_remaining": 900,
                "budget_source": "configured",
                "as_of": "2026-09-25T10:00:00Z",
            },
        )
    )

    usage = await client.usage.get()

    assert mfx.last.url.path == "/v1/usage"
    assert usage.budget_remaining == 900
    assert usage.budget_source.value == "configured", "a ceiling, not a measurement"
    assert usage.limits is not None and usage.limits.commands_per_s == 5


async def test_another_tenants_object_is_a_404_and_reaches_the_caller_as_one(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an id belonging to another tenant / When it is read / Then the caller gets
    NotFoundError from the typed hierarchy, never a 403.

    Another tenant's object reads as absent: a 403 would confirm the object exists."""
    from .conftest import error

    mfx.responses.append(error(404, "not_found", "no such terminal"))

    with pytest.raises(NotFoundError):
        await client.accounts.account(TERMINAL_ID)


async def test_a_tenant_can_see_a_switched_off_server_before_it_asks_for_a_terminal(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a broker with one usable server and one switched off / When the catalogue is read /
    Then each server says whether MFX can use it now, and why not in the operator's own words.

    Without per-server state in the tenant contract, the only way to
    learn a server was off was to request a terminal on it and be refused. `disabled_reason` is the
    same sentence the refusal carries, so a caller can show a user the reason *before* it asks
    rather than after."""
    mfx.responses.append(
        _page(
            [
                {
                    "id": BROKER_ID,
                    "server_name": "EquitiSecurities-Demo",
                    "kind": "demo",
                    "enabled": True,
                    "disabled_reason": None,
                },
                {
                    "id": BROKER_ID,
                    "server_name": "EquitiSecurities-Live",
                    "kind": "live",
                    "enabled": False,
                    "disabled_reason": "Switched off while its canary set is rebuilt.",
                },
            ]
        )
    )

    servers = await client.catalog.servers(BROKER_ID)

    usable = [s for s in servers if s.enabled]
    assert [s.server_name for s in usable] == ["EquitiSecurities-Demo"]
    off = next(s for s in servers if not s.enabled)
    assert off.disabled_reason == "Switched off while its canary set is rebuilt."
    assert usable[0].disabled_reason is None, "null while enabled, never an empty excuse"
