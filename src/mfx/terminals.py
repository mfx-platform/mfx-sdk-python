"""``client.terminals`` — a tenant's terminals.

The first vertical slice, and the one a tenant's first hour is made of: ask for a terminal, submit
the login that makes it real, watch it reach ACTIVE, retire it when it is done.

Two rules show up in every signature here:

* **Every write takes ``idempotency_key`` and it has no default**. A default would be
  a value someone did not choose, and the point of the key is that the caller can retry with the
  same one and get the same answer back rather than a second terminal.
* **A credential is a** :class:`~mfx.secrets.Secret`, not a ``str``. It is read once, sent once and
  never stored, logged or echoed; the type makes printing it by accident impossible.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from mfx._generated.api.credentials import submit_credentials as _submit_credentials
from mfx._generated.api.expert_advisors import (
    attach_expert_advisor as _attach_expert_advisor,
)
from mfx._generated.api.expert_advisors import (
    confirm_expert_advisor as _confirm_expert_advisor,
)
from mfx._generated.api.expert_advisors import (
    detach_expert_advisor as _detach_expert_advisor,
)
from mfx._generated.api.terminals import (
    create_terminal as _create_terminal,
)
from mfx._generated.api.terminals import (
    drain_terminal as _drain_terminal,
)
from mfx._generated.api.terminals import (
    get_terminal as _get_terminal,
)
from mfx._generated.api.terminals import (
    get_terminal_operation as _get_terminal_operation,
)
from mfx._generated.api.terminals import (
    list_terminals as _list_terminals,
)
from mfx._generated.api.terminals import (
    replace_terminal_instruments as _replace_terminal_instruments,
)
from mfx._generated.api.terminals import (
    restart_terminal as _restart_terminal,
)
from mfx._generated.api.terminals import (
    resume_terminal as _resume_terminal,
)
from mfx._generated.api.terminals import (
    retire_terminal as _retire_terminal,
)
from mfx._generated.models.credential_accepted import CredentialAccepted
from mfx._generated.models.credential_submission import CredentialSubmission
from mfx._generated.models.credential_submission_cred_type import CredentialSubmissionCredType
from mfx._generated.models.expert_advisor_attach import ExpertAdvisorAttach
from mfx._generated.models.expert_advisor_attach_timeframe import ExpertAdvisorAttachTimeframe
from mfx._generated.models.expert_advisor_attachment import ExpertAdvisorAttachment
from mfx._generated.models.expert_advisor_confirm import ExpertAdvisorConfirm
from mfx._generated.models.operation_accepted import OperationAccepted
from mfx._generated.models.tenant_terminal import TenantTerminal
from mfx._generated.models.tenant_terminal_state import TenantTerminalState
from mfx._generated.models.terminal_create import TerminalCreate
from mfx._generated.models.terminal_create_labels import TerminalCreateLabels
from mfx._generated.models.terminal_create_redundancy import TerminalCreateRedundancy
from mfx._generated.models.terminal_drain import TerminalDrain
from mfx._generated.models.terminal_instruments import TerminalInstruments
from mfx._generated.models.terminal_operation import TerminalOperation
from mfx._generated.models.terminal_restart import TerminalRestart
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of
from mfx.secrets import Secret

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = ["OFFLINE_IS_TEMPORARY", "OPERATION_FINAL", "Terminals", "is_usable"]

Redundancy = Literal["none", "active_passive", "active_active"]
CredentialType = Literal["master", "investor"]
Timeframe = Literal["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]
#: An operation is over in any of these; every other state is on its way (TerminalOperation).
OPERATION_FINAL: frozenset[str] = frozenset(
    {"SUCCEEDED", "FAILED", "NOT_STARTED", "EXPIRED", "CANCELLED", "SUPERSEDED"}
)
_POLL_FROM_S = 2.0
_POLL_CAP_S = 15.0
#: Ids are uuids on the wire and in the generated models. Callers may hand over either, because a
#: tenant reading an id out of its own database has a string and should not have to know that.
Id = str | UUID


#: A terminal is usable only while it is ACTIVE, and ACTIVE now means its cell can actually run it
#:. Before OFFLINE existed, a terminal whose cell had been turned off, or whose VM was
#: gone, or which had not been heard from for minutes, still read ACTIVE — so a caller checking
#: `state == "ACTIVE"` was told it could trade when nothing was there to trade with. Checking it
#: through this function means the next state the platform adds cannot quietly read as usable.
_USABLE_STATES: frozenset[TenantTerminalState] = frozenset({TenantTerminalState.ACTIVE})

#: OFFLINE needs nothing from you. The platform brings the terminal back by itself when its cell
#: reports again, and moves it to another cell of its farm when the cell's VM is gone or the cell is
#: still down after fifteen minutes. Retrying a request against an OFFLINE terminal is the right
#: thing to do; re-creating the terminal is not.
OFFLINE_IS_TEMPORARY = True


def is_usable(terminal: TenantTerminal) -> bool:
    """Can this terminal be used right now — market data, execution, account reads?

    True only in ACTIVE. Every other state means not yet (REQUESTED, PROVISIONING, LOGGING_IN),
    not any more (DRAINING, RETIRED), not until it is resumed (DRAINED), or not at the moment
    (OFFLINE, FAILED).

    `OFFLINE` is the state worth knowing about, because it is the one that used to be
    hidden inside ACTIVE: the terminal is fine, its *cell* is not — turned off outside MFX Hub, its
    VM missing in Azure, or silent for three minutes. ``terminal.offline_reason`` says which of the
    three. It is not something to act on: see :data:`OFFLINE_IS_TEMPORARY`.
    """
    state = terminal.state
    return isinstance(state, TenantTerminalState) and state in _USABLE_STATES


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(value)


def _op_state(operation: TerminalOperation) -> str:
    return str(getattr(operation.state, "value", operation.state))


class Terminals:
    """Provision, inspect, drain and retire the terminals this key's tenant owns."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        broker_id: Id,
        server_id: Id,
        idempotency_key: str,
        farm_id: Id | None = None,
        streaming: bool = False,
        execution: bool = False,
        instruments: list[str] | None = None,
        labels: dict[str, str] | None = None,
        redundancy: Redundancy = "none",
    ) -> TenantTerminal:
        """Ask for a terminal. Answered at once in state ``REQUESTED``.

        The move to a cell is asynchronous, and the credential is submitted separately, so a
        terminal exists before its login does. ``instruments`` are the broker's own symbol names
        (``EURUSD.sd``): MFX never renames an instrument on a tenant's behalf.

        **``farm_id`` is optional**. Leave it out and the platform chooses: your own
        ACTIVE farms first, then the shared ones, offering the usages this terminal needs, in the
        server's region, with room; the oldest wins a tie. The farm it picked is on the answer, so
        the choice is never silent. Nothing fits is ``409 no_farm`` rather than a terminal parked
        somewhere it cannot run. ``client.farms.list()`` shows what could be chosen from.

        Naming one is still the way to place a terminal deliberately, and it is checked rather than
        trusted: a farm that is not yours, or cannot take it, is refused.
        """
        body = TerminalCreate(
            farm_id=_uuid(farm_id) if farm_id is not None else UNSET,
            broker_id=_uuid(broker_id),
            server_id=_uuid(server_id),
            streaming=streaming,
            execution=execution,
            instruments=instruments if instruments is not None else UNSET,
            labels=TerminalCreateLabels.from_dict(labels) if labels is not None else UNSET,
            redundancy=TerminalCreateRedundancy(redundancy),
        )
        terminal = await self._client.write(
            lambda: _create_terminal.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /terminals",
        )
        return terminal  # type: ignore[no-any-return]

    async def get(self, terminal_id: Id) -> TenantTerminal:
        """One terminal: its state, how long it has been in it, and its observed conditions.

        Another tenant's id is a 404, never a 403.
        """
        terminal = await self._client.read(
            lambda: _get_terminal.asyncio_detailed(
                id=_uuid(terminal_id), client=self._client.generated
            ),
            f"GET /terminals/{terminal_id}",
        )
        return terminal  # type: ignore[no-any-return]

    async def page(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantTerminal]:
        """One page of this tenant's terminals, newest first."""
        parsed = await self._client.read(
            lambda: _list_terminals.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            "GET /terminals",
        )
        return page_of(parsed)

    async def list(self, *, limit: int | None = None) -> AsyncIterator[TenantTerminal]:
        """Every terminal, following the cursor.

        There is no `total` and no page number anywhere in the API, and there never will be
        (guardrail 7), so this follows the cursor rather than counting.
        """
        cursor: str | None = None
        while True:
            page = await self.page(cursor=cursor, limit=limit)
            for terminal in page.items:
                yield terminal
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return

    async def submit_credentials(
        self,
        terminal_id: Id,
        *,
        login: int,
        password: Secret | str,
        server: str,
        idempotency_key: str,
        cred_type: CredentialType = "master",
    ) -> CredentialAccepted:
        """Put a broker login on a terminal. The only request in MFX that carries a secret.

        It is wrapped, written to Key Vault and never stored, logged or echoed; the answer is a
        reference and nothing else. An ``investor`` credential turns execution off, and
        ``execution_disabled`` on the answer says so here rather than at the first refused order.
        """
        body = CredentialSubmission(
            login=login,
            password=Secret(password).reveal(),
            server=server,
            cred_type=CredentialSubmissionCredType(cred_type),
        )
        accepted = await self._client.write(
            lambda: _submit_credentials.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /terminals/{terminal_id}/credentials",
        )
        return accepted  # type: ignore[no-any-return]

    async def restart(
        self,
        terminal_id: Id,
        *,
        reason: str,
        idempotency_key: str,
        confirm_open_positions: bool = False,
    ) -> OperationAccepted:
        """Restart a stuck terminal: MT5 is closed and started again on the same cell.

        Answered ``202`` with the operation to follow; the terminal is not back until the
        operation succeeds, which takes a minute or two. ``reason`` is required and is **shown to
        operators in the console's activity feed and read back by this API**, so it is written for
        a person, not for a tracker.

        ``confirm_open_positions`` has no default on purpose at the platform: a restart drops the
        broker session for a few seconds, and on an account with positions open that is a decision
        the caller makes deliberately. Positions live at the broker and are not closed by a
        restart; the flag is there so nobody does this to a live account without saying so.

        Seven rules govern it: a cooldown, a rate limit, one
        operation at a time per terminal, and the states a restart can act on. A refusal names its
        rule in ``error.code``, with ``Retry-After`` when waiting is what helps.
        """
        accepted = await self._client.write(
            lambda: _restart_terminal.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=TerminalRestart(reason=reason, confirm_open_positions=confirm_open_positions),
                idempotency_key=idempotency_key,
            ),
            f"POST /terminals/{terminal_id}/restart",
        )
        return accepted  # type: ignore[no-any-return]

    async def replace_instruments(
        self,
        terminal_id: Id,
        instruments: Sequence[str],
        *,
        depth_instruments: Sequence[str] | None = None,
        idempotency_key: str,
    ) -> TenantTerminal:
        """Replace the terminal's whole instrument list, in the broker's own names.

        ``depth_instruments`` are the symbols of ``instruments`` whose order book it reads and
        streams on :meth:`mfx.streaming.Channel.book`: the whole list; ``[]`` stops
        depth; left out, the terminal keeps the depth symbols still in ``instruments``. A farm that
        offers no depth answers 422 ``depth_not_offered``; more than the farm allows, or a symbol
        not in ``instruments``, is 422 ``unprocessable``. Many brokers publish no book for most FX
        symbols; asking costs nothing then and the channel stays quiet.
        """
        body = TerminalInstruments(
            instruments=list(instruments),
            depth_instruments=UNSET if depth_instruments is None else list(depth_instruments),
        )
        terminal = await self._client.write(
            lambda: _replace_terminal_instruments.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PUT /terminals/{terminal_id}/instruments",
        )
        return terminal  # type: ignore[no-any-return]

    async def attach_expert_advisor(  # noqa: PLR0913 - the route's own fields
        self,
        terminal_id: Id,
        expert_advisor_id: Id,
        *,
        symbol: str,
        timeframe: Timeframe,
        reason: str,
        idempotency_key: str,
        queue: bool = False,
        confirm_open_positions: bool = False,
    ) -> OperationAccepted:
        """Attach an approved version to this terminal, on the symbol's chart and timeframe. A
        governed relaunch, answered 202 with the operation to follow (:meth:`wait_for_operation`).
        The expert then runs its trial with trading off; it trades only after a green trial, and on
        a real-money account only after :meth:`confirm_expert_advisor`."""
        body = ExpertAdvisorAttach(
            expert_advisor_id=_uuid(expert_advisor_id),
            symbol=symbol,
            timeframe=ExpertAdvisorAttachTimeframe(timeframe),
            reason=reason,
            queue=queue,
            confirm_open_positions=confirm_open_positions,
        )
        accepted = await self._client.write(
            lambda: _attach_expert_advisor.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"PUT /terminals/{terminal_id}/expert-advisor",
        )
        return accepted  # type: ignore[no-any-return]

    async def detach_expert_advisor(
        self,
        terminal_id: Id,
        *,
        reason: str,
        idempotency_key: str,
        queue: bool = False,
        confirm_open_positions: bool = False,
    ) -> OperationAccepted:
        """Take the expert off this terminal: a governed relaunch that rebuilds the folder, 202."""
        accepted = await self._client.write(
            lambda: _detach_expert_advisor.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                reason=reason,
                queue=queue,
                confirm_open_positions=confirm_open_positions,
                idempotency_key=idempotency_key,
            ),
            f"DELETE /terminals/{terminal_id}/expert-advisor",
        )
        return accepted  # type: ignore[no-any-return]

    async def confirm_expert_advisor(
        self, terminal_id: Id, *, code: str
    ) -> ExpertAdvisorAttachment:
        """Turn on live trading on a real-money account after a green trial, with the one-time
        code sent to the account's representative. A wrong, used or expired code is 403
        ``confirmation_refused`` and the answer does not say which; five in a row lock it."""
        attachment = await self._client.write(
            lambda: _confirm_expert_advisor.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=ExpertAdvisorConfirm(code=code),
            ),
            f"POST /terminals/{terminal_id}/expert-advisor/confirm",
        )
        return attachment  # type: ignore[no-any-return]

    async def get_operation(self, terminal_id: Id, operation_id: Id) -> TerminalOperation:
        """One operation on the terminal (restart, attach, detach): its state, step and timeline."""
        operation = await self._client.read(
            lambda: _get_terminal_operation.asyncio_detailed(
                id=_uuid(terminal_id),
                operation_id=_uuid(operation_id),
                client=self._client.generated,
            ),
            f"GET /terminals/{terminal_id}/operations/{operation_id}",
        )
        return operation  # type: ignore[no-any-return]

    async def wait_for_operation(
        self, terminal_id: Id, operation_id: Id, *, timeout_s: float = 900.0
    ) -> TerminalOperation:
        """Read the operation until it is over (:data:`OPERATION_FINAL`), or until ``timeout_s``.
        Returns the last read either way: an operation still running when the time runs out is
        reported as it is. Serves restart, attach and detach alike."""
        deadline = self._client.wall() + timeout_s
        wait = _POLL_FROM_S
        operation = await self.get_operation(terminal_id, operation_id)
        while _op_state(operation) not in OPERATION_FINAL and self._client.wall() < deadline:
            await self._client.pause(min(wait, _POLL_CAP_S))
            wait *= 2
            operation = await self.get_operation(terminal_id, operation_id)
        return operation

    async def drain(
        self,
        terminal_id: Id,
        *,
        idempotency_key: str,
        reason: str | None = None,
        confirm_open_positions: bool = False,
    ) -> TenantTerminal:
        """Close the terminal gracefully and keep it: DRAINED holds no cell and is not billed.

        Answered with the terminal ``DRAINING``; it is ``DRAINED`` once its cell has stopped it,
        and the operation (kind ``drain``) succeeds. A drained terminal keeps its id, account,
        credential, instruments, labels and expert-advisor record and runs nothing until
        :meth:`resume`. It still counts toward the terminal quota. Retire it with :meth:`retire`.

        Governed as :meth:`restart` is: one operation at a time, a cooldown, the tenant's rate and
        the farm's blast radius, each refusal naming its rule. ``confirm_open_positions`` is
        required true when the account has positions open (409 ``positions_open``); positions stay
        open at the broker while the terminal is drained. ``reason`` goes to the audit log and the
        terminal's history; left out, it is recorded as not given.
        """
        body = TerminalDrain(
            reason=reason if reason is not None else UNSET,
            confirm_open_positions=confirm_open_positions,
        )
        terminal = await self._client.write(
            lambda: _drain_terminal.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /terminals/{terminal_id}/drain",
        )
        return terminal  # type: ignore[no-any-return]

    async def resume(self, terminal_id: Id, *, idempotency_key: str) -> TenantTerminal:
        """Place a DRAINED terminal again: back to ``REQUESTED``, then placed and logged in as new.

        What can never work is refused at once - its farm not taking terminals, its broker or
        server no longer supported, a usage its farm no longer offers. Otherwise it waits for room
        as a new terminal does and is billed again from ACTIVE. A terminal already on its way back
        is answered as it is, so a resume sent twice is one resume; a DRAINING one is 409
        ``state_error`` until it is DRAINED.
        """
        terminal = await self._client.write(
            lambda: _resume_terminal.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"POST /terminals/{terminal_id}/resume",
        )
        return terminal  # type: ignore[no-any-return]

    async def retire(self, terminal_id: Id, *, idempotency_key: str) -> TenantTerminal:
        """Retire a terminal: it drains, then retires. Answered with its state now (DRAINING)."""
        terminal = await self._client.write(
            lambda: _retire_terminal.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            f"DELETE /terminals/{terminal_id}",
        )
        return terminal  # type: ignore[no-any-return]
