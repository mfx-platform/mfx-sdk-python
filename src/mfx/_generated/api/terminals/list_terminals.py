from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_terminals_state_item import ListTerminalsStateItem
from ...models.tenant_terminal_page import TenantTerminalPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    label: Union[Unset, list[str]] = UNSET,
    state: Union[Unset, list[ListTerminalsStateItem]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_label: Union[Unset, list[str]] = UNSET
    if not isinstance(label, Unset):
        json_label = label

    params["label"] = json_label

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/terminals",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantTerminalPage]:
    if response.status_code == 200:
        response_200 = TenantTerminalPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TenantTerminalPage]]:
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
    label: Union[Unset, list[str]] = UNSET,
    state: Union[Unset, list[ListTerminalsStateItem]] = UNSET,
) -> Response[Union[Error, TenantTerminalPage]]:
    """List the tenant's terminals, newest first (cursor pagination), filtered by label and state

     Every terminal of yours, RETIRED ones included, newest first. `label` and `state` narrow the list in
    the query, before the page is cut, so a filtered page is never short for being filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        label (Union[Unset, list[str]]):
        state (Union[Unset, list[ListTerminalsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminalPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        label=label,
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
    label: Union[Unset, list[str]] = UNSET,
    state: Union[Unset, list[ListTerminalsStateItem]] = UNSET,
) -> Optional[Union[Error, TenantTerminalPage]]:
    """List the tenant's terminals, newest first (cursor pagination), filtered by label and state

     Every terminal of yours, RETIRED ones included, newest first. `label` and `state` narrow the list in
    the query, before the page is cut, so a filtered page is never short for being filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        label (Union[Unset, list[str]]):
        state (Union[Unset, list[ListTerminalsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminalPage]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        label=label,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    label: Union[Unset, list[str]] = UNSET,
    state: Union[Unset, list[ListTerminalsStateItem]] = UNSET,
) -> Response[Union[Error, TenantTerminalPage]]:
    """List the tenant's terminals, newest first (cursor pagination), filtered by label and state

     Every terminal of yours, RETIRED ones included, newest first. `label` and `state` narrow the list in
    the query, before the page is cut, so a filtered page is never short for being filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        label (Union[Unset, list[str]]):
        state (Union[Unset, list[ListTerminalsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminalPage]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        label=label,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    label: Union[Unset, list[str]] = UNSET,
    state: Union[Unset, list[ListTerminalsStateItem]] = UNSET,
) -> Optional[Union[Error, TenantTerminalPage]]:
    """List the tenant's terminals, newest first (cursor pagination), filtered by label and state

     Every terminal of yours, RETIRED ones included, newest first. `label` and `state` narrow the list in
    the query, before the page is cut, so a filtered page is never short for being filtered.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        label (Union[Unset, list[str]]):
        state (Union[Unset, list[ListTerminalsStateItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminalPage]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            label=label,
            state=state,
        )
    ).parsed
