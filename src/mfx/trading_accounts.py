"""``client.trading_accounts`` — the tenant's trading accounts over every venue.

One trading account is one account at one venue: an MT5 account (run by one terminal, or two with
HA), and from the cTrader release a cTrader account. An MT5 account's id is its terminal's id, so an
id you already hold reads its account, and :meth:`TradingAccounts.get` also takes either HA
terminal's id. Its ``state`` is a word that holds on every venue (``CONNECTED``, ``DEGRADED``,
``REAUTH_NEEDED``, ...); :meth:`mfx.terminals.Terminals.get` has the MT5 detail. Needs
``acct:read``.

DECISION: a namespace of its own beside ``client.accounts``, which stays what it was: the balance,
positions and deals of a terminal's account. Folding the two together would give ``accounts.get``
two meanings.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from mfx._generated.api.accounts import get_trading_account as _get_trading_account
from mfx._generated.api.accounts import list_trading_accounts as _list_trading_accounts
from mfx._generated.models.list_trading_accounts_environment import (
    ListTradingAccountsEnvironment,
)
from mfx._generated.models.list_trading_accounts_state_item import ListTradingAccountsStateItem
from mfx._generated.models.list_trading_accounts_venue_item import ListTradingAccountsVenueItem
from mfx._generated.models.trading_account import TradingAccount
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of, states_param

if TYPE_CHECKING:
    from mfx.client import MfxClient

__all__ = ["AccountEnvironment", "AccountStateName", "TradingAccounts", "VenueName"]

#: The trading technologies an account can be on.
VenueName = Literal["mt5", "ctrader"]
#: Live or demo.
AccountEnvironment = Literal["live", "demo"]
#: An account's state, in words that hold on every venue.
AccountStateName = Literal[
    "PENDING",
    "CONNECTING",
    "CONNECTED",
    "DEGRADED",
    "PAUSED",
    "REAUTH_NEEDED",
    "RETIRED",
    "FAILED",
]

Id = str | UUID


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


class TradingAccounts:
    """Read the trading accounts this key's tenant holds."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def get(self, account_id: Id) -> TradingAccount:
        """One trading account, by its own id or by one of its terminals' ids.

        Another tenant's, or an id that is not an account of yours, is a 404, never a 403.
        """
        account = await self._client.read(
            lambda: _get_trading_account.asyncio_detailed(
                id=_uuid(account_id), client=self._client.generated
            ),
            f"GET /accounts/{account_id}",
        )
        return account  # type: ignore[no-any-return]

    async def page(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        venue: VenueName | Sequence[VenueName] | None = None,
        environment: AccountEnvironment | None = None,
        state: AccountStateName | Sequence[AccountStateName] | None = None,
    ) -> Page[TradingAccount]:
        """One page of this tenant's trading accounts, newest first, retired ones included.

        ``venue`` and ``state`` are one value or a sequence, each sent as one comma-separated value
        and checked here, so a misspelt one is a ``ValueError`` at the call. ``environment`` is
        ``live`` or ``demo``. Every filter narrows the list on the platform before the page is cut.
        """
        venues = states_param(venue, ListTradingAccountsVenueItem)
        states = states_param(state, ListTradingAccountsStateItem)
        environments = (
            ListTradingAccountsEnvironment(environment) if environment is not None else UNSET
        )
        parsed = await self._client.read(
            lambda: _list_trading_accounts.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
                venue=venues,
                environment=environments,
                state=states,
            ),
            "GET /accounts",
        )
        return page_of(parsed)

    async def list(
        self,
        *,
        limit: int | None = None,
        venue: VenueName | Sequence[VenueName] | None = None,
        environment: AccountEnvironment | None = None,
        state: AccountStateName | Sequence[AccountStateName] | None = None,
    ) -> AsyncIterator[TradingAccount]:
        """Every trading account, following the cursor, narrowed as :meth:`page` is."""
        cursor: str | None = None
        while True:
            page = await self.page(
                cursor=cursor, limit=limit, venue=venue, environment=environment, state=state
            )
            for account in page.items:
                yield account
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return
