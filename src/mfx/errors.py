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
from http import HTTPStatus
from typing import Any, Final

__all__ = [
    "AuthError",
    "ConflictError",
    "ForbiddenError",
    "InternalError",
    "MfxApiError",
    "MfxError",
    "MfxTimeout",
    "MfxTransportError",
    "NotFoundError",
    "PlacementError",
    "RateLimitError",
    "StateError",
    "TenantDisabledError",
    "TenantSuspendedError",
    "UnsupportedBrokerError",
    "DependencyUnavailableError",
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
        self.status = status
        self.code = code
        self.details = details or {}
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
    "not_found": NotFoundError,
    "conflict": ConflictError,
    "state_error": StateError,
    "placement_error": PlacementError,
    # Mapped by code, which is the only way to get this right. The two refusals
    # on POST /terminals are no longer the same thing said twice, as they read when this mapping was
    # written: a 422 `validation_error` means the request names no broker or server MFX lists at all
    # (unknown, retired, or a server belonging to another broker), and a 409 with this code means a
    # broker or server MFX *does* list but cannot use now. The first is the caller's mistake; the
    # second is a fact about the platform that may change in an hour. Mapping by status would merge
    # them again.
    "broker_not_supported": UnsupportedBrokerError,
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
