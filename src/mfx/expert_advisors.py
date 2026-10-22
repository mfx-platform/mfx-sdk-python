"""``client.expert_advisors`` and ``client.tenant`` — the tenant's own Expert Advisor.

The order a tenant meets it in:

1. **Upload** the source (``.mq5`` and its ``.mqh``, as text) with :meth:`ExpertAdvisors.upload`.
   The same bundle again answers the version it already made; nothing is checked twice.
2. **Wait for the verdict** with :meth:`ExpertAdvisors.wait_for_verdict`, then read the
   :meth:`ExpertAdvisors.report`. Green runs; amber and red are held or refused, with the line.
3. **Attach** the approved version to a terminal on a farm that runs customer code
   (:meth:`mfx.terminals.Terminals.attach_expert_advisor`), and follow the operation with
   :meth:`mfx.terminals.Terminals.wait_for_operation`. A trial runs with trading off first.
4. On a real-money account, **confirm** live trading after the trial with the one-time code sent to
   the account's representative (:meth:`mfx.terminals.Terminals.confirm_expert_advisor`).
5. **Read what it writes** on ``Channel.ea(terminal_id)`` with :func:`telemetry_of`.

The source is read by the platform's checks, and the fenced part of it by a model provider; a
version's bytes are never served back by the API.
"""

from __future__ import annotations

import base64
from collections.abc import AsyncIterator, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final
from uuid import UUID

from mfx._generated.api.expert_advisors import (
    get_expert_advisor as _get,
)
from mfx._generated.api.expert_advisors import (
    get_expert_advisor_report as _report,
)
from mfx._generated.api.expert_advisors import (
    get_tenant_contacts as _contacts,
)
from mfx._generated.api.expert_advisors import (
    list_expert_advisors as _list,
)
from mfx._generated.api.expert_advisors import (
    upload_expert_advisor as _upload,
)
from mfx._generated.api.expert_advisors import (
    withdraw_expert_advisor as _withdraw,
)
from mfx._generated.models.expert_advisor_upload import ExpertAdvisorUpload
from mfx._generated.models.expert_advisor_upload_files_item import ExpertAdvisorUploadFilesItem
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of

if TYPE_CHECKING:  # pragma: no cover - typing only
    from mfx._generated.models.ea_report import EaReport
    from mfx._generated.models.own_contacts import OwnContacts
    from mfx._generated.models.tenant_expert_advisor import TenantExpertAdvisor
    from mfx.client import MfxClient
    from mfx.streaming import StreamMessage

__all__ = [
    "EaRecord",
    "EaTelemetry",
    "EaTelemetryLost",
    "ExpertAdvisors",
    "Tenant",
    "telemetry_of",
]

Id = str | UUID
#: A version stops changing on its own once it is in one of these (``judged`` is on the way to one).
_SETTLED: Final = frozenset({"approved", "held", "rejected", "withdrawn", "revoked"})
TELEMETRY: Final = "expert_advisor.telemetry"
TELEMETRY_LOST: Final = "expert_advisor.telemetry_lost"
_POLL_FROM_S: Final = 2.0
_POLL_CAP_S: Final = 15.0


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


def _text(content: bytes | str) -> str:
    return content.decode("utf-8") if isinstance(content, bytes) else content


class ExpertAdvisors:
    """The tenant's Expert Advisor versions (``ea:read`` to read, ``ea:write`` to upload)."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def upload(
        self, name: str, files: Mapping[str, bytes | str], *, idempotency_key: str
    ) -> TenantExpertAdvisor:
        """Upload a bundle: ``{path: source}``, exactly one ``.mq5`` and any ``.mqh`` it includes,
        as UTF-8 text. Never a compiled file. A new bundle answers its version in ``uploaded``, with
        the checks started; the same bundle again answers the version it made, as it stands. A
        file the platform will not take is 422 with ``details.why``; no farm that runs customer
        code is 409 ``no_customer_code_farm``."""
        body = ExpertAdvisorUpload(
            name=name,
            files=[
                ExpertAdvisorUploadFilesItem(
                    path=path, content_base64=base64.b64encode(_text(src).encode()).decode()
                )
                for path, src in files.items()
            ],
        )
        version = await self._client.write(
            lambda: _upload.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /expert-advisors",
        )
        return version  # type: ignore[no-any-return]

    async def get(self, expert_advisor_id: Id) -> TenantExpertAdvisor:
        """One version: its state, verdict, each check and where it stands, and the terminals
        that carry it. Never its bytes."""
        version = await self._client.read(
            lambda: _get.asyncio_detailed(
                id=_uuid(expert_advisor_id), client=self._client.generated
            ),
            f"GET /expert-advisors/{expert_advisor_id}",
        )
        return version  # type: ignore[no-any-return]

    async def page(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantExpertAdvisor]:
        """One page of the tenant's versions, newest first."""
        parsed = await self._client.read(
            lambda: _list.asyncio_detailed(
                client=self._client.generated,
                cursor=UNSET if cursor is None else cursor,
                limit=UNSET if limit is None else limit,
            ),
            "GET /expert-advisors",
        )
        return page_of(parsed)

    async def list(self, *, limit: int | None = None) -> AsyncIterator[TenantExpertAdvisor]:
        """Every version, following the cursor to the end."""
        cursor: str | None = None
        while True:
            page = await self.page(cursor=cursor, limit=limit)
            for version in page:
                yield version
            if page.next_cursor is None:
                return
            cursor = page.next_cursor

    async def report(self, expert_advisor_id: Id) -> EaReport:
        """The checks' report: each finding with its rule, colour and line. 409 until the verdict
        is set; wait for it with :meth:`wait_for_verdict`."""
        report = await self._client.read(
            lambda: _report.asyncio_detailed(
                id=_uuid(expert_advisor_id), client=self._client.generated
            ),
            f"GET /expert-advisors/{expert_advisor_id}/report",
        )
        return report  # type: ignore[no-any-return]

    async def delete(self, expert_advisor_id: Id, *, idempotency_key: str) -> TenantExpertAdvisor:
        """Withdraw a version; a check still running stops. 409 while a terminal carries it."""
        version = await self._client.write(
            lambda: _withdraw.asyncio_detailed(
                id=_uuid(expert_advisor_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"DELETE /expert-advisors/{expert_advisor_id}",
        )
        return version  # type: ignore[no-any-return]

    async def wait_for_verdict(
        self, expert_advisor_id: Id, *, timeout_s: float = 600.0
    ) -> TenantExpertAdvisor:
        """Read the version until its checks have settled it (approved, held, rejected,
        withdrawn or revoked), or until ``timeout_s``. Returns the last read either way: a version
        still being checked when the time runs out is reported as it is, not raised."""
        deadline = self._client.wall() + timeout_s
        wait = _POLL_FROM_S
        version = await self.get(expert_advisor_id)
        while _state(version) not in _SETTLED and self._client.wall() < deadline:
            await self._client.pause(min(wait, _POLL_CAP_S))
            wait *= 2
            version = await self.get(expert_advisor_id)
        return version


def _state(version: TenantExpertAdvisor) -> str:
    state = version.state
    return str(getattr(state, "value", state))


class Tenant:
    """What the tenant reads about itself."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def contacts(self) -> OwnContacts:
        """The tenant's contacts and their roles, as an operator set them (the trial's code goes
        to the representative). Read-only for a tenant."""
        contacts = await self._client.read(
            lambda: _contacts.asyncio_detailed(client=self._client.generated),
            "GET /tenant/contacts",
        )
        return contacts  # type: ignore[no-any-return]


@dataclass(frozen=True, slots=True)
class EaRecord:
    """One record the expert wrote. ``(segment, line)`` is its place in the expert's files: a
    record seen twice (delivery is at least once) has the same pair."""

    segment: int
    line: int
    record: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class EaTelemetry:
    """A batch of records, in the order written. ``skipped`` (lines the cell could not read) and
    ``dropped`` (left out by the platform) count since the message before."""

    channel: str
    seq: int | None
    records: tuple[EaRecord, ...]
    skipped: int
    dropped: int


@dataclass(frozen=True, slots=True)
class EaTelemetryLost:
    """The expert wrote faster than its records could be delivered and the oldest waiting files,
    ``segment_from`` to ``segment_to``, were discarded: ``records`` of them. Trading is never held
    for telemetry."""

    channel: str
    seq: int | None
    segment_from: int
    segment_to: int
    records: int


def telemetry_of(message: StreamMessage) -> EaTelemetry | EaTelemetryLost | None:
    """A message from an ``ea:`` channel as what it is, or None for any other message.

    .. code-block:: python

        await stream.subscribe(Channel.ea(terminal_id))
        seen = set()
        async for message in stream:
            batch = telemetry_of(message)
            if isinstance(batch, EaTelemetry):
                for r in batch.records:
                    if (r.segment, r.line) not in seen:
                        seen.add((r.segment, r.line))
                        handle(r.record)
    """
    kind = getattr(message, "type", None)
    data: Mapping[str, Any] = message.data
    if kind == TELEMETRY:
        return EaTelemetry(
            channel=message.channel,
            seq=message.seq,
            records=tuple(
                EaRecord(segment=int(r["segment"]), line=int(r["line"]), record=dict(r["record"]))
                for r in data.get("records") or ()
            ),
            skipped=int(data.get("skipped") or 0),
            dropped=int(data.get("dropped") or 0),
        )
    if kind == TELEMETRY_LOST:
        return EaTelemetryLost(
            channel=message.channel,
            seq=message.seq,
            segment_from=int(data["segment_from"]),
            segment_to=int(data["segment_to"]),
            records=int(data["records"]),
        )
    return None
