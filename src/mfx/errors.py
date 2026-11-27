"""What a read method raises, mapped from the API's own error class.

The API answers a failure with ``{"error": {"code", "message", "details"}}``, where ``code`` is the
*class* of the failure and not the HTTP status (``validation_error``, ``conflict``, ``rate_limited``
…). This hierarchy mirrors it, so a caller writes ``except NotFoundError`` and never
``if response.status_code == 404``.

The code is mapped first and the status only as a fallback: two 409s that mean different things
(``conflict`` and ``placement_error``) are different exceptions, and a status the SDK has never seen
still arrives as a typed ``MfxApiError`` rather than as a KeyError inside the SDK.

Execution methods are the exception to all of this: they never raise across the boundary and return
an ``ExecutionResult`` instead. Nothing here reaches a caller of ``mfx.execution``.
"""

from __future__ import annotations

import datetime as dt
import json
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from http import HTTPStatus
from typing import Any, Final

__all__ = [
    "AuthError",
    "BillingAction",
    "BillingPaymentRequiredError",
    "ConflictError",
    "ForbiddenError",
    "InternalError",
    "MfxApiError",
    "MfxError",
    "MfxTimeout",
    "MfxTransportError",
    "NotFoundError",
    "PaymentRequiredError",
    "PlacementError",
    "PlanChange",
    "RateLimitError",
    "RiskOverrideRequiredError",
    "RiskRefusal",
    "RiskRefusedError",
    "ServiceAgreementNotAccepted",
    "StateError",
    "TenantDisabledError",
    "TenantSuspendedError",
    "TermsNotAccepted",
    "UnsupportedBrokerError",
    "DependencyUnavailableError",
    "DocumentDue",
    "EdgeError",
    "MaintenanceError",
    "UpstreamError",
    "ValidationError",
    "error_for",
    "raise_for",
]


class MfxError(Exception):
    """Every failure this SDK raises."""


class MfxTransportError(MfxError):
    """The request never got an answer: DNS, TCP, TLS, a dropped connection.

    ``may_have_reached`` says whether the request could have arrived. It is False only when the
    connection never opened, so nothing was sent; a connection that dropped after the request was
    written may have delivered it, and an order sent that way may already be a position.
    """

    def __init__(self, message: str = "", *, may_have_reached: bool = True) -> None:
        super().__init__(message)
        #: False only when the connection never opened, so nothing was sent.
        self.may_have_reached = may_have_reached


class MfxTimeout(MfxTransportError):  # noqa: N818 - "Error" would read as MfxTimeoutError
    """The request got no answer in time. Never retried by the SDK for a write."""


class MfxApiError(MfxError):
    """MFX answered, and the answer was a failure."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: str,
        details: dict[str, Any] | None = None,
        retry_after_s: float | None = None,
    ) -> None:
        super().__init__(message)
        #: The platform's sentence alone, as it was written. ``str()`` puts the code and the
        #: status in front of it; this is the part to show a person.
        self.message = message
        #: The HTTP status of the answer.
        self.status = status
        #: The API's error code, such as ``not_found``: what to branch on, rather than the status.
        self.code = code
        #: What the platform added about this failure; empty when it added nothing.
        self.details = details or {}
        #: How long the platform asked you to wait before trying again, in seconds; None when it
        #: did not say.
        self.retry_after_s = retry_after_s

    def __str__(self) -> str:
        return f"{self.code} ({self.status}): {super().__str__()}"


class ValidationError(MfxApiError):
    """The request was refused before anything happened: 400, or 422 for an unsupported broker."""


class AuthError(MfxApiError):
    """The signature, key, timestamp or nonce was not accepted."""


class ForbiddenError(MfxApiError):
    """The key is valid and this is not in its scopes."""


def _time_in(details: Mapping[str, Any], name: str) -> dt.datetime | None:
    """An ISO 8601 moment from ``details``, aware; None when absent or not one."""
    raw = details.get(name)
    if not isinstance(raw, str) or not raw:
        return None
    try:
        moment = dt.datetime.fromisoformat(raw)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=dt.UTC)


class TenantDisabledError(ForbiddenError):
    """The operator has disabled this tenant: every call is refused until it is enabled.

    Nothing is wrong with the key, its scopes or the request, and retrying changes nothing: it
    ends when the operator enables the tenant. ``message`` is what the operator wrote for the
    tenant, word for word, and is the thing to show or log. The tenant's terminals keep running
    meanwhile. An open stream is closed with the same error.
    """

    @property
    def since(self) -> dt.datetime | None:
        """When the tenant was disabled; None if the platform did not say."""
        return _time_in(self.details, "since")


class TenantSuspendedError(ForbiddenError):
    """The operator has suspended this tenant: writes are refused now, reads for a while yet.

    Orders, closes and every other write are refused from the moment of suspension. Reads and
    the stream go on working until ``reads_until``, the end of the suspension's grace, and are
    then refused with this same error. It is not retryable: it ends when the operator resumes
    the tenant. ``message`` is what the operator wrote for the tenant, word for word.

    Execution methods never raise: a suspended tenant's order comes back as a
    refused ``ExecutionResult`` whose ``detail`` carries this error's text.
    """

    @property
    def since(self) -> dt.datetime | None:
        """When the suspension began; None if the platform did not say."""
        return _time_in(self.details, "since")

    @property
    def reads_until(self) -> dt.datetime | None:
        """When reads stop working too; None if the platform named no grace."""
        return _time_in(self.details, "reads_until")


class MaintenanceError(ForbiddenError):
    """A planned maintenance window suspends this for you until :attr:`ends_at`.

    403 ``maintenance``. Nothing is wrong with the key or the request: it works again when the
    window ends, so wait until ``ends_at`` and send it again (the same idempotency key for a
    write). Only the window's own scope is refused, and open positions are never closed by a
    window. ``message`` is the platform's sentence ("Paused for planned maintenance until 02:38
    UTC.") and is the part to show a person; ``client.maintenance.list()`` says what else is
    suspended and is answered throughout.
    """

    @property
    def window_id(self) -> str | None:
        """The window's id, for ``client.maintenance.terminals(window_id)``."""
        value = self.details.get("window_id")
        return value if isinstance(value, str) else None

    @property
    def window(self) -> str | None:
        """The window's label as people say it: ``MW-0031``."""
        value = self.details.get("window")
        return value if isinstance(value, str) else None

    @property
    def ends_at(self) -> dt.datetime | None:
        """The window's current end, aware; None if the platform did not say. It can move."""
        return _time_in(self.details, "ends_at")

    @property
    def service(self) -> str | None:
        """The suspended service that refused this call, e.g. ``order_placement``."""
        value = self.details.get("service")
        return value if isinstance(value, str) else None

    @property
    def suspended(self) -> list[str]:
        """Every service the window suspends for you."""
        value = self.details.get("suspended")
        return [s for s in value if isinstance(s, str)] if isinstance(value, list) else []


@dataclass(frozen=True, slots=True)
class RiskRefusal:
    """What a Risk Management refusal names: the rule, the figures and the policy or challenge
    behind it, as a refusal's details and a copy refusal's ``risk`` carry them. Figures stay
    text, as the platform wrote them; ``policy_id`` and ``version`` are None when a challenge's
    rule refused, and ``challenge_id`` and ``challenge_version`` are None when a policy's did."""

    reason: str
    rule: str | None
    policy_id: str | None
    version: int | None
    challenge_id: str | None
    challenge_version: int | None
    used: str | None
    limit: str | None
    would_be: str | None


def _text_or_none(details: Mapping[str, Any], name: str) -> str | None:
    value = details.get(name)
    return None if value is None or value == "" else str(value)


def _int_or_none(details: Mapping[str, Any], name: str) -> int | None:
    value = details.get(name)
    if isinstance(value, bool) or value is None or value == "":
        return None
    try:
        return int(str(value))
    except ValueError:
        return None


class RiskRefusedError(ValidationError):
    """422 ``risk_refused``: a new entry broke a Risk Management rule in force on the account and
    nothing was sent to the broker. ``refusal`` says which rule, the figure it used, its limit
    and what the entry would have made it. Send a smaller entry, add a stop, or wait for the
    inputs to be fresh (``reason`` ``risk_inputs_stale``) or for the window to open."""

    @property
    def refusal(self) -> RiskRefusal:
        """What refused the entry, read from ``details``."""
        d = self.details
        return RiskRefusal(
            reason=str(d.get("reason") or "risk_refused"),
            rule=_text_or_none(d, "rule"),
            policy_id=_text_or_none(d, "policy_id"),
            version=_int_or_none(d, "version"),
            challenge_id=_text_or_none(d, "challenge_id"),
            challenge_version=_int_or_none(d, "challenge_version"),
            used=_text_or_none(d, "used"),
            limit=_text_or_none(d, "limit"),
            would_be=_text_or_none(d, "would_be"),
        )


class RiskOverrideRequiredError(ForbiddenError):
    """403 ``risk_override_required``: the change relaxes protection, and needs a key with
    ``risk:override`` and a ``reason``. Nothing was changed."""


class PaymentRequiredError(MfxApiError):
    """402: a payment is missing. Not retryable unchanged: it ends when someone pays.

    :class:`BillingPaymentRequiredError` is the one the platform sends with an API key; a 402
    whose code this version does not know arrives as this class, by its status.
    """


@dataclass(frozen=True, slots=True)
class BillingAction:
    """What clears a billing standing (the contract's ``BillingAction``).

    ``kind`` is ``top_up`` or ``pay_invoice``. ``portal_path`` is the portal page that does it,
    relative to the portal's address (``/billing/top-up``): join it to the portal's address to
    give a person a link. ``amount_usd`` is at least what clears it, exact; ``invoice_id`` is the
    invoice to pay, None for a top-up.
    """

    kind: str
    portal_path: str
    amount_usd: Decimal | None
    invoice_id: str | None


def _decimal_or_none(details: Mapping[str, Any], name: str) -> Decimal | None:
    value = details.get(name)
    if not isinstance(value, str) or not value:
        return None
    try:
        figure = Decimal(value)
    except InvalidOperation:
        return None
    return figure if figure.is_finite() else None


class BillingPaymentRequiredError(PaymentRequiredError):
    """402 ``billing_payment_required``: a payment is missing on the billing profile the request
    falls under, and nothing was done.

    It is **not retryable**: sending the same request again changes nothing until the payment is
    made. At ``stage`` ``reminder`` it comes only from a request that adds something billed (a new
    account, an add-on switched on). Once ``stage`` is ``suspended`` it can come from **any
    write** on the tenant or the profile - orders, account changes, copy settings - whatever route
    it was sent to, not only the routes that document it. **Reads keep working** throughout, the
    billing reads (``client.billing``) included.

    What a caller does: show ``message`` and :attr:`action` to a person. ``action.portal_path`` is
    the portal page where they fix it (a top-up, or the invoice to pay), relative to the portal's
    address. Once paid, the accounts are released, usually within the hour; then send the request
    again (a write under the same idempotency key). ``pay_by`` is the last moment a payment avoids
    the suspension that begins at ``suspends_at``.

    Execution methods never raise: an order refused for billing comes back as a refused
    ``ExecutionResult`` whose ``detail`` carries this error's text.
    """

    @property
    def tenant_id(self) -> str | None:
        """The tenant the refusal concerns."""
        return _text_or_none(self.details, "tenant_id")

    @property
    def billing_profile_id(self) -> str | None:
        """The billing profile the request falls under; on Standard, its one profile."""
        return _text_or_none(self.details, "billing_profile_id")

    @property
    def stage(self) -> str | None:
        """``reminder`` (only what adds something billed is refused) or ``suspended`` (every
        write on the profile's accounts is). Read a word you do not know as text."""
        value = self.details.get("stage")
        return value if isinstance(value, str) else None

    @property
    def cause(self) -> str | None:
        """Why: ``balance_used_up`` or ``invoice_overdue``."""
        value = self.details.get("cause")
        return value if isinstance(value, str) else None

    @property
    def since(self) -> dt.datetime | None:
        """When the stage began, aware; None if the platform did not say."""
        return _time_in(self.details, "since")

    @property
    def suspends_at(self) -> dt.datetime | None:
        """The first suspended moment, aware; None if the platform did not say."""
        return _time_in(self.details, "suspends_at")

    @property
    def pay_by(self) -> dt.datetime | None:
        """The last moment a payment avoids the suspension, aware; None if not said."""
        return _time_in(self.details, "pay_by")

    @property
    def action(self) -> BillingAction | None:
        """What clears it, with the portal page that does it; None if the platform named none."""
        raw = self.details.get("action")
        if not isinstance(raw, Mapping):
            return None
        kind, path = raw.get("kind"), raw.get("portal_path")
        if not isinstance(kind, str) or not isinstance(path, str):
            return None
        return BillingAction(
            kind=kind,
            portal_path=path,
            amount_usd=_decimal_or_none(raw, "amount_usd"),
            invoice_id=_text_or_none(raw, "invoice_id"),
        )


class NotFoundError(MfxApiError):
    """No such object *for this tenant*. Another tenant's id is a 404 here, never a 403."""


class ConflictError(MfxApiError):
    """The request cannot apply to the object as it is now."""


class StateError(ConflictError):
    """The object is in a state this cannot be done from."""


class PlacementError(ConflictError):
    """No farm can carry what was asked for."""


class UnsupportedBrokerError(ConflictError):
    """MFX does not support this broker or this server *now*.

    Refused at request time and never passed to a terminal, so a tenant learns it here rather than
    from a terminal that sits in ``REQUESTED`` and never moves. ``message`` is the sentence an
    operator recorded, which is the part worth showing a user; the rest says which of the two
    switches was closed:

    * ``refused_by`` — ``permission`` (the broker's legal position: MFX may not carry it for this
      tenant) or ``server_disabled`` (the broker is fine, this one server is switched off).
    * ``reason``, ``broker_id``, ``server_id`` — as the platform recorded them.

    The distinction matters to a caller: ``server_disabled`` means try another server of the same
    broker, ``permission`` means this broker is not available at all.
    """

    @property
    def refused_by(self) -> str | None:
        """``permission`` or ``server_disabled``; None if the platform did not say."""
        value = self.details.get("refused_by")
        return value if isinstance(value, str) else None

    @property
    def reason(self) -> str | None:
        """The platform's own reason code, unbucketed."""
        value = self.details.get("reason")
        return value if isinstance(value, str) else None

    @property
    def broker_id(self) -> str | None:
        """The broker the refusal concerns, when the platform names one."""
        value = self.details.get("broker_id")
        return value if isinstance(value, str) else None

    @property
    def server_id(self) -> str | None:
        """The broker server the refusal concerns, when the platform names one."""
        value = self.details.get("server_id")
        return value if isinstance(value, str) else None


@dataclass(frozen=True, slots=True)
class DocumentDue:
    """A legal document version the organisation must accept before it can add anything.

    ``document`` is the document's key: ``terms``, ``mt5_licence``, or a plan's Service
    Agreement, ``service_agreement_<plan>`` (``service_agreement_enterprise``). The list is open:
    read a key you do not know as one more document, by its name. ``number`` is the version,
    ``plan`` the plan an agreement belongs to (None for the Terms and the licence), and
    ``grace_ends_at`` when its grace period ends or ended, aware; None for a plan change's
    agreement, which waits for acceptance instead.
    """

    document: str
    number: int | None
    plan: str | None
    grace_ends_at: dt.datetime | None


@dataclass(frozen=True, slots=True)
class PlanChange:
    """A move from one plan to another, as the customer sees it (the contract's
    ``PlanChangeSummary``).

    ``from_`` is the plan in force and ``to`` the plan after acceptance; ``state`` is
    ``awaiting_acceptance``, ``active``, ``lapsed`` or ``withdrawn`` (read a word you do not know
    as text). ``until`` is when an awaiting change lapses if nobody accepts it, None once decided.
    ``requested_by_operator`` is True when MFX Hub asked for the change, False when the
    organisation did, None if the platform did not say.
    """

    id: str
    from_: str
    to: str
    state: str
    requested_at: dt.datetime | None
    until: dt.datetime | None
    requested_by_operator: bool | None


def _documents_due(details: Mapping[str, Any]) -> list[DocumentDue]:
    """``details.documents``, keeping only the entries that name a document."""
    raw = details.get("documents")
    if not isinstance(raw, list):
        return []
    documents = []
    for entry in raw:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("document"), str):
            continue
        number = entry.get("number")
        documents.append(
            DocumentDue(
                document=entry["document"],
                number=number if isinstance(number, int) and not isinstance(number, bool) else None,
                plan=_text_or_none(entry, "plan"),
                grace_ends_at=_time_in(entry, "grace_ends_at"),
            )
        )
    return documents


class TermsNotAccepted(ConflictError):  # noqa: N818 - the name the SDKs share
    """409 ``terms_not_accepted``: a Terms of Service or MetaTrader 5 licence version the
    organisation must accept is past its grace period unaccepted, and nothing was done.

    Only additions are refused - a new terminal, attaching an expert advisor. Nothing running is
    touched: reads, orders, positions, restarts and detaches all work. It is **not retryable**
    unchanged: an owner or admin of the organisation accepts the version in the customer portal,
    then send the request again (a write under the same idempotency key). :attr:`documents` names
    each version due.
    """

    @property
    def documents(self) -> list[DocumentDue]:
        """Each document version due, with when its grace period ended."""
        return _documents_due(self.details)


class ServiceAgreementNotAccepted(ConflictError):  # noqa: N818 - the name the SDKs share
    """409 ``service_agreement_not_accepted``: a plan change awaits acceptance of the new plan's
    Service Agreement, or a version of the plan's agreement is past its grace period unaccepted,
    and nothing was done.

    Only additions are refused - a new terminal, attaching an expert advisor, generating or
    replacing an API key, asking for higher limits. Nothing running is touched: reads, orders,
    positions and anything already running all work. While a plan change waits, the plan in force
    stays as it is. Where the Terms are held as well, this is the error that answers, and
    :attr:`documents` lists every document due.

    It is **not retryable** unchanged. What a caller does: show ``message`` and :attr:`accept_url`
    to a person; an owner or admin of the organisation accepts there, then send the request again
    (a write under the same idempotency key). ``client.tenant.service_agreement()`` says what is
    due at any time.
    """

    @property
    def plan_change(self) -> PlanChange | None:
        """The plan change awaiting acceptance; None when there is none or it cannot be read."""
        raw = self.details.get("plan_change")
        if not isinstance(raw, Mapping):
            return None
        names = ("id", "from", "to", "state")
        if not all(isinstance(raw.get(name), str) for name in names):
            return None
        by_operator = raw.get("requested_by_operator")
        return PlanChange(
            id=raw["id"],
            from_=raw["from"],
            to=raw["to"],
            state=raw["state"],
            requested_at=_time_in(raw, "requested_at"),
            until=_time_in(raw, "until"),
            requested_by_operator=by_operator if isinstance(by_operator, bool) else None,
        )

    @property
    def documents(self) -> list[DocumentDue]:
        """Each document version due: the new plan's agreement, and any other held with it."""
        return _documents_due(self.details)

    @property
    def accept_url(self) -> str | None:
        """Where an owner or admin accepts, in the customer portal; None if not said."""
        return _text_or_none(self.details, "accept_url")


class RateLimitError(MfxApiError):
    """The key is over its budget. ``retry_after_s`` is the server's own answer."""


class UpstreamError(MfxApiError):
    """Something MFX depends on did not answer as it needs: your terminal, the broker, or a service
    of its own. Always 503 from the platform, told apart by ``error.code``:

    * ``upstream_error`` - your terminal or the broker, raised as this class: ``reason`` says why
      where there is one (``terminal_timeout``, ``deals_unreadable``, ``no_tick`` ...). No
      ``Retry-After``: whether waiting helps depends on the terminal, so read its state first.
    * ``dependency_unavailable`` - a store of the platform's own, raised as
      :class:`DependencyUnavailableError`; ``retry_after_s`` says when.

    The platform never answers 502 or 504. One of those came from the network in between (the
    edge's own page, with no MFX body), and is raised as :class:`EdgeError`, ``from_edge`` true.
    Both are subclasses, so ``except UpstreamError`` still catches all three.
    """

    @property
    def reason(self) -> str | None:
        """The platform's word for what failed (``details.reason``), or None when it gave none."""
        value = self.details.get("reason")
        return value if isinstance(value, str) else None

    @property
    def from_edge(self) -> bool:
        """True for a 502 or 504: not the platform's answer, the network's."""
        return self.status in (502, 504)


class DependencyUnavailableError(UpstreamError):
    """503 ``dependency_unavailable``: a store of the platform's own did not answer.

    Not your terminal and not the broker: the request was valid, and waiting ``retry_after_s``
    and sending it again is the right thing to do.
    """


class EdgeError(UpstreamError):
    """A 502 or 504 with no MFX body: the network in front of MFX Hub answered, not the platform.

    MFX Hub never answers either itself, so this says the platform could not be
    reached, not that it failed. A write may or may not have arrived: retry it with the same
    idempotency key, which answers the original if it did.
    """


class InternalError(MfxApiError):
    """MFX failed, and it is not the caller's request that is wrong."""


_BY_CODE: Final[dict[str, type[MfxApiError]]] = {
    "validation_error": ValidationError,
    "auth_error": AuthError,
    "forbidden": ForbiddenError,
    # Both are 403, and neither is about the key's scopes, which is what a bare ForbiddenError
    # says: they are the operator's decision about the whole tenant, with the operator's own
    # message. Mapped by code, as everything here is.
    "tenant_disabled": TenantDisabledError,
    "tenant_suspended": TenantSuspendedError,
    # 403 too, and not about the key either: a planned window, which ends at details.ends_at.
    "maintenance": MaintenanceError,
    # 402, and about neither the key nor the request: a payment is missing on the billing
    # profile. Mapped by code because once a profile is suspended any write can answer it.
    "billing_payment_required": BillingPaymentRequiredError,
    "not_found": NotFoundError,
    "conflict": ConflictError,
    "state_error": StateError,
    "placement_error": PlacementError,
    # Risk Management: a refused entry carries its rule and figures in details, and a
    # relaxing change made without risk:override is the key's to fix, not the request's.
    "risk_refused": RiskRefusedError,
    "risk_override_required": RiskOverrideRequiredError,
    # Mapped by code, which is the only way to get this right. The two refusals
    # on POST /terminals are no longer the same thing said twice, as they read when this mapping was
    # written: a 422 `validation_error` means the request names no broker or server MFX lists at all
    # (unknown, retired, or a server belonging to another broker), and a 409 with this code means a
    # broker or server MFX *does* list but cannot use now. The first is the caller's mistake; the
    # second is a fact about the platform that may change in an hour. Mapping by status would merge
    # them again.
    "broker_not_supported": UnsupportedBrokerError,
    # 409, and about neither the request nor the object: the organisation has something to
    # accept before it can add anything. Nothing running is refused, so a caller tells these
    # apart from a conflict to show a person where to accept.
    "terms_not_accepted": TermsNotAccepted,
    "service_agreement_not_accepted": ServiceAgreementNotAccepted,
    "rate_limited": RateLimitError,
    "upstream_error": UpstreamError,
    # 503 as well, and told apart by its code alone: a store of the platform's own, with
    # Retry-After, where upstream_error is the tenant's terminal or broker, with none. A subclass,
    # so code that waits on any upstream failure goes on catching it.
    "dependency_unavailable": DependencyUnavailableError,
    "internal_error": InternalError,
}

_BY_STATUS: Final[dict[int, type[MfxApiError]]] = {
    400: ValidationError,
    401: AuthError,
    402: PaymentRequiredError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
    500: InternalError,
    # The platform answers neither 502 nor 504; either is the edge's own page. Reached
    # only without an MFX code, which is what an edge's page is.
    502: EdgeError,
    503: UpstreamError,
    504: EdgeError,
}


def retry_after_seconds(headers: Mapping[str, str]) -> float | None:
    """``Retry-After`` in seconds, or None when it is absent or not a number of seconds."""
    raw = headers.get("Retry-After")
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:  # an HTTP-date is legal and this SDK does not parse one
        return None


def raise_for(status: int, headers: Mapping[str, str], content: bytes, what: str) -> None:
    """Raise the typed error for a failed answer. Returns quietly for a successful one.

    ``what`` is the call in the caller's words ("POST /terminals"), used when the body carries no
    message of its own — an error that says only "500" has told the caller nothing.
    """
    if HTTPStatus.OK <= status < HTTPStatus.BAD_REQUEST:
        return
    code, message, details = "", "", {}
    try:
        body = json.loads(content or b"")
    except ValueError:
        body = None
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        error = body["error"]
        code = str(error.get("code") or "")
        message = str(error.get("message") or "")
        raw_details = error.get("details")
        details = raw_details if isinstance(raw_details, dict) else {}
    raise error_for(
        code,
        message or f"{what} failed",
        status=status,
        details=details,
        retry_after_s=retry_after_seconds(headers),
    )


def error_for(
    code: str,
    message: str,
    *,
    status: int,
    details: dict[str, Any] | None = None,
    retry_after_s: float | None = None,
) -> MfxApiError:
    """The typed error for a failure the platform described, wherever it arrived.

    One mapping for a call's answer and for the stream's error frame, so a tenant shut out of
    the API meets the same exception on both. The code decides; the status only when the code
    is one this version does not know.
    """
    kind = _BY_CODE.get(code) or _BY_STATUS.get(status, MfxApiError)
    return kind(
        message,
        status=status,
        code=code or kind.__name__,
        details=details,
        retry_after_s=retry_after_s,
    )
