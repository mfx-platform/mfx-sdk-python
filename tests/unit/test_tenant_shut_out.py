"""A tenant the operator has disabled or suspended is told so, in the operator's words.

The public API answers such a tenant ``403 tenant_disabled`` or ``403 tenant_suspended``.
``message`` is the text the operator wrote for the tenant, to be shown as given;
``details.since`` is when it began, and for a suspension ``details.reads_until`` is when the reads
that still work will stop. Neither is retryable: it ends when the operator enables or resumes the
tenant.

Before this, both arrived as a bare ``ForbiddenError`` whose docstring says "the key is valid and
this is not in its scopes" - which sends a tenant to look at its key's scopes for a problem that is
an operator's decision about the whole account.
"""

from __future__ import annotations

import datetime as dt

import httpx
import pytest

from mfx import TenantDisabledError, TenantSuspendedError
from mfx.client import MfxClient
from mfx.errors import ForbiddenError, MfxApiError
from mfx.results import Reason
from mfx.streaming import Channel

from .conftest import SERVER_ID, TERMINAL_ID, FakeMfx
from .test_streaming import SYMBOL, FakeTransport, ack, collect, tick

DISABLED_WORDS = (
    "Your account is paused while we verify your company details. Write to ops@mfxhub.com."
)
SUSPENDED_WORDS = "Invoice 2026-091 is 30 days overdue; orders are off until it is paid."


def _refusal(code: str, message: str, **details: str) -> httpx.Response:
    return httpx.Response(
        403, json={"error": {"code": code, "message": message, "details": details}}
    )


async def test_a_disabled_tenant_is_told_so_in_the_operators_words(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant the operator has disabled, with a message written for it
    When the tenant makes any call, here a read of one terminal
    Then the SDK raises TenantDisabledError: ``message`` is the operator's text word for word,
    ``since`` is when it began as a time and not a string, the platform's code and status are
    kept, and it is still a ForbiddenError for code that catches the broader kind."""
    mfx.responses.append(_refusal("tenant_disabled", DISABLED_WORDS, since="2026-10-02T09:14:07Z"))

    with pytest.raises(TenantDisabledError) as raised:
        await client.terminals.get(TERMINAL_ID)

    error = raised.value
    assert error.message == DISABLED_WORDS, "word for word, nothing added"
    assert DISABLED_WORDS in str(error)
    assert error.since == dt.datetime(2026, 10, 2, 9, 14, 7, tzinfo=dt.UTC)
    assert (error.code, error.status) == ("tenant_disabled", 403)
    assert isinstance(error, ForbiddenError)
    assert len(mfx.requests) == 1, "not retried: only the operator ends it"


async def test_a_suspended_tenant_learns_why_and_until_when_its_reads_still_work(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a suspended tenant: writes are refused now, reads work until its grace ends
    When it restarts a terminal, and then places an order
    Then the restart raises TenantSuspendedError with the operator's message, ``since`` and
    ``reads_until`` as times; the order does not raise, as no execution method does, and comes
    back refused with the operator's message in its detail. And a suspension that names no
    grace, or a date the SDK cannot read, gives None for that time and never an error of the
    SDK's own."""
    mfx.responses.extend(
        [
            _refusal(
                "tenant_suspended",
                SUSPENDED_WORDS,
                since="2026-10-06T08:00:00Z",
                reads_until="2026-10-08T08:00:00+00:00",
            ),
            _refusal("tenant_suspended", SUSPENDED_WORDS, since="2026-10-06T08:00:00Z"),
            _refusal("tenant_suspended", SUSPENDED_WORDS, since="yesterday", reads_until=""),
        ]
    )

    with pytest.raises(TenantSuspendedError) as raised:
        await client.terminals.restart(TERMINAL_ID, reason="weekly", idempotency_key="r-1")
    error = raised.value
    assert error.message == SUSPENDED_WORDS
    assert error.since == dt.datetime(2026, 10, 6, 8, 0, tzinfo=dt.UTC)
    assert error.reads_until == dt.datetime(2026, 10, 8, 8, 0, tzinfo=dt.UTC)
    assert (error.code, error.status) == ("tenant_suspended", 403)
    assert isinstance(error, ForbiddenError) and not isinstance(error, TenantDisabledError)

    result = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="0.10", idempotency_key="order-1"
    )
    assert result.ok is False and result.reason is Reason.REFUSED
    assert SUSPENDED_WORDS in (result.detail or ""), "the tenant's log says why"

    with pytest.raises(TenantSuspendedError) as unreadable:
        await client.terminals.get(TERMINAL_ID)
    assert unreadable.value.since is None and unreadable.value.reads_until is None
    assert unreadable.value.message == SUSPENDED_WORDS


async def test_a_stream_closed_for_a_disabled_tenant_raises_the_same_error(
    client: MfxClient,
) -> None:
    """Given an open stream, and an operator who disables the tenant
    When the platform sends its error frame for the connection before closing it
    Then the stream raises TenantDisabledError with the operator's message, the same error a
    call would raise, and not a bare MfxApiError the caller has to read a code out of."""
    md = Channel.md(SERVER_ID, SYMBOL)
    frame = {
        "op": "error",
        "error": {
            "code": "tenant_disabled",
            "message": DISABLED_WORDS,
            "details": {"since": "2026-10-02T09:14:07Z"},
        },
    }
    transport = FakeTransport([ack(md), tick(md, 1), frame])

    async with client.stream(connect=transport) as stream:
        await stream.subscribe(md)
        with pytest.raises(TenantDisabledError) as raised:
            await collect(stream, 3)

    assert raised.value.message == DISABLED_WORDS
    assert raised.value.since == dt.datetime(2026, 10, 2, 9, 14, 7, tzinfo=dt.UTC)
    assert isinstance(raised.value, MfxApiError)
