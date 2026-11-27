"""``client.billing`` — your organisation's billing, as an integration reads it (``billing:read``).

Read only: the standing of each billing profile, its balance and month to date, the forecast to
month end, the prices you pay, the public price list and your invoices. Top-ups, payment methods
and profiles are changed in the portal, never here::

    summary = await client.billing.summary()
    if summary.standing.stage.value != "ok":
        print(summary.standing.action)  # what clears it, and the portal page that does it
    async for invoice in client.billing.invoices(state="overdue"):
        print(invoice.number, invoice.total_usd)

Money stays exact: every amount is the contract's decimal string (``"184.20"``) as the platform
wrote it, never a float. ``Decimal(invoice.total_usd)`` when you need to add it up.

A write anywhere else in the API can be refused for billing with
:class:`mfx.errors.BillingPaymentRequiredError` (402); these reads never are.

Invoices come two ways, as Risk Management's lists do: :meth:`Billing.invoices_page` returns one
page, and :meth:`Billing.invoices` follows the cursor to the end.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID

from mfx._generated.api.billing import get_billing as _summary
from mfx._generated.api.billing import get_billing_forecast as _forecast
from mfx._generated.api.billing import get_billing_invoice as _invoice
from mfx._generated.api.billing import get_billing_prices as _prices
from mfx._generated.api.billing import get_billing_profile as _profile
from mfx._generated.api.billing import get_price_list as _price_list
from mfx._generated.api.billing import list_billing_invoices as _invoices
from mfx._generated.models.list_billing_invoices_state_item import ListBillingInvoicesStateItem
from mfx._generated.types import UNSET
from mfx.pages import states_param

if TYPE_CHECKING:  # pragma: no cover - typing only
    from mfx._generated.models.billing_forecast import BillingForecast
    from mfx._generated.models.billing_invoice import BillingInvoice
    from mfx._generated.models.billing_invoice_detail import BillingInvoiceDetail
    from mfx._generated.models.billing_invoice_page import BillingInvoicePage
    from mfx._generated.models.billing_price_list import BillingPriceList
    from mfx._generated.models.billing_profile import BillingProfile
    from mfx._generated.models.billing_summary import BillingSummary
    from mfx.client import MfxClient

__all__ = ["Billing", "InvoiceState"]

Id = str | UUID

InvoiceState = Literal[
    "issued", "due", "overdue", "settlement_in_progress", "part_settled", "settled", "void"
]


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


def _opt(value: Any) -> Any:  # noqa: ANN401
    return UNSET if value is None else value


class Billing:
    """Billing reads (``billing:read``; :meth:`price_list` needs no scope). Never refused for
    billing: a suspended profile still reads its own standing."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    @property
    def _g(self) -> Any:  # noqa: ANN401 - the generated client
        return self._client.generated

    async def price_list(self) -> BillingPriceList:
        """The public price list: the plans, every item with its monthly price, and ``next``, the
        following list once it is released.

        It needs no key. The SDK signs it as it signs every request, which the platform accepts
        and ignores, so the same client reads it whatever its key's scopes.
        """
        found = await self._client.read(
            lambda: _price_list.asyncio_detailed(client=self._g), "GET /price-list"
        )
        return found  # type: ignore[no-any-return]

    async def summary(self) -> BillingSummary:
        """The organisation's billing: every billing profile with its standing, and ``standing``
        at the top, the most urgent of theirs.

        Named ``summary`` rather than ``get``: the route is the root of billing (``GET
        /billing``) and answers the contract's ``BillingSummary``, an overview of every profile
        and not one object of a kind, which :meth:`profile` reads in full.
        """
        found = await self._client.read(
            lambda: _summary.asyncio_detailed(client=self._g), "GET /billing"
        )
        return found  # type: ignore[no-any-return]

    async def profile(self, profile_id: Id) -> BillingProfile:
        """One billing profile: its balance, today's daily charge, month to date and standing."""
        found = await self._client.read(
            lambda: _profile.asyncio_detailed(id=_uuid(profile_id), client=self._g),
            f"GET /billing/profiles/{profile_id}",
        )
        return found  # type: ignore[no-any-return]

    async def forecast(self, profile_id: Id, *, month: str | None = None) -> BillingForecast:
        """A month for one billing profile, to date by product and forecast to month end.

        ``month`` is ``YYYY-MM``, this month when left out; a past month gives its final figures.
        """
        found = await self._client.read(
            lambda: _forecast.asyncio_detailed(
                id=_uuid(profile_id), client=self._g, month=_opt(month)
            ),
            f"GET /billing/profiles/{profile_id}/forecast",
        )
        return found  # type: ignore[no-any-return]

    async def prices(self) -> BillingPriceList:
        """The prices your organisation pays, in the price list's shape: your Enterprise
        agreement's (``scope`` ``tenant``) when one is in force, otherwise the list in force."""
        found = await self._client.read(
            lambda: _prices.asyncio_detailed(client=self._g), "GET /billing/prices"
        )
        return found  # type: ignore[no-any-return]

    async def invoice(self, invoice_id: Id) -> BillingInvoiceDetail:
        """One invoice, with its summary by product, tax, what is matched and how to pay."""
        found = await self._client.read(
            lambda: _invoice.asyncio_detailed(id=_uuid(invoice_id), client=self._g),
            f"GET /billing/invoices/{invoice_id}",
        )
        return found  # type: ignore[no-any-return]

    async def invoices_page(
        self,
        *,
        billing_profile_id: Id | None = None,
        state: InvoiceState | Sequence[InvoiceState] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> BillingInvoicePage:
        """One page of invoices, newest first, across your billing profiles.

        ``billing_profile_id`` keeps one profile's; ``state`` is one state or several (sent
        comma-separated, checked here). ``limit`` is up to 200 (50 when left out); pass the page's
        ``next_cursor`` back as ``cursor`` for the next, until it is None.
        """
        states = states_param(state, ListBillingInvoicesStateItem)
        profile = UNSET if billing_profile_id is None else _uuid(billing_profile_id)
        page = await self._client.read(
            lambda: _invoices.asyncio_detailed(
                client=self._g, billing_profile_id=profile, state=states, cursor=_opt(cursor),
                limit=_opt(limit),
            ),
            "GET /billing/invoices",
        )  # fmt: skip
        return page  # type: ignore[no-any-return]

    async def invoices(
        self,
        *,
        billing_profile_id: Id | None = None,
        state: InvoiceState | Sequence[InvoiceState] | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[BillingInvoice]:
        """Every invoice, newest first, following the cursor; narrowed as :meth:`invoices_page`
        is. ``limit`` is the page size, not a total."""
        cursor: str | None = None
        while True:
            page = await self.invoices_page(
                billing_profile_id=billing_profile_id, state=state, cursor=cursor, limit=limit
            )
            for invoice in page.items:
                yield invoice
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return
