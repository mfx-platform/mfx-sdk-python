"""``client.terminals`` — a tenant's first hour.

Ask for a terminal, put a login on it, watch it, retire it. These assert what goes on the wire,
because the SDK's job is to be the one place that is right about the contract.
"""

from __future__ import annotations

import inspect
import json

import httpx
import pytest

from mfx._generated.models.tenant_terminal import TenantTerminal
from mfx._generated.models.tenant_terminal_state import TenantTerminalState
from mfx.client import MfxClient
from mfx.errors import (
    ConflictError,
    MfxApiError,
    NotFoundError,
    PlacementError,
    RateLimitError,
    UnsupportedBrokerError,
    ValidationError,
)
from mfx.secrets import Secret
from mfx.terminals import Terminals, is_usable

from .conftest import (
    BROKER_ID,
    FARM_ID,
    SERVER_ID,
    TERMINAL_ID,
    FakeMfx,
    accepted,
    body_of,
    error,
    page,
    terminal_body,
)

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.

WRITES = ("create", "submit_credentials", "drain", "retire")


def test_write_without_idempotency_key_is_refused_by_the_sdk() -> None:
    """Given the SDK's write methods / When one is called without an idempotency key / Then it is a
    TypeError at the call, not a request MFX has to refuse.

    The parameter is required and keyword-only, and it has **no default**. A default
    would be a key nobody chose, which is worse than none: the caller would retry with a fresh one
    and get a second terminal, which is the whole failure idempotency exists to prevent."""
    for name in WRITES:
        signature = inspect.signature(getattr(Terminals, name))
        key = signature.parameters.get("idempotency_key")
        assert key is not None, f"{name} takes no idempotency_key"
        assert key.default is inspect.Parameter.empty, f"{name} defaults its idempotency_key"
        assert key.kind is inspect.Parameter.KEYWORD_ONLY, f"{name} allows it positionally"


async def test_asking_for_a_terminal_sends_what_the_tenant_asked_for(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant with a farm, a broker and a server / When it asks for a streaming terminal /
    Then one POST /terminals goes out carrying the idempotency key as a header and the request as
    the body, and the answer is the terminal in state REQUESTED.

    The instruments are the broker's own names and the SDK does not touch them: MFX never renames
    an instrument on a tenant's behalf."""
    mfx.responses.append(accepted("REQUESTED"))

    terminal = await client.terminals.create(
        farm_id=FARM_ID,
        broker_id=BROKER_ID,
        server_id=SERVER_ID,
        streaming=True,
        instruments=["EURUSD.sd", "BTCUSD.lv"],
        labels={"desk": "fx-1"},
        idempotency_key="first-terminal",
    )

    request = mfx.last
    assert request.method == "POST"
    assert request.url.path == "/v1/terminals"
    assert request.headers["Idempotency-Key"] == "first-terminal"
    assert body_of(request) == {
        "farm_id": FARM_ID,
        "broker_id": BROKER_ID,
        "server_id": SERVER_ID,
        "streaming": True,
        "execution": False,
        "instruments": ["EURUSD.sd", "BTCUSD.lv"],
        "labels": {"desk": "fx-1"},
        "redundancy": "none",
    }
    assert str(terminal.id) == TERMINAL_ID
    assert terminal.state.value == "REQUESTED"


async def test_a_credential_is_sent_once_and_never_rendered(
    client: MfxClient, mfx: FakeMfx, caplog: pytest.LogCaptureFixture
) -> None:
    """Given a broker password / When it is submitted for a terminal / Then it is in the request
    body exactly once and appears in no repr, no log line and no exception text, and the answer is
    a reference with execution_disabled on it.

    The only request in MFX that carries a secret. A password that reaches a log has
    already leaked, whatever the response says."""
    mfx.responses.append(
        httpx.Response(
            202,
            json={
                # Deliberately low-entropy: a random-looking uuid beside a key called
                # credential_ref_id is what a secret scanner is for, and a test fixture should not
                # be the thing that teaches everyone to ignore it.
                "credential_ref_id": "00000000-0000-4000-8000-000000000001",
                "terminal_id": TERMINAL_ID,
                "cred_type": "investor",
                "execution_disabled": True,
                # Required since credential rotation: a first credential replaced
                # nothing and is used at the terminal's first login, so no operation was opened.
                "rotated": False,
                "takes_effect": "first_login",
                "operation_id": None,
            },
        )
    )
    password = "s3cret-Pepperstone!"

    with caplog.at_level("DEBUG"):
        accepted_ref = await client.terminals.submit_credentials(
            TERMINAL_ID,
            login=61587349,
            password=Secret(password),
            server="EquitiSecurities-Demo",
            cred_type="investor",
            idempotency_key="cred-1",
        )

    request = mfx.last
    assert request.url.path == f"/v1/terminals/{TERMINAL_ID}/credentials"
    assert body_of(request)["password"] == password, "sent once, in the body, where it belongs"
    assert accepted_ref.execution_disabled is True, "an investor credential turns execution off"
    assert password not in caplog.text
    assert password not in repr(Secret(password))
    assert password not in f"{Secret(password)}"
    assert password not in str(Secret(password))


async def test_watching_a_terminal_reach_active_and_retiring_it(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal that is LOGGING_IN / When it is polled until ACTIVE and then retired /
    Then each poll is a GET on its own path, and the retirement is a DELETE carrying an idempotency
    key and answered with the terminal DRAINING.

    This is the tenant half of the from-scratch proof, in four calls."""
    mfx.responses.extend(
        [
            httpx.Response(200, json=terminal_body("LOGGING_IN")),
            httpx.Response(200, json=terminal_body("ACTIVE", login_masked="****7349")),
            httpx.Response(202, json=terminal_body("DRAINING")),
        ]
    )

    assert (await client.terminals.get(TERMINAL_ID)).state.value == "LOGGING_IN"
    active = await client.terminals.get(TERMINAL_ID)
    assert active.state.value == "ACTIVE" and active.login_masked == "****7349"

    retired = await client.terminals.retire(TERMINAL_ID, idempotency_key="retire-1")

    assert [r.method for r in mfx.requests] == ["GET", "GET", "DELETE"]
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}"
    assert mfx.last.headers["Idempotency-Key"] == "retire-1"
    assert retired.state.value == "DRAINING", "retire is answered with the state now, not RETIRED"


async def test_a_list_follows_the_cursor_and_yields_every_terminal(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given more terminals than one page holds / When they are listed / Then every terminal is
    yielded, each page is fetched with the previous page's cursor, and the walk stops on a null
    cursor.

    There is no total and no page number in this API and there never will be (guardrail 7), so the
    cursor is the only way to advance."""
    first = [terminal_body("ACTIVE", id=f"0191f0c2-0000-7000-8000-00000000000{n}") for n in (1, 2)]
    second = [terminal_body("REQUESTED", id="0191f0c2-0000-7000-8000-000000000003")]
    mfx.responses.extend([page(first, "cursor-2"), page(second, None)])

    seen = [str(terminal.id) async for terminal in client.terminals.list(limit=2)]

    assert seen == [
        "0191f0c2-0000-7000-8000-000000000001",
        "0191f0c2-0000-7000-8000-000000000002",
        "0191f0c2-0000-7000-8000-000000000003",
    ]
    assert mfx.requests[0].url.params.get("limit") == "2"
    assert "cursor" not in mfx.requests[0].url.params
    assert mfx.requests[1].url.params.get("cursor") == "cursor-2"


async def test_a_page_reports_what_it_returned_without_pretending_to_be_a_total(
    client: MfxClient, mfx: FakeMfx
) -> None:
    mfx.responses.append(page([terminal_body("ACTIVE")], None))
    one = await client.terminals.page()
    assert one.returned == 1 and one.next_cursor is None and len(one.items) == 1


async def test_read_methods_raise_the_typed_hierarchy_mapped_from_http(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given failures of each kind / When a read or a write meets one / Then the SDK raises the
    typed error for the API's own error *code*, not for the status.

    Two 409s that mean different things are different exceptions: a conflict is "not from this
    state", a placement error is "no farm can carry this". A caller that has to read a string to
    tell them apart will not."""
    mfx.responses.extend(
        [
            error(404, "not_found", "no such terminal"),
            error(409, "placement_error", "no farm carries md:write in uk-west"),
            error(409, "state_error", "a RETIRED terminal cannot be drained"),
            error(422, "validation_error", "server does not belong to broker"),
        ]
    )

    with pytest.raises(NotFoundError) as not_found:
        await client.terminals.get(TERMINAL_ID)
    assert not_found.value.status == 404 and not_found.value.code == "not_found"
    assert "no such terminal" in str(not_found.value)

    with pytest.raises(PlacementError):
        await client.terminals.create(
            farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
        )
    with pytest.raises(ConflictError):  # StateError is one
        await client.terminals.drain(TERMINAL_ID, idempotency_key="k")
    with pytest.raises(ValidationError):
        await client.terminals.create(
            farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
        )


async def test_an_unsupported_broker_or_server_is_one_refusal_that_says_which_switch_was_closed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a broker MFX may not carry, or a server switched off / When a terminal is requested on
    it / Then the request is refused at request time as UnsupportedBrokerError, carrying which of
    the two switches was closed.

    The distinction is what the caller acts on: `server_disabled` means try another server of the
    same broker, `permission` means this broker is not available at all. Bucketing both into
    "conflict" leaves a tenant re-requesting the same refusal forever.

    It is mapped by the API's error *code*, not by its status, and that is the only
    way to get it right: a 422 `validation_error` on this route means the request names no broker
    or server MFX lists at all, while this 409 means one it *does* list and cannot use now. The
    first is the caller's mistake, the second is a fact that may change in an hour. Mapping by
    status would merge them."""
    refusal = {
        "error": {
            "code": "broker_not_supported",
            "message": "Pepperstone is not onboarded for this tenant yet.",
            "details": {
                "refused_by": "permission",
                "reason": "broker_not_onboarded",
                "broker_id": BROKER_ID,
                "server_id": SERVER_ID,
            },
        }
    }
    disabled = {
        "error": {
            "code": "broker_not_supported",
            "message": "EquitiSecurities-Demo is switched off while its canary set is rebuilt.",
            "details": {"refused_by": "server_disabled", "reason": "server_switched_off"},
        }
    }
    mfx.responses.extend([httpx.Response(409, json=refusal), httpx.Response(422, json=disabled)])

    with pytest.raises(UnsupportedBrokerError) as not_permitted:
        await client.terminals.create(
            farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
        )
    assert not_permitted.value.refused_by == "permission"
    assert not_permitted.value.reason == "broker_not_onboarded"
    assert not_permitted.value.broker_id == BROKER_ID
    assert not_permitted.value.server_id == SERVER_ID
    assert "not onboarded" in str(not_permitted.value), "the operator's own sentence survives"
    assert isinstance(not_permitted.value, ConflictError), "still catchable by the broader kind"

    with pytest.raises(UnsupportedBrokerError) as switched_off:
        await client.terminals.create(
            farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
        )
    assert switched_off.value.refused_by == "server_disabled", "the code decides, not the status"
    assert switched_off.value.broker_id is None, "absent is None, never an invented id"
    assert switched_off.value.server_id is None


async def test_an_error_the_sdk_has_never_seen_is_still_typed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A code this version does not know, and a body that is not JSON at all, both arrive as
    MfxApiError carrying the status — never as a KeyError from inside the SDK."""
    mfx.responses.extend(
        [
            error(418, "brand_new_code", "invented after this SDK shipped"),
            httpx.Response(503, content=b"<html>gateway</html>"),
        ]
    )

    with pytest.raises(MfxApiError) as unknown:
        await client.terminals.get(TERMINAL_ID)
    assert unknown.value.status == 418 and unknown.value.code == "brand_new_code"

    with pytest.raises(MfxApiError) as not_json:
        await client.terminals.get(TERMINAL_ID)
    assert not_json.value.status == 503
    assert f"GET /terminals/{TERMINAL_ID} failed" in str(not_json.value)


async def test_a_success_with_no_body_is_a_contract_breach_not_a_terminal(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A 2xx carrying an error envelope would otherwise be read as a terminal, and the caller would
    find out by reading .state off it."""
    mfx.responses.append(
        httpx.Response(202, json={"error": {"code": "conflict", "message": "confused"}})
    )
    with pytest.raises(MfxApiError, match="could not read"):
        await client.terminals.create(
            farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
        )


async def test_a_page_that_is_not_a_page_is_refused(client: MfxClient, mfx: FakeMfx) -> None:
    """An answer the SDK cannot read is named as such, with the call that produced it — never a
    ValueError from inside a generated module."""
    mfx.responses.append(httpx.Response(200, json=["not", "a", "page"]))
    with pytest.raises(MfxApiError, match="GET /terminals answered something"):
        await client.terminals.page()


async def test_rate_limit_is_raised_with_what_the_server_said(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """A write is never retried, so its 429 reaches the caller with Retry-After on it."""
    mfx.responses.append(error(429, "rate_limited", "over budget", **{"Retry-After": "12"}))
    with pytest.raises(RateLimitError) as limited:
        await client.terminals.retire(TERMINAL_ID, idempotency_key="k")
    assert limited.value.retry_after_s == 12.0
    assert len(mfx.requests) == 1, "a retried write is a second order"


async def test_the_json_the_sdk_sends_is_the_json_the_spec_describes(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """No nulls for things the caller did not set: an absent optional is absent, not null, because
    additionalProperties is false and a null is a value."""
    mfx.responses.append(accepted())
    await client.terminals.create(
        farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="k"
    )
    sent = json.loads(mfx.last.content)
    assert "instruments" not in sent and "labels" not in sent


async def test_a_terminal_can_be_created_without_naming_a_farm(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant that does not care which farm a terminal lands on
    When it creates one without a farm_id
    Then the field is absent from the body rather than sent as null, and naming one still names it.

    Absent and null are not the same thing on the wire: the contract makes `farm_id`
    optional, and a JSON `null` would be a value the server must reject rather than a field it may
    fill in. The platform then chooses - own ACTIVE farms first, then shared, in the server's
    region, with room - and reports the choice on the answer, so it is never silent.
    """
    mfx.responses.append(accepted("REQUESTED"))

    await client.terminals.create(
        broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="no-farm"
    )

    assert "farm_id" not in body_of(mfx.last), "omitted, not null: the platform chooses"

    mfx.responses.append(accepted("REQUESTED"))
    await client.terminals.create(
        farm_id=FARM_ID, broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="a-farm"
    )
    assert body_of(mfx.last)["farm_id"] == FARM_ID, "naming one still names it"


async def test_a_stuck_terminal_is_restarted_through_the_sdk(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal that needs restarting, one of them holding open positions
    When the tenant restarts it through the SDK
    Then the reason and the open-positions confirmation reach the platform as sent, the idempotency
    key is required as on every other write, and the operation to follow it comes back.

    The endpoint and the generated call for it existed before there was a hand-written
    surface - so a tenant had to import from `mfx._generated`, which is private by
    convention and regenerated. `confirm_open_positions` defaults to False here because that is the
    platform's own default and the point of the flag: a restart drops the broker session for a few
    seconds, and on an account with positions open that is a decision taken deliberately rather
    than inherited from a library.
    """
    mfx.responses.extend(
        [
            httpx.Response(202, json={"operation_id": str(TERMINAL_ID), "state": "ACCEPTED"}),
            httpx.Response(202, json={"operation_id": str(TERMINAL_ID), "state": "ACCEPTED"}),
        ]
    )

    accepted_plain = await client.terminals.restart(
        TERMINAL_ID, reason="it has stopped quoting", idempotency_key="k1"
    )
    assert accepted_plain.state == "ACCEPTED"
    sent = body_of(mfx.requests[-1])
    # `queue` is the contract's own default, sent as the generated model states
    # it: a refusal for a busy platform stays a 429 unless the caller asks to be held.
    assert sent == {
        "reason": "it has stopped quoting",
        "confirm_open_positions": False,
        "queue": False,
    }
    assert mfx.requests[-1].url.path.endswith(f"/terminals/{TERMINAL_ID}/restart")
    assert mfx.requests[-1].headers["Idempotency-Key"] == "k1"

    await client.terminals.restart(
        TERMINAL_ID,
        reason="checking a terminal on a full core",
        idempotency_key="k2",
        confirm_open_positions=True,
    )
    assert body_of(mfx.requests[-1])["confirm_open_positions"] is True

    with pytest.raises(TypeError):
        await client.terminals.restart(TERMINAL_ID, reason="no key")  # type: ignore[call-arg]


async def test_an_offline_terminal_is_not_usable_and_says_why(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal whose cell was turned off outside MFX Hub
    When the SDK reads it
    Then its state is OFFLINE, `offline_reason` says which of the three causes, and `is_usable`
    is false.

    A terminal is ACTIVE only while its cell can run it. Before OFFLINE
    existed, a terminal whose cell had been turned off, whose VM was gone, or which had not been
    heard from for minutes still read ACTIVE - so a caller that checked `state == "ACTIVE"` was
    told it could trade when there was nothing on the other end. The SDK has to carry the new
    value, or every caller's check is wrong in the same way.
    """
    mfx.responses.append(
        httpx.Response(200, json=terminal_body("OFFLINE", offline_reason="power_off"))
    )
    terminal = await client.terminals.get(TERMINAL_ID)

    assert terminal.state.value == "OFFLINE"
    assert terminal.offline_reason == "power_off"
    assert is_usable(terminal) is False


def test_exactly_one_terminal_state_is_usable_so_a_new_one_cannot_read_as_usable() -> None:
    """Given every terminal state the contract defines
    When each is tested for usability
    Then only ACTIVE is usable, and a state the SDK has not been taught about is not.

    The rule is "anything that treats ACTIVE as usable must treat OFFLINE as not
    usable", and the way to keep that true is to make usability a closed question asked in one
    place. A state added to the contract tomorrow is not usable until somebody decides it is, which
    is the safe direction to be wrong in: refusing to trade on a terminal that turns out to be fine
    costs a retry, and trading on one that is not costs an order.
    """
    usable = {
        state.value
        for state in TenantTerminalState
        if is_usable(TenantTerminal.from_dict(terminal_body(state.value)))
    }
    assert usable == {"ACTIVE"}
    assert "OFFLINE" in {state.value for state in TenantTerminalState}, "the contract carries it"


async def test_offline_reason_is_null_in_every_other_state(client: MfxClient, mfx: FakeMfx) -> None:
    """Given an ACTIVE terminal
    When the SDK reads it
    Then `offline_reason` is null, and a terminal answered without the field at all still parses.

    `offline_reason` is null in every state but OFFLINE. It is additive, so a control
    plane that has not shipped it yet omits it - and an SDK that cannot read that answer would turn
    a rollout into an outage.
    """
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE", offline_reason=None)))
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    explicit = await client.terminals.get(TERMINAL_ID)
    omitted = await client.terminals.get(TERMINAL_ID)

    assert explicit.offline_reason is None
    assert is_usable(explicit) is True
    assert is_usable(omitted) is True


async def test_a_parked_terminal_reads_and_is_not_usable_and_an_unknown_state_is_named(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a terminal the platform has parked: a suspended tenant whose service was
    resumed still has its terminals PARKED until the login queue reaches each
    When the SDK reads it, alone and in a list beside an ACTIVE one
    Then it reads as PARKED, the list is read whole, and `is_usable` is false for it.
    And when the platform answers a state this SDK has never heard of, the caller gets an MFX
    error that names the call and the value, never a ValueError from inside a generated module.

    The generated enum once lacked PARKED, so `terminals.list()` raised in exactly the
    minutes after Resume, when a tenant is most likely to be looking.
    """
    mfx.responses.append(httpx.Response(200, json=terminal_body("PARKED")))
    mfx.responses.append(
        page(
            [terminal_body("ACTIVE"), terminal_body("PARKED", id=str(TERMINAL_ID)[:-1] + "9")],
            None,
        )
    )
    parked = await client.terminals.get(TERMINAL_ID)
    listed = [terminal async for terminal in client.terminals.list()]

    assert parked.state is TenantTerminalState.PARKED
    assert is_usable(parked) is False
    assert [t.state.value for t in listed] == ["ACTIVE", "PARKED"]
    assert [is_usable(t) for t in listed] == [True, False]

    mfx.responses.append(httpx.Response(200, json=terminal_body("HIBERNATING")))
    with pytest.raises(MfxApiError, match="HIBERNATING") as raised:
        await client.terminals.get(TERMINAL_ID)
    assert raised.value.code == "contract_breach"
