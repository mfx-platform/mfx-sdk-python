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
from collections.abc import Awaitable, Callable, Iterator
from types import TracebackType
from typing import TYPE_CHECKING, Any, Self

from mfx.client import MfxClient
from mfx.pages import Page

if TYPE_CHECKING:
    from mfx._generated.models.account import Account
    from mfx._generated.models.candle_list import CandleList
    from mfx._generated.models.credential_accepted import CredentialAccepted
    from mfx._generated.models.deal import Deal
    from mfx._generated.models.pending_order_list import PendingOrderList
    from mfx._generated.models.position_list import PositionList
    from mfx._generated.models.spread_list import SpreadList
    from mfx._generated.models.symbol import Symbol
    from mfx._generated.models.symbol_quote import SymbolQuote
    from mfx._generated.models.tenant_broker import TenantBroker
    from mfx._generated.models.tenant_broker_server import TenantBrokerServer
    from mfx._generated.models.tenant_terminal import TenantTerminal
    from mfx._generated.models.tick_list import TickList
    from mfx._generated.models.usage import Usage
    from mfx.results import ExecutionResult
    from mfx.secrets import Secret
    from mfx.terminals import CredentialType, Id, Redundancy

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

    def terminals(self, *, limit: int | None = None) -> Iterator[TenantTerminal]:
        """Every terminal, following the cursor — as an ordinary iterator.

        Each page is one call; the walk is not read ahead, so a script that stops early has not
        paid for the rest.
        """
        return self._pages(lambda cursor: self._client.terminals.page(cursor=cursor, limit=limit))

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
