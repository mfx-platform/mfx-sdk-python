from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.command_accepted import CommandAccepted
from ...models.error import Error
from ...models.order_place import OrderPlace
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: OrderPlace,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/orders".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CommandAccepted, Error]:
    if response.status_code == 202:
        response_202 = CommandAccepted.from_dict(response.json())

        return response_202

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CommandAccepted, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderPlace,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Place a market or pending order → 202 + command_id (the command expires in 10 s, or expires_in_ms)

    Args:
        id (UUID):
        idempotency_key (str):
        body (OrderPlace): Place an order. Refused before it reaches the broker — never rounded or
            trimmed: a volume off the symbol's step, a comment MT5 would truncate, a pending order
            with no price. Every decimal here is a **string**, exactly as every decimal the API
            returns already is, because a float price is a wrong price in either direction: a computed
            size is the ordinary path for a strategy, and `0.07 * 3` is `0.21000000000000002` as a
            JSON number. Send what `Decimal` gives you. The one thing the platform changes is binary
            float noise that arrives anyway — a decimal within 1e-6 of a multiple of the symbol's own
            increment, its `volume_step` for a volume or its tick size for a price, is put exactly
            onto that multiple. A value further off than that is what you asked for and is sent
            unchanged: the platform never moves a price you chose. **When the command is SUCCEEDED.**
            The outcome is the broker's answer to the one `order_send`, never a later event. A market
            order is SUCCEEDED when the broker reports the deal: `mt5_retcode` 10009
            (TRADE_RETCODE_DONE) or 10010 (DONE_PARTIAL); `tickets.order`, `tickets.deal` and
            `tickets.position` are set and `exec_price` and `exec_volume` are the fill (a broker on
            exchange execution that answers a market order 10008 instead gives the same SUCCEEDED with
            `tickets.deal` null). A pending order (limit, stop, stop_limit) is SUCCEEDED when the
            broker accepts it onto its book: `mt5_retcode` 10008 (TRADE_RETCODE_PLACED),
            `retcode_text` placed. Then `tickets.order` is the pending order's ticket - the one to
            cancel or amend it by - and `tickets.deal` and `tickets.position` are null, because
            nothing has filled; `exec_price` is null, and `exec_volume`, when present, is the order's
            volume as the broker echoed it, not a fill. A placement interrupted and then reconciled
            from the terminal's order history reads the same (10008, `tickets.order` set). **The fill
            of a pending order is not a command outcome**: no second `command.completed` is sent. When
            the order triggers and fills, it leaves the pending orders (`GET
            /terminals/{id}/orders/pending` and the `pending` of `account.snapshot`), a deal whose
            `order` is that ticket appears in `GET /terminals/{id}/history/deals`, and the position
            arrives as `position.opened` on `events` (`position.modified` when a netting account adds
            it to a position already open). Match a fill to its order by the deal's `order`: MT5
            usually gives the position the order's ticket, but not always. An order that lapses at its
            `expires_at` or is cancelled leaves the pending orders with no deal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderPlace,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Place a market or pending order → 202 + command_id (the command expires in 10 s, or expires_in_ms)

    Args:
        id (UUID):
        idempotency_key (str):
        body (OrderPlace): Place an order. Refused before it reaches the broker — never rounded or
            trimmed: a volume off the symbol's step, a comment MT5 would truncate, a pending order
            with no price. Every decimal here is a **string**, exactly as every decimal the API
            returns already is, because a float price is a wrong price in either direction: a computed
            size is the ordinary path for a strategy, and `0.07 * 3` is `0.21000000000000002` as a
            JSON number. Send what `Decimal` gives you. The one thing the platform changes is binary
            float noise that arrives anyway — a decimal within 1e-6 of a multiple of the symbol's own
            increment, its `volume_step` for a volume or its tick size for a price, is put exactly
            onto that multiple. A value further off than that is what you asked for and is sent
            unchanged: the platform never moves a price you chose. **When the command is SUCCEEDED.**
            The outcome is the broker's answer to the one `order_send`, never a later event. A market
            order is SUCCEEDED when the broker reports the deal: `mt5_retcode` 10009
            (TRADE_RETCODE_DONE) or 10010 (DONE_PARTIAL); `tickets.order`, `tickets.deal` and
            `tickets.position` are set and `exec_price` and `exec_volume` are the fill (a broker on
            exchange execution that answers a market order 10008 instead gives the same SUCCEEDED with
            `tickets.deal` null). A pending order (limit, stop, stop_limit) is SUCCEEDED when the
            broker accepts it onto its book: `mt5_retcode` 10008 (TRADE_RETCODE_PLACED),
            `retcode_text` placed. Then `tickets.order` is the pending order's ticket - the one to
            cancel or amend it by - and `tickets.deal` and `tickets.position` are null, because
            nothing has filled; `exec_price` is null, and `exec_volume`, when present, is the order's
            volume as the broker echoed it, not a fill. A placement interrupted and then reconciled
            from the terminal's order history reads the same (10008, `tickets.order` set). **The fill
            of a pending order is not a command outcome**: no second `command.completed` is sent. When
            the order triggers and fills, it leaves the pending orders (`GET
            /terminals/{id}/orders/pending` and the `pending` of `account.snapshot`), a deal whose
            `order` is that ticket appears in `GET /terminals/{id}/history/deals`, and the position
            arrives as `position.opened` on `events` (`position.modified` when a netting account adds
            it to a position already open). Match a fill to its order by the deal's `order`: MT5
            usually gives the position the order's ticket, but not always. An order that lapses at its
            `expires_at` or is cancelled leaves the pending orders with no deal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderPlace,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Place a market or pending order → 202 + command_id (the command expires in 10 s, or expires_in_ms)

    Args:
        id (UUID):
        idempotency_key (str):
        body (OrderPlace): Place an order. Refused before it reaches the broker — never rounded or
            trimmed: a volume off the symbol's step, a comment MT5 would truncate, a pending order
            with no price. Every decimal here is a **string**, exactly as every decimal the API
            returns already is, because a float price is a wrong price in either direction: a computed
            size is the ordinary path for a strategy, and `0.07 * 3` is `0.21000000000000002` as a
            JSON number. Send what `Decimal` gives you. The one thing the platform changes is binary
            float noise that arrives anyway — a decimal within 1e-6 of a multiple of the symbol's own
            increment, its `volume_step` for a volume or its tick size for a price, is put exactly
            onto that multiple. A value further off than that is what you asked for and is sent
            unchanged: the platform never moves a price you chose. **When the command is SUCCEEDED.**
            The outcome is the broker's answer to the one `order_send`, never a later event. A market
            order is SUCCEEDED when the broker reports the deal: `mt5_retcode` 10009
            (TRADE_RETCODE_DONE) or 10010 (DONE_PARTIAL); `tickets.order`, `tickets.deal` and
            `tickets.position` are set and `exec_price` and `exec_volume` are the fill (a broker on
            exchange execution that answers a market order 10008 instead gives the same SUCCEEDED with
            `tickets.deal` null). A pending order (limit, stop, stop_limit) is SUCCEEDED when the
            broker accepts it onto its book: `mt5_retcode` 10008 (TRADE_RETCODE_PLACED),
            `retcode_text` placed. Then `tickets.order` is the pending order's ticket - the one to
            cancel or amend it by - and `tickets.deal` and `tickets.position` are null, because
            nothing has filled; `exec_price` is null, and `exec_volume`, when present, is the order's
            volume as the broker echoed it, not a fill. A placement interrupted and then reconciled
            from the terminal's order history reads the same (10008, `tickets.order` set). **The fill
            of a pending order is not a command outcome**: no second `command.completed` is sent. When
            the order triggers and fills, it leaves the pending orders (`GET
            /terminals/{id}/orders/pending` and the `pending` of `account.snapshot`), a deal whose
            `order` is that ticket appears in `GET /terminals/{id}/history/deals`, and the position
            arrives as `position.opened` on `events` (`position.modified` when a netting account adds
            it to a position already open). Match a fill to its order by the deal's `order`: MT5
            usually gives the position the order's ticket, but not always. An order that lapses at its
            `expires_at` or is cancelled leaves the pending orders with no deal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderPlace,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Place a market or pending order → 202 + command_id (the command expires in 10 s, or expires_in_ms)

    Args:
        id (UUID):
        idempotency_key (str):
        body (OrderPlace): Place an order. Refused before it reaches the broker — never rounded or
            trimmed: a volume off the symbol's step, a comment MT5 would truncate, a pending order
            with no price. Every decimal here is a **string**, exactly as every decimal the API
            returns already is, because a float price is a wrong price in either direction: a computed
            size is the ordinary path for a strategy, and `0.07 * 3` is `0.21000000000000002` as a
            JSON number. Send what `Decimal` gives you. The one thing the platform changes is binary
            float noise that arrives anyway — a decimal within 1e-6 of a multiple of the symbol's own
            increment, its `volume_step` for a volume or its tick size for a price, is put exactly
            onto that multiple. A value further off than that is what you asked for and is sent
            unchanged: the platform never moves a price you chose. **When the command is SUCCEEDED.**
            The outcome is the broker's answer to the one `order_send`, never a later event. A market
            order is SUCCEEDED when the broker reports the deal: `mt5_retcode` 10009
            (TRADE_RETCODE_DONE) or 10010 (DONE_PARTIAL); `tickets.order`, `tickets.deal` and
            `tickets.position` are set and `exec_price` and `exec_volume` are the fill (a broker on
            exchange execution that answers a market order 10008 instead gives the same SUCCEEDED with
            `tickets.deal` null). A pending order (limit, stop, stop_limit) is SUCCEEDED when the
            broker accepts it onto its book: `mt5_retcode` 10008 (TRADE_RETCODE_PLACED),
            `retcode_text` placed. Then `tickets.order` is the pending order's ticket - the one to
            cancel or amend it by - and `tickets.deal` and `tickets.position` are null, because
            nothing has filled; `exec_price` is null, and `exec_volume`, when present, is the order's
            volume as the broker echoed it, not a fill. A placement interrupted and then reconciled
            from the terminal's order history reads the same (10008, `tickets.order` set). **The fill
            of a pending order is not a command outcome**: no second `command.completed` is sent. When
            the order triggers and fills, it leaves the pending orders (`GET
            /terminals/{id}/orders/pending` and the `pending` of `account.snapshot`), a deal whose
            `order` is that ticket appears in `GET /terminals/{id}/history/deals`, and the position
            arrives as `position.opened` on `events` (`position.modified` when a netting account adds
            it to a position already open). Match a fill to its order by the deal's `order`: MT5
            usually gives the position the order's ticket, but not always. An order that lapses at its
            `expires_at` or is cancelled leaves the pending orders with no deal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
