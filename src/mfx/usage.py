"""``client.usage`` — what this tenant has consumed, and what this key may still spend.

The limits are the **calling key's**, not the tenant's, so one runaway integration cannot starve a
tenant's production traffic. ``budget_source`` says whether ``budget_remaining`` is a measurement
or the key's configured allowance — a ceiling read as a reading is how a quota surprises someone.
The same distinction rides every response as ``X-MFX-Budget-Source`` and is on ``client.budget``.
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
        """Consumption per metric, this key's ceilings, and the remaining budget with its source."""
        parsed = await self._client.read(
            lambda: _get_usage.asyncio_detailed(client=self._client.generated),
            "GET /usage",
        )
        return parsed  # type: ignore[no-any-return]
