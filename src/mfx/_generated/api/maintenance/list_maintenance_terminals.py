from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_maintenance_terminal_page import TenantMaintenanceTerminalPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/maintenance/{id}/terminals".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantMaintenanceTerminalPage]:
    if response.status_code == 200:
        response_200 = TenantMaintenanceTerminalPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TenantMaintenanceTerminalPage]]:
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Error, TenantMaintenanceTerminalPage]]:
    """Your terminals in one window - waiting for their batch, moving to a new machine, back - each with
    its own expected time

     Only your own terminals in the window's scope. A window you are not in, or another tenant's, is 404.
    Answered under every suspension. Open positions stay at the broker throughout.

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantMaintenanceTerminalPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Error, TenantMaintenanceTerminalPage]]:
    """Your terminals in one window - waiting for their batch, moving to a new machine, back - each with
    its own expected time

     Only your own terminals in the window's scope. A window you are not in, or another tenant's, is 404.
    Answered under every suspension. Open positions stay at the broker throughout.

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantMaintenanceTerminalPage]
    """

    return sync_detailed(
        id=id,
        client=client,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[Error, TenantMaintenanceTerminalPage]]:
    """Your terminals in one window - waiting for their batch, moving to a new machine, back - each with
    its own expected time

     Only your own terminals in the window's scope. A window you are not in, or another tenant's, is 404.
    Answered under every suspension. Open positions stay at the broker throughout.

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantMaintenanceTerminalPage]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[Error, TenantMaintenanceTerminalPage]]:
    """Your terminals in one window - waiting for their batch, moving to a new machine, back - each with
    its own expected time

     Only your own terminals in the window's scope. A window you are not in, or another tenant's, is 404.
    Answered under every suspension. Open positions stay at the broker throughout.

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantMaintenanceTerminalPage]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
