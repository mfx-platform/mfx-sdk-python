"""``client.billing`` — the billing reads, and the 402 a missing payment answers a write with.

A billing profile whose payment is missing goes from a notice to a reminder, when a request that
adds something billed is refused, to a suspension, when every write on its accounts is. Both
refusals are 402 ``billing_payment_required``, with the stage, the dates and the portal page that
clears it in ``details``. Reads keep answering throughout, the billing reads among them.
"""

from __future__ import annotations

import asyncio
import datetime as dt
from decimal import Decimal
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import mfx as sdk
from mfx.client import MfxClient
from mfx.errors import (
    BillingAction,
    BillingPaymentRequiredError,
    MfxApiError,
    PaymentRequiredError,
)
from mfx.results import Reason
from mfx.sync import SyncMfxClient

from .conftest import BASE_URL, BROKER_ID, KEY_ID, SERVER_ID, TERMINAL_ID, FakeMfx, terminal_body
from .test_risk import ID, answer, of, query

PROFILE = "0b7e5c1a-3d2f-4e6a-8b9c-1d2e3f4a5b6c"
TENANT = "6f1c2a0e-1b8d-4f7a-9a51-7d0c1a2b3c4d"
INVOICE = "7d1c2a0e-1b8d-4f7a-9a51-7d0c1a2b3c4d"
WORDS = "A payment is missing on billing profile Default: top up to keep your accounts running."


def _details(**over: Any) -> dict[str, Any]:
    """The contract's own example of ``BillingPaymentRequiredDetails``, changed where asked."""
    details: dict[str, Any] = dict(SPEC_EXAMPLE)
    details.update(over)
    return details


SPEC_EXAMPLE: dict[str, Any] = {
    "tenant_id": TENANT,
    "billing_profile_id": PROFILE,
    "stage": "reminder",
    "cause": "balance_used_up",
    "since": "2026-11-20T00:05:00Z",
    "suspends_at": "2026-11-23T00:05:00Z",
    "pay_by": "2026-11-23T00:04:59Z",
    "action": {
        "kind": "top_up",
        "portal_path": "/billing/top-up",
        "amount_usd": "10.00",
        "invoice_id": None,
    },
}


def _payment_required(details: Any, code: str = "billing_payment_required") -> httpx.Response:  # noqa: ANN401
    return httpx.Response(402, json={"error": {"code": code, "message": WORDS, "details": details}})


async def test_a_missing_payment_is_a_typed_402_with_its_stage_dates_and_the_portal_page(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a billing profile whose payment is missing, first at the reminder stage and then
    suspended
    When the tenant asks for a new terminal (adding something billed) at the reminder, and
    restarts a terminal once suspended
    Then each raises BillingPaymentRequiredError, a PaymentRequiredError and an MfxApiError, with
    the platform's code, 402 and message; the tenant, the billing profile, the stage, the cause,
    since, suspends_at and pay_by are read from details, the times as aware datetimes; the action
    names its kind, the portal page relative to the portal's address, the amount as an exact
    Decimal and the invoice to pay; nothing is retried. A 402 whose code this SDK does not know
    is a PaymentRequiredError by its status, and details that are missing or unreadable read as
    None, never as an error of the SDK's own."""
    mfx.responses.append(_payment_required(_details()))
    with pytest.raises(BillingPaymentRequiredError) as raised:
        await client.terminals.create(
            broker_id=BROKER_ID, server_id=SERVER_ID, idempotency_key="t-1"
        )
    reminder = raised.value
    assert isinstance(reminder, PaymentRequiredError) and isinstance(reminder, MfxApiError)
    assert (reminder.code, reminder.status, reminder.message) == (
        "billing_payment_required", 402, WORDS,
    )  # fmt: skip
    assert (reminder.tenant_id, reminder.billing_profile_id) == (TENANT, PROFILE)
    assert (reminder.stage, reminder.cause) == ("reminder", "balance_used_up")
    assert reminder.since == dt.datetime(2026, 11, 20, 0, 5, tzinfo=dt.UTC)
    assert reminder.suspends_at == dt.datetime(2026, 11, 23, 0, 5, tzinfo=dt.UTC)
    assert reminder.pay_by == dt.datetime(2026, 11, 23, 0, 4, 59, tzinfo=dt.UTC)
    assert reminder.action == BillingAction(
        kind="top_up", portal_path="/billing/top-up", amount_usd=Decimal("10.00"), invoice_id=None
    )
    assert len(mfx.requests) == 1, "not retried: it ends when someone pays"

    mfx.responses.append(
        _payment_required(
            _details(
                stage="suspended",
                cause="invoice_overdue",
                since="2026-11-23T00:05:00+00:00",
                action={
                    "kind": "pay_invoice",
                    "portal_path": f"/billing/invoices/{INVOICE}",
                    "amount_usd": "184.200001",
                    "invoice_id": INVOICE,
                },
            )
        )
    )
    with pytest.raises(BillingPaymentRequiredError) as raised:
        await client.terminals.restart(TERMINAL_ID, reason="weekly", idempotency_key="r-1")
    suspended = raised.value
    assert (suspended.stage, suspended.cause) == ("suspended", "invoice_overdue")
    assert suspended.since == dt.datetime(2026, 11, 23, 0, 5, tzinfo=dt.UTC)
    action = suspended.action
    assert action is not None and action.kind == "pay_invoice"
    assert action.portal_path == f"/billing/invoices/{INVOICE}" and action.invoice_id == INVOICE
    assert action.amount_usd == Decimal("184.200001"), "exact, never a float"

    unreadable = [
        _details(action={"kind": "top_up", "portal_path": "/billing/top-up"}, since="soon"),
        _details(action={"kind": "top_up", "portal_path": "/x", "amount_usd": "lots"}),
        _details(action={"kind": "top_up", "portal_path": "/x", "amount_usd": "NaN"}),
        _details(action={"kind": "top_up"}),
        _details(action="top up"),
        {},
    ]
    for details in unreadable:
        mfx.responses.append(_payment_required(details))
    seen = []
    for n in range(len(unreadable)):
        with pytest.raises(BillingPaymentRequiredError) as raised:
            await client.terminals.restart(TERMINAL_ID, reason="weekly", idempotency_key=f"u-{n}")
        seen.append(raised.value)
    assert seen[0].since is None and seen[0].action is not None
    assert seen[0].action.amount_usd is None
    assert seen[1].action is not None and seen[1].action.amount_usd is None
    assert seen[2].action is not None and seen[2].action.amount_usd is None
    assert seen[3].action is None and seen[4].action is None
    bare = seen[5]
    assert (bare.tenant_id, bare.billing_profile_id, bare.stage, bare.cause) == (None,) * 4
    assert (bare.since, bare.suspends_at, bare.pay_by, bare.action) == (None,) * 4

    mfx.responses.append(_payment_required({"payment_id": ID}, code="payment_failed"))
    with pytest.raises(PaymentRequiredError) as by_status:
        await client.terminals.restart(TERMINAL_ID, reason="weekly", idempotency_key="p-1")
    assert type(by_status.value) is PaymentRequiredError
    assert by_status.value.code == "payment_failed"

    assert sdk.BillingPaymentRequiredError is BillingPaymentRequiredError
    assert {"BillingAction", "BillingPaymentRequiredError", "PaymentRequiredError"} <= set(
        sdk.__all__
    )


async def test_an_order_refused_for_billing_comes_back_refused_and_reads_keep_working(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a billing profile suspended for a missing payment
    When the tenant places an order on one of its terminals, and then reads the terminal and its
    billing
    Then the order does not raise, as no execution method does: it comes back refused, not ok and
    not retryable, with the platform's message and code in its detail; the reads still answer, as
    the platform keeps them answering, and the billing summary names the suspended stage."""
    mfx.responses.append(_payment_required(_details(stage="suspended")))
    result = await client.execution.place_order(
        TERMINAL_ID, symbol="EURUSD.sd", side="buy", volume="0.10", idempotency_key="order-1"
    )
    assert result.ok is False and result.reason is Reason.REFUSED
    assert result.retryable is False and result.idempotency_key == "order-1"
    assert WORDS in (result.detail or "") and "billing_payment_required" in (result.detail or "")
    assert len(mfx.requests) == 1, "never retried"

    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))
    terminal = await client.terminals.get(TERMINAL_ID)
    assert terminal.state.value == "ACTIVE"

    summary_body = of("BillingSummary")
    summary_body["standing"] = of("BillingStanding", stage="suspended", cause="invoice_overdue")
    mfx.responses.append(httpx.Response(200, json=summary_body))
    summary = await client.billing.summary()
    assert summary.standing.stage.value == "suspended"


def _signed(request: httpx.Request) -> bool:
    return (
        all(
            request.headers.get(name)
            for name in ("X-MFX-Key", "X-MFX-Timestamp", "X-MFX-Nonce", "X-MFX-Signature")
        )
        and request.headers["X-MFX-Key"] == KEY_ID
    )


async def test_each_billing_read_is_its_own_signed_route_the_price_list_included(
    client: MfxClient, mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given a key with billing:read
    When it reads the public price list, the billing summary, a profile, its forecast for a
    month and for this month, the prices it pays and one invoice
    Then each is one GET to its own route, signed with the key, the price list too (it needs no
    key and accepts a signed request); the forecast sends the month only when one is asked for;
    each answers the API's own model with money as the exact decimal text the platform wrote; an
    unknown profile is a NotFoundError. And the blocking client reads the same routes."""
    price_list = of("BillingPriceList")
    mfx.responses.append(httpx.Response(200, json=price_list))
    listed = await client.billing.price_list()
    assert (mfx.last.method, mfx.last.url.path) == ("GET", "/v1/price-list")
    assert listed.to_dict()["version"] == price_list["version"]

    summary_body = of("BillingSummary")
    summary_body["profiles"] = [of("BillingProfileSummary", id=PROFILE, balance_usd="9.500000")]
    mfx.responses.append(httpx.Response(200, json=summary_body))
    summary = await client.billing.summary()
    assert mfx.last.url.path == "/v1/billing"
    assert summary.profiles[0].balance_usd == "9.500000", "exact, as written"

    mfx.responses.append(answer("BillingProfile", id=PROFILE, daily_usd="1.716667"))
    profile = await client.billing.profile(PROFILE)
    assert mfx.last.url.path == f"/v1/billing/profiles/{PROFILE}"
    assert Decimal(profile.daily_usd) == Decimal("1.716667")

    mfx.responses.append(answer("BillingForecast", billing_profile_id=PROFILE))
    await client.billing.forecast(PROFILE, month="2026-10")
    assert mfx.last.url.path == f"/v1/billing/profiles/{PROFILE}/forecast"
    assert query(mfx.last) == {"month": ["2026-10"]}
    mfx.responses.append(answer("BillingForecast", billing_profile_id=PROFILE))
    forecast = await client.billing.forecast(PROFILE)
    assert query(mfx.last) == {} and str(forecast.billing_profile_id) == PROFILE

    mfx.responses.append(answer("BillingPriceList"))
    await client.billing.prices()
    assert mfx.last.url.path == "/v1/billing/prices"

    mfx.responses.append(answer("BillingInvoiceDetail"))
    await client.billing.invoice(INVOICE)
    assert mfx.last.url.path == f"/v1/billing/invoices/{INVOICE}"

    assert all(r.method == "GET" and _signed(r) for r in mfx.requests)
    assert len(mfx.requests) == 7  # noqa: PLR2004

    mfx.responses.append(
        httpx.Response(404, json={"error": {"code": "not_found", "message": "no such profile"}})
    )
    with pytest.raises(sdk.NotFoundError):
        await client.billing.profile(ID)

    def blocking() -> list[str]:
        with SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as sync:
            mfx.responses.extend(
                [
                    answer("BillingPriceList"),
                    answer("BillingSummary"),
                    answer("BillingProfile"),
                    answer("BillingForecast"),
                    answer("BillingPriceList"),
                    answer("BillingInvoiceDetail"),
                    answer("BillingInvoicePage", next_cursor=None),
                ]
            )
            sync.billing.price_list()
            sync.billing.summary()
            sync.billing.profile(PROFILE)
            sync.billing.forecast(PROFILE, month="2026-10")
            sync.billing.prices()
            sync.billing.invoice(INVOICE)
            sync.billing.invoices_page(limit=10)
        return [r.url.path for r in mfx.requests[-7:]]

    assert await asyncio.to_thread(blocking) == [
        "/v1/price-list",
        "/v1/billing",
        f"/v1/billing/profiles/{PROFILE}",
        f"/v1/billing/profiles/{PROFILE}/forecast",
        "/v1/billing/prices",
        f"/v1/billing/invoices/{INVOICE}",
        "/v1/billing/invoices",
    ]


async def test_invoices_page_by_cursor_and_the_walk_follows_it_to_the_last_page(
    client: MfxClient, mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given three pages of invoices
    When one page is read with a profile, two states, a cursor and a limit of 200, and then every
    invoice is walked with a page size
    Then the page is GET /billing/invoices with the profile, the states comma-separated, the
    cursor and the limit, and answers its items and next_cursor; the walk sends no cursor first,
    then each next_cursor in turn, keeps the page size and the filters on every page, and stops
    on the page whose next_cursor is null; a misspelt state is a ValueError before anything is
    sent. The blocking client walks the same pages."""
    first = of("BillingInvoicePage", next_cursor="c2")
    first["items"] = [of("BillingInvoice", number="INV-2026-1104", total_usd="184.20")]
    mfx.responses.append(httpx.Response(200, json=first))
    page = await client.billing.invoices_page(
        billing_profile_id=PROFILE, state=["due", "overdue"], cursor="c1", limit=200
    )
    assert (mfx.last.method, mfx.last.url.path) == ("GET", "/v1/billing/invoices")
    assert query(mfx.last) == {
        "billing_profile_id": [PROFILE],
        "state": ["due,overdue"],
        "cursor": ["c1"],
        "limit": ["200"],
    }
    assert page.next_cursor == "c2" and page.items[0].total_usd == "184.20"

    def pages() -> list[httpx.Response]:
        numbers = iter(["INV-1", "INV-2", "INV-3"])
        bodies = []
        for cursor in ("c2", "c3", None):
            body = of("BillingInvoicePage", next_cursor=cursor)
            body["items"] = [of("BillingInvoice", number=next(numbers))]
            bodies.append(httpx.Response(200, json=body))
        return bodies

    mfx.responses.extend(pages())
    before = len(mfx.requests)
    walked = [i.number async for i in client.billing.invoices(state="overdue", limit=1)]
    assert walked == ["INV-1", "INV-2", "INV-3"]
    sent = [query(r) for r in mfx.requests[before:]]
    assert [q.get("cursor") for q in sent] == [None, ["c2"], ["c3"]]
    assert all(q["limit"] == ["1"] and q["state"] == ["overdue"] for q in sent)

    count = len(mfx.requests)
    with pytest.raises(ValueError, match="paid"):
        await client.billing.invoices_page(state="paid")  # type: ignore[arg-type]
    assert len(mfx.requests) == count, "refused before sending"

    def blocking() -> list[str]:
        with SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as sync:
            mfx.responses.extend(pages())
            return [i.number for i in sync.billing.invoices(limit=1)]

    assert await asyncio.to_thread(blocking) == ["INV-1", "INV-2", "INV-3"]
    assert [query(r).get("cursor") for r in mfx.requests[-3:]] == [None, ["c2"], ["c3"]]
