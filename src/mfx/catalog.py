"""``client.catalog`` — what MFX supports, and what a broker actually lists.

A tenant asks for a terminal on a broker and a server, and streams instruments in *that broker's*
own names. This is where those names come from: the brokers MFX supports, the servers each one
runs, and the symbols a server lists with the facts a caller needs before trading them —
``trade_mode``, and ``pip_value_per_lot`` read from the terminal rather than derived.

Reads raise the typed hierarchy. Nothing here is an execution call.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mfx._generated.api.md import get_symbol as _get_symbol
from mfx._generated.api.md import get_symbol_quote as _get_symbol_quote
from mfx._generated.api.md import list_broker_servers as _list_broker_servers
from mfx._generated.api.md import list_brokers as _list_brokers
from mfx._generated.api.md import list_symbols as _list_symbols
from mfx._generated.models.symbol import Symbol
from mfx._generated.models.symbol_quote import SymbolQuote
from mfx._generated.models.tenant_broker import TenantBroker
from mfx._generated.models.tenant_broker_server import TenantBrokerServer
from mfx._generated.types import UNSET
from mfx.pages import Page, page_of
from mfx.terminals import Id, _uuid

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Awaitable, Callable

    from mfx.client import MfxClient

__all__ = ["Catalog"]


class Catalog:
    """The brokers, servers and symbols this tenant may use."""

    def __init__(self, client: MfxClient) -> None:
        self._client = client

    async def brokers(
        self, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantBroker]:
        """One page of the brokers MFX supports, with each one's status.

        ``status`` is the broker's: ``active`` is usable, ``suspended`` and ``retired`` are not.
        A terminal requested on a broker that is not usable is refused at request time, and the
        SDK turns that refusal into :class:`~mfx.errors.UnsupportedBrokerError`.
        """
        parsed = await self._client.read(
            lambda: _list_brokers.asyncio_detailed(
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            "GET /brokers",
        )
        return page_of(parsed)

    async def all_brokers(self) -> AsyncIterator[TenantBroker]:
        """Every broker, following the cursor."""
        async for broker in _walk(self.brokers):
            yield broker

    async def servers(
        self, broker_id: Id, *, cursor: str | None = None, limit: int | None = None
    ) -> Page[TenantBrokerServer]:
        """The MT5 servers this broker runs, and whether MFX can use each one now.

        ``server_name`` is what a credential names. ``enabled`` is the per-server switch and
        ``disabled_reason`` is the sentence the operator recorded for it — the same words the
        refusal carries, so a caller can show a user why before it asks for a terminal rather than
        after the platform split them. A terminal requested on a disabled server is refused 409
        and reaches the caller as :class:`~mfx.errors.UnsupportedBrokerError` with
        ``refused_by == "server_disabled"``, which means *try another server of this broker*.
        """
        parsed = await self._client.read(
            lambda: _list_broker_servers.asyncio_detailed(
                id=_uuid(broker_id),
                client=self._client.generated,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            f"GET /brokers/{broker_id}/servers",
        )
        return page_of(parsed)

    async def symbols(
        self,
        broker_id: Id,
        *,
        server_id: Id | None = None,
        account_type: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page[Symbol]:
        """The symbols this broker lists, in its own names.

        ``server_id`` and ``account_type`` narrow the list to one server or one account type,
        for a tenant with more than one on this broker.

        These are the names to pass to ``terminals.create`` and to ``execution.place_order``: MFX
        never renames an instrument on a tenant's behalf, so ``BTCUSD.lv`` is what a
        broker that calls it that will answer to.
        """
        which = _which(server_id, account_type)
        parsed = await self._client.read(
            lambda: _list_symbols.asyncio_detailed(
                # The symbol endpoints take the id as a string rather than a UUID; it is still
                # parsed first, so a malformed id fails here and not as a 404 from the server.
                id=str(_uuid(broker_id)),
                client=self._client.generated,
                **which,
                cursor=cursor if cursor is not None else UNSET,
                limit=limit if limit is not None else UNSET,
            ),
            f"GET /brokers/{broker_id}/symbols",
        )
        return page_of(parsed)

    async def symbol(
        self,
        broker_id: Id,
        symbol: str,
        *,
        server_id: Id | None = None,
        account_type: str | None = None,
    ) -> Symbol:
        """One symbol's specification, including ``pip_value_per_lot``.

        A symbol listed on more than one of the tenant's servers or account types is answered
        409 ``ambiguous_symbol``; name ``server_id`` and ``account_type`` to say which.
        """
        which = _which(server_id, account_type)
        parsed = await self._client.read(
            lambda: _get_symbol.asyncio_detailed(
                id=str(_uuid(broker_id)),
                symbol=symbol,
                client=self._client.generated,
                **which,
            ),
            f"GET /brokers/{broker_id}/symbols/{symbol}",
        )
        return parsed  # type: ignore[no-any-return]

    async def quote(
        self,
        broker_id: Id,
        symbol: str,
        *,
        server_id: Id | None = None,
        account_type: str | None = None,
    ) -> SymbolQuote:
        """The current quote for one symbol, with its age.

        A quote is never returned without saying how old it is: a stale quote reads exactly like a
        live one and gets acted on.

        A symbol listed on more than one of the tenant's servers or account types is answered
        409 ``ambiguous_symbol``; name ``server_id`` and ``account_type`` to say which.
        """
        which = _which(server_id, account_type)
        parsed = await self._client.read(
            lambda: _get_symbol_quote.asyncio_detailed(
                id=str(_uuid(broker_id)),
                symbol=symbol,
                client=self._client.generated,
                **which,
            ),
            f"GET /brokers/{broker_id}/symbols/{symbol}/quote",
        )
        return parsed  # type: ignore[no-any-return]


def _which(server_id: Id | None, account_type: str | None) -> dict[str, Any]:
    """The two query parameters that say which of a tenant's servers and account types is meant.

    What the caller did not name is left out of the request altogether, never sent empty. The
    server id is parsed here, before the request is built, so a malformed one is a ValueError at
    the call and neither a 404 from the server nor an answer the SDK could not read.
    """
    return {
        "server_id": _uuid(server_id) if server_id is not None else UNSET,
        "account_type": account_type if account_type is not None else UNSET,
    }


async def _walk[T](page: Callable[..., Awaitable[Page[T]]]) -> AsyncIterator[T]:
    """Follow a cursor to the end. There is no total to check against, by design."""
    cursor: str | None = None
    while True:
        answer = await page(cursor=cursor)
        for row in answer.items:
            yield row
        cursor = answer.next_cursor
        if not cursor:
            return
