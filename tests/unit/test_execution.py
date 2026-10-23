"""``client.execution`` — the boundary that never raises.

These are the tests a trading loop's safety rests on: that a fault is a *result*, that nothing is
retried behind the caller's back, and that an unread outcome is never reported as retryable.
"""

from __future__ import annotations

import datetime as dt
import inspect
from decimal import Decimal
from typing import Any

import httpx
import pytest

from mfx.client import MfxClient
from mfx.execution import Execution
from mfx.results import CommandState, ExecutionResult, Reason

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx, body_of, error

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

COMMAND_ID = "0191f0c2-bbbb-7ccc-8ddd-000000000001"
WRITES = ("place_order", "cancel_order", "modify_order", "modify_position", "close_position",
          "close_position_by", "close_position_partial", "set_trailing_stop",
          "clear_trailing_stop")  # fmt: skip


def accepted(state: str = "ACCEPTED", **extra: Any) -> httpx.Response:
    return httpx.Response(
        202, json={"command_id": COMMAND_ID, "state": state, "duplicate": False, **extra}
    )


def command(state: str, result: dict[str, Any] | None, **extra: Any) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "command_id": COMMAND_ID,
            "terminal_id": TERMINAL_ID,
            "kind": "order_place",
            "state": state,
            "final": state in {"SUCCEEDED", "FAILED", "EXPIRED", "REJECTED"},
            "created_at": "2026-09-25T09:00:00Z",
            "updated_at": "2026-09-25T09:00:01Z",
            "result": result,
            **extra,
        },
    )


def filled(**changes: Any) -> dict[str, Any]:
    return {
        "ok": True,
        "reason": None,
        "retryable": False,
        "mt5_retcode": 10009,
        "retcode_text": "TRADE_RETCODE_DONE",
        "comment_raw": "filled",
        "terminal_state": "ACTIVE",
        "tickets": {"order": 8811, "deal": 9922, "position": 8811},
        "exec_price": "1.09431",
        "exec_volume": "0.10",
        "broker_latency_ms": 41,
        "agent_latency_ms": 7,
        "attempts": 1,
        **changes,
    }


def test_every_execution_write_requires_an_idempotency_key() -> None:
    """Given every Execution method that can place or change an order / When its signature is
    inspected / Then idempotency_key is there, keyword-only, and has no default.

    Every write carries a key the caller chose, checked on the boundary where it matters most.
    The other half of this rule — the client refusing a write that omits the key — is in
    test_terminals.py."""
    for name in WRITES:
        key = inspect.signature(getattr(Execution, name)).parameters.get("idempotency_key")
        assert key is not None and key.default is inspect.Parameter.empty, name
        assert key.kind is inspect.Parameter.KEYWORD_ONLY, name


async def test_placing_an_order_sends_what_was_asked_for_and_returns_the_command(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a market order / When it is placed / Then one POST carries the order and the key, and
    the answer is a result naming the command — not an exception, and not a fill that has not
    happened yet."""
    mfx.responses.append(accepted())

    result = await client.execution.place_order(
        TERMINAL_ID,
        symbol="EURUSD.sd",
        side="buy",
        volume="0.10",
        sl="1.0900",
        comment="strategy-7",
        idempotency_key="order-1",
    )

    request = mfx.last
    assert request.url.path == f"/v1/terminals/{TERMINAL_ID}/orders"
    assert request.headers["Idempotency-Key"] == "order-1"
    assert body_of(request) == {
        "symbol": "EURUSD.sd",
        "side": "buy",
        "volume": "0.10",
        "order_type": "market",
        "sl": "1.0900",
        "comment": "strategy-7",
    }
    assert result.command_id == COMMAND_ID
    assert result.state is CommandState.ACCEPTED
    assert result.ok is False and result.final is False, "accepted is not filled"
    assert result.idempotency_key == "order-1"
    assert result.client_rtt_ms >= 0


async def test_every_execution_result_carries_broker_and_agent_latency(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a command the platform has finished / When its result is read / Then broker and agent
    latency are reported separately, the SDK's own round trip is on every result, prices are
    Decimals, and the terminal state rides along.

    Gap G5 for the terminal state. The SDK's round trip is on every result,
    including the ones the platform never answered."""
    mfx.responses.append(command("SUCCEEDED", filled()))

    done = await client.execution.get_command(COMMAND_ID)

    assert done.ok is True and done.final is True
    assert done.broker_latency_ms == 41 and done.agent_latency_ms == 7
    assert done.client_rtt_ms >= 0
    assert done.exec_price == Decimal("1.09431"), "a decimal, not a float: a float price is wrong"
    assert done.exec_volume == Decimal("0.10")
    assert done.tickets.order == 8811 and done.tickets.position == 8811
    assert done.terminal_state == "ACTIVE", "gap G5: on every result"


async def test_execution_methods_never_raise_transport_timeout_and_429_are_results(
    private_key: object, sleeps: list[float]
) -> None:
    """Given a connection that never opened, one dropped after the order was sent, a timeout and a
    rate limit / When an order is placed into each / Then each is an ExecutionResult with its own
    reason, nothing is raised, and **nothing is retried**; only the order that never left may be
    sent again under a new key, and the dropped one reads UNKNOWN.

    A trading loop that has to catch exceptions to find out whether it has a position is a trading
    loop that will one day place two."""
    attempts: list[httpx.Request] = []

    def refuse(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        raise httpx.ConnectError("no route to host", request=request)

    def time_out(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        raise httpx.ReadTimeout("too slow", request=request)

    def drop(request: httpx.Request) -> httpx.Response:
        # The order was written to the connection and the server closed it before answering:
        # it may have reached the broker. Found by the shared suite's dropped-connection case.
        attempts.append(request)
        raise httpx.RemoteProtocolError("server disconnected without a response", request=request)

    for handler, reason, retryable, state in (
        (refuse, Reason.TRANSPORT_ERROR, True, None),
        (drop, Reason.TRANSPORT_ERROR, False, CommandState.UNKNOWN),
        (time_out, Reason.TIMEOUT, False, None),
    ):
        attempts.clear()
        async with MfxClient(
            BASE_URL, KEY_ID, private_key, transport=httpx.MockTransport(handler)
        ) as client:
            result = await client.execution.place_order(
                TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="k"
            )
        assert result.ok is False and result.reason is reason
        assert result.command_id is None, "it never reached the platform"
        assert result.final is True
        assert len(attempts) == 1, "never retried behind the caller's back"
        # A timeout is never retryable: the order may already be a position, and deal-history
        # reconciliation is the only safe recovery.
        assert result.retryable is retryable
        assert result.state is state

    limited = FakeMfx()
    limited.responses.append(error(429, "rate_limited", "over budget", **{"Retry-After": "30"}))
    async with MfxClient(
        BASE_URL, KEY_ID, private_key, transport=limited.transport, sleep=_no_wait(sleeps)
    ) as client:
        result = await client.execution.place_order(
            TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="k"
        )
    assert result.reason is Reason.RATE_LIMITED and result.ok is False
    assert len(limited.requests) == 1, "an execution 429 is never retried"
    assert sleeps == [], "and nothing waited"


async def test_result_reason_is_granular_not_bucketed_and_comment_raw_is_present(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a broker rejection / When the command is read / Then the reason is the platform's own
    granular one, the broker's comment is there verbatim beside it, and a reason this SDK has never
    heard of survives as itself rather than becoming "rejected_other"."""
    mfx.responses.append(
        command(
            "FAILED",
            filled(
                ok=False,
                reason="no_liquidity",
                retryable=True,
                mt5_retcode=10031,
                retcode_text="TRADE_RETCODE_NO_CONNECTION",
                comment_raw="No prices for EURUSD.sd",
            ),
        )
    )
    rejected = await client.execution.get_command(COMMAND_ID)
    assert rejected.reason is Reason.NO_LIQUIDITY
    assert rejected.mt5_retcode == 10031
    assert rejected.comment_raw == "No prices for EURUSD.sd"
    assert rejected.retryable is True

    mfx.responses.append(command("FAILED", filled(ok=False, reason="broker_on_fire")))
    novel = await client.execution.get_command(COMMAND_ID)
    assert novel.reason is None, "not forced into a bucket"
    assert novel.reason_text == "broker_on_fire", "and not lost either"


async def test_an_unknown_command_is_never_reported_as_retryable(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a command whose outcome could not be read / When it is inspected / Then it is not
    final and **not retryable**, whatever the body says.

    The order may have reached the broker. Re-sending it is how one fill becomes two, so
    the flag a caller acts on must not say "go ahead" while nobody knows."""
    mfx.responses.append(command("UNKNOWN", filled(ok=False, reason=None, retryable=True)))

    unread = await client.execution.get_command(COMMAND_ID)

    assert unread.state is CommandState.UNKNOWN
    assert unread.final is False
    assert unread.retryable is False, "the platform said true; UNKNOWN overrides it"


async def test_the_same_key_returns_the_original_command_and_says_so(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an order placed with an idempotency key / When the same key is sent again / Then the
    answer is the original command id, marked duplicate — never a second order."""
    mfx.responses.extend([accepted(), accepted(duplicate=True)])

    first = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="same"
    )
    again = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="same"
    )

    assert first.command_id == again.command_id
    assert first.duplicate is False and again.duplicate is True


async def test_cancel_modify_and_close_are_first_class(client: MfxClient, mfx: FakeMfx) -> None:
    """Given a pending order and an open position / When each is cancelled, modified, closed and
    part-closed / Then each is its own call on its own path.

    Gap G1: cancelling a pending order is not a modify with a special case. The reserved case named
    only cancel; this test is that case, widened to the three neighbours it cannot be proved
    without."""
    mfx.responses.extend([accepted()] * 4)

    await client.execution.cancel_order(TERMINAL_ID, 8811, idempotency_key="c1")
    assert mfx.last.url.path.endswith("/orders/8811/cancel")

    await client.execution.modify_position(TERMINAL_ID, 8811, sl="1.08", idempotency_key="m1")
    assert mfx.last.url.path.endswith("/positions/8811/modify")
    assert body_of(mfx.last) == {"sl": "1.08"}

    await client.execution.close_position(TERMINAL_ID, 8811, idempotency_key="x1")
    assert mfx.last.url.path.endswith("/positions/8811/close")

    await client.execution.close_position_partial(
        TERMINAL_ID, 8811, volume="0.05", idempotency_key="p1"
    )
    assert mfx.last.url.path.endswith("/positions/8811/close-partial")
    assert body_of(mfx.last) == {"volume": "0.05"}


async def test_a_modify_that_changes_nothing_is_refused_at_the_call(client: MfxClient) -> None:
    """The one thing this module raises on: a request that cannot mean anything. It never reached
    the platform, so there is no result to report."""
    with pytest.raises(ValueError, match="sl, tp, or both"):
        await client.execution.modify_position(TERMINAL_ID, 8811, idempotency_key="m")


async def test_waiting_for_a_command_stops_when_it_is_final(
    client: MfxClient, mfx: FakeMfx, sleeps: list[float]
) -> None:
    """wait_for polls until the command settles, backing off as it goes."""
    mfx.responses.extend(
        [
            command("EXECUTING", None),
            command("EXECUTING", None),
            command("SUCCEEDED", filled()),
        ]
    )

    done = await client.execution.wait_for(COMMAND_ID, timeout_s=30.0)

    assert done.final is True and done.ok is True
    assert len(mfx.requests) == 3
    assert sleeps == [0.2, 0.4], "it backs off rather than spinning"


async def test_waiting_gives_back_what_it_has_when_the_time_runs_out(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A command still running when the clock runs out is reported as it is — never raised, never
    guessed at, and never a licence to re-send."""
    mfx.responses.extend([command("EXECUTING", None)] * 12)

    stuck = await client.execution.wait_for(COMMAND_ID, timeout_s=0.0)

    assert stuck.final is False and stuck.retryable is False
    assert len(mfx.requests) == 1


async def test_a_platform_refusal_is_a_result_with_the_reason_it_gave(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a refusal the platform states — no execution usage on this farm, a suspended tenant —
    / When an order is placed / Then it is a result carrying what the platform said, not an
    exception a trading loop has to catch."""
    mfx.responses.extend(
        [
            error(403, "forbidden", "execution_not_permitted: the farm has no order_execution"),
            error(409, "state_error", "tenant suspended"),
        ]
    )

    refused = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="k1"
    )
    assert refused.ok is False and refused.reason is Reason.REFUSED
    assert "execution_not_permitted" in (refused.detail or "")
    assert refused.retryable is False

    suspended = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="k2"
    )
    assert suspended.reason is Reason.REFUSED and "suspended" in (suspended.detail or "")


async def test_an_answer_the_sdk_cannot_read_is_a_result_too(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A 200 carrying something that is not a command — a proxy's HTML, a truncated body — is a
    refusal with the call named, never a parse error escaping into a trading loop."""
    mfx.responses.append(httpx.Response(200, content=b"<html>gateway</html>"))
    unreadable = await client.execution.get_command(COMMAND_ID)
    assert unreadable.reason is Reason.REFUSED
    assert "commands" in (unreadable.detail or "")

    mfx.responses.append(httpx.Response(202, content=b"{not json"))
    nonsense = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD", side="buy", volume="0.1", idempotency_key="k"
    )
    assert nonsense.command_id is None, "nothing usable, and nothing invented"


def test_a_body_that_is_not_an_object_yields_nothing_rather_than_raising() -> None:
    """The last line of defence in this module: whatever arrived, reading it must not raise inside
    a call whose whole contract is that it does not."""
    from types import SimpleNamespace

    from mfx.execution import _body_of  # noqa: PLC0415 - the parser under test

    assert _body_of(SimpleNamespace(content=b'{"command_id": "x"}')) == {"command_id": "x"}
    assert _body_of(SimpleNamespace(content=b"{not json")) == {}
    assert _body_of(SimpleNamespace(content=b"[1,2,3]")) == {}
    assert _body_of(SimpleNamespace(content=b"")) == {}


def test_a_price_that_is_not_a_number_is_none_rather_than_a_guess() -> None:
    """Prices arrive as decimal strings. One that is not a number is unknown, not zero."""
    from mfx.results import _decimal, _state  # noqa: PLC0415 - the parsers under test

    assert _decimal("1.5") == Decimal("1.5")
    assert _decimal(None) is None
    assert _decimal("not a price") is None
    assert _state("EXECUTING") is CommandState.EXECUTING
    assert _state("INVENTED_LATER") is None, "a state this version does not know is not a guess"


def _no_wait(sleeps: list[float]) -> Any:
    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    return sleep


def test_an_execution_result_is_the_whole_answer() -> None:
    """Every field a caller needs is on one object, so nothing has to be looked up elsewhere."""
    result = ExecutionResult.refused(
        Reason.TIMEOUT, idempotency_key="k", client_rtt_ms=31.0, detail="timed out"
    )
    assert result.ok is False and result.retryable is False and result.final is True
    assert result.tickets.order is None
    assert "timed out" in (result.detail or "")


async def test_a_computed_float_is_refused_at_the_call_site_not_sent(client: MfxClient) -> None:
    """Given a size computed the way position sizing computes one — a risk budget over a stop
    distance — which in binary is 0.21000000000000002 rather than 0.21
    When it is passed to place_order as a float
    Then the SDK raises TypeError naming the field and saying what to send, and nothing is sent. A
    400 from the edge would be a worse answer, and accepting it would leave the caller believing
    their computed size arrived intact."""
    computed = 0.07 * 3
    assert computed != 0.21, "the premise: a computed float is not the decimal you meant"

    with pytest.raises(TypeError, match="must be a Decimal, a str or an int, not a float"):
        await client.execution.place_order(
            TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume=computed, idempotency_key="f1"
        )
    with pytest.raises(TypeError, match="sl must be"):
        await client.execution.modify_position(TERMINAL_ID, 8811, sl=1.08, idempotency_key="f2")
    with pytest.raises(TypeError, match="volume must be"):
        await client.execution.close_position_partial(
            TERMINAL_ID, 8811, volume=0.05, idempotency_key="f3"
        )


@pytest.mark.parametrize(
    ("given", "wire"),
    [
        (Decimal("0.21"), "0.21"),
        (Decimal("0.07") * 3, "0.21"),
        ("0.21", "0.21"),
        (1, "1"),
        (Decimal("1E+3"), "1000"),
        (Decimal("0.0000001"), "0.0000001"),
        (Decimal("1.10021"), "1.10021"),
    ],
)
async def test_every_accepted_decimal_reaches_the_wire_in_plain_notation(
    client: MfxClient, mfx: FakeMfx, given: object, wire: str
) -> None:
    """Given a Decimal, a string or an int — including the two forms str() would render in
    scientific notation
    When an order is placed
    Then the body carries plain notation, because the contract's pattern refuses an exponent:
    str(Decimal("0.0000001")) is "1E-7" and str(Decimal("1E+3")) is "1E+3", so the SDK uses
    format(value, "f"). Decimal("0.07") * 3 is exactly 0.21, which is the point of Decimal."""
    mfx.responses.append(accepted())
    await client.execution.place_order(
        TERMINAL_ID,
        symbol="EURUSD.sd",
        side="buy",
        volume=given,  # type: ignore[arg-type]
        idempotency_key=f"d-{wire}",
    )
    assert body_of(mfx.last)["volume"] == wire
    assert "E" not in body_of(mfx.last)["volume"]


async def test_a_string_that_is_not_a_decimal_is_refused_with_the_field_named(
    client: MfxClient,
) -> None:
    """Given a string that is not a decimal, and a negative one
    When either is passed
    Then ValueError names the field and shows the value. The SDK refuses locally what the edge would
    refuse anyway, so the error arrives where the caller can see which argument caused it."""
    for bad in ("", "abc", "1,5", "-0.21", "nan", "Infinity"):
        with pytest.raises(ValueError, match="volume"):
            await client.execution.place_order(
                TERMINAL_ID,
                symbol="EURUSD.sd",
                side="buy",
                volume=bad,
                idempotency_key=f"b-{bad}",
            )


async def test_modify_order_merges_the_sent_fields_and_tells_the_three_expiry_states_apart(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a pending order's ticket
    When a tenant amends its price and stop, then its expiry three ways
    Then each is one POST to the order's own modify path carrying only what was sent (what is not
    sent is left to the order, 2.13), and the expiry is told apart: leaving expires_at out omits
    it, None sends it as null (good-till-cancelled), and a time sends that instant."""
    mfx.responses.extend([accepted()] * 4)

    await client.execution.modify_order(
        TERMINAL_ID, 8811, price="1.20500", sl="1.21500", idempotency_key="am-1"
    )
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/orders/8811/modify"
    assert mfx.last.headers["Idempotency-Key"] == "am-1"
    assert body_of(mfx.last) == {"price": "1.20500", "sl": "1.21500"}

    await client.execution.modify_order(TERMINAL_ID, 8811, sl="0", idempotency_key="am-2")
    assert body_of(mfx.last) == {"sl": "0"}

    await client.execution.modify_order(TERMINAL_ID, 8811, expires_at=None, idempotency_key="am-3")
    assert body_of(mfx.last) == {"expires_at": None}

    when = dt.datetime(2026, 9, 16, 18, 0, tzinfo=dt.UTC)
    await client.execution.modify_order(TERMINAL_ID, 8811, expires_at=when, idempotency_key="am-4")
    body = body_of(mfx.last)
    assert set(body) == {"expires_at"} and body["expires_at"].startswith("2026-09-16T18:00:00")


async def test_modify_order_needs_a_change_and_refuses_a_float(client: MfxClient) -> None:
    """Given an amend with nothing to change, and one that carries a float price
    When each is called
    Then the first is a ValueError at the call (it can mean nothing), and the second is refused
    because a float price is a wrong price; neither reaches MFX."""
    with pytest.raises(ValueError, match="price, stop_limit_price, sl, tp, or expires_at"):
        await client.execution.modify_order(TERMINAL_ID, 8811, idempotency_key="none")

    with pytest.raises((ValueError, TypeError)):
        await client.execution.modify_order(TERMINAL_ID, 8811, price=1.205, idempotency_key="flt")


async def test_a_stop_limit_order_carries_both_prices_and_an_amend_can_set_the_second(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant placing a stop-limit order, then amending only its second price
    When each call is made
    Then the place is one POST with order_type stop_limit, price as the stop price and
    stop_limit_price as the limit placed when it wakes, both decimal strings; the
    amend carries stop_limit_price and nothing else; and a float second price is
    refused before the wire, as every price is."""
    mfx.responses.extend([accepted()] * 2)

    await client.execution.place_order(
        TERMINAL_ID,
        symbol="EURUSD.sd",
        side="buy",
        volume="0.10",
        order_type="stop_limit",
        price="1.10500",
        stop_limit_price=Decimal("1.10400"),
        idempotency_key="sl-1",
    )
    body = body_of(mfx.last)
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/orders"
    assert (body["order_type"], body["price"], body["stop_limit_price"]) == (
        "stop_limit",
        "1.10500",
        "1.10400",
    )

    await client.execution.modify_order(
        TERMINAL_ID, 8811, stop_limit_price="1.10300", idempotency_key="sl-2"
    )
    assert body_of(mfx.last) == {"stop_limit_price": "1.10300"}

    with pytest.raises((ValueError, TypeError)):
        await client.execution.modify_order(
            TERMINAL_ID,
            8811,
            stop_limit_price=1.103,  # type: ignore[arg-type]
            idempotency_key="sl-3",
        )
    assert len(mfx.requests) == 2, "the float never reached MFX"


async def test_a_position_is_closed_by_an_opposite_one_and_a_refusal_is_a_result(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a hedging account with two opposite positions, and then two tickets the platform
    refuses
    When a tenant closes one by the other
    Then it is one POST to the position's own close-by path naming the opposite ticket, with the
    idempotency key; and the refusal comes back as a result that is not
    ok, never as an exception, like every other order call."""
    mfx.responses.extend([accepted(), error(422, "invalid_request", "by_ticket must differ")])

    taken = await client.execution.close_position_by(
        TERMINAL_ID, 8811, 8812, idempotency_key="cb-1"
    )

    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/positions/8811/close-by"
    assert mfx.last.headers["Idempotency-Key"] == "cb-1"
    assert body_of(mfx.last) == {"by_ticket": 8812}
    assert taken.command_id is not None

    refused = await client.execution.close_position_by(
        TERMINAL_ID, 8811, 8811, idempotency_key="cb-2"
    )
    assert not refused.ok
