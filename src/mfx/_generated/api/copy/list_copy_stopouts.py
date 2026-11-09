from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_stopout_page import CopyStopoutPage
from ...models.copy_stopout_state import CopyStopoutState
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

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
        "url": "/copy/followers/{id}/stopouts".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyStopoutPage, Error]:
    if response.status_code == 200:
        response_200 = CopyStopoutPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyStopoutPage, Error]]:
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
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
) -> Response[Union[CopyStopoutPage, Error]]:
    """A follower's stop-outs, newest first

     Each stop-out with the limit reached, what was used, its period, the copied volume it closed and,
    once reset, who reset it and why

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyStopoutState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyStopoutPage, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
        state=state,
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
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
) -> Optional[Union[CopyStopoutPage, Error]]:
    """A follower's stop-outs, newest first

     Each stop-out with the limit reached, what was used, its period, the copied volume it closed and,
    once reset, who reset it and why

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyStopoutState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyStopoutPage, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        cursor=cursor,
        limit=limit,
        state=state,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
) -> Response[Union[CopyStopoutPage, Error]]:
    """A follower's stop-outs, newest first

     Each stop-out with the limit reached, what was used, its period, the copied volume it closed and,
    once reset, who reset it and why

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyStopoutState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyStopoutPage, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        cursor=cursor,
        limit=limit,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    state: Union[Unset, list[CopyStopoutState]] = UNSET,
) -> Optional[Union[CopyStopoutPage, Error]]:
    """A follower's stop-outs, newest first

     Each stop-out with the limit reached, what was used, its period, the copied volume it closed and,
    once reset, who reset it and why

    Args:
        id (UUID):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        state (Union[Unset, list[CopyStopoutState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyStopoutPage, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            cursor=cursor,
            limit=limit,
            state=state,
        )
    ).parsed
