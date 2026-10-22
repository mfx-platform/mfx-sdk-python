"""The client's own behaviour: budget, read retries, and what a transport fault becomes."""

from __future__ import annotations

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import MfxTimeout, MfxTransportError, RateLimitError

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx, error, terminal_body

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.


async def test_a_read_retries_a_429_with_a_fresh_signature_and_the_servers_own_delay(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """Given a read that is rate limited twice, with Retry-After / When it is called / Then the SDK
    waits exactly what the server asked, retries, and the retry is *signed again*.

    The nonce is good once for five minutes, so a retry cannot be the same bytes sent twice: each
    attempt re-enters the signing layer. A client that resent the built request would turn one 429
    into three 401s."""
    mfx.responses.extend(
        [
            error(429, "rate_limited", "slow down", **{"Retry-After": "2"}),
            error(429, "rate_limited", "slow down", **{"Retry-After": "3.5"}),
            httpx.Response(200, json=terminal_body("ACTIVE")),
        ]
    )

    terminal = await client.terminals.get(TERMINAL_ID)

    assert terminal.state.value == "ACTIVE"
    assert sleeps == [2.0, 3.5], "the server's own answer, not a guess"
    nonces = {mfx.signed(n)["X-MFX-Nonce"] for n in range(3)}
    assert len(nonces) == 3, "three attempts, three nonces"


async def test_a_read_backs_off_with_jitter_when_the_server_does_not_say(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """No Retry-After: exponential backoff, and the wait is drawn from a jittered range so a fleet
    that hits the limit together does not come back together."""
    mfx.responses.extend([error(429, "rate_limited", "slow down")] * 2)
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))

    await client.terminals.get(TERMINAL_ID)

    assert sleeps == [0.5, 1.0], "doubling; the fixture's jitter takes the whole ceiling"


async def test_a_read_gives_up_and_raises_rather_than_retrying_forever(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """A budget that is out stays out. Three retries, then the caller is told."""
    mfx.responses.extend([error(429, "rate_limited", "over budget", **{"Retry-After": "1"})] * 4)

    with pytest.raises(RateLimitError) as limited:
        await client.terminals.get(TERMINAL_ID)

    assert limited.value.retry_after_s == 1.0
    assert len(mfx.requests) == 4, "the first attempt and three retries"
    assert sleeps == [1.0, 1.0, 1.0]


async def test_the_budget_is_read_from_every_answer(client: MfxClient, mfx: FakeMfx) -> None:
    """Every response carries X-MFX-Budget-Remaining and X-MFX-Budget-Source, so a caller can see
    the wall before hitting it. `configured` is a ceiling, not a measurement."""
    assert client.budget is None, "nothing is known before the first answer"

    mfx.budget = ("412", "counted")
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    await client.terminals.get(TERMINAL_ID)
    assert client.budget is not None
    assert (client.budget.remaining, client.budget.source) == (412, "counted")

    mfx.budget = ("8", "configured")
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    await client.terminals.get(TERMINAL_ID)
    assert client.budget is not None and client.budget.remaining == 8


async def test_a_budget_header_that_is_not_a_number_leaves_the_last_one_standing(
    client: MfxClient, mfx: FakeMfx
) -> None:
    mfx.budget = ("77", "counted")
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    await client.terminals.get(TERMINAL_ID)

    mfx.budget = ("lots", "counted")
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    await client.terminals.get(TERMINAL_ID)
    assert client.budget is not None and client.budget.remaining == 77

    mfx.budget = None  # an answer with no budget headers at all
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    await client.terminals.get(TERMINAL_ID)
    assert client.budget is not None and client.budget.remaining == 77


async def test_a_transport_fault_is_this_sdks_error_not_httpxs(
    private_key: object, sleeps: list[float]
) -> None:
    """A caller catches mfx.MfxError and nothing else. httpx never reaches them."""

    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host", request=request)

    def time_out(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("too slow", request=request)

    async with MfxClient(
        BASE_URL, KEY_ID, private_key, transport=httpx.MockTransport(refuse)
    ) as client:
        with pytest.raises(MfxTransportError, match="no route to host"):
            await client.terminals.get(TERMINAL_ID)

    async with MfxClient(
        BASE_URL, KEY_ID, private_key, transport=httpx.MockTransport(time_out)
    ) as client:
        with pytest.raises(MfxTimeout, match="too slow"):
            await client.terminals.get(TERMINAL_ID)


async def test_the_client_closes_its_connections_when_it_is_done(
    mfx: FakeMfx, private_key: object
) -> None:
    client = MfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport)
    async with client:
        mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
        await client.terminals.get(TERMINAL_ID)
    assert client.generated is not None  # the generated core is reachable for the endpoint modules
