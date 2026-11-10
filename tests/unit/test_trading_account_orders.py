"""``client.trading_accounts`` trades and reads one account on any venue, and connects cTrader ones.

The commands are the execution commands keyed on the account: the same bodies, the same rules,
sent to ``/accounts/{id}/...``. These tests assert the wire - path, verb, body, key - and that the
result reads what a cTrader answer adds: the venue, its own code, its deals and its flags.
"""

from __future__ import annotations

import datetime as dt
import inspect
from typing import Any

import httpx
import pytest

from mfx.client import MfxClient
from mfx.results import CommandState, Reason
from mfx.trading_accounts import TradingAccounts

from .conftest import TERMINAL_ID, FakeMfx, body_of, error, page

COMMAND_ID = "0191f0c2-bbbb-7ccc-8ddd-000000000001"
GRANT_ID = "0191f0c2-cccc-7ddd-8eee-000000000003"

ACCOUNT_ID = TERMINAL_ID
WRITES = ("place_order", "cancel_order", "modify_order", "modify_position", "close_position",
          "close_position_by", "close_position_partial", "set_trailing_stop",
          "clear_trailing_stop")  # fmt: skip


def accepted() -> httpx.Response:
    return httpx.Response(
        202, json={"command_id": COMMAND_ID, "state": "ACCEPTED", "duplicate": False}
    )


def command(result: dict[str, Any], state: str = "SUCCEEDED") -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "command_id": COMMAND_ID,
            "terminal_id": TERMINAL_ID,
            "kind": "order_place",
            "state": state,
            "final": True,
            "created_at": "2026-11-10T09:00:00Z",
            "updated_at": "2026-11-10T09:00:01Z",
            "result": result,
        },
    )


def trading_account(account_id: str = ACCOUNT_ID) -> dict[str, Any]:
    return {
        "id": account_id,
        "venue": "ctrader",
        "environment": "demo",
        "label": None,
        "state": "PENDING",
        "broker": {"id": None, "name": "Pepperstone"},
        "login_masked": "****4321",
        "runners": [],
        "created_at": "2026-11-10T09:00:00Z",
    }


def grant(state: str = "ACTIVE") -> dict[str, Any]:
    return {
        "id": GRANT_ID,
        "environment": "demo",
        "scope": "trading",
        "state": state,
        "return_url": "https://example.com/back",
        "tenant_state": "u-7",
        "created_at": "2026-11-10T09:00:00Z",
        "granted_at": "2026-11-10T09:01:00Z",
        "revoked_at": None,
        "accounts": [
            {
                "ctid_trader_account_id": "4321",
                "live": False,
                "broker_name": "Pepperstone",
                "login_masked": "****4321",
                "account_id": None,
            }
        ],
    }


def test_every_account_command_requires_an_idempotency_key() -> None:
    """Given every TradingAccounts method that places or changes an order / When its signature is
    inspected / Then idempotency_key is there, keyword-only, with no default - the rule the
    terminal commands keep, kept on the account's."""
    for name in WRITES:
        key = inspect.signature(getattr(TradingAccounts, name)).parameters.get("idempotency_key")
        assert key is not None and key.default is inspect.Parameter.empty, name
        assert key.kind is inspect.Parameter.KEYWORD_ONLY, name


@pytest.mark.parametrize(
    ("call", "verb", "path", "body"),
    [
        (
            lambda a: a.place_order(
                ACCOUNT_ID, symbol="EURUSD", side="buy", volume="0.10", magic=7,
                idempotency_key="k",
            ),
            "POST", "orders",
            {"symbol": "EURUSD", "side": "buy", "volume": "0.10", "order_type": "market",
             "magic": 7},
        ),
        (lambda a: a.cancel_order(ACCOUNT_ID, 11, idempotency_key="k"),
         "POST", "orders/11/cancel", None),
        (lambda a: a.modify_order(ACCOUNT_ID, 11, price="1.1000", idempotency_key="k"),
         "POST", "orders/11/modify", {"price": "1.1000"}),
        (lambda a: a.modify_position(ACCOUNT_ID, 12, sl="1.0900", idempotency_key="k"),
         "POST", "positions/12/modify", {"sl": "1.0900"}),
        (lambda a: a.close_position(ACCOUNT_ID, 12, idempotency_key="k"),
         "POST", "positions/12/close", {}),
        (lambda a: a.close_position_by(ACCOUNT_ID, 12, 13, idempotency_key="k"),
         "POST", "positions/12/close-by", {"by_ticket": 13}),
        (lambda a: a.close_position_partial(ACCOUNT_ID, 12, volume="0.05", idempotency_key="k"),
         "POST", "positions/12/close-partial", {"volume": "0.05"}),
        (lambda a: a.set_trailing_stop(ACCOUNT_ID, 12, distance="0.0020", idempotency_key="k"),
         "PUT", "positions/12/trailing-stop", {"distance": "0.0020"}),
        (lambda a: a.clear_trailing_stop(ACCOUNT_ID, 12, idempotency_key="k"),
         "DELETE", "positions/12/trailing-stop", None),
    ],
)  # fmt: skip
async def test_each_account_command_goes_to_the_accounts_route_with_the_terminal_routes_body(
    client: MfxClient, mfx: FakeMfx, call: Any, verb: str, path: str, body: Any
) -> None:
    """Given one of the nine commands on a trading account / When it is sent / Then one request
    goes to /v1/accounts/{id}/... with the verb and body the terminal route takes and the key in
    Idempotency-Key, and the answer is a result naming the command, never an exception."""
    mfx.responses.append(accepted())

    result = await call(client.trading_accounts)

    request = mfx.last
    assert request.method == verb
    assert request.url.path == f"/v1/accounts/{ACCOUNT_ID}/{path}"
    assert request.headers["Idempotency-Key"] == "k"
    if body is not None:
        assert body_of(request) == body
    assert result.command_id == COMMAND_ID
    assert result.state is CommandState.ACCEPTED


async def test_an_account_command_returns_a_refusal_and_a_rate_limit_as_results(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given the platform refuses one account order (409) and rate-limits the next (429) / When
    both are placed / Then each comes back as a result with its reason and the platform's words
    - nothing raised, nothing retried by the SDK."""
    mfx.responses.extend(
        [error(409, "state_error", "not connected"), error(429, "rate_limited", "slow down")]
    )

    refused = await client.trading_accounts.place_order(
        ACCOUNT_ID, symbol="EURUSD", side="sell", volume="1", idempotency_key="a"
    )
    limited = await client.trading_accounts.place_order(
        ACCOUNT_ID, symbol="EURUSD", side="sell", volume="1", idempotency_key="b"
    )

    assert refused.reason is Reason.REFUSED and refused.ok is False
    assert refused.detail == "state_error (409): not connected"
    assert {r.url.path for r in mfx.requests} == {f"/v1/accounts/{ACCOUNT_ID}/orders"}
    assert limited.reason is Reason.RATE_LIMITED
    assert len(mfx.requests) == 2, "the SDK retries no write"


async def test_a_ctrader_result_reads_its_venue_code_deals_and_flags_and_mt5_reads_none(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a cTrader close-by done as two closes, a cTrader refusal for want of money, a venue
    that was unavailable, a kind the venue cannot take, and an MT5 fill / When each command is
    read / Then the cTrader one carries venue, both deals in units and the flags; the refusal its
    classified reason beside the venue's own code; venue_unavailable is retryable and
    not_on_this_venue is not; the MT5 one has no deals, units or venue code."""
    deals = [
        {"deal": 501, "order": 401, "position": 12, "volume_units": "50000", "price": "1.10010"},
        {"deal": 502, "order": 402, "position": 13, "volume_units": "50000", "price": "1.10020"},
    ]
    base = {"retryable": False, "tickets": {"order": None, "deal": None, "position": None},
            "attempts": 1}  # fmt: skip
    mfx.responses.extend(
        [
            command({**base, "ok": True, "reason": None, "venue": "ctrader", "deals": deals,
                     "volume_units": "100000", "close_by_emulated": True,
                     "protection_not_set": False, "venue_code": None}),
            command({**base, "ok": False, "reason": "insufficient_funds", "venue": "ctrader",
                     "venue_code": "NOT_ENOUGH_MONEY", "deals": [{"no": "deal"}]},
                    state="FAILED"),
            command({**base, "ok": False, "reason": "venue_unavailable", "retryable": True,
                     "venue": "ctrader"}, state="FAILED"),
            command({**base, "ok": False, "reason": "not_on_this_venue", "venue": "ctrader"},
                    state="REJECTED"),
            command({**base, "ok": True, "reason": None, "venue": "mt5", "mt5_retcode": 10009,
                     "deals": None, "volume_units": None, "close_by_emulated": False,
                     "protection_not_set": False}),
        ]
    )  # fmt: skip

    emulated = await client.execution.get_command(COMMAND_ID)
    broke = await client.execution.get_command(COMMAND_ID)
    away = await client.execution.get_command(COMMAND_ID)
    cannot = await client.execution.get_command(COMMAND_ID)
    mt5 = await client.execution.get_command(COMMAND_ID)

    assert emulated.venue == "ctrader" and emulated.close_by_emulated is True
    assert [d.deal for d in emulated.deals] == [501, 502]
    assert emulated.deals[0].volume_units is not None and str(emulated.deals[0].price) == "1.10010"
    assert str(emulated.volume_units) == "100000"
    assert broke.reason is Reason.INSUFFICIENT_FUNDS and broke.venue_code == "NOT_ENOUGH_MONEY"
    assert broke.deals == (), "an entry without a deal number is not a deal"
    assert away.reason is Reason.VENUE_UNAVAILABLE and away.retryable is True
    assert cannot.reason is Reason.NOT_ON_THIS_VENUE and cannot.retryable is False
    assert mt5.venue == "mt5" and mt5.deals == () and mt5.volume_units is None
    assert mt5.venue_code is None and mt5.protection_not_set is False


async def test_an_accounts_funds_positions_orders_deals_and_symbols_are_read_by_the_account(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a trading account / When its funds, positions, pending orders, the deals of one
    position in a window, and its symbols are read / Then each is one GET under
    /v1/accounts/{id}, the deals carry the window and the position, and each answer is typed."""
    mfx.responses.extend(
        [
            httpx.Response(200, json={"terminal_id": TERMINAL_ID, "snapshot": None,
                                      "profile": None, "stale": True}),
            httpx.Response(200, json={"as_of": "2026-11-10T09:00:00Z", "stale": False,
                                      "items": []}),
            httpx.Response(200, json={"as_of": "2026-11-10T09:00:00Z", "stale": False,
                                      "items": []}),
            page([], None),
            httpx.Response(200, json={"account_id": ACCOUNT_ID, "as_of": "2026-11-10T09:00:00Z",
                                      "items": [{"name": "EURUSD", "symbol_id": 1, "digits": 5,
                                                 "pip_position": 4, "lot_size": "100000",
                                                 "volume_step": "0.01", "volume_min": "0.01",
                                                 "volume_max": "100", "leverage": 500,
                                                 "margin_rate": None, "base_asset": "EUR",
                                                 "quote_asset": "USD", "enabled": True}]}),
        ]
    )  # fmt: skip
    since = dt.datetime(2026, 11, 3, tzinfo=dt.UTC)
    until = dt.datetime(2026, 11, 10, tzinfo=dt.UTC)

    funds = await client.trading_accounts.funds(ACCOUNT_ID)
    positions = await client.trading_accounts.positions(ACCOUNT_ID)
    pending = await client.trading_accounts.pending_orders(ACCOUNT_ID)
    deals = await client.trading_accounts.deals(ACCOUNT_ID, from_=since, to=until, position=12)
    symbols = await client.trading_accounts.symbols(ACCOUNT_ID)

    paths = [r.url.path for r in mfx.requests]
    root = f"/v1/accounts/{ACCOUNT_ID}"
    assert paths == [f"{root}/account", f"{root}/positions", f"{root}/orders/pending",
                     f"{root}/history/deals", f"{root}/symbols"]  # fmt: skip
    assert {r.method for r in mfx.requests} == {"GET"}
    query = mfx.requests[3].url.params
    assert query["position"] == "12" and query["from"].startswith("2026-11-03")
    assert funds.stale is True and positions.items == [] and pending.items == []
    assert deals.items == []
    assert symbols.items[0].volume_step == "0.01" and symbols.items[0].leverage == 500


async def test_a_ctrader_grant_is_started_read_its_accounts_connected_and_revoked(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant connecting a trader's cTrader demo accounts / When it starts a grant, reads
    it, connects one of its accounts and later revokes it / Then the start sends the environment,
    scope, return URL, its own state and key and answers the consent link; the connect sends
    cTrader's ids as strings and answers trading accounts; the revoke is a DELETE with its key."""
    mfx.responses.extend(
        [
            httpx.Response(201, json={"grant_id": GRANT_ID,
                                      "consent_url": "https://connect.example.com/c/abc",
                                      "expires_at": "2026-11-10T09:15:00Z"}),
            httpx.Response(200, json=grant()),
            httpx.Response(200, json={"items": [trading_account()]}),
            httpx.Response(200, json=grant("REVOKED")),
        ]
    )  # fmt: skip

    started = await client.trading_accounts.start_ctrader_grant(
        environment="demo",
        scope="trading",
        return_url="https://example.com/back",
        tenant_state="u-7",
        idempotency_key="g-1",
    )
    got = await client.trading_accounts.ctrader_grant(started.grant_id)
    connected = await client.trading_accounts.connect_ctrader_accounts(
        GRANT_ID, [4321], idempotency_key="g-2"
    )
    revoked = await client.trading_accounts.revoke_ctrader_grant(GRANT_ID, idempotency_key="g-3")

    start, read, connect, revoke = mfx.requests
    assert (start.method, start.url.path) == ("POST", "/v1/accounts/ctrader/grants")
    assert start.headers["Idempotency-Key"] == "g-1"
    assert body_of(start) == {"environment": "demo", "scope": "trading",
                              "return_url": "https://example.com/back",
                              "tenant_state": "u-7"}  # fmt: skip
    assert str(started.consent_url).startswith("https://")
    assert read.url.path == f"/v1/accounts/ctrader/grants/{GRANT_ID}"
    assert got.accounts[0].ctid_trader_account_id == "4321"
    assert connect.url.path == f"/v1/accounts/ctrader/grants/{GRANT_ID}/accounts"
    assert body_of(connect) == {"ctid_trader_account_ids": ["4321"]}
    assert connect.headers["Idempotency-Key"] == "g-2"
    assert [a.venue.value for a in connected] == ["ctrader"]
    assert (revoke.method, revoke.headers["Idempotency-Key"]) == ("DELETE", "g-3")
    assert revoked.state.value == "REVOKED"


async def test_connecting_no_accounts_is_refused_at_the_call_and_nothing_is_sent(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an empty choice of accounts / When connect is called / Then it is a ValueError at
    the call and no request goes out - the platform would refuse it anyway."""
    with pytest.raises(ValueError, match="at least one"):
        await client.trading_accounts.connect_ctrader_accounts(GRANT_ID, [], idempotency_key="x")
    assert mfx.requests == []
