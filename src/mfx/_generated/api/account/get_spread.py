from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.spread_list import SpreadList
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/terminals/{id}/spread".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, SpreadList]:
    if response.status_code == 200:
        response_200 = SpreadList.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, SpreadList]]:
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
) -> Response[Union[Error, SpreadList]]:
    """The user's own spread per instrument, read from the user's terminal (a shared feed cannot serve it)

     The last tick of every instrument this terminal streams, as the tenant's own terminals on this
    server reported it. Nothing is sent to the cell, and a tick report arrives about once a minute, so
    read `age_s`: for a price now, read the symbol's quote or subscribe to `md`. An instrument with no
    tick yet is left out, so the list can be shorter than the terminal's instruments and is empty for a
    terminal that streams none. Only an ACTIVE terminal answers: any other state is 409 `state_error`
    with `details.state`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SpreadList]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, SpreadList]]:
    """The user's own spread per instrument, read from the user's terminal (a shared feed cannot serve it)

     The last tick of every instrument this terminal streams, as the tenant's own terminals on this
    server reported it. Nothing is sent to the cell, and a tick report arrives about once a minute, so
    read `age_s`: for a price now, read the symbol's quote or subscribe to `md`. An instrument with no
    tick yet is left out, so the list can be shorter than the terminal's instruments and is empty for a
    terminal that streams none. Only an ACTIVE terminal answers: any other state is 409 `state_error`
    with `details.state`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SpreadList]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, SpreadList]]:
    """The user's own spread per instrument, read from the user's terminal (a shared feed cannot serve it)

     The last tick of every instrument this terminal streams, as the tenant's own terminals on this
    server reported it. Nothing is sent to the cell, and a tick report arrives about once a minute, so
    read `age_s`: for a price now, read the symbol's quote or subscribe to `md`. An instrument with no
    tick yet is left out, so the list can be shorter than the terminal's instruments and is empty for a
    terminal that streams none. Only an ACTIVE terminal answers: any other state is 409 `state_error`
    with `details.state`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SpreadList]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, SpreadList]]:
    """The user's own spread per instrument, read from the user's terminal (a shared feed cannot serve it)

     The last tick of every instrument this terminal streams, as the tenant's own terminals on this
    server reported it. Nothing is sent to the cell, and a tick report arrives about once a minute, so
    read `age_s`: for a price now, read the symbol's quote or subscribe to `md`. An instrument with no
    tick yet is left out, so the list can be shorter than the terminal's instruments and is empty for a
    terminal that streams none. Only an ACTIVE terminal answers: any other state is 409 `state_error`
    with `details.state`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SpreadList]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
