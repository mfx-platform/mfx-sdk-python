from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_maintenance_state import ListMaintenanceState
from ...models.tenant_maintenance_page import TenantMaintenancePage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListMaintenanceState] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/maintenance",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantMaintenancePage]:
    if response.status_code == 200:
        response_200 = TenantMaintenancePage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TenantMaintenancePage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListMaintenanceState] = UNSET,
) -> Response[Union[Error, TenantMaintenancePage]]:
    """Planned maintenance on your terminals - windows scheduled, in progress and recently ended

     A window in progress is listed to every tenant in its scope; a scheduled one once it has been
    announced to you. `suspended` is what the API refuses you while it is in progress, with 403
    `maintenance` and `details.ends_at`; `console` is what your console shows. Answered under every
    suspension, including a console made unavailable. Unfiltered: scheduled and in progress, soonest
    first.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListMaintenanceState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantMaintenancePage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListMaintenanceState] = UNSET,
) -> Optional[Union[Error, TenantMaintenancePage]]:
    """Planned maintenance on your terminals - windows scheduled, in progress and recently ended

     A window in progress is listed to every tenant in its scope; a scheduled one once it has been
    announced to you. `suspended` is what the API refuses you while it is in progress, with 403
    `maintenance` and `details.ends_at`; `console` is what your console shows. Answered under every
    suspension, including a console made unavailable. Unfiltered: scheduled and in progress, soonest
    first.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListMaintenanceState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantMaintenancePage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListMaintenanceState] = UNSET,
) -> Response[Union[Error, TenantMaintenancePage]]:
    """Planned maintenance on your terminals - windows scheduled, in progress and recently ended

     A window in progress is listed to every tenant in its scope; a scheduled one once it has been
    announced to you. `suspended` is what the API refuses you while it is in progress, with 403
    `maintenance` and `details.ends_at`; `console` is what your console shows. Answered under every
    suspension, including a console made unavailable. Unfiltered: scheduled and in progress, soonest
    first.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListMaintenanceState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantMaintenancePage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, ListMaintenanceState] = UNSET,
) -> Optional[Union[Error, TenantMaintenancePage]]:
    """Planned maintenance on your terminals - windows scheduled, in progress and recently ended

     A window in progress is listed to every tenant in its scope; a scheduled one once it has been
    announced to you. `suspended` is what the API refuses you while it is in progress, with 403
    `maintenance` and `details.ends_at`; `console` is what your console shows. Answered under every
    suspension, including a console made unavailable. Unfiltered: scheduled and in progress, soonest
    first.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, ListMaintenanceState]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantMaintenancePage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            state=state,
        )
    ).parsed
