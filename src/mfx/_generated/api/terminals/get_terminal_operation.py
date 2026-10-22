from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.terminal_operation import TerminalOperation
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    operation_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/terminals/{id}/operations/{operation_id}".format(
            id=id,
            operation_id=operation_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TerminalOperation]:
    if response.status_code == 200:
        response_200 = TerminalOperation.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TerminalOperation]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, TerminalOperation]]:
    """A lifecycle operation on the terminal — its state and timeline

    Args:
        id (UUID):
        operation_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalOperation]]
    """

    kwargs = _get_kwargs(
        id=id,
        operation_id=operation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TerminalOperation]]:
    """A lifecycle operation on the terminal — its state and timeline

    Args:
        id (UUID):
        operation_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalOperation]
    """

    return sync_detailed(
        id=id,
        operation_id=operation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, TerminalOperation]]:
    """A lifecycle operation on the terminal — its state and timeline

    Args:
        id (UUID):
        operation_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalOperation]]
    """

    kwargs = _get_kwargs(
        id=id,
        operation_id=operation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TerminalOperation]]:
    """A lifecycle operation on the terminal — its state and timeline

    Args:
        id (UUID):
        operation_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalOperation]
    """

    return (
        await asyncio_detailed(
            id=id,
            operation_id=operation_id,
            client=client,
        )
    ).parsed
