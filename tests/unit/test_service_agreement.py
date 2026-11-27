"""The Service Agreement: what an organisation must accept before it can add anything.

Each plan has its own Service Agreement, and a plan change waits until an owner or an admin
accepts the new plan's. While a change waits, or a version of an agreement, the Terms or the
MetaTrader 5 licence is past its grace period unaccepted, additions (a terminal, an expert
advisor, an API key, higher limits) are refused 409; nothing running is ever refused. Every
answer carries ``MFX-Service-Agreement: due`` while something is due, and
``GET /tenant/service-agreement`` says what (legal documents design, section 7).
"""

from __future__ import annotations

import asyncio
import datetime as dt
import logging
import threading
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import mfx as sdk
from mfx._generated.models.tenant_service_agreement import TenantServiceAgreement
from mfx.client import MfxClient
from mfx.errors import (
    ConflictError,
    DocumentDue,
    PlanChange,
    ServiceAgreementNotAccepted,
    TermsNotAccepted,
)
from mfx.sync import SyncMfxClient

from .conftest import BASE_URL, BROKER_ID, KEY_ID, SERVER_ID, TERMINAL_ID, FakeMfx

CHANGE = "5b1e2c3d-4f5a-4b6c-8d7e-9f0a1b2c3d4e"
ACCEPT_URL = "https://portal.mfxhub.com/organisation/legal"
SA_WORDS = "Your organisation must accept the Enterprise Service Agreement before adding this."
TERMS_WORDS = "Your organisation must accept the Terms of Service before adding this."
WARNING = sdk.SERVICE_AGREEMENT_WARNING


def _plan_change(**over: Any) -> dict[str, Any]:
    change: dict[str, Any] = {
        "id": CHANGE,
        "from": "standard",
        "to": "enterprise",
        "state": "awaiting_acceptance",
        "requested_at": "2026-11-17T09:00:00Z",
        "until": "2026-12-01T09:00:00Z",
        "requested_by_operator": True,
    }
    change.update(over)
    return change


def _sa_details(**over: Any) -> dict[str, Any]:
    details: dict[str, Any] = {
        "plan_change": _plan_change(),
        "documents": [
            {
                "document": "service_agreement_enterprise",
                "number": 1,
                "plan": "enterprise",
                "grace_ends_at": None,
            },
            {
                "document": "terms",
                "number": 4,
                "plan": None,
                "grace_ends_at": "2026-11-10T00:00:00Z",
            },
        ],
        "accept_url": ACCEPT_URL,
    }
    details.update(over)
    return details


def _refused(code: str, message: str, details: Any) -> httpx.Response:  # noqa: ANN401
    return httpx.Response(
        409,
        json={"error": {"code": code, "message": message, "details": details}},
        headers={"MFX-Service-Agreement": "due"},
    )


def _agreement_body(**over: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "due": True,
        "held": True,
        "plan": "standard",
        "plan_change": _plan_change(),
        "documents": [
            {
                "document": "service_agreement_enterprise",
                "number": 1,
                "plan": "enterprise",
                "grace_ends_at": None,
                "held": True,
            }
        ],
        "accept_url": ACCEPT_URL,
    }
    body.update(over)
    return body


def _warnings(caplog: pytest.LogCaptureFixture) -> list[logging.LogRecord]:
    return [r for r in caplog.records if r.name == "mfx" and r.getMessage() == WARNING]


async def test_a_service_agreement_hold_is_a_typed_409_with_the_change_documents_and_accept_url(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an organisation whose move from Standard to Enterprise awaits acceptance of the
    Enterprise Service Agreement, with a Terms version past its grace period as well
    When the tenant asks for a new terminal
    Then it raises ServiceAgreementNotAccepted, a ConflictError, with the code
    service_agreement_not_accepted, 409 and the platform's message, sent once and never retried;
    plan_change is a PlanChange with its id, from_, to, state, requested_at and until as aware
    datetimes and requested_by_operator; documents lists each DocumentDue with its document, number,
    plan and grace_ends_at (None for the plan change's agreement, which waits instead); and
    accept_url is where an owner or admin accepts."""
    mfx.responses.append(_refused("service_agreement_not_accepted", SA_WORDS, _sa_details()))
    with pytest.raises(ServiceAgreementNotAccepted) as raised:
        await client.terminals.create(
            broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="t-1"
        )

    held = raised.value
    assert isinstance(held, ConflictError)
    assert (held.code, held.status, held.message) == (
        "service_agreement_not_accepted",
        409,
        SA_WORDS,
    )
    assert held.plan_change == PlanChange(
        id=CHANGE,
        from_="standard",
        to="enterprise",
        state="awaiting_acceptance",
        requested_at=dt.datetime(2026, 11, 17, 9, tzinfo=dt.UTC),
        until=dt.datetime(2026, 12, 1, 9, tzinfo=dt.UTC),
        requested_by_operator=True,
    )
    assert held.documents == [
        DocumentDue(
            document="service_agreement_enterprise", number=1, plan="enterprise", grace_ends_at=None
        ),
        DocumentDue(
            document="terms",
            number=4,
            plan=None,
            grace_ends_at=dt.datetime(2026, 11, 10, tzinfo=dt.UTC),
        ),
    ]
    assert held.accept_url == ACCEPT_URL
    assert len(mfx.requests) == 1, "not retried: it ends when someone accepts"


async def test_a_hold_with_no_plan_change_or_unreadable_details_reads_as_none_not_an_sdk_error(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given service_agreement_not_accepted answers whose details carry no plan change (a version
    of the plan's own agreement past its grace period), a plan change missing what identifies it,
    documents that are not a list or hold entries that are not documents, a plan or a document key
    this SDK has never heard of, and no details at all
    When the tenant attaches an expert advisor each time
    Then each raises ServiceAgreementNotAccepted; plan_change is None where there is none or it
    cannot be read; documents keeps only entries that name a document, an unknown key and plan
    included as text, and is empty otherwise; accept_url is None when absent; and nothing raised is
    an error of the SDK's own."""
    answers = [
        _sa_details(plan_change=None),
        _sa_details(plan_change={"from": "standard"}, documents="terms"),
        _sa_details(
            plan_change=_plan_change(
                requested_at="soon", until=None, state="a_state_from_next_year"
            ),
            documents=[
                "terms",
                {"number": 2},
                {"document": "service_agreement_developer", "number": "two", "plan": "developer"},
            ],
        ),
        {},
    ]
    for details in answers:
        mfx.responses.append(_refused("service_agreement_not_accepted", SA_WORDS, details))
    seen = []
    for n in range(len(answers)):
        with pytest.raises(ServiceAgreementNotAccepted) as raised:
            await client.terminals.attach_expert_advisor(
                TERMINAL_ID,
                CHANGE,
                symbol="EURUSD",
                timeframe="H1",
                reason="go live",
                idempotency_key=f"ea-{n}",
            )
        seen.append(raised.value)

    none, unreadable, odd, empty = seen
    assert none.plan_change is None and len(none.documents) == 2 and none.accept_url == ACCEPT_URL
    assert unreadable.plan_change is None and unreadable.documents == []
    assert odd.plan_change is not None
    assert (odd.plan_change.state, odd.plan_change.requested_at, odd.plan_change.until) == (
        "a_state_from_next_year", None, None,
    )  # fmt: skip
    assert odd.documents == [
        DocumentDue(
            document="service_agreement_developer",
            number=None,
            plan="developer",
            grace_ends_at=None,
        )
    ]
    assert (empty.plan_change, empty.documents, empty.accept_url) == (None, [], None)


async def test_a_terms_hold_is_a_typed_409_naming_each_document_and_when_its_grace_ended(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an organisation that has not accepted a Terms of Service version and a MetaTrader 5
    licence version past their grace period
    When the tenant asks for a new terminal
    Then it raises TermsNotAccepted, a ConflictError and not a ServiceAgreementNotAccepted, with the
    code terms_not_accepted, 409 and the platform's message; documents lists each DocumentDue, its
    grace_ends_at read from the grace_ends_at the platform sends, as an aware datetime, and plan
    None; and it is sent once."""
    details = {
        "documents": [
            {"document": "terms", "number": 4, "grace_ends_at": "2026-11-10T00:00:00Z"},
            {"document": "mt5_licence", "number": 2, "grace_ends_at": "2026-11-12T08:30:00+00:00"},
        ]
    }
    mfx.responses.append(_refused("terms_not_accepted", TERMS_WORDS, details))
    with pytest.raises(TermsNotAccepted) as raised:
        await client.terminals.create(
            broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="t-2"
        )

    held = raised.value
    assert isinstance(held, ConflictError) and not isinstance(held, ServiceAgreementNotAccepted)
    assert (held.code, held.status, held.message) == ("terms_not_accepted", 409, TERMS_WORDS)
    assert held.documents == [
        DocumentDue(
            document="terms",
            number=4,
            plan=None,
            grace_ends_at=dt.datetime(2026, 11, 10, tzinfo=dt.UTC),
        ),
        DocumentDue(
            document="mt5_licence",
            number=2,
            plan=None,
            grace_ends_at=dt.datetime(2026, 11, 12, 8, 30, tzinfo=dt.UTC),
        ),
    ]
    assert len(mfx.requests) == 1


async def test_tenant_service_agreement_reads_what_is_due_over_its_own_signed_route(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an organisation with a plan change awaiting acceptance, and later one with nothing due
    When the tenant calls client.tenant.service_agreement() each time
    Then it sends a signed GET /tenant/service-agreement with no body, and answers the API's own
    TenantServiceAgreement: due, held, the plan in force, the plan change (None when there is
    none), each document with its number, plan, grace_ends_at and held, and accept_url."""
    mfx.responses.append(httpx.Response(200, json=_agreement_body()))
    mfx.responses.append(
        httpx.Response(
            200, json=_agreement_body(due=False, held=False, plan_change=None, documents=[])
        )
    )

    due = await client.tenant.service_agreement()
    assert isinstance(due, TenantServiceAgreement)
    request = mfx.last
    assert (request.method, request.url.path) == ("GET", "/v1/tenant/service-agreement")
    assert request.content == b"" and request.headers["X-MFX-Key"] == KEY_ID
    assert (due.due, due.held, due.plan, due.accept_url) == (True, True, "standard", ACCEPT_URL)
    assert due.plan_change is not None and str(due.plan_change.id) == CHANGE
    assert (due.plan_change.from_, due.plan_change.to) == ("standard", "enterprise")
    [document] = due.documents
    assert (document.document, document.number, document.plan, document.held) == (
        "service_agreement_enterprise", 1, "enterprise", True,
    )  # fmt: skip

    clear = await client.tenant.service_agreement()
    assert (clear.due, clear.held, clear.plan_change, clear.documents) == (False, False, None, [])


def test_the_sync_client_reads_the_service_agreement_and_the_contacts_as_tenant(
    mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given a script with no event loop holding a SyncMfxClient
    When it calls sync.tenant.service_agreement() and sync.tenant.contacts()
    Then each blocks and answers what MfxClient.tenant answers, over GET /tenant/service-agreement
    and GET /tenant/contacts; and a held addition raises the same ServiceAgreementNotAccepted."""
    mfx.responses.append(httpx.Response(200, json=_agreement_body()))
    mfx.responses.append(httpx.Response(200, json={"items": []}))
    mfx.responses.append(_refused("service_agreement_not_accepted", SA_WORDS, _sa_details()))
    with SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as sync:
        agreement = sync.tenant.service_agreement()
        sync.tenant.contacts()
        with pytest.raises(ServiceAgreementNotAccepted) as raised:
            sync.create_terminal(broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="t-3")
    assert isinstance(agreement, TenantServiceAgreement) and agreement.due is True
    assert raised.value.accept_url == ACCEPT_URL
    assert [r.url.path for r in mfx.requests] == [
        "/v1/tenant/service-agreement", "/v1/tenant/contacts", "/v1/terminals",
    ]  # fmt: skip


async def test_an_agreement_due_logs_one_warning_per_client_the_first_time_and_never_again(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, caplog: pytest.LogCaptureFixture
) -> None:
    """Given an organisation with an agreement due, so every answer carries
    MFX-Service-Agreement: due, success and refusal alike
    When one client makes a call whose answer does not carry it, then several calls whose
    answers do, one of them refused, and then a second client makes a call whose answer does
    Then nothing is logged before the header is seen; the first answer carrying it logs one
    WARNING on the SDK's logger, mfx, whose message is SERVICE_AGREEMENT_WARNING and which names
    the key; that client never logs it again; and the second client logs its own one warning."""
    caplog.set_level(logging.WARNING, logger="mfx")
    due = {"MFX-Service-Agreement": "due"}
    mfx.responses.append(httpx.Response(200, json=_agreement_body(due=False, held=False)))
    mfx.responses.append(httpx.Response(200, json=_agreement_body(), headers=due))
    mfx.responses.append(httpx.Response(200, json=_agreement_body(), headers=due))
    mfx.responses.append(_refused("service_agreement_not_accepted", SA_WORDS, _sa_details()))
    mfx.responses.append(httpx.Response(200, json=_agreement_body(), headers=due))

    async with MfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as first:
        await first.tenant.service_agreement()
        assert _warnings(caplog) == [], "no header, no warning"
        await first.tenant.service_agreement()
        await first.tenant.service_agreement()
        with pytest.raises(ServiceAgreementNotAccepted):
            await first.terminals.create(
                broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="t-4"
            )
    [warned] = _warnings(caplog)
    assert warned.levelno == logging.WARNING
    assert warned.mfx["key_id"] == KEY_ID  # type: ignore[attr-defined]

    async with MfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as second:
        await second.tenant.service_agreement()
    assert len(_warnings(caplog)) == 2, "one for each client"
    assert "tenant.service_agreement()" in WARNING and "MFX-Service-Agreement" in WARNING


def test_concurrent_calls_on_one_client_seeing_an_agreement_due_still_log_one_warning(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, caplog: pytest.LogCaptureFixture
) -> None:
    """Given every answer carrying MFX-Service-Agreement: due
    When twenty calls run at once on one MfxClient, and eight threads call one SyncMfxClient at once
    Then each client logs exactly one warning, however the answers interleave."""
    caplog.set_level(logging.WARNING, logger="mfx")

    def answer(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_agreement_body(), headers={"MFX-Service-Agreement": "due"})

    transport = httpx.MockTransport(answer)

    async def many() -> None:
        async with MfxClient(BASE_URL, KEY_ID, private_key, transport=transport) as client:
            await asyncio.gather(*(client.tenant.service_agreement() for _ in range(20)))

    asyncio.run(many())
    assert len(_warnings(caplog)) == 1

    with SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=transport) as sync:
        threads = [threading.Thread(target=sync.tenant.service_agreement) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    assert len(_warnings(caplog)) == 2, "one more, for the sync client"


def test_the_agreement_errors_and_their_values_are_part_of_the_package() -> None:
    """Given a tenant importing the package
    When it names the Service Agreement's errors, their values and the warning text from mfx
    Then ServiceAgreementNotAccepted, TermsNotAccepted, PlanChange, DocumentDue and
    SERVICE_AGREEMENT_WARNING are each exported, and each error is mapped from its own code."""
    from mfx.errors import _BY_CODE

    for name in (
        "ServiceAgreementNotAccepted",
        "TermsNotAccepted",
        "PlanChange",
        "DocumentDue",
        "SERVICE_AGREEMENT_WARNING",
    ):
        assert name in sdk.__all__ and hasattr(sdk, name), name
    assert _BY_CODE["service_agreement_not_accepted"] is ServiceAgreementNotAccepted
    assert _BY_CODE["terms_not_accepted"] is TermsNotAccepted
