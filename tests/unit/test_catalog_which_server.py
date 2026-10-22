"""A symbol on more than one server or account type can be named exactly.

On 2 Oct 2026 a tenant with two Equiti demo accounts of different account types on one server asked
for a quote: ``catalog.quote(broker_id, "EURUSD.sd")`` raised ``ConflictError: ambiguous_symbol
(409): EURUSD.sd is on more than one server or account type; name server_id and account_type``. The
API takes both as query parameters and the generated call has them. The facade did not pass them,
so the caller was told exactly what to do and given no way to do it.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import ConflictError

from .conftest import BROKER_ID, SERVER_ID, FakeMfx
from .test_reads import SYMBOL, _page, _symbol

QUOTE: dict[str, Any] = {
    "symbol": SYMBOL,
    "server_id": SERVER_ID,
    "account_type": "sd",
    "bid": "1.09431",
    "ask": "1.09445",
    "tick_time": "2026-09-25T09:59:59Z",
    "broker_time": "2026-09-25 12:59:59",
    "age_s": 0.8,
    "state": "open",
}
AMBIGUOUS = {
    "error": {
        "code": "ambiguous_symbol",
        "message": (
            f"{SYMBOL} is on more than one server or account type; name server_id and account_type"
        ),
        "details": {},
    }
}


def _query(request: httpx.Request) -> dict[str, str]:
    return dict(request.url.params)


async def test_a_caller_told_a_symbol_is_ambiguous_can_name_the_server_and_account_type(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant whose two accounts on one broker both list EURUSD.sd, so a quote asked for by
    broker and symbol alone is answered 409 ambiguous_symbol, naming what to send
    When the caller asks again with server_id and account_type
    Then both go out as query parameters, the server id as text whether it was given as text or
    as a UUID, and the quote comes back. Asked for without them, the request carries neither -
    not an empty parameter the platform would have to guess the meaning of."""
    mfx.responses.extend([httpx.Response(409, json=AMBIGUOUS), httpx.Response(200, json=QUOTE)])

    with pytest.raises(ConflictError) as refused:
        await client.catalog.quote(BROKER_ID, SYMBOL)
    assert refused.value.code == "ambiguous_symbol"
    assert _query(mfx.last) == {}

    quote = await client.catalog.quote(BROKER_ID, SYMBOL, server_id=SERVER_ID, account_type="sd")
    assert _query(mfx.last) == {"server_id": SERVER_ID, "account_type": "sd"}
    assert mfx.last.url.path == f"/v1/brokers/{BROKER_ID}/symbols/{SYMBOL}/quote"
    assert quote.account_type == "sd"


async def test_a_symbols_specification_and_the_symbol_list_take_the_same_two_names(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given the two other symbol reads the contract gives the same parameters
    When a symbol's specification, or a broker's symbol list, is asked for with server_id,
    account_type, or one of the two
    Then what was named is sent and what was not is left out, on each read; the list keeps its
    cursor and limit beside them."""
    mfx.responses.extend(
        [
            httpx.Response(200, json=_symbol()),
            httpx.Response(200, json=_symbol()),
            _page([_symbol()]),
            _page([_symbol()]),
        ]
    )

    await client.catalog.symbol(BROKER_ID, SYMBOL, server_id=SERVER_ID, account_type="sd")
    assert _query(mfx.last) == {"server_id": SERVER_ID, "account_type": "sd"}
    await client.catalog.symbol(BROKER_ID, SYMBOL, account_type="standard")
    assert _query(mfx.last) == {"account_type": "standard"}

    await client.catalog.symbols(BROKER_ID, server_id=SERVER_ID, limit=50, cursor="c2")
    assert _query(mfx.last) == {"server_id": SERVER_ID, "limit": "50", "cursor": "c2"}
    await client.catalog.symbols(BROKER_ID)
    assert _query(mfx.last) == {}

    with pytest.raises(ValueError):  # a malformed id fails here, before any request
        await client.catalog.quote(BROKER_ID, SYMBOL, server_id="not-an-id")
