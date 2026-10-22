"""``client.webhooks`` and :func:`verify` — MFX Hub calling the tenant's own address.

A tenant registers an HTTPS address and the event types it wants; MFX
Hub then POSTs each such event there, exactly as the ``events`` channel carries it, signed. Two
halves live here:

* **Managing endpoints** (``hook:read`` / ``hook:write``): register, read, change, pause, remove,
  rotate the secret, ask for a test event, read what did not arrive, and ask for events again.

* **Receiving** — :func:`verify`, one call for the receiver's side, with no client and no network.
  It checks ``MFX-Signature`` over the body *as received* (re-serialising parsed JSON changes the
  bytes and the signature with them) and refuses a timestamp more than five minutes from the
  receiver's clock::

      from mfx.webhooks import verify, WebhookSignatureError

      try:
          verify(request.body, request.headers["MFX-Signature"], secret)
      except WebhookSignatureError:
          return 400
      handle(json.loads(request.body))   # de-duplicate on MFX-Event-Id: delivery is at least once

The secret is shown once, when the endpoint is made (:meth:`Webhooks.create`) and at each rotation
(:meth:`Webhooks.rotate_secret`), and never again. For a day after a rotation both secrets sign, the
new one first; a receiver that holds both passes them as a list.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from collections.abc import AsyncIterator, Awaitable, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID

from mfx._generated.api.webhooks import (
    create_webhook as _create,
)
from mfx._generated.api.webhooks import (
    delete_webhook as _delete,
)
from mfx._generated.api.webhooks import (
    get_webhook as _get,
)
from mfx._generated.api.webhooks import (
    list_webhook_failures as _failures,
)
from mfx._generated.api.webhooks import (
    list_webhooks as _list,
)
from mfx._generated.api.webhooks import (
    replay_webhook as _replay,
)
from mfx._generated.api.webhooks import (
    rotate_webhook_secret as _rotate,
)
from mfx._generated.api.webhooks import (
    test_webhook as _test,
)
from mfx._generated.api.webhooks import (
    update_webhook as _update,
)
from mfx._generated.models.list_webhook_failures_state import ListWebhookFailuresState
from mfx._generated.models.webhook_endpoint_create import WebhookEndpointCreate
from mfx._generated.models.webhook_endpoint_update import WebhookEndpointUpdate
from mfx._generated.models.webhook_endpoint_update_status import WebhookEndpointUpdateStatus
from mfx._generated.models.webhook_replay import WebhookReplay
from mfx._generated.types import UNSET
from mfx.errors import MfxError
from mfx.secrets import Secret

if TYPE_CHECKING:  # pragma: no cover - typing only
    from mfx._generated.models.webhook_endpoint import WebhookEndpoint
    from mfx._generated.models.webhook_endpoint_created import WebhookEndpointCreated
    from mfx._generated.models.webhook_failure import WebhookFailure
    from mfx._generated.models.webhook_replay_accepted import WebhookReplayAccepted
    from mfx._generated.models.webhook_secret_rotated import WebhookSecretRotated
    from mfx._generated.models.webhook_test_accepted import WebhookTestAccepted
    from mfx.client import MfxClient

__all__ = ["SIGNATURE_HEADER", "TOLERANCE_S", "WebhookSignatureError", "Webhooks", "verify"]

#: The headers MFX Hub sends with every delivery.
SIGNATURE_HEADER = "MFX-Signature"
EVENT_ID_HEADER = "MFX-Event-Id"
EVENT_TYPE_HEADER = "MFX-Event-Type"
ATTEMPT_HEADER = "MFX-Delivery-Attempt"
#: How far the signed time may be from the receiver's clock, either way.
TOLERANCE_S = 300

Id = str | UUID
FailureState = Literal["retrying", "dead", "delivered"]


class WebhookSignatureError(MfxError):
    """The delivery is not provably from MFX Hub: refuse it. ``reason`` is one word —
    ``malformed`` (no ``t`` or no ``v1``), ``stale`` (outside the tolerance) or ``mismatch``."""

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason


def _parts(header: str) -> tuple[int, list[str]]:
    stamp: int | None = None
    signatures: list[str] = []
    for item in header.split(","):
        key, _, value = item.strip().partition("=")
        if key == "t" and value.isdigit():
            stamp = int(value)
        elif key == "v1" and value:
            signatures.append(value)
    if stamp is None or not signatures:
        raise WebhookSignatureError("malformed", f"{SIGNATURE_HEADER} needs t= and v1=: {header!r}")
    return stamp, signatures


def verify(
    body: bytes | str,
    header: str,
    secret: str | Secret | Sequence[str | Secret],
    *,
    tolerance_s: float = TOLERANCE_S,
    now: float | None = None,
) -> int:
    """Check one delivery's ``MFX-Signature`` and return its signed time (unix seconds).

    ``body`` is the request body exactly as received. ``secret`` is the endpoint's secret as it was
    shown, or several (the new and the previous, for the day after a rotation): the delivery is
    genuine when any one of them made any one of the header's ``v1`` values. Raises
    :class:`WebhookSignatureError` otherwise, and when the signed time is more than
    ``tolerance_s`` from ``now`` (the receiver's clock), which is what stops a captured delivery
    being sent again later.
    """
    raw = body.encode() if isinstance(body, str) else body
    stamp, signatures = _parts(header)
    clock = time.time() if now is None else now
    if abs(clock - stamp) > tolerance_s:
        raise WebhookSignatureError(
            "stale", f"signed at {stamp}, {abs(clock - stamp):.0f} s from this clock"
        )
    keys = [secret] if isinstance(secret, str | Secret) else list(secret)
    signed = str(stamp).encode() + b"." + raw
    for key in keys:
        text = key.reveal() if isinstance(key, Secret) else key
        expected = hmac.new(text.encode(), signed, hashlib.sha256).hexdigest()
        if any(hmac.compare_digest(expected, given) for given in signatures):
            return stamp
    raise WebhookSignatureError("mismatch", "no secret given made this signature")


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


class Webhooks:
    """The tenant's webhook endpoints (``hook:read`` to read, ``hook:write`` to change)."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def create(
        self,
        url: str,
        event_types: Sequence[str],
        *,
        description: str | None = None,
        idempotency_key: str,
    ) -> WebhookEndpointCreated:
        """Register an HTTPS address for these event types (``position.closed``, ``terminal.*``,
        or ``*``). The answer carries the signing ``secret`` - shown here and never again, so keep
        it before doing anything else. An address that resolves to a private, loopback,
        link-local or metadata address is refused (422)."""
        body = WebhookEndpointCreate(
            url=url,
            event_types=list(event_types),
            description=UNSET if description is None else description,
        )
        created = await self._client.write(
            lambda: _create.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /webhooks",
        )
        return created  # type: ignore[no-any-return]

    async def list(self) -> list[WebhookEndpoint]:
        """Every endpoint of the tenant, each with how it is doing (delivered, retrying, dead)."""
        listed = await self._client.read(
            lambda: _list.asyncio_detailed(client=self._client.generated), "GET /webhooks"
        )
        return list(listed.items)

    async def get(self, endpoint_id: Id) -> WebhookEndpoint:
        """One endpoint; another tenant's id is a 404."""
        endpoint = await self._client.read(
            lambda: _get.asyncio_detailed(id=_uuid(endpoint_id), client=self._client.generated),
            f"GET /webhooks/{endpoint_id}",
        )
        return endpoint  # type: ignore[no-any-return]

    async def update(
        self,
        endpoint_id: Id,
        *,
        url: str | None = None,
        event_types: Sequence[str] | None = None,
        description: str | None = None,
        paused: bool | None = None,
        idempotency_key: str,
    ) -> WebhookEndpoint:
        """Change the address or the types, or pause (``paused=True``) and resume it. What is not
        given is left as it is."""
        body = WebhookEndpointUpdate(
            url=UNSET if url is None else url,
            event_types=UNSET if event_types is None else list(event_types),
            description=UNSET if description is None else description,
            status=UNSET
            if paused is None
            else WebhookEndpointUpdateStatus("paused" if paused else "active"),
        )
        endpoint = await self._client.write(
            lambda: _update.asyncio_detailed(
                id=_uuid(endpoint_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PATCH /webhooks/{endpoint_id}",
        )
        return endpoint  # type: ignore[no-any-return]

    async def delete(self, endpoint_id: Id) -> None:
        """Remove the endpoint and its secret. Nothing more is sent to it."""
        await self._client.write(
            lambda: _delete.asyncio_detailed(id=_uuid(endpoint_id), client=self._client.generated),
            f"DELETE /webhooks/{endpoint_id}",
        )

    async def rotate_secret(self, endpoint_id: Id, *, idempotency_key: str) -> WebhookSecretRotated:
        """A new secret, shown once; the previous one also signs until ``previous_secret_until``."""
        rotated = await self._client.write(
            lambda: _rotate.asyncio_detailed(
                id=_uuid(endpoint_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /webhooks/{endpoint_id}/rotate-secret",
        )
        return rotated  # type: ignore[no-any-return]

    async def test(self, endpoint_id: Id) -> WebhookTestAccepted:
        """Ask for a ``webhook.test`` event at the endpoint, delivered and signed like any other."""
        accepted = await self._client.write(
            lambda: _test.asyncio_detailed(id=_uuid(endpoint_id), client=self._client.generated),
            f"POST /webhooks/{endpoint_id}/test",
        )
        return accepted  # type: ignore[no-any-return]

    async def failures(
        self, endpoint_id: Id, *, state: FailureState | None = None, limit: int | None = None
    ) -> AsyncIterator[WebhookFailure]:
        """What did not arrive: each failed event with every attempt on it, following the cursor
        to the end. ``state`` narrows to ``retrying``, ``dead`` (gave up) or ``delivered``."""
        cursor: str | None = None

        def call(after: str | None) -> Awaitable[Any]:
            return _failures.asyncio_detailed(
                id=_uuid(endpoint_id),
                client=self._client.generated,
                state=UNSET if state is None else ListWebhookFailuresState(state),
                cursor=UNSET if after is None else after,
                limit=UNSET if limit is None else limit,
            )

        while True:
            page = await self._client.read(
                partial(call, cursor), f"GET /webhooks/{endpoint_id}/failures"
            )
            for failure in page.items:
                yield failure
            cursor = page.next_cursor
            if not cursor:
                return

    async def replay(
        self,
        endpoint_id: Id,
        *,
        after: str | None = None,
        failure_id: Id | None = None,
        idempotency_key: str,
    ) -> WebhookReplayAccepted:
        """Send events again: every one after a stream cursor (``after``, an ``MFX-Event-Id``),
        or one failure (``failure_id``). A cursor the stream no longer holds is refused."""
        if (after is None) == (failure_id is None):
            raise ValueError("give exactly one of after= and failure_id=")
        body = WebhookReplay(
            after=UNSET if after is None else after,
            failure_id=UNSET if failure_id is None else _uuid(failure_id),
        )
        accepted = await self._client.write(
            lambda: _replay.asyncio_detailed(
                id=_uuid(endpoint_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /webhooks/{endpoint_id}/replay",
        )
        return accepted  # type: ignore[no-any-return]
