"""``client.execution`` — placing and changing orders.

Every method here **returns** an :class:`~mfx.results.ExecutionResult` and never raises. A transport
fault, a timeout, a rate limit, a refusal and a broker rejection are all outcomes of trying to
trade, and a caller that must wrap each one in ``try`` to learn whether it has a position will
eventually place two.

Execution is asynchronous by design: the platform answers `202` with a ``command_id`` once the
command is persisted, and the outcome arrives later on the stream or from
:meth:`Execution.get_command`. :meth:`Execution.wait_for` is the convenience that polls until the
command is final, and it is the one place in this module that waits.

Three rules show up in every signature:

* **``idempotency_key`` is required and has no default**. A retry reuses the same key and
  gets the original command back with ``duplicate=True`` — never a second order.
* **Nothing is retried automatically.** Not a timeout (the order may have been placed), not a rate
  limit, not a 5xx. The SDK reports; the caller decides, with ``retryable`` to decide from.
* **Both latencies are on every result**, and the SDK adds its own ``client_rtt_ms``.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING, Any, Literal

from mfx._generated.api.execution import (
    cancel_order as _cancel_order,
)
from mfx._generated.api.execution import (
    clear_trailing_stop as _clear_trailing_stop,
)
from mfx._generated.api.execution import (
    close_position as _close_position,
)
from mfx._generated.api.execution import (
    close_position_by as _close_position_by,
)
from mfx._generated.api.execution import (
    close_position_partial as _close_position_partial,
)
from mfx._generated.api.execution import (
    get_command as _get_command,
)
from mfx._generated.api.execution import (
    modify_order as _modify_order,
)
from mfx._generated.api.execution import (
    modify_position as _modify_position,
)
from mfx._generated.api.execution import (
    place_order as _place_order,
)
from mfx._generated.api.execution import (
    set_trailing_stop as _set_trailing_stop,
)
from mfx._generated.models.order_modify import OrderModify
from mfx._generated.models.order_place import OrderPlace
from mfx._generated.models.order_place_order_type import OrderPlaceOrderType
from mfx._generated.models.order_place_side import OrderPlaceSide
from mfx._generated.models.position_close import PositionClose
from mfx._generated.models.position_close_by import PositionCloseBy
from mfx._generated.models.position_close_partial import PositionClosePartial
from mfx._generated.models.position_modify import PositionModify
from mfx._generated.models.trailing_stop_set import TrailingStopSet
from mfx._generated.types import UNSET
from mfx.errors import (
    MaintenanceError,
    MfxApiError,
    MfxTimeout,
    MfxTransportError,
    RateLimitError,
)
from mfx.results import ExecutionResult, Reason
from mfx.terminals import Id, _uuid

if TYPE_CHECKING:
    import datetime as dt
    from collections.abc import Awaitable, Callable

    from mfx._generated.types import Response as GeneratedResponse
    from mfx.client import MfxClient

__all__ = ["Execution"]

Side = Literal["buy", "sell"]
OrderType = Literal["market", "limit", "stop", "stop_limit"]

#: What a decimal field accepts. A `float` is deliberately **not** here: `0.07 * 3` is
#: 0.21000000000000002, and position sizing is arithmetic, so the ordinary path for a strategy is a
#: computed value. Taking a float would put that on the wire, which decimal strings prevent.
Amount = Decimal | str | int


class _Keep:
    """The default for :meth:`Execution.modify_order`'s ``expires_at``: leave the order's
    own expiry unchanged. It is what tells 'leave it' from ``None`` ('clear it to
    good-till-cancelled') — a plain default of ``None`` could not say both."""


_KEEP: _Keep = _Keep()


def _decimal(name: str, value: Amount) -> str:
    """One decimal as the contract wants it: plain notation, no sign, no exponent.

    **`format(value, "f")`, never `str(value)`.** `str(Decimal("0.0000001"))` is `"1E-7"` and
    `str(Decimal("1E+3"))` is `"1E+3"`; the contract's pattern refuses both, so the obvious
    conversion produces a body the edge rejects — on a seven-digit symbol, or on any value that has
    been through `.normalize()`.

    A `float` is refused here rather than converted, and the message says what to send instead. A
    type error at the call site is a better answer than a 400 from the edge, and silently accepting
    one would leave the caller believing their computed size arrived intact.
    """
    if isinstance(value, float):
        raise TypeError(
            f"{name} must be a Decimal, a str or an int, not a float: a computed float carries "
            f"binary error (0.07 * 3 is 0.21000000000000002) and the platform takes decimals as "
            f'strings so nothing is lost. Send Decimal("{value!r}") or a string.'
        )
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name} is not a decimal: {value!r}") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"{name} must be a finite, non-negative decimal, not {value!r}")
    return format(number, "f")


#: How often wait_for asks, and the longest it will ever sleep between asks. Execution results
#: arrive in milliseconds when they arrive at all; the stream is the right answer for anything
#: that needs to be sooner than this.
_POLL_FROM_S = 0.2
_POLL_CAP_S = 2.0


class Execution:
    """Order entry for one tenant. Every method returns a result; none raises."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def place_order(
        self,
        terminal_id: Id,
        *,
        symbol: str,
        side: Side,
        volume: Amount,
        idempotency_key: str,
        order_type: OrderType = "market",
        price: Amount | None = None,
        stop_limit_price: Amount | None = None,
        sl: Amount | None = None,
        tp: Amount | None = None,
        deviation_points: int | None = None,
        expires_at: dt.datetime | None = None,
        magic: int | None = None,
        comment: str | None = None,
    ) -> ExecutionResult:
        """Place a market or pending order.

        ``symbol`` is the broker's own name (``EURUSD.sd``): MFX never renames an instrument on a
        tenant's behalf. ``comment`` longer than 31 characters is refused rather than
        truncated, because MT5 cuts it without saying so.

        A ``stop_limit`` order has two prices: ``price`` is the stop
        price, where the order wakes up, and ``stop_limit_price`` is the limit order placed when
        it does. ``stop_limit_price`` is required with ``stop_limit`` and refused with any other
        type; the platform says so, and the refusal comes back as the result.

        ``volume``, ``price``, ``stop_limit_price``, ``sl`` and ``tp`` take a ``Decimal``, a
        string or an int, and **refuse a float** — see :func:`_decimal`.
        """
        body = OrderPlace(
            symbol=symbol,
            side=OrderPlaceSide(side),
            volume=_decimal("volume", volume),
            order_type=OrderPlaceOrderType(order_type),
            price=_decimal("price", price) if price is not None else UNSET,
            stop_limit_price=(
                _decimal("stop_limit_price", stop_limit_price)
                if stop_limit_price is not None
                else UNSET
            ),
            sl=_decimal("sl", sl) if sl is not None else UNSET,
            tp=_decimal("tp", tp) if tp is not None else UNSET,
            deviation_points=deviation_points if deviation_points is not None else UNSET,
            expires_at=expires_at if expires_at is not None else UNSET,
            magic=magic if magic is not None else UNSET,
            comment=comment if comment is not None else UNSET,
        )
        return await self._command(
            lambda: _place_order.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/orders",
        )

    async def cancel_order(
        self, terminal_id: Id, ticket: int, *, idempotency_key: str
    ) -> ExecutionResult:
        """Cancel a pending order. First class, not a modify with a special case."""
        return await self._command(
            lambda: _cancel_order.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/orders/{ticket}/cancel",
        )

    async def modify_position(
        self,
        terminal_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        sl: Amount | None = None,
        tp: Amount | None = None,
    ) -> ExecutionResult:
        """Move the stop loss, the take profit, or both. At least one is required."""
        if sl is None and tp is None:
            raise ValueError("modify_position needs sl, tp, or both")
        body = PositionModify(
            sl=_decimal("sl", sl) if sl is not None else UNSET,
            tp=_decimal("tp", tp) if tp is not None else UNSET,
        )
        return await self._command(
            lambda: _modify_position.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/positions/{ticket}/modify",
        )

    async def modify_order(
        self,
        terminal_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        price: Amount | None = None,
        stop_limit_price: Amount | None = None,
        sl: Amount | None = None,
        tp: Amount | None = None,
        expires_at: dt.datetime | None | _Keep = _KEEP,
    ) -> ExecutionResult:
        """Amend a pending order's price, stops or expiry. At least one must change.

        What is not given keeps the order's present value, because MetaTrader's amend takes
        the whole order. A level of ``\"0\"`` clears a stop or a
        take-profit. For the expiry the three states are told apart: leaving ``expires_at``
        out keeps the order's own, ``None`` makes it good-till-cancelled, and a time sets it.
        Volume, side, type and symbol cannot be amended — a tenant cancels and places again.

        ``stop_limit_price`` is a stop-limit order's second price (2.14); on any other order
        the cell refuses it, and the refusal comes back as the result.

        ``price``, ``stop_limit_price``, ``sl`` and ``tp`` take a ``Decimal``, a string or an
        int, and **refuse a float** — see :func:`_decimal`.
        """
        nothing_to_change = (
            price is None
            and stop_limit_price is None
            and sl is None
            and tp is None
            and isinstance(expires_at, _Keep)
        )
        if nothing_to_change:
            raise ValueError("modify_order needs price, stop_limit_price, sl, tp, or expires_at")
        body = OrderModify(
            price=_decimal("price", price) if price is not None else UNSET,
            stop_limit_price=(
                _decimal("stop_limit_price", stop_limit_price)
                if stop_limit_price is not None
                else UNSET
            ),
            sl=_decimal("sl", sl) if sl is not None else UNSET,
            tp=_decimal("tp", tp) if tp is not None else UNSET,
            expires_at=UNSET if isinstance(expires_at, _Keep) else expires_at,
        )
        return await self._command(
            lambda: _modify_order.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/orders/{ticket}/modify",
        )

    async def close_position(
        self,
        terminal_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        deviation_points: int | None = None,
    ) -> ExecutionResult:
        """Close a position in full.

        No comment parameter: PositionClose has no such field and forbids extras, so one would be
        refused by the platform rather than ignored.
        """
        body = PositionClose(
            deviation_points=deviation_points if deviation_points is not None else UNSET
        )
        return await self._command(
            lambda: _close_position.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/positions/{ticket}/close",
        )

    async def close_position_by(
        self,
        terminal_id: Id,
        ticket: int,
        by_ticket: int,
        *,
        idempotency_key: str,
    ) -> ExecutionResult:
        """Close a position against an opposite one in the same symbol (hedging accounts).

        ``ticket`` is the position being closed and ``by_ticket`` the opposite one. The smaller
        of the two disappears and the larger is reduced by its volume, and the spread is paid
        once and not twice. The result's ``exec_volume`` is the
        volume closed; it has no ``exec_price``, because a close-by has no single price.

        Two tickets that are not open positions of the account, in one symbol, on opposite
        sides are refused before the broker is asked - which is also what a netting account
        gets, since there the two cannot both exist. The refusal comes back as the result.
        """
        body = PositionCloseBy(by_ticket=by_ticket)
        return await self._command(
            lambda: _close_position_by.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/positions/{ticket}/close-by",
        )

    async def close_position_partial(
        self,
        terminal_id: Id,
        ticket: int,
        *,
        volume: Amount,
        idempotency_key: str,
        deviation_points: int | None = None,
    ) -> ExecutionResult:
        """Close part of a position — the volume to close, inside the symbol's step.

        Takes a ``Decimal``, a string or an int and refuses a float.
        """
        body = PositionClosePartial(
            volume=_decimal("volume", volume),
            deviation_points=deviation_points if deviation_points is not None else UNSET,
        )
        return await self._command(
            lambda: _close_position_partial.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"POST /terminals/{terminal_id}/positions/{ticket}/close-partial",
        )

    async def set_trailing_stop(
        self,
        terminal_id: Id,
        ticket: int,
        *,
        distance: Amount,
        idempotency_key: str,
    ) -> ExecutionResult:
        """Keep the position's stop loss ``distance`` behind the best price it reaches.

        ``distance`` is a price difference above zero - ``Decimal("0.0020")`` on EURUSD is twenty
        pips - and a ``float`` is refused. The worker on the cell moves the broker's stop,
        only ever tighter, at most once a second and by at least a tenth of the distance. Setting
        again replaces the distance and keeps what the stop has reached. A stop loss set by anyone
        else ends it, and the stream says so (``position.trailing_stop_changed``). Refused as a
        result with ``invalid_stops`` when the distance is inside the symbol's stops level, and
        ``invalid_request`` when the ticket is not an open position of the account.
        """
        body = TrailingStopSet(distance=_decimal("distance", distance))
        return await self._command(
            lambda: _set_trailing_stop.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"PUT /terminals/{terminal_id}/positions/{ticket}/trailing-stop",
        )

    async def clear_trailing_stop(
        self, terminal_id: Id, ticket: int, *, idempotency_key: str
    ) -> ExecutionResult:
        """Remove the position's trailing stop. The stop loss stays where the trail left it."""
        return await self._command(
            lambda: _clear_trailing_stop.asyncio_detailed(
                id=_uuid(terminal_id),
                ticket=ticket,
                client=self._client.generated,
                idempotency_key=idempotency_key,
            ),
            idempotency_key,
            f"DELETE /terminals/{terminal_id}/positions/{ticket}/trailing-stop",
        )

    async def get_command(self, command_id: Id, *, idempotency_key: str = "") -> ExecutionResult:
        """One command and its result. A command belonging to another tenant is a 404, never 403.

        Reading is on the execution boundary too: a caller checking what happened to an order must
        not have to catch an exception to find out that it cannot tell.
        """
        return await self._command(
            lambda: _get_command.asyncio_detailed(
                id=_uuid(command_id), client=self._client.generated
            ),
            idempotency_key,
            f"GET /commands/{command_id}",
        )

    async def wait_for(
        self, command_id: Id, *, timeout_s: float = 30.0, idempotency_key: str = ""
    ) -> ExecutionResult:
        """Poll until the command is final, or until ``timeout_s``.

        Returns the last answer either way — a command that is still EXECUTING when the time runs
        out is reported as it is, not raised and not guessed at. **A non-final result is never a
        licence to re-send**: an UNKNOWN command may already be a position.
        """
        deadline = self._client.wall() + timeout_s
        wait = _POLL_FROM_S
        result = await self.get_command(command_id, idempotency_key=idempotency_key)
        while not result.final and self._client.wall() < deadline:
            await self._client.pause(min(wait, _POLL_CAP_S))
            wait *= 2
            result = await self.get_command(command_id, idempotency_key=idempotency_key)
        return result

    async def _command(
        self,
        call: Callable[[], Awaitable[GeneratedResponse[Any]]],
        idempotency_key: str,
        what: str,
    ) -> ExecutionResult:
        """Run one execution call and turn *everything* it can do into a result."""
        started = self._client.wall()

        def elapsed() -> float:
            return (self._client.wall() - started) * 1000.0

        try:
            response = await self._client.send(call, what)
        except MfxTimeout as exc:
            # Never retried, by the SDK or by anyone: the order may have reached the broker, and
            # deal-history reconciliation is the only safe recovery.
            return ExecutionResult.refused(
                Reason.TIMEOUT,
                idempotency_key=idempotency_key,
                client_rtt_ms=elapsed(),
                detail=f"{what}: {exc}",
            )
        except MfxTransportError as exc:
            return ExecutionResult.refused(
                Reason.TRANSPORT_ERROR,
                idempotency_key=idempotency_key,
                client_rtt_ms=elapsed(),
                detail=f"{what}: {exc}",
            )
        except MfxApiError as exc:  # an answer the generated core could not read
            return ExecutionResult.refused(
                Reason.REFUSED,
                idempotency_key=idempotency_key,
                client_rtt_ms=elapsed(),
                detail=f"{what}: {exc}",
            )

        status = int(response.status_code)
        if status >= 400:  # noqa: PLR2004 - "not a success" needs no name
            try:
                self._client.raise_for_answer(response, what)
            except MaintenanceError as paused:
                return ExecutionResult.refused(
                    Reason.MAINTENANCE,
                    idempotency_key=idempotency_key,
                    client_rtt_ms=elapsed(),
                    detail=str(paused),
                    retry_at=paused.ends_at,
                )
            except RateLimitError as limited:
                return ExecutionResult.refused(
                    Reason.RATE_LIMITED,
                    idempotency_key=idempotency_key,
                    client_rtt_ms=elapsed(),
                    detail=str(limited),
                )
            except MfxApiError as refused:
                return ExecutionResult.refused(
                    Reason.REFUSED,
                    idempotency_key=idempotency_key,
                    client_rtt_ms=elapsed(),
                    detail=str(refused),
                )
        return ExecutionResult.from_command(
            _body_of(response), idempotency_key=idempotency_key, client_rtt_ms=elapsed()
        )


def _body_of(response: GeneratedResponse[Any]) -> dict[str, Any]:
    """The answer as a plain object: 202 gives a CommandAccepted, 200 a whole Command."""
    import json

    try:
        body = json.loads(response.content or b"{}")
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}
