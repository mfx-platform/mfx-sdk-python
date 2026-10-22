"""``client.maintenance`` - planned maintenance on this tenant's terminals.

While a window runs, what it suspends for you is refused with 403 ``maintenance``
(:class:`~mfx.errors.MaintenanceError`, or an execution result with reason ``maintenance``) until
``ends_at``. These two reads say what is scheduled and in progress and where each of your terminals
is, and are answered under every suspension, so a caller that has just been refused can always ask
how long for. Open positions are never closed by a window.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from uuid import UUID

from mfx._generated.api.maintenance import list_maintenance as _list_maintenance
from mfx._generated.api.maintenance import (
    list_maintenance_terminals as _list_maintenance_terminals,
)
from mfx._generated.models.list_maintenance_state import ListMaintenanceState
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from mfx._generated.models.tenant_maintenance import TenantMaintenance
    from mfx._generated.models.tenant_maintenance_terminal import TenantMaintenanceTerminal
    from mfx.client import MfxClient
    from mfx.terminals import Id

__all__ = ["Maintenance", "WindowState"]

#: A window as a tenant sees it: ``in_progress`` covers running, paused and verifying.
WindowState = Literal["scheduled", "in_progress", "completed", "cancelled"]


class Maintenance:
    """The windows that reach this tenant, and its terminals in each."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def page(
        self,
        *,
        state: WindowState | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page[TenantMaintenance]:
        """One page of windows. Unfiltered: scheduled and in progress, soonest first.

        ``completed`` lists the last 30 days. A scheduled window is listed once it has been
        announced to you.
        """
        parsed = await self._client.read(
            lambda: _list_maintenance.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                state=ListMaintenanceState(state) if state is not None else UNSET,
            ),
            "GET /maintenance",
        )
        return page_of(parsed)

    async def list(
        self, *, state: WindowState | None = None, limit: int | None = None
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
