"""``client.trading_accounts`` — the tenant's trading accounts over every venue.

One trading account is one account at one venue: an MT5 account (run by one terminal, or two with
HA), and a cTrader account. An MT5 account takes its first terminal's id, and
:meth:`TradingAccounts.get` also takes any of its terminals' ids. Its ``state`` is a word that
holds on every venue (``CONNECTED``, ``DEGRADED``, ``REAUTH_NEEDED``, ...);
:meth:`mfx.terminals.Terminals.get` has the MT5 detail. Reads need ``acct:read``.

The same object trades an account and reads it on any venue: the nine commands of
:class:`mfx.execution.Execution`, keyed on the account instead of a terminal (``exec:write``), and
the account's funds, positions, pending orders, deals and symbols. The platform hands each to the
account's lead runner. Commands follow the execution rules: an ``idempotency_key`` on every one,
an :class:`~mfx.results.ExecutionResult` returned and never raised, nothing retried by the SDK.

A cTrader account is connected through a grant: :meth:`TradingAccounts.start_ctrader_grant` answers
the cTrader consent link to send the trader to; after consent, :meth:`TradingAccounts.ctrader_grant`
lists the accounts they shared and :meth:`TradingAccounts.connect_ctrader_accounts` makes the
chosen ones trading accounts of yours. Starting, connecting and revoking need ``term:write``.

DECISION: a namespace of its own beside ``client.accounts``, which stays what it was: the balance,
positions and deals of a terminal's account. Folding the two together would give ``accounts.get``
two meanings.
"""

from __future__ import annotations

import builtins
import datetime as dt
from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from mfx._generated.api.accounts import connect_ctrader_accounts as _connect_ctrader_accounts
from mfx._generated.api.accounts import get_ctrader_grant as _get_ctrader_grant
from mfx._generated.api.accounts import get_trading_account as _get_trading_account
from mfx._generated.api.accounts import get_trading_account_funds as _get_funds
from mfx._generated.api.accounts import list_trading_account_deals as _list_deals
from mfx._generated.api.accounts import (
    list_trading_account_pending_orders as _list_pending_orders,
)
from mfx._generated.api.accounts import list_trading_account_positions as _list_positions
from mfx._generated.api.accounts import list_trading_account_symbols as _list_symbols
from mfx._generated.api.accounts import list_trading_accounts as _list_trading_accounts
from mfx._generated.api.accounts import revoke_ctrader_grant as _revoke_ctrader_grant
from mfx._generated.api.accounts import start_ctrader_grant as _start_ctrader_grant
from mfx._generated.models.account import Account
from mfx._generated.models.ctrader_accounts_choice import CtraderAccountsChoice
from mfx._generated.models.ctrader_grant import CtraderGrant
from mfx._generated.models.ctrader_grant_create import CtraderGrantCreate
from mfx._generated.models.ctrader_grant_create_environment import (
    CtraderGrantCreateEnvironment,
)
from mfx._generated.models.ctrader_grant_create_scope import CtraderGrantCreateScope
from mfx._generated.models.ctrader_grant_started import CtraderGrantStarted
from mfx._generated.models.deal import Deal
from mfx._generated.models.list_trading_accounts_environment import (
    ListTradingAccountsEnvironment,
)
from mfx._generated.models.list_trading_accounts_state_item import ListTradingAccountsStateItem
from mfx._generated.models.list_trading_accounts_venue_item import ListTradingAccountsVenueItem
from mfx._generated.models.pending_order_list import PendingOrderList
from mfx._generated.models.position_list import PositionList
from mfx._generated.models.trading_account import TradingAccount
from mfx._generated.models.trading_symbol_list import TradingSymbolList
from mfx._generated.types import UNSET
from mfx.execution import _ACCOUNT_ROUTES, _KEEP, Amount, Execution, OrderType, Side, _Keep
from mfx.pages import Page, page_of, states_param

if TYPE_CHECKING:
    from mfx.client import MfxClient
    from mfx.results import ExecutionResult

__all__ = [
    "AccountEnvironment",
    "AccountStateName",
    "GrantScope",
    "TradingAccounts",
    "VenueName",
]

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

#: What a cTrader grant lets MFX Hub do: ``accounts`` reads the accounts only, ``trading`` reads
#: and trades them.
GrantScope = Literal["accounts", "trading"]

Id = str | UUID


def _uuid(value: Id) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


class TradingAccounts:
    """Read the trading accounts this key's tenant holds."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client
        self._orders = Execution(client, routes=_ACCOUNT_ROUTES)

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

    # ------------------------------------------------------------------------------- reads

    async def funds(self, account_id: Id) -> Account:
        """Balance, equity, margin and profile, answered by the account's lead runner.

        On cTrader the equity is computed by the platform (the venue sends none) and ``stale`` says
        when it could not be computed recently. Another tenant's account is a 404.
        """
        parsed = await self._client.read(
            lambda: _get_funds.asyncio_detailed(
                id=_uuid(account_id), client=self._client.generated
            ),
            f"GET /accounts/{account_id}/account",
        )
        return parsed  # type: ignore[no-any-return]

    async def positions(self, account_id: Id) -> PositionList:
        """Every open position, as one snapshot with its ``as_of``. On cTrader ``volume`` is in lots
        and ``ticket`` is the venue's position id."""
        parsed = await self._client.read(
            lambda: _list_positions.asyncio_detailed(
                id=_uuid(account_id), client=self._client.generated
            ),
            f"GET /accounts/{account_id}/positions",
        )
        return parsed  # type: ignore[no-any-return]

    async def pending_orders(self, account_id: Id) -> PendingOrderList:
        """Every pending order, as one snapshot with its ``as_of``."""
        parsed = await self._client.read(
            lambda: _list_pending_orders.asyncio_detailed(
                id=_uuid(account_id), client=self._client.generated
            ),
            f"GET /accounts/{account_id}/orders/pending",
        )
        return parsed  # type: ignore[no-any-return]

    async def deals(  # noqa: PLR0913 - the window, the position and the page
        self,
        account_id: Id,
        *,
        from_: dt.datetime,
        to: dt.datetime,
        position: int | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page[Deal]:
        """Deals newest first inside a window of at most 31 days, optionally of one position.

        Read from the venue when asked: a venue that does not answer in time is an
        ``UpstreamError``, and a window wider than 31 days a ``ValidationError``. On cTrader every
        time is UTC and ``magic`` is the origin marker the order was placed with.
        """
        parsed = await self._client.read(
            lambda: _list_deals.asyncio_detailed(
                id=_uuid(account_id),
                client=self._client.generated,
                from_=from_,
                to=to,
                position=position if position is not None else UNSET,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            f"GET /accounts/{account_id}/history/deals",
        )
        return page_of(parsed)

    async def symbols(self, account_id: Id) -> TradingSymbolList:
        """The symbols a cTrader account can trade, with their volume rules in lots and leverage.

        A volume a command sends must be a whole ``volume_step`` between ``volume_min`` and
        ``volume_max``. An MT5 account is refused (its symbols are its broker's catalogue), and a
        cTrader account that is not connected now is an ``UpstreamError``.
        """
        parsed = await self._client.read(
            lambda: _list_symbols.asyncio_detailed(
                id=_uuid(account_id), client=self._client.generated
            ),
            f"GET /accounts/{account_id}/symbols",
        )
        return parsed  # type: ignore[no-any-return]

    # ---------------------------------------------------------------------------- commands
    # The same bodies and rules as client.execution, sent to /accounts/{id}/...; each returns
    # an ExecutionResult and never raises. Read the outcome with client.execution.wait_for.

    async def place_order(  # noqa: PLR0913 - an order's every field
        self,
        account_id: Id,
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
        """Place a market or pending order on the account; as
        :meth:`mfx.execution.Execution.place_order`.

        ``volume`` is in lots on every venue, and on cTrader must be a whole step of the symbol
        (:meth:`symbols`). On cTrader ``magic`` stays on the order as its label and comes back on
        the deals, and a market order's stop loss and take profit are set just after the fill
        (``protection_not_set`` says when that failed).
        """
        return await self._orders.place_order(
            account_id,
            symbol=symbol,
            side=side,
            volume=volume,
            idempotency_key=idempotency_key,
            order_type=order_type,
            price=price,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            deviation_points=deviation_points,
            expires_at=expires_at,
            magic=magic,
            comment=comment,
        )

    async def cancel_order(
        self, account_id: Id, ticket: int, *, idempotency_key: str
    ) -> ExecutionResult:
        """Cancel a pending order; as :meth:`mfx.execution.Execution.cancel_order`."""
        return await self._orders.cancel_order(account_id, ticket, idempotency_key=idempotency_key)

    async def modify_order(  # noqa: PLR0913 - every field an amend can change
        self,
        account_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        price: Amount | None = None,
        stop_limit_price: Amount | None = None,
        sl: Amount | None = None,
        tp: Amount | None = None,
        expires_at: dt.datetime | None | _Keep = _KEEP,
    ) -> ExecutionResult:
        """Amend a pending order; as :meth:`mfx.execution.Execution.modify_order`."""
        return await self._orders.modify_order(
            account_id,
            ticket,
            idempotency_key=idempotency_key,
            price=price,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            expires_at=expires_at,
        )

    async def modify_position(
        self,
        account_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        sl: Amount | None = None,
        tp: Amount | None = None,
    ) -> ExecutionResult:
        """Move a position's stop loss, take profit or both; as
        :meth:`mfx.execution.Execution.modify_position`."""
        return await self._orders.modify_position(
            account_id, ticket, idempotency_key=idempotency_key, sl=sl, tp=tp
        )

    async def close_position(
        self,
        account_id: Id,
        ticket: int,
        *,
        idempotency_key: str,
        deviation_points: int | None = None,
    ) -> ExecutionResult:
        """Close a position in full; as :meth:`mfx.execution.Execution.close_position`."""
        return await self._orders.close_position(
            account_id, ticket, idempotency_key=idempotency_key, deviation_points=deviation_points
        )

    async def close_position_by(
        self, account_id: Id, ticket: int, by_ticket: int, *, idempotency_key: str
    ) -> ExecutionResult:
        """Close a position against an opposite one; as
        :meth:`mfx.execution.Execution.close_position_by`.

        cTrader has no close-by: it is done as two closes, the result says ``close_by_emulated``
        and ``deals`` holds both.
        """
        return await self._orders.close_position_by(
            account_id, ticket, by_ticket, idempotency_key=idempotency_key
        )

    async def close_position_partial(
        self,
        account_id: Id,
        ticket: int,
        *,
        volume: Amount,
        idempotency_key: str,
        deviation_points: int | None = None,
    ) -> ExecutionResult:
        """Close part of a position, in lots; as
        :meth:`mfx.execution.Execution.close_position_partial`."""
        return await self._orders.close_position_partial(
            account_id,
            ticket,
            volume=volume,
            idempotency_key=idempotency_key,
            deviation_points=deviation_points,
        )

    async def set_trailing_stop(
        self, account_id: Id, ticket: int, *, distance: Amount, idempotency_key: str
    ) -> ExecutionResult:
        """Trail a position's stop loss; as :meth:`mfx.execution.Execution.set_trailing_stop`.

        A venue that has no trailing stop yet refuses it, and the refusal comes back as the result.
        """
        return await self._orders.set_trailing_stop(
            account_id, ticket, distance=distance, idempotency_key=idempotency_key
        )

    async def clear_trailing_stop(
        self, account_id: Id, ticket: int, *, idempotency_key: str
    ) -> ExecutionResult:
        """Remove a position's trailing stop; as
        :meth:`mfx.execution.Execution.clear_trailing_stop`."""
        return await self._orders.clear_trailing_stop(
            account_id, ticket, idempotency_key=idempotency_key
        )

    # ------------------------------------------------------------------------ cTrader grants

    async def start_ctrader_grant(
        self,
        *,
        environment: AccountEnvironment,
        scope: GrantScope,
        return_url: str,
        idempotency_key: str,
        tenant_state: str | None = None,
    ) -> CtraderGrantStarted:
        """Start connecting a trader's cTrader accounts; answers the consent link to send them to.

        The trader signs in at cTrader with their cTrader ID (MFX Hub never sees the password)
        and chooses the accounts to share, then comes back to ``return_url`` (https) with
        ``grant_id``, ``result`` and your ``tenant_state``. The link lives 15 minutes. One grant
        covers ``live`` or ``demo`` accounts. A plan without cTrader is a ``ForbiddenError``.
        """
        body = CtraderGrantCreate(
            environment=CtraderGrantCreateEnvironment(environment),
            scope=CtraderGrantCreateScope(scope),
            return_url=return_url,
            tenant_state=tenant_state if tenant_state is not None else UNSET,
        )
        started = await self._client.write(
            lambda: _start_ctrader_grant.asyncio_detailed(
                client=self._client.generated, body=body, idempotency_key=idempotency_key
            ),
            "POST /accounts/ctrader/grants",
        )
        return started  # type: ignore[no-any-return]

    async def ctrader_grant(self, grant_id: Id) -> CtraderGrant:
        """One grant: its state (PENDING, ACTIVE, REVOKED or EXPIRED) and, once ACTIVE, the cTrader
        accounts the trader shared."""
        grant = await self._client.read(
            lambda: _get_ctrader_grant.asyncio_detailed(
                id=_uuid(grant_id), client=self._client.generated
            ),
            f"GET /accounts/ctrader/grants/{grant_id}",
        )
        return grant  # type: ignore[no-any-return]

    async def connect_ctrader_accounts(
        self,
        grant_id: Id,
        ctid_trader_account_ids: Sequence[str | int],
        *,
        idempotency_key: str,
    ) -> builtins.list[TradingAccount]:
        """Make some of an ACTIVE grant's accounts trading accounts of yours, by cTrader's ids.

        Each starts PENDING and is CONNECTED once authorised at cTrader (an ``account.connected``
        event says so). Choosing one already connected returns it unchanged. 1 to 50 ids.
        """
        ids = [str(i) for i in ctid_trader_account_ids]
        if not ids:
            raise ValueError("connect_ctrader_accounts needs at least one account id")
        body = CtraderAccountsChoice(ctid_trader_account_ids=ids)
        connected = await self._client.write(
            lambda: _connect_ctrader_accounts.asyncio_detailed(
                id=_uuid(grant_id),
                client=self._client.generated,
                body=body,
                idempotency_key=idempotency_key,
            ),
            f"POST /accounts/ctrader/grants/{grant_id}/accounts",
        )
        return list(connected.items)

    async def revoke_ctrader_grant(self, grant_id: Id, *, idempotency_key: str) -> CtraderGrant:
        """Revoke a grant: its accounts move to REAUTH_NEEDED (an ``account.reauth_needed`` event
        each) and a new grant reconnects them. Revoking a revoked grant answers it unchanged."""
        grant = await self._client.write(
            lambda: _revoke_ctrader_grant.asyncio_detailed(
                id=_uuid(grant_id), client=self._client.generated, idempotency_key=idempotency_key
            ),
            f"DELETE /accounts/ctrader/grants/{grant_id}",
        )
        return grant  # type: ignore[no-any-return]
