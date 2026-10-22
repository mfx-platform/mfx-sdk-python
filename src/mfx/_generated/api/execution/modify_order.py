from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.command_accepted import CommandAccepted
from ...models.error import Error
from ...models.order_modify import OrderModify
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    ticket: int,
    *,
    body: OrderModify,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/orders/{ticket}/modify".format(
            id=id,
            ticket=ticket,
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
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderModify,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Amend a pending order - its price, stop loss, take profit or expiry; what is not sent stays as it is

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (OrderModify): Amend an order that is still pending: a limit or a stop the broker has
            not filled. Send only what changes; a field that is absent keeps the order's present
            value, so amending the price does not touch its stops. The ticket in the path is the
            order's. An order that is no longer pending - filled, cancelled, expired, or never on this
            account - is refused before the broker with `invalid_request`; a filled order is a
            position, and its stops are amended with modifyPosition. Every decimal is a string and is
            treated as on OrderPlace: float noise is snapped onto the symbol's tick, and a price
            deliberately finer than the tick is sent as given, for the broker to accept or refuse. The
            order's volume, side, type and symbol cannot be amended: cancel the order and place
            another.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        ticket=ticket,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderModify,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Amend a pending order - its price, stop loss, take profit or expiry; what is not sent stays as it is

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (OrderModify): Amend an order that is still pending: a limit or a stop the broker has
            not filled. Send only what changes; a field that is absent keeps the order's present
            value, so amending the price does not touch its stops. The ticket in the path is the
            order's. An order that is no longer pending - filled, cancelled, expired, or never on this
            account - is refused before the broker with `invalid_request`; a filled order is a
            position, and its stops are amended with modifyPosition. Every decimal is a string and is
            treated as on OrderPlace: float noise is snapped onto the symbol's tick, and a price
            deliberately finer than the tick is sent as given, for the broker to accept or refuse. The
            order's volume, side, type and symbol cannot be amended: cancel the order and place
            another.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return sync_detailed(
        id=id,
        ticket=ticket,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderModify,
    idempotency_key: str,
) -> Response[Union[CommandAccepted, Error]]:
    """Amend a pending order - its price, stop loss, take profit or expiry; what is not sent stays as it is

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (OrderModify): Amend an order that is still pending: a limit or a stop the broker has
            not filled. Send only what changes; a field that is absent keeps the order's present
            value, so amending the price does not touch its stops. The ticket in the path is the
            order's. An order that is no longer pending - filled, cancelled, expired, or never on this
            account - is refused before the broker with `invalid_request`; a filled order is a
            position, and its stops are amended with modifyPosition. Every decimal is a string and is
            treated as on OrderPlace: float noise is snapped onto the symbol's tick, and a price
            deliberately finer than the tick is sent as given, for the broker to accept or refuse. The
            order's volume, side, type and symbol cannot be amended: cancel the order and place
            another.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CommandAccepted, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        ticket=ticket,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    ticket: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: OrderModify,
    idempotency_key: str,
) -> Optional[Union[CommandAccepted, Error]]:
    """Amend a pending order - its price, stop loss, take profit or expiry; what is not sent stays as it is

    Args:
        id (UUID):
        ticket (int):
        idempotency_key (str):
        body (OrderModify): Amend an order that is still pending: a limit or a stop the broker has
            not filled. Send only what changes; a field that is absent keeps the order's present
            value, so amending the price does not touch its stops. The ticket in the path is the
            order's. An order that is no longer pending - filled, cancelled, expired, or never on this
            account - is refused before the broker with `invalid_request`; a filled order is a
            position, and its stops are amended with modifyPosition. Every decimal is a string and is
            treated as on OrderPlace: float noise is snapped onto the symbol's tick, and a price
            deliberately finer than the tick is sent as given, for the broker to accept or refuse. The
            order's volume, side, type and symbol cannot be amended: cancel the order and place
            another.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CommandAccepted, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            ticket=ticket,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
