"""``client.accounts`` — what a terminal's account looks like right now.

Reads, all of them, raising the typed hierarchy. Two things are worth knowing before
using any of it:

* **Live lists are snapshots**. Positions and pending orders come back whole with their
  ``as_of``, never behind a cursor — a cursor over a set that changes while you page skips or
  repeats rows. History (deals) *is* paged, newest first, inside a from/to window.
* **Everything carries when it was observed.** The account's numerics and its slow profile facts
  are two halves with their own timestamps, and a half never observed is null rather than zero.
  A spread is never returned without ``age_s``, because a stale spread reads as a live one.
"""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

from mfx._generated.api.account import (
    get_account as _get_account,
)
from mfx._generated.api.account import (
    get_spread as _get_spread,
)
from mfx._generated.api.account import (
    list_deals as _list_deals,
)
from mfx._generated.api.account import (
    list_pending_orders as _list_pending_orders,
)
from mfx._generated.api.account import (
    list_positions as _list_positions,
)
from mfx._generated.models.account import Account
from mfx._generated.models.deal import Deal
from mfx._generated.models.pending_order_list import PendingOrderList
from mfx._generated.models.position_list import PositionList
from mfx._generated.models.spread_list import SpreadList
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of
from mfx.terminals import Id, _uuid

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = ["Accounts"]


class Accounts:
    """Balance, positions, orders, history and spreads for one tenant's terminals."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def account(self, terminal_id: Id) -> Account:
        """Balance, equity and margin, plus the slow profile facts. Each half with its own ``ts``;
        a half never observed is null, not zero."""
        parsed = await self._client.read(
            lambda: _get_account.asyncio_detailed(
                id=_uuid(terminal_id), client=self._client.generated
            ),
            f"GET /terminals/{terminal_id}/account",
        )
        return parsed  # type: ignore[no-any-return]

    async def positions(self, terminal_id: Id) -> PositionList:
        """Every open position, as one snapshot with its ``as_of``."""
        parsed = await self._client.read(
            lambda: _list_positions.asyncio_detailed(
                id=_uuid(terminal_id), client=self._client.generated
            ),
            f"GET /terminals/{terminal_id}/positions",
        )
        return parsed  # type: ignore[no-any-return]

    async def pending_orders(self, terminal_id: Id) -> PendingOrderList:
        """Every pending order, as one snapshot with its ``as_of``."""
        parsed = await self._client.read(
            lambda: _list_pending_orders.asyncio_detailed(
                id=_uuid(terminal_id), client=self._client.generated
            ),
            f"GET /terminals/{terminal_id}/orders/pending",
        )
        return parsed  # type: ignore[no-any-return]

    async def deals(
        self,
        terminal_id: Id,
        *,
        from_: dt.datetime,
        to: dt.datetime,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page[Deal]:
        """Closed deals, newest first, inside a window.

        The window is required, by the API and so by this: an unbounded history request over a
        partitioned table is the query that takes a database down. Paged, because history does not
        change under you the way a live list does.
        """
        parsed = await self._client.read(
            lambda: _list_deals.asyncio_detailed(
                id=_uuid(terminal_id),
                client=self._client.generated,
                from_=from_,
                to=to,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            f"GET /terminals/{terminal_id}/history/deals",
        )
        return page_of(parsed)

    async def spread(self, terminal_id: Id) -> SpreadList:
        """The spread this terminal's own account is quoted, with each reading's age.

        A pool cannot answer this: the spread a user trades against is the one their broker gives
        *their* account, so it is read from their terminal.
        """
        parsed = await self._client.read(
            lambda: _get_spread.asyncio_detailed(
                id=_uuid(terminal_id), client=self._client.generated
            ),
            f"GET /terminals/{terminal_id}/spread",
        )
        return parsed  # type: ignore[no-any-return]
