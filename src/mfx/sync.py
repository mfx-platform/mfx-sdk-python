"""``SyncMfxClient`` — the async client for scripts that are not async.

For a migration, a cron job, a notebook, a one-off reconciliation: code with no event loop and no
reason to grow one. Everything else uses :class:`~mfx.client.MfxClient` directly.

Three limits, stated here because each one is a decision rather than an omission:

* **REST only. There is no sync stream** (a deliberate choice). A WebSocket that
  reconnects, resumes and counts gaps is a long-lived concurrent thing; wrapping it in blocking
  calls produces something that looks like an iterator and drops ticks whenever the caller is
  between them. A script that needs live prices needs an event loop, and should say so.

* **One loop, on one background thread, for the client's lifetime.** Not ``anyio.run`` per call:
  that makes a fresh event loop each time, and the connection pool opened under the first one is
  dead by the second — the failure arrives as ``Event loop is closed`` on the *second* call, which
  is a miserable thing to debug in a cron job. One long-lived loop keeps the pool, the retry
  policy and the budget counter intact, and calls are sequential by construction.

* **It must not be called from inside a running event loop.** It would block that loop while
  waiting, stalling everything else on it, so it raises instead and says which client to use.
  This is the mistake this facade invites most.

The surface deliberately mirrors the async one method for method, so moving a script to async is
deleting ``Sync`` and adding ``await`` rather than relearning the API.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import functools
import threading
from collections.abc import Awaitable, Callable, Iterator, Mapping, Sequence
from types import TracebackType
from typing import TYPE_CHECKING, Any, Self

from mfx.client import MfxClient
from mfx.pages import Page

if TYPE_CHECKING:
    from mfx._generated.models.account import Account
    from mfx._generated.models.billing_forecast import BillingForecast
    from mfx._generated.models.billing_invoice import BillingInvoice
    from mfx._generated.models.billing_invoice_detail import BillingInvoiceDetail
    from mfx._generated.models.billing_invoice_page import BillingInvoicePage
    from mfx._generated.models.billing_price_list import BillingPriceList
    from mfx._generated.models.billing_profile import BillingProfile
    from mfx._generated.models.billing_summary import BillingSummary
    from mfx._generated.models.broker_catalogue import BrokerCatalogue
    from mfx._generated.models.candle_list import CandleList
    from mfx._generated.models.copy_close import CopyClose
    from mfx._generated.models.copy_close_page_stats import CopyClosePageStats
    from mfx._generated.models.copy_follower import CopyFollower
    from mfx._generated.models.copy_follower_page_stats import CopyFollowerPageStats
    from mfx._generated.models.copy_group import CopyGroup
    from mfx._generated.models.copy_group_close_result import CopyGroupCloseResult
    from mfx._generated.models.copy_group_members_result import CopyGroupMembersResult
    from mfx._generated.models.copy_group_page_stats import CopyGroupPageStats
    from mfx._generated.models.copy_group_rollover_result import CopyGroupRolloverResult
    from mfx._generated.models.copy_leader import CopyLeader
    from mfx._generated.models.copy_leader_page_stats import CopyLeaderPageStats
    from mfx._generated.models.copy_log_entry import CopyLogEntry
    from mfx._generated.models.copy_log_page_stats import CopyLogPageStats
    from mfx._generated.models.copy_preview import CopyPreview
    from mfx._generated.models.copy_signal_accepted import CopySignalAccepted
    from mfx._generated.models.copy_signal_entry import CopySignalEntry
    from mfx._generated.models.copy_signal_page_stats import CopySignalPageStats
    from mfx._generated.models.copy_stopout import CopyStopout
    from mfx._generated.models.copy_tenant_stopout_page_stats import CopyTenantStopoutPageStats
    from mfx._generated.models.credential_accepted import CredentialAccepted
    from mfx._generated.models.ctrader_grant import CtraderGrant
    from mfx._generated.models.ctrader_grant_started import CtraderGrantStarted
    from mfx._generated.models.deal import Deal
    from mfx._generated.models.own_contacts import OwnContacts
    from mfx._generated.models.pending_order_list import PendingOrderList
    from mfx._generated.models.position_list import PositionList
    from mfx._generated.models.spread_list import SpreadList
    from mfx._generated.models.symbol import Symbol
    from mfx._generated.models.symbol_quote import SymbolQuote
    from mfx._generated.models.tenant_broker import TenantBroker
    from mfx._generated.models.tenant_broker_server import TenantBrokerServer
    from mfx._generated.models.tenant_service_agreement import TenantServiceAgreement
    from mfx._generated.models.tenant_terminal import TenantTerminal
    from mfx._generated.models.terminal_journal import TerminalJournal
    from mfx._generated.models.tick_list import TickList
    from mfx._generated.models.trading_account import TradingAccount
    from mfx._generated.models.trading_symbol_list import TradingSymbolList
    from mfx._generated.models.usage import Usage
    from mfx.billing import Billing
    from mfx.copy_trading import Copy, CopyPage
    from mfx.expert_advisors import Tenant
    from mfx.results import ExecutionResult
    from mfx.secrets import Secret
    from mfx.terminals import CredentialType, Id, Redundancy, TerminalStateName
    from mfx.trading_accounts import AccountEnvironment, AccountStateName, VenueName

__all__ = ["SyncMfxClient"]

#: The worker loop has nothing left to do once `aclose` has returned, so the join is a formality.
#: It is bounded anyway: a script exiting must not hang on a thread that will not stop.
_SHUTDOWN_TIMEOUT_S = 5.0


async def _awaited[T](call: Callable[[], Awaitable[T]]) -> T:
    """Turn the deferred call into a coroutine *on the worker loop*.

    Built there rather than by the caller because a coroutine object created on one thread and
    awaited on another is a bug waiting for the first httpx timeout to expose it.
    """
    return await call()


class SyncMfxClient:
    """The MFX client for code with no event loop. Use it as a context manager::

    with SyncMfxClient(base_url, key_id, private_key) as mfx:
        terminal = mfx.get_terminal(terminal_id)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Takes exactly what :class:`~mfx.client.MfxClient` takes."""
        self._client = MfxClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, name="mfx-sync", daemon=True)
        self._thread.start()
        self._closed = False
        #: Copy Trading, blocking: the same methods as ``MfxClient.copy``.
        self.copy = SyncCopy(self)
        #: Billing reads, blocking: the same methods as ``MfxClient.billing``.
        self.billing = SyncBilling(self)
        #: What the tenant reads about itself, blocking: the same methods as ``MfxClient.tenant``.
        self.tenant = SyncTenant(self)

    # ---------------------------------------------------------------- the loop, and the one rule

    def _run[T](self, call: Callable[[], Awaitable[T]]) -> T:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            raise RuntimeError(
                "SyncMfxClient cannot be called from inside a running event loop: waiting for it "
                "would block that loop and everything else on it. Use MfxClient and await the "
                "same method - the surfaces match."
            )
        if self._closed:
            raise RuntimeError("this SyncMfxClient is closed")
        return asyncio.run_coroutine_threadsafe(_awaited(call), self._loop).result()

    # ---------------------------------------------------------------------------- terminals

    def create_terminal(
        self,
        *,
        broker_id: Id,
        server_id: Id,
        idempotency_key: str,
        farm_id: Id | None = None,
        streaming: bool = False,
        execution: bool = False,
        instruments: list[str] | None = None,
        labels: dict[str, str] | None = None,
        redundancy: Redundancy = "none",
    ) -> TenantTerminal:
        """Blocking form of :meth:`mfx.terminals.Terminals.create`."""
        return self._run(
            lambda: self._client.terminals.create(
                farm_id=farm_id,
                broker_id=broker_id,
                server_id=server_id,
                idempotency_key=idempotency_key,
                streaming=streaming,
                execution=execution,
                instruments=instruments,
                labels=labels,
                redundancy=redundancy,
            )
        )

    def get_terminal(self, terminal_id: Id) -> TenantTerminal:
        """Blocking form of :meth:`mfx.terminals.Terminals.get`."""
        return self._run(lambda: self._client.terminals.get(terminal_id))

    def terminals(
        self,
        *,
        limit: int | None = None,
        label: Mapping[str, str] | None = None,
        state: TerminalStateName | Sequence[TerminalStateName] | None = None,
    ) -> Iterator[TenantTerminal]:
        """Every terminal, following the cursor — as an ordinary iterator.

        Each page is one call; the walk is not read ahead, so a script that stops early has not
        paid for the rest. ``label`` and ``state`` narrow the list as
        :meth:`mfx.terminals.Terminals.page` describes.
        """
        return self._pages(
            lambda cursor: self._client.terminals.page(
                cursor=cursor, limit=limit, label=label, state=state
            )
        )

    def get_trading_account(self, account_id: Id) -> TradingAccount:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.get`."""
        return self._run(lambda: self._client.trading_accounts.get(account_id))

    def trading_accounts(
        self,
        *,
        limit: int | None = None,
        venue: VenueName | Sequence[VenueName] | None = None,
        environment: AccountEnvironment | None = None,
        state: AccountStateName | Sequence[AccountStateName] | None = None,
    ) -> Iterator[TradingAccount]:
        """Every trading account, following the cursor, as an ordinary iterator; narrowed as
        :meth:`mfx.trading_accounts.TradingAccounts.page` describes."""
        return self._pages(
            lambda cursor: self._client.trading_accounts.page(
                cursor=cursor, limit=limit, venue=venue, environment=environment, state=state
            )
        )

    # ------------------------------------------------------------- trading accounts, by account
    # Every venue's account, read and traded by the account's own id. The names say "account"
    # where the terminal-keyed method above already has the short one (`positions`, `place_order`).

    def trading_account_funds(self, account_id: Id) -> Account:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.funds`."""
        return self._run(lambda: self._client.trading_accounts.funds(account_id))

    def trading_account_positions(self, account_id: Id) -> PositionList:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.positions`."""
        return self._run(lambda: self._client.trading_accounts.positions(account_id))

    def trading_account_pending_orders(self, account_id: Id) -> PendingOrderList:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.pending_orders`."""
        return self._run(lambda: self._client.trading_accounts.pending_orders(account_id))

    def trading_account_deals(
        self,
        account_id: Id,
        *,
        from_: dt.datetime,
        to: dt.datetime,
        position: int | None = None,
    ) -> Iterator[Deal]:
        """Every deal in the window, following the cursor.

        Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.deals`.
        """
        return self._pages(
            lambda cursor: self._client.trading_accounts.deals(
                account_id, from_=from_, to=to, position=position, cursor=cursor
            )
        )

    def trading_account_symbols(self, account_id: Id) -> TradingSymbolList:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.symbols`."""
        return self._run(lambda: self._client.trading_accounts.symbols(account_id))

    def place_account_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Never raises for a refused or failed order, as :meth:`place_order`; see
        :meth:`mfx.trading_accounts.TradingAccounts.place_order`."""
        return self._run(lambda: self._client.trading_accounts.place_order(*args, **kwargs))

    def cancel_account_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.cancel_order`."""
        return self._run(lambda: self._client.trading_accounts.cancel_order(*args, **kwargs))

    def modify_account_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.modify_order`."""
        return self._run(lambda: self._client.trading_accounts.modify_order(*args, **kwargs))

    def modify_account_position(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.modify_position`."""
        return self._run(lambda: self._client.trading_accounts.modify_position(*args, **kwargs))

    def close_account_position(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.close_position`."""
        return self._run(lambda: self._client.trading_accounts.close_position(*args, **kwargs))

    def close_account_position_by(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.close_position_by`."""
        return self._run(lambda: self._client.trading_accounts.close_position_by(*args, **kwargs))

    def close_account_position_partial(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.close_position_partial`."""
        return self._run(
            lambda: self._client.trading_accounts.close_position_partial(*args, **kwargs)
        )

    def set_account_trailing_stop(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.set_trailing_stop`."""
        return self._run(lambda: self._client.trading_accounts.set_trailing_stop(*args, **kwargs))

    def clear_account_trailing_stop(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.clear_trailing_stop`."""
        return self._run(lambda: self._client.trading_accounts.clear_trailing_stop(*args, **kwargs))

    def wait_for(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.wait_for`: poll a command until it is
        final. A non-final result is never a reason to send again."""
        return self._run(lambda: self._client.execution.wait_for(*args, **kwargs))

    # ---------------------------------------------------------------------- cTrader grants

    def start_ctrader_grant(self, **kwargs: Any) -> CtraderGrantStarted:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.start_ctrader_grant`."""
        return self._run(lambda: self._client.trading_accounts.start_ctrader_grant(**kwargs))

    def ctrader_grant(self, grant_id: Id) -> CtraderGrant:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.ctrader_grant`."""
        return self._run(lambda: self._client.trading_accounts.ctrader_grant(grant_id))

    def connect_ctrader_accounts(
        self, grant_id: Id, ctid_trader_account_ids: Sequence[str | int], *, idempotency_key: str
    ) -> list[TradingAccount]:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.connect_ctrader_accounts`.

        1 to 50 ids; none is a ``ValueError``.
        """
        return self._run(
            lambda: self._client.trading_accounts.connect_ctrader_accounts(
                grant_id, ctid_trader_account_ids, idempotency_key=idempotency_key
            )
        )

    def revoke_ctrader_grant(self, grant_id: Id, *, idempotency_key: str) -> CtraderGrant:
        """Blocking form of :meth:`mfx.trading_accounts.TradingAccounts.revoke_ctrader_grant`."""
        return self._run(
            lambda: self._client.trading_accounts.revoke_ctrader_grant(
                grant_id, idempotency_key=idempotency_key
            )
        )

    def terminal_journal(self, terminal_id: Id, *, lines: int | None = None) -> TerminalJournal:
        """Blocking form of :meth:`mfx.terminals.Terminals.journal`."""
        return self._run(lambda: self._client.terminals.journal(terminal_id, lines=lines))

    def submit_credentials(
        self,
        terminal_id: Id,
        *,
        login: int,
        password: Secret | str,
        server: str,
        idempotency_key: str,
        cred_type: CredentialType = "master",
    ) -> CredentialAccepted:
        """Blocking form of :meth:`mfx.terminals.Terminals.submit_credentials`."""
        return self._run(
            lambda: self._client.terminals.submit_credentials(
                terminal_id,
                login=login,
                password=password,
                server=server,
                idempotency_key=idempotency_key,
                cred_type=cred_type,
            )
        )

    def drain_terminal(
        self,
        terminal_id: Id,
        *,
        idempotency_key: str,
        reason: str | None = None,
        confirm_open_positions: bool = False,
    ) -> TenantTerminal:
        """Blocking form of :meth:`mfx.terminals.Terminals.drain`."""
        return self._run(
            lambda: self._client.terminals.drain(
                terminal_id,
                idempotency_key=idempotency_key,
                reason=reason,
                confirm_open_positions=confirm_open_positions,
            )
        )

    def resume_terminal(self, terminal_id: Id, *, idempotency_key: str) -> TenantTerminal:
        """Blocking form of :meth:`mfx.terminals.Terminals.resume`."""
        return self._run(
            lambda: self._client.terminals.resume(terminal_id, idempotency_key=idempotency_key)
        )

    def retire_terminal(self, terminal_id: Id, *, idempotency_key: str) -> TenantTerminal:
        """Blocking form of :meth:`mfx.terminals.Terminals.retire`."""
        return self._run(
            lambda: self._client.terminals.retire(terminal_id, idempotency_key=idempotency_key)
        )

    # ---------------------------------------------------------------------------- catalogue

    def brokers(self) -> Iterator[TenantBroker]:
        """Every broker, following the cursor.

        Blocking form of :meth:`mfx.catalog.Catalog.brokers`.
        """
        return self._pages(lambda cursor: self._client.catalog.brokers(cursor=cursor))

    def servers(self, broker_id: Id) -> Iterator[TenantBrokerServer]:
        """Every server of a broker, following the cursor.

        Blocking form of :meth:`mfx.catalog.Catalog.servers`.
        """
        return self._pages(lambda cursor: self._client.catalog.servers(broker_id, cursor=cursor))

    def catalogues(self, broker_id: Id) -> list[BrokerCatalogue]:
        """Blocking form of :meth:`mfx.catalog.Catalog.catalogues`."""
        return self._run(lambda: self._client.catalog.catalogues(broker_id))

    def symbols(self, broker_id: Id) -> Iterator[Symbol]:
        """Every symbol of a broker, following the cursor.

        Blocking form of :meth:`mfx.catalog.Catalog.symbols`.
        """
        return self._pages(lambda cursor: self._client.catalog.symbols(broker_id, cursor=cursor))

    def symbol(self, broker_id: Id, symbol: str) -> Symbol:
        """Blocking form of :meth:`mfx.catalog.Catalog.symbol`."""
        return self._run(lambda: self._client.catalog.symbol(broker_id, symbol))

    def quote(self, broker_id: Id, symbol: str) -> SymbolQuote:
        """Blocking form of :meth:`mfx.catalog.Catalog.quote`."""
        return self._run(lambda: self._client.catalog.quote(broker_id, symbol))

    # ----------------------------------------------------------------------------- accounts

    def account(self, terminal_id: Id) -> Account:
        """Blocking form of :meth:`mfx.accounts.Accounts.account`."""
        return self._run(lambda: self._client.accounts.account(terminal_id))

    def positions(self, terminal_id: Id) -> PositionList:
        """Blocking form of :meth:`mfx.accounts.Accounts.positions`."""
        return self._run(lambda: self._client.accounts.positions(terminal_id))

    def pending_orders(self, terminal_id: Id) -> PendingOrderList:
        """Blocking form of :meth:`mfx.accounts.Accounts.pending_orders`."""
        return self._run(lambda: self._client.accounts.pending_orders(terminal_id))

    def deals(self, terminal_id: Id, *, from_: dt.datetime, to: dt.datetime) -> Iterator[Deal]:
        """Every deal in the window, following the cursor.

        Blocking form of :meth:`mfx.accounts.Accounts.deals`.
        """
        return self._pages(
            lambda cursor: self._client.accounts.deals(
                terminal_id, from_=from_, to=to, cursor=cursor
            )
        )

    def spread(self, terminal_id: Id) -> SpreadList:
        """Blocking form of :meth:`mfx.accounts.Accounts.spread`."""
        return self._run(lambda: self._client.accounts.spread(terminal_id))

    def usage(self) -> Usage:
        """Blocking form of :meth:`mfx.usage.UsageReader.get`."""
        return self._run(lambda: self._client.usage.get())

    # ---------------------------------------------------------------------------- execution

    def candles(self, *args: Any, **kwargs: Any) -> CandleList:
        """A symbol's bars for a window; see :meth:`mfx.md.MarketData.candles`."""
        return self._run(lambda: self._client.md.candles(*args, **kwargs))

    def ticks(self, *args: Any, **kwargs: Any) -> TickList:
        """One read of tick history; see :meth:`mfx.md.MarketData.ticks`."""
        return self._run(lambda: self._client.md.ticks(*args, **kwargs))

    def place_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Never raises for a refused or failed order — it returns the result, exactly as the
        async boundary does. A script that treats an exception as "it did not
        happen" would treat a refusal as a network fault and retry a filled order."""
        return self._run(lambda: self._client.execution.place_order(*args, **kwargs))

    def cancel_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.cancel_order`."""
        return self._run(lambda: self._client.execution.cancel_order(*args, **kwargs))

    def modify_order(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.modify_order`."""
        return self._run(lambda: self._client.execution.modify_order(*args, **kwargs))

    def modify_position(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.modify_position`."""
        return self._run(lambda: self._client.execution.modify_position(*args, **kwargs))

    def close_position(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.close_position`."""
        return self._run(lambda: self._client.execution.close_position(*args, **kwargs))

    def close_position_by(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.close_position_by`."""
        return self._run(lambda: self._client.execution.close_position_by(*args, **kwargs))

    def close_position_partial(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.close_position_partial`."""
        return self._run(lambda: self._client.execution.close_position_partial(*args, **kwargs))

    def set_trailing_stop(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.set_trailing_stop`."""
        return self._run(lambda: self._client.execution.set_trailing_stop(*args, **kwargs))

    def clear_trailing_stop(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.clear_trailing_stop`."""
        return self._run(lambda: self._client.execution.clear_trailing_stop(*args, **kwargs))

    def get_command(self, *args: Any, **kwargs: Any) -> ExecutionResult:
        """Blocking form of :meth:`mfx.execution.Execution.get_command`."""
        return self._run(lambda: self._client.execution.get_command(*args, **kwargs))

    # ------------------------------------------------------------------------------- paging

    def _pages[T](self, fetch: Callable[[str | None], Awaitable[Page[T]]]) -> Iterator[T]:
        cursor: str | None = None
        while True:
            page = self._run(functools.partial(fetch, cursor))
            yield from page.items
            cursor = page.next_cursor
            if not cursor:
                return

    # ------------------------------------------------------------------------------ closing

    @property
    def budget(self) -> Any:  # noqa: ANN401 - Budget | None, without importing it at runtime
        """What the key had left when MFX last answered."""
        return self._client.budget

    def close(self) -> None:
        """Close the connections, stop the loop and join its thread. Closing twice is harmless."""
        if self._closed:
            return
        self._run(self._client.aclose)
        self._closed = True
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=_SHUTDOWN_TIMEOUT_S)
        self._loop.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"SyncMfxClient({self._client!r})"


class SyncCopy:
    """Blocking form of :class:`mfx.copy_trading.Copy`: ``SyncMfxClient.copy``.

    Method for method the async namespace, taking the same arguments; a page method answers the
    same :class:`~mfx.copy_trading.CopyPage`, and each ``all_*`` method is an ordinary iterator
    that reads one page a call, never ahead.
    """

    def __init__(self, sync: SyncMfxClient) -> None:
        self._sync = sync

    def _copy(self) -> Copy:
        return self._sync._client.copy

    def create_leader(self, **kwargs: Any) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.create_leader`."""
        return self._sync._run(lambda: self._copy().create_leader(**kwargs))

    def get_leader(self, leader_id: Id) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.get_leader`."""
        return self._sync._run(lambda: self._copy().get_leader(leader_id))

    def leaders(self, **kwargs: Any) -> CopyPage[CopyLeader, CopyLeaderPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.leaders`."""
        return self._sync._run(lambda: self._copy().leaders(**kwargs))

    def all_leaders(self, **kwargs: Any) -> Iterator[CopyLeader]:
        """Every leader, following the cursor; narrowed as :meth:`mfx.copy_trading.Copy.leaders`."""
        return self._sync._pages(lambda cursor: self._copy().leaders(cursor=cursor, **kwargs))

    def update_leader(self, leader_id: Id, **kwargs: Any) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.update_leader`."""
        return self._sync._run(lambda: self._copy().update_leader(leader_id, **kwargs))

    def pause_leader(self, leader_id: Id, *, idempotency_key: str) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.pause_leader`."""
        return self._sync._run(
            lambda: self._copy().pause_leader(leader_id, idempotency_key=idempotency_key)
        )

    def resume_leader(self, leader_id: Id, *, idempotency_key: str) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.resume_leader`."""
        return self._sync._run(
            lambda: self._copy().resume_leader(leader_id, idempotency_key=idempotency_key)
        )

    def retire_leader(self, leader_id: Id, **kwargs: Any) -> CopyLeader:
        """Blocking form of :meth:`mfx.copy_trading.Copy.retire_leader`."""
        return self._sync._run(lambda: self._copy().retire_leader(leader_id, **kwargs))

    def send_open_signal(self, leader_id: Id, **kwargs: Any) -> CopySignalAccepted:
        """Blocking form of :meth:`mfx.copy_trading.Copy.send_open_signal`."""
        return self._sync._run(lambda: self._copy().send_open_signal(leader_id, **kwargs))

    def send_close_signal(self, leader_id: Id, **kwargs: Any) -> CopySignalAccepted:
        """Blocking form of :meth:`mfx.copy_trading.Copy.send_close_signal`."""
        return self._sync._run(lambda: self._copy().send_close_signal(leader_id, **kwargs))

    def create_follower(self, **kwargs: Any) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.create_follower`."""
        return self._sync._run(lambda: self._copy().create_follower(**kwargs))

    def preview_follower(self, **kwargs: Any) -> CopyPreview:
        """Blocking form of :meth:`mfx.copy_trading.Copy.preview_follower`."""
        return self._sync._run(lambda: self._copy().preview_follower(**kwargs))

    def get_follower(self, follower_id: Id) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.get_follower`."""
        return self._sync._run(lambda: self._copy().get_follower(follower_id))

    def followers(self, **kwargs: Any) -> CopyPage[CopyFollower, CopyFollowerPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.followers`."""
        return self._sync._run(lambda: self._copy().followers(**kwargs))

    def all_followers(self, **kwargs: Any) -> Iterator[CopyFollower]:
        """Every follower, following the cursor; narrowed as
        :meth:`mfx.copy_trading.Copy.followers`."""
        return self._sync._pages(lambda cursor: self._copy().followers(cursor=cursor, **kwargs))

    def update_follower(self, follower_id: Id, **kwargs: Any) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.update_follower`."""
        return self._sync._run(lambda: self._copy().update_follower(follower_id, **kwargs))

    def pause_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.pause_follower`."""
        return self._sync._run(
            lambda: self._copy().pause_follower(follower_id, idempotency_key=idempotency_key)
        )

    def resume_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.resume_follower`."""
        return self._sync._run(
            lambda: self._copy().resume_follower(follower_id, idempotency_key=idempotency_key)
        )

    def resync_follower(self, follower_id: Id, *, idempotency_key: str) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.resync_follower`."""
        return self._sync._run(
            lambda: self._copy().resync_follower(follower_id, idempotency_key=idempotency_key)
        )

    def unfollow(self, follower_id: Id, **kwargs: Any) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.unfollow`."""
        return self._sync._run(lambda: self._copy().unfollow(follower_id, **kwargs))

    def stopouts(self, follower_id: Id, **kwargs: Any) -> Page[CopyStopout]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.stopouts`."""
        return self._sync._run(lambda: self._copy().stopouts(follower_id, **kwargs))

    def all_stopouts(self, follower_id: Id, **kwargs: Any) -> Iterator[CopyStopout]:
        """Every stop-out of a follower, following the cursor."""
        return self._sync._pages(
            lambda cursor: self._copy().stopouts(follower_id, cursor=cursor, **kwargs)
        )

    def reset_stopouts(self, follower_id: Id, **kwargs: Any) -> CopyFollower:
        """Blocking form of :meth:`mfx.copy_trading.Copy.reset_stopouts`."""
        return self._sync._run(lambda: self._copy().reset_stopouts(follower_id, **kwargs))

    def create_group(self, **kwargs: Any) -> CopyGroup:
        """Blocking form of :meth:`mfx.copy_trading.Copy.create_group`."""
        return self._sync._run(lambda: self._copy().create_group(**kwargs))

    def get_group(self, group_id: Id) -> CopyGroup:
        """Blocking form of :meth:`mfx.copy_trading.Copy.get_group`."""
        return self._sync._run(lambda: self._copy().get_group(group_id))

    def groups(self, **kwargs: Any) -> CopyPage[CopyGroup, CopyGroupPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.groups`."""
        return self._sync._run(lambda: self._copy().groups(**kwargs))

    def all_groups(self, **kwargs: Any) -> Iterator[CopyGroup]:
        """Every group, following the cursor."""
        return self._sync._pages(lambda cursor: self._copy().groups(cursor=cursor, **kwargs))

    def update_group(self, group_id: Id, **kwargs: Any) -> CopyGroup:
        """Blocking form of :meth:`mfx.copy_trading.Copy.update_group`."""
        return self._sync._run(lambda: self._copy().update_group(group_id, **kwargs))

    def add_group_followers(
        self, group_id: Id, follower_ids: Sequence[Id], *, idempotency_key: str
    ) -> CopyGroupMembersResult:
        """Blocking form of :meth:`mfx.copy_trading.Copy.add_group_followers`."""
        return self._sync._run(
            lambda: self._copy().add_group_followers(
                group_id, follower_ids, idempotency_key=idempotency_key
            )
        )

    def remove_group_followers(
        self, group_id: Id, follower_ids: Sequence[Id], *, idempotency_key: str
    ) -> CopyGroupMembersResult:
        """Blocking form of :meth:`mfx.copy_trading.Copy.remove_group_followers`."""
        return self._sync._run(
            lambda: self._copy().remove_group_followers(
                group_id, follower_ids, idempotency_key=idempotency_key
            )
        )

    def pause_group(self, group_id: Id, *, idempotency_key: str) -> CopyGroup:
        """Blocking form of :meth:`mfx.copy_trading.Copy.pause_group`."""
        return self._sync._run(
            lambda: self._copy().pause_group(group_id, idempotency_key=idempotency_key)
        )

    def resume_group(self, group_id: Id, *, idempotency_key: str) -> CopyGroup:
        """Blocking form of :meth:`mfx.copy_trading.Copy.resume_group`."""
        return self._sync._run(
            lambda: self._copy().resume_group(group_id, idempotency_key=idempotency_key)
        )

    def close_group(
        self, group_id: Id, *, reason: str, pause: bool, idempotency_key: str
    ) -> CopyGroupCloseResult:
        """Blocking form of :meth:`mfx.copy_trading.Copy.close_group`."""
        return self._sync._run(
            lambda: self._copy().close_group(
                group_id, reason=reason, pause=pause, idempotency_key=idempotency_key
            )
        )

    def rollover_group(self, group_id: Id, **kwargs: Any) -> CopyGroupRolloverResult:
        """Blocking form of :meth:`mfx.copy_trading.Copy.rollover_group`."""
        return self._sync._run(lambda: self._copy().rollover_group(group_id, **kwargs))

    def closes(self, **kwargs: Any) -> CopyPage[CopyClose, CopyClosePageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.closes`."""
        return self._sync._run(lambda: self._copy().closes(**kwargs))

    def all_closes(self, **kwargs: Any) -> Iterator[CopyClose]:
        """Every requested close the filters and window match, following the cursor."""
        return self._sync._pages(lambda cursor: self._copy().closes(cursor=cursor, **kwargs))

    def get_close(self, close_id: Id) -> CopyClose:
        """Blocking form of :meth:`mfx.copy_trading.Copy.get_close`."""
        return self._sync._run(lambda: self._copy().get_close(close_id))

    def signals(self, **kwargs: Any) -> CopyPage[CopySignalEntry, CopySignalPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.signals`."""
        return self._sync._run(lambda: self._copy().signals(**kwargs))

    def all_signals(self, **kwargs: Any) -> Iterator[CopySignalEntry]:
        """Every signal the filters and window match, following the cursor."""
        return self._sync._pages(lambda cursor: self._copy().signals(cursor=cursor, **kwargs))

    def tenant_stopouts(self, **kwargs: Any) -> CopyPage[CopyStopout, CopyTenantStopoutPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.tenant_stopouts`."""
        return self._sync._run(lambda: self._copy().tenant_stopouts(**kwargs))

    def all_tenant_stopouts(self, **kwargs: Any) -> Iterator[CopyStopout]:
        """Every stop-out of your followers the filters and window match, following the cursor."""
        return self._sync._pages(
            lambda cursor: self._copy().tenant_stopouts(cursor=cursor, **kwargs)
        )

    def log(self, **kwargs: Any) -> CopyPage[CopyLogEntry, CopyLogPageStats]:
        """Blocking form of :meth:`mfx.copy_trading.Copy.log`."""
        return self._sync._run(lambda: self._copy().log(**kwargs))

    def all_log(self, **kwargs: Any) -> Iterator[CopyLogEntry]:
        """Every row of the copy log the filters and window match, following the cursor."""
        return self._sync._pages(lambda cursor: self._copy().log(cursor=cursor, **kwargs))


class SyncBilling:
    """Blocking form of :class:`mfx.billing.Billing`: ``SyncMfxClient.billing``.

    Method for method the async namespace; :meth:`invoices` is an ordinary iterator that reads
    one page a call, never ahead.
    """

    def __init__(self, sync: SyncMfxClient) -> None:
        self._sync = sync

    def _billing(self) -> Billing:
        return self._sync._client.billing

    def price_list(self) -> BillingPriceList:
        """Blocking form of :meth:`mfx.billing.Billing.price_list`."""
        return self._sync._run(lambda: self._billing().price_list())

    def summary(self) -> BillingSummary:
        """Blocking form of :meth:`mfx.billing.Billing.summary`."""
        return self._sync._run(lambda: self._billing().summary())

    def profile(self, profile_id: Id) -> BillingProfile:
        """Blocking form of :meth:`mfx.billing.Billing.profile`."""
        return self._sync._run(lambda: self._billing().profile(profile_id))

    def forecast(self, profile_id: Id, *, month: str | None = None) -> BillingForecast:
        """Blocking form of :meth:`mfx.billing.Billing.forecast`."""
        return self._sync._run(lambda: self._billing().forecast(profile_id, month=month))

    def prices(self) -> BillingPriceList:
        """Blocking form of :meth:`mfx.billing.Billing.prices`."""
        return self._sync._run(lambda: self._billing().prices())

    def invoice(self, invoice_id: Id) -> BillingInvoiceDetail:
        """Blocking form of :meth:`mfx.billing.Billing.invoice`."""
        return self._sync._run(lambda: self._billing().invoice(invoice_id))

    def invoices_page(self, **kwargs: Any) -> BillingInvoicePage:
        """Blocking form of :meth:`mfx.billing.Billing.invoices_page`."""
        return self._sync._run(lambda: self._billing().invoices_page(**kwargs))

    def invoices(self, **kwargs: Any) -> Iterator[BillingInvoice]:
        """Every invoice, following the cursor; narrowed as
        :meth:`mfx.billing.Billing.invoices_page`."""
        cursor: str | None = None
        while True:
            fetch = functools.partial(self._billing().invoices_page, cursor=cursor, **kwargs)
            page = self._sync._run(fetch)
            yield from page.items
            cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
            if not cursor:
                return


class SyncTenant:
    """Blocking form of :class:`mfx.expert_advisors.Tenant`: ``SyncMfxClient.tenant``."""

    def __init__(self, sync: SyncMfxClient) -> None:
        self._sync = sync

    def _tenant(self) -> Tenant:
        return self._sync._client.tenant

    def contacts(self) -> OwnContacts:
        """Blocking form of :meth:`mfx.expert_advisors.Tenant.contacts`."""
        return self._sync._run(lambda: self._tenant().contacts())

    def service_agreement(self) -> TenantServiceAgreement:
        """Blocking form of :meth:`mfx.expert_advisors.Tenant.service_agreement`."""
        return self._sync._run(lambda: self._tenant().service_agreement())
