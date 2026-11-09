"""``client.trading_accounts`` — the trading accounts over every venue.

These assert what goes on the wire: the path, each filter in the form the platform reads, and
nothing sent when a filter is wrong.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx._generated.models.trading_account_state import TradingAccountState
from mfx.client import MfxClient
from mfx.errors import NotFoundError
from mfx.sync import SyncMfxClient
from mfx.trading_accounts import TradingAccounts

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx, error, page

SECOND = "0191f0c2-aaaa-7bbb-8ccc-000000000002"


def account(account_id: str = TERMINAL_ID, state: str = "CONNECTED") -> dict[str, Any]:
    return {
        "id": account_id,
        "venue": "mt5",
        "environment": "demo",
        "label": None,
        "state": state,
        "broker": {"id": None, "name": "MetaQuotes"},
        "login_masked": "****6933",
        "runners": [{"terminal_id": account_id, "role": None}],
        "created_at": "2026-11-09T16:00:00Z",
    }


@pytest.fixture
def sync_client(mfx: FakeMfx, private_key: Ed25519PrivateKey) -> Iterator[SyncMfxClient]:
    client = SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    yield client
    client.close()


async def test_a_trading_account_is_read_by_its_id_and_another_tenants_is_not_found(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an account id held as a string / When the SDK reads the trading account, and then one
    the platform answers 404 / Then one GET /accounts/{id} goes out, the answer is the typed
    account with its venue-neutral state, and the 404 is NotFoundError."""
    mfx.responses.extend([httpx.Response(200, json=account()), error(404, "not_found", "no")])
    got = await client.trading_accounts.get(TERMINAL_ID)
    assert got.state is TradingAccountState.CONNECTED
    assert mfx.requests[0].method == "GET"
    assert mfx.requests[0].url.path == f"/v1/accounts/{TERMINAL_ID}"
    with pytest.raises(NotFoundError):
        await client.trading_accounts.get(SECOND)


async def test_a_page_sends_venue_and_state_comma_separated_and_the_environment_as_given(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given two venues, an environment, two states, a cursor and a page size / When the SDK reads a
    page, and then a page with no filter / Then venue and state each go as one comma-separated
    value, the environment, cursor and size as given, the page comes back with its next cursor, and
    the plain page sends no filter."""
    mfx.responses.extend([page([account()], "c2"), page([], None)])
    got = await client.trading_accounts.page(
        cursor="c1",
        limit=20,
        venue=["mt5", "ctrader"],
        environment="live",
        state=["CONNECTED", "DEGRADED"],
    )
    assert [str(a.id) for a in got.items] == [TERMINAL_ID]
    assert got.next_cursor == "c2"
    params = mfx.requests[0].url.params
    assert params["venue"] == "mt5,ctrader"
    assert params["state"] == "CONNECTED,DEGRADED"
    assert (params["environment"], params["cursor"], params["limit"]) == ("live", "c1", "20")
    await client.trading_accounts.page()
    assert set(mfx.requests[1].url.params) <= {"limit"}


async def test_a_misspelt_venue_state_or_environment_is_refused_before_sending(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a venue, a state and an environment the contract does not name / When the SDK reads a
    page with each / Then each is a ValueError at the call and nothing is sent."""
    with pytest.raises(ValueError, match="mt4"):
        await client.trading_accounts.page(venue="mt4")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="ACTIVE"):
        await client.trading_accounts.page(state=["ACTIVE"])  # type: ignore[list-item]
    with pytest.raises(ValueError, match="paper"):
        await client.trading_accounts.page(environment="paper")  # type: ignore[arg-type]
    assert mfx.requests == []


async def test_every_trading_account_is_listed_following_the_cursor_with_the_filters_kept(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given two pages of accounts / When the SDK lists every account narrowed to one venue,
    environment and state / Then the second page is read with the first page's cursor and the same
    filters, and every account is yielded once."""
    mfx.responses.extend([page([account()], "n"), page([account(SECOND)], None)])
    seen = [
        str(a.id)
        async for a in client.trading_accounts.list(
            limit=1, venue="mt5", environment="demo", state="CONNECTED"
        )
    ]
    assert seen == [TERMINAL_ID, SECOND]
    assert mfx.requests[1].url.params["cursor"] == "n"
    for request in mfx.requests:
        assert request.url.params["venue"] == "mt5"
        assert request.url.params["environment"] == "demo"
        assert request.url.params["state"] == "CONNECTED"


def test_a_script_reads_trading_accounts_through_the_blocking_client(
    sync_client: SyncMfxClient, mfx: FakeMfx
) -> None:
    """Given a script with no event loop / When it reads one trading account and iterates every one
    narrowed to a venue / Then the account comes back and the iterator follows the cursor a page at
    a time."""
    mfx.responses.extend(
        [httpx.Response(200, json=account()), page([account()], "n"), page([account(SECOND)], None)]
    )
    assert str(sync_client.get_trading_account(TERMINAL_ID).id) == TERMINAL_ID
    seen = [str(a.id) for a in sync_client.trading_accounts(venue="mt5")]
    assert seen == [TERMINAL_ID, SECOND]
    assert mfx.requests[2].url.params["cursor"] == "n"


def test_the_client_offers_trading_accounts_beside_the_balance_view(client: MfxClient) -> None:
    """Given a client / When it is built / Then client.trading_accounts is a TradingAccounts and
    client.accounts is still the account behind a terminal."""
    assert isinstance(client.trading_accounts, TradingAccounts)
    assert client.accounts is not client.trading_accounts
