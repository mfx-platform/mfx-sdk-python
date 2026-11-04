"""``client.maintenance`` - planned maintenance on this tenant's terminals.

While a window runs, what it suspends for you is refused with 403 ``maintenance``
(:class:`~mfx.errors.MaintenanceError`, or an execution result with reason ``maintenance``) until
``ends_at``. These two reads say what is scheduled and in progress and where each of your terminals
is, and are answered under every suspension, so a caller that has just been refused can always ask
how long for. Open positions are never closed by a window.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal
from uuid import UUID

from mfx._generated.api.maintenance import list_maintenance as _list_maintenance
from mfx._generated.api.maintenance import (
    list_maintenance_terminals as _list_maintenance_terminals,
)
from mfx._generated.models.list_maintenance_state_item import ListMaintenanceStateItem
from mfx._generated.models.maintenance_window_changed import MaintenanceWindowChanged
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of, states_param

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Sequence

    from mfx._generated.models.tenant_maintenance import TenantMaintenance
    from mfx._generated.models.tenant_maintenance_terminal import TenantMaintenanceTerminal
    from mfx.client import MfxClient
    from mfx.streaming import StreamMessage
    from mfx.terminals import Id

__all__ = ["WINDOW_CHANGED", "Maintenance", "WindowState", "window_event"]

#: A window as a tenant sees it: ``in_progress`` covers running, paused and verifying.
WindowState = Literal["scheduled", "in_progress", "completed", "cancelled"]

#: The message on ``events``, and the webhook event type, that says a window reached you or moved.
WINDOW_CHANGED: Final = "maintenance.window_changed"


def window_event(message: StreamMessage) -> MaintenanceWindowChanged | None:
    """A message from ``events`` as the window change it is, or None for any other.

    .. code-block:: python

        async for message in stream:
            change = window_event(message)
            if change is not None and change.change == "started":
                pause_orders(until=change.ends_at)

    It is sent when a window is announced to you, starts, has its expected end or its message
    moved, ends or is cancelled; ``change`` says which, and the rest is the window as it stands
    after the change, the same fields ``GET /maintenance`` answers. On the stream every value
    arrives as text, so ``terminals`` is a count written as digits. A webhook endpoint asks for
    the same event by the type :data:`WINDOW_CHANGED`.
    """
    if getattr(message, "type", None) != WINDOW_CHANGED:
        return None
    return MaintenanceWindowChanged.from_dict(message.data)


class Maintenance:
    """The windows that reach this tenant, and its terminals in each."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def page(
        self,
        *,
        state: WindowState | Sequence[WindowState] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page[TenantMaintenance]:
        """One page of windows. Unfiltered: scheduled and in progress, soonest first.

        ``state`` is one state or a sequence of them, sent as one comma-separated value.

        ``completed`` lists the last 30 days. A scheduled window is listed once it has been
        announced to you.
        """
        wanted = states_param(state, ListMaintenanceStateItem)  # before the call: a bad one is ours
        parsed = await self._client.read(
            lambda: _list_maintenance.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=wanted,
            ),
            "GET /maintenance",
        )
        return page_of(parsed)

    async def list(
        self, *, state: WindowState | Sequence[WindowState] | None = None, limit: int | None = None
    ) -> AsyncIterator[TenantMaintenance]:
        """Every window, following the cursor."""
        cursor: str | None = None
        while True:
            page = await self.page(state=state, cursor=cursor, limit=limit)
            for window in page.items:
                yield window
            cursor = page.next_cursor
            if not cursor:
                return

    async def terminals_page(
        self, window_id: Id, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantMaintenanceTerminal]:
        """One page of your terminals in one window, each with its state and expected time back.

        A window you are not in, or another tenant's, is 404.
        """
        parsed = await self._client.read(
            lambda: _list_maintenance_terminals.asyncio_detailed(
                id=window_id if isinstance(window_id, UUID) else UUID(window_id),
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            f"GET /maintenance/{window_id}/terminals",
        )
        return page_of(parsed)

    async def terminals(
        self, window_id: Id, *, limit: int | None = None
    ) -> AsyncIterator[TenantMaintenanceTerminal]:
        """Every one of your terminals in the window, following the cursor."""
        cursor: str | None = None
        while True:
            page = await self.terminals_page(window_id, cursor=cursor, limit=limit)
            for terminal in page.items:
                yield terminal
            cursor = page.next_cursor
            if not cursor:
                return
