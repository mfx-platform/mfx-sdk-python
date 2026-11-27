import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_close_page import CopyClosePage
from ...models.copy_close_state import CopyCloseState
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    follower_id: Union[Unset, UUID] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
    batch_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CopyCloseState]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_follower_id: Union[Unset, str] = UNSET
    if not isinstance(follower_id, Unset):
        json_follower_id = str(follower_id)
    params["follower_id"] = json_follower_id

    json_leader_id: Union[Unset, str] = UNSET
    if not isinstance(leader_id, Unset):
        json_leader_id = str(leader_id)
    params["leader_id"] = json_leader_id

    json_group_id: Union[Unset, str] = UNSET
    if not isinstance(group_id, Unset):
        json_group_id = str(group_id)
    params["group_id"] = json_group_id

    json_batch_id: Union[Unset, str] = UNSET
    if not isinstance(batch_id, Unset):
        json_batch_id = str(batch_id)
    params["batch_id"] = json_batch_id

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/closes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyClosePage, Error]:
    if response.status_code == 200:
        response_200 = CopyClosePage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyClosePage, Error]]:
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
    follower_id: Union[Unset, UUID] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
    batch_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CopyCloseState]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[CopyClosePage, Error]]:
    """Your requested closes of copied positions, newest first, with a count of each state

     Each close an unfollow or a retire with `close_copied`, or a group's close, asked. Every filter
    narrows the rows in the query, and the stats row is over the same rows: the whole filtered window,
    on every page. The window is `from` to `to` on when the close was asked, at most 31 days (422
    `window_too_wide`); without `from` it is the last 24 hours. A retire's or a group close's closes
    share one `batch_id`.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        follower_id (Union[Unset, UUID]):
        leader_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):
        batch_id (Union[Unset, UUID]):
        state (Union[Unset, list[CopyCloseState]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyClosePage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        follower_id=follower_id,
        leader_id=leader_id,
        group_id=group_id,
        batch_id=batch_id,
        state=state,
        from_=from_,
        to=to,
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
    follower_id: Union[Unset, UUID] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
    batch_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CopyCloseState]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[CopyClosePage, Error]]:
    """Your requested closes of copied positions, newest first, with a count of each state

     Each close an unfollow or a retire with `close_copied`, or a group's close, asked. Every filter
    narrows the rows in the query, and the stats row is over the same rows: the whole filtered window,
    on every page. The window is `from` to `to` on when the close was asked, at most 31 days (422
    `window_too_wide`); without `from` it is the last 24 hours. A retire's or a group close's closes
    share one `batch_id`.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        follower_id (Union[Unset, UUID]):
        leader_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):
        batch_id (Union[Unset, UUID]):
        state (Union[Unset, list[CopyCloseState]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyClosePage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        follower_id=follower_id,
        leader_id=leader_id,
        group_id=group_id,
        batch_id=batch_id,
        state=state,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    follower_id: Union[Unset, UUID] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
    batch_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CopyCloseState]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[CopyClosePage, Error]]:
    """Your requested closes of copied positions, newest first, with a count of each state

     Each close an unfollow or a retire with `close_copied`, or a group's close, asked. Every filter
    narrows the rows in the query, and the stats row is over the same rows: the whole filtered window,
    on every page. The window is `from` to `to` on when the close was asked, at most 31 days (422
    `window_too_wide`); without `from` it is the last 24 hours. A retire's or a group close's closes
    share one `batch_id`.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        follower_id (Union[Unset, UUID]):
        leader_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):
        batch_id (Union[Unset, UUID]):
        state (Union[Unset, list[CopyCloseState]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyClosePage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        follower_id=follower_id,
        leader_id=leader_id,
        group_id=group_id,
        batch_id=batch_id,
        state=state,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    follower_id: Union[Unset, UUID] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    group_id: Union[Unset, UUID] = UNSET,
    batch_id: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CopyCloseState]] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[CopyClosePage, Error]]:
    """Your requested closes of copied positions, newest first, with a count of each state

     Each close an unfollow or a retire with `close_copied`, or a group's close, asked. Every filter
    narrows the rows in the query, and the stats row is over the same rows: the whole filtered window,
    on every page. The window is `from` to `to` on when the close was asked, at most 31 days (422
    `window_too_wide`); without `from` it is the last 24 hours. A retire's or a group close's closes
    share one `batch_id`.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        follower_id (Union[Unset, UUID]):
        leader_id (Union[Unset, UUID]):
        group_id (Union[Unset, UUID]):
        batch_id (Union[Unset, UUID]):
        state (Union[Unset, list[CopyCloseState]]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyClosePage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            follower_id=follower_id,
            leader_id=leader_id,
            group_id=group_id,
            batch_id=batch_id,
            state=state,
            from_=from_,
            to=to,
        )
    ).parsed
