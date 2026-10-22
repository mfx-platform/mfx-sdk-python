"""What an execution call answers, and the reasons it can carry.

**Execution never raises across this boundary.** A transport fault, a timeout, a rate limit and a
broker rejection are all *results*, because a trading loop that has to catch exceptions to find out
whether it has a position is a trading loop that will one day place two.

That makes :class:`ExecutionResult` the one type a caller has to understand, so it carries the whole
answer: whether MFX accepted the command, what the broker did with it, both latencies, and
— when it went wrong — a reason from a granular vocabulary rather than a bucket.

**``UNKNOWN`` is not a failure and must never be retried.** The order may have reached the broker
and the outcome could not be read. Reconciliation against the terminal's deal history
resolves it on its own. ``retryable`` is false while a command is UNKNOWN, and that is the flag to
act on — never the reason, and never the state read by hand.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Any, Final, Self

__all__ = ["CommandState", "ExecutionResult", "Reason", "Tickets"]


class Reason(StrEnum):
    """Why a command ended as it did.

    The platform's dictionary of reasons plus the four the SDK itself can
    conclude. A reason the platform adds later arrives as its own string rather than as one of
    these — see :meth:`ExecutionResult.reason_text` — because bucketing a reason the caller has
    never seen is how a granular vocabulary quietly becomes "failed".
    """

    SUCCESS = "success"
    REQUOTE = "requote"
    INSTRUMENT_DISABLED = "instrument_disabled"
    NO_LIQUIDITY = "no_liquidity"
    MARKET_CLOSED = "market_closed"
    INVALID_STOPS = "invalid_stops"
    INVALID_VOLUME = "invalid_volume"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    TRADE_DISABLED = "trade_disabled"
    REJECTED_OTHER = "rejected_other"
    RATE_LIMITED = "rate_limited"
    EXPIRED = "expired"
    UNKNOWN = "unknown"
    #: A planned maintenance window suspended order placement for this terminal: the
    #: API refused it with 403 ``maintenance``, or a command queued before the window was refused
    #: by the platform before it ran. Nothing reached the broker, so it is **retryable** once the
    #: window ends - :attr:`ExecutionResult.retry_at` says when, where the platform said.
    MAINTENANCE = "maintenance"

    #: Concluded by the SDK, never sent by the platform: the request never got an answer.
    TRANSPORT_ERROR = "transport_error"
    #: Concluded by the SDK: no answer in time. **Never retried** — a timed-out order may have
    #: been placed, and deal-history reconciliation is the only safe recovery.
    TIMEOUT = "timeout"
    #: The platform refused the request itself: a 4xx that is not a rate limit.
    REFUSED = "refused"


class CommandState(StrEnum):
    """Final: SUCCEEDED, FAILED, EXPIRED, REJECTED. UNKNOWN is visible and not final."""

    ACCEPTED = "ACCEPTED"
    ENQUEUED = "ENQUEUED"
    DELIVERED = "DELIVERED"
    EXECUTING = "EXECUTING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


_FINAL: Final = frozenset(
    {CommandState.SUCCEEDED, CommandState.FAILED, CommandState.EXPIRED, CommandState.REJECTED}
)


@dataclass(frozen=True, slots=True)
class Tickets:
    """MT5 relates one order, one deal and one position per fill; null where MT5 has none yet."""

    order: int | None = None
    deal: int | None = None
    position: int | None = None

    @classmethod
    def from_dict(cls, raw: Any) -> Tickets:
        """Read tickets from the API's object; anything else reads as no tickets."""
        if not isinstance(raw, dict):
            return cls()
        return cls(
            order=_int(raw.get("order")),
            deal=_int(raw.get("deal")),
            position=_int(raw.get("position")),
        )


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _decimal(value: Any) -> Decimal | None:
    """Prices, volumes and money are decimals as strings: a float price is a wrong price."""
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """The whole answer to one execution call. Never raised — always returned.

    Read ``state`` first: ``SUCCEEDED`` is done; ``FAILED``, ``EXPIRED`` and ``REJECTED`` did not
    happen; ``UNKNOWN`` may already be a position and must never be sent again under a new key.
    ``final`` says whether the platform can still change the answer;
    :meth:`mfx.execution.Execution.wait_for` waits until it cannot.
    """

    #: True when the command succeeded.
    ok: bool
    #: The idempotency key this call was made with, so a retry can reuse it without bookkeeping.
    idempotency_key: str
    #: How long the SDK waited, end to end. Always known, even when nothing else is.
    client_rtt_ms: float
    #: The platform's id for the command; give it to ``wait_for`` or ``get_command``.
    command_id: str | None = None
    #: Where the command is: on its way (ACCEPTED, ENQUEUED, DELIVERED, EXECUTING), final
    #: (SUCCEEDED, FAILED, EXPIRED, REJECTED), or UNKNOWN.
    state: CommandState | None = None
    #: True once the platform will not change this answer again.
    final: bool = False
    #: Whether sending the same order again under a NEW key can succeed. **False while UNKNOWN.**
    retryable: bool = False
    #: The same key with the same body: this is the original command, not a second one.
    duplicate: bool = False
    #: Why it ended as it did, for a failure or a refusal. None when the platform gives no reason,
    #: which is what a success looks like: read ``state`` to know it succeeded.
    reason: Reason | None = None
    #: The reason exactly as it arrived, including one this SDK version does not know.
    reason_text: str | None = None
    #: The trading platform's own return code for the request, and its meaning in words.
    mt5_retcode: int | None = None
    retcode_text: str | None = None
    #: The broker's own comment, verbatim, for a human to read beside the reason.
    comment_raw: str | None = None
    #: The terminal's state when the command was answered.
    terminal_state: str | None = None
    #: The order, deal and position the broker gave this fill: ``tickets.position`` is what
    #: ``close_position`` and ``modify_position`` take.
    tickets: Tickets = field(default_factory=Tickets)
    #: The price and volume the broker filled at, as decimals.
    exec_price: Decimal | None = None
    exec_volume: Decimal | None = None
    #: Time at the broker, and time inside the platform's terminal, for this command.
    broker_latency_ms: int | None = None
    agent_latency_ms: int | None = None
    #: How many times the platform sent it to the broker.
    attempts: int = 0
    #: The terminal a failover moved this command from, when one did.
    rerouted_from: str | None = None
    #: What the platform said when it refused the request outright.
    detail: str | None = None
    #: When sending it again can work: the maintenance window's end, for a ``maintenance`` refusal.
    retry_at: dt.datetime | None = None

    @classmethod
    def from_command(cls, body: Any, *, idempotency_key: str, client_rtt_ms: float) -> Self:
        """Build from a Command or a CommandAccepted body, whichever the call answered with."""
        raw: dict[str, Any] = body if isinstance(body, dict) else {}
        state = _state(raw.get("state"))
        answer = raw.get("result")
        result: dict[str, Any] = answer if isinstance(answer, dict) else {}
        reason_text = result.get("reason")
        reason_text = reason_text if isinstance(reason_text, str) and reason_text else None
        return cls(
            ok=bool(result.get("ok", False)),
            idempotency_key=idempotency_key,
            client_rtt_ms=client_rtt_ms,
            command_id=str(raw["command_id"]) if raw.get("command_id") else None,
            state=state,
            final=bool(raw.get("final", state in _FINAL if state is not None else False)),
            # Never retryable while the outcome is unread: that is how one fill becomes two. A
            # maintenance refusal is, whatever the flag says: the consumer refused it before it ran.
            retryable=(bool(result.get("retryable", False)) or reason_text == Reason.MAINTENANCE)
            and state is not CommandState.UNKNOWN,
            duplicate=bool(raw.get("duplicate", False)),
            reason=_reason(reason_text),
            reason_text=reason_text,
            mt5_retcode=_int(result.get("mt5_retcode")),
            retcode_text=result.get("retcode_text"),
            comment_raw=result.get("comment_raw"),
            terminal_state=result.get("terminal_state"),
            tickets=Tickets.from_dict(result.get("tickets")),
            exec_price=_decimal(result.get("exec_price")),
            exec_volume=_decimal(result.get("exec_volume")),
            broker_latency_ms=_int(result.get("broker_latency_ms")),
            agent_latency_ms=_int(result.get("agent_latency_ms")),
            attempts=_int(result.get("attempts")) or 0,
            rerouted_from=result.get("rerouted_from"),
        )

    @classmethod
    def refused(  # noqa: PLR0913 - every field of a refusal the SDK concludes
        cls,
        reason: Reason,
        *,
        idempotency_key: str,
        client_rtt_ms: float,
        detail: str,
        retry_at: dt.datetime | None = None,
    ) -> Self:
        """An answer the SDK concluded itself: no transport, no time, or a refusal."""
        return cls(
            ok=False,
            idempotency_key=idempotency_key,
            client_rtt_ms=client_rtt_ms,
            reason=reason,
            reason_text=str(reason),
            # A timeout is never retryable: the order may have been placed (the platform's
            # rules). A transport error before the request left is, a rate limit is, and so is a
            # maintenance window's refusal, once it ends.
            retryable=reason in {Reason.TRANSPORT_ERROR, Reason.RATE_LIMITED, Reason.MAINTENANCE},
            final=True,
            detail=detail,
            retry_at=retry_at,
        )


def _state(raw: Any) -> CommandState | None:
    try:
        return CommandState(raw)
    except ValueError:
        return None


def _reason(raw: str | None) -> Reason | None:
    if raw is None:
        return None
    try:
        return Reason(raw)
    except ValueError:
        # A reason this version has never heard of. It is kept verbatim in reason_text and is not
        # forced into rejected_other, which would make a new reason indistinguishable from an old.
        return None
