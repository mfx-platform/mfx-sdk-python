"""The SDK's types carry the broker's own facts the API serves. Every one is nullable: a row
the platform has not refreshed yet, or a broker that does not report the figure, reads None,
never a zero."""

from __future__ import annotations

import datetime as dt
from typing import Any

from mfx._generated.models.account import Account
from mfx._generated.models.deal import Deal
from mfx._generated.models.position import Position
from mfx._generated.models.symbol import Symbol

TERMINAL = "0191f0c2-aaaa-7bbb-8ccc-000000000001"


def _symbol(**facts: Any) -> dict[str, Any]:
    return {
        "symbol": "EURUSD", "description": "Euro vs US Dollar",
        "server_id": "3c2d3e4f-5a6b-7c8d-9e0f-102030405060", "account_type": "",
        "digits": 5, "contract_size": "100000", "volume_min": "0.01", "volume_max": "100",
        "volume_step": "0.01", "trade_mode": "full", "margin_currency": "EUR",
        "pip_value_per_lot": "10", "spec_hash": "abc", "trade_sessions": None,
        "refreshed_at": "2026-10-22T05:00:00Z",
        "status": {"state": "open", "reason": None, "since": None, "next_open": None,
                   "last_tick_age_s": 0.2, "quote_watched": True, "as_of": "2026-10-22T05:00:00Z"},
        **facts,
    }  # fmt: skip


def test_a_symbol_deal_position_and_account_carry_the_brokers_facts_and_none_where_unreported(
) -> None:  # fmt: skip
    """Given the figures dev-002's terminal reported on 22 Oct, and rows from before they existed
    When they are read into the SDK's types
    Then a symbol carries its stops and freeze levels, swaps and their unit, tick size and value,
    margin settings, margin per lot, profit currency and filling modes; a deal its fee, the balance
    after it and a closing deal's stops; a position its commission and margin; the account its
    credit and its currency's decimals; and every one is None on a row that does not carry it."""
    symbol = Symbol.from_dict(_symbol(
        profit_currency="USD", point="0.00001", tick_size="0.00001", tick_value="1",
        stops_level=0, freeze_level=0, swap_long="-7.21", swap_short="1.53", swap_type="points",
        margin_initial="100000", margin_maintenance="0", margin_per_lot="561.67",
        filling_modes=["ioc"],
    ))  # fmt: skip
    swap = symbol.swap_type.value  # type: ignore[union-attr]
    assert (symbol.stops_level, swap, symbol.margin_per_lot) == (0, "points", "561.67")
    assert [mode.value for mode in symbol.filling_modes] == ["ioc"]  # type: ignore[union-attr]
    bare = Symbol.from_dict(_symbol())
    assert not isinstance(bare.stops_level, int) and not isinstance(bare.margin_per_lot, str)

    deal = Deal.from_dict({
        "deal": 1, "order": 1, "position": 1, "symbol": "NZDUSD", "side": "sell", "entry": "out",
        "volume": "0.5", "price": "0.56923", "profit": "-145.18", "commission": "0.00",
        "swap": "0.00", "time": "2026-10-22T05:01:57Z", "magic": 0, "comment": "",
        "close_reason": "sl", "fee": "0.00", "balance": "45156.38", "sl": "0.56925", "tp": None,
    })  # fmt: skip
    assert (deal.balance, deal.fee, deal.sl, deal.tp) == ("45156.38", "0.00", "0.56925", None)

    position = Position.from_dict({
        "ticket": 7, "symbol": "NVDA.US", "side": "buy", "volume": "7.9", "open_price": "227.56",
        "sl": None, "tp": None, "profit": "-44.24", "swap": "0",
        "open_time": "2026-10-21T15:00:00Z",
        "magic": 0, "comment": "", "commission": "-0.16", "margin": "359.54",
    })  # fmt: skip
    assert (position.commission, position.margin) == ("-0.16", "359.54")

    account = Account.from_dict({
        "terminal_id": TERMINAL, "stale": False,
        "snapshot": {"ts": "2026-10-22T05:10:00Z", "balance": "45156.38", "equity": "45109.09",
                     "margin": "359.54", "margin_free": "44749.55", "margin_level": None,
                     "credit": "0.00", "open_positions_count": 1},
        "profile": {"currency": "USD", "currency_digits": 2, "leverage": 500},
    })  # fmt: skip
    assert account.snapshot.credit == "0.00"  # type: ignore[union-attr]
    assert account.profile.currency_digits == 2  # type: ignore[union-attr]
    assert isinstance(deal.time, dt.datetime)
