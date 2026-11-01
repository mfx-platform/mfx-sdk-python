"""``client.usage`` — every limit that applies to this key and its tenant, and how much is used.

Each limit says its figure, where it comes from (the plan, the tenant's own figure, or this key's
cap), whether the platform applies it yet, and how much of it is in use where that is measured.
``key`` is the calling key's view, ``tenant`` the ceiling for all its keys together, so one runaway
integration can be told apart from a tenant at its ceiling. The remaining budget still rides every
response as ``X-MFX-Budget-Remaining`` and ``X-MFX-Budget-Source``, and is on ``client.budget``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mfx._generated.api.usage import get_usage as _get_usage
from mfx._generated.models.usage import Usage

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = ["UsageReader"]


class UsageReader:
    """One call, because there is one question: what has been used and what is left."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def get(self) -> Usage:
        """Every limit for this key and its tenant: figure, source, whether applied, and use."""
        parsed = await self._client.read(
            lambda: _get_usage.asyncio_detailed(client=self._client.generated),
            "GET /usage",
        )
        return parsed  # type: ignore[no-any-return]
