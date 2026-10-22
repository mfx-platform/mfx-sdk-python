"""``client.farms`` - the farms this tenant's plan places terminals on.

Each says its operating system, region, the usages it offers, its refresh rate and its instrument
limits. ``client.terminals.create`` takes a ``farm_id`` from here, or leaves it out and the
platform chooses.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from mfx._generated.api.farms import get_farm as _get_farm
from mfx._generated.api.farms import list_farms as _list_farms
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from mfx._generated.models.tenant_farm import TenantFarm
    from mfx.client import MfxClient
    from mfx.terminals import Id

__all__ = ["Farms"]


class Farms:
    """The farms the plan allows. Any other farm, another tenant's included, is 404."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def page(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantFarm]:
        """One page of farms."""
        parsed = await self._client.read(
            lambda: _list_farms.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            "GET /farms",
        )
        return page_of(parsed)

    async def list(self, *, limit: int | None = None) -> AsyncIterator[TenantFarm]:
        """Every farm, following the cursor."""
        cursor: str | None = None
        while True:
            page = await self.page(cursor=cursor, limit=limit)
            for farm in page.items:
                yield farm
            cursor = page.next_cursor
            if not cursor:
                return

    async def get(self, farm_id: Id) -> TenantFarm:
        """One farm the plan allows."""
        farm = await self._client.read(
            lambda: _get_farm.asyncio_detailed(
                id=farm_id if isinstance(farm_id, UUID) else UUID(farm_id),
                client=self._client.generated,
            ),
            f"GET /farms/{farm_id}",
        )
        return farm  # type: ignore[no-any-return]
