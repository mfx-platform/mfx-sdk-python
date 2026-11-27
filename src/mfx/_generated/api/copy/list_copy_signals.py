import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_signal_page import CopySignalPage
from ...models.error import Error
from ...models.list_copy_signals_action_item import ListCopySignalsActionItem
from ...models.list_copy_signals_kind_item import ListCopySignalsKindItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    kind: Union[Unset, list[ListCopySignalsKindItem]] = UNSET,
    action: Union[Unset, list[ListCopySignalsActionItem]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_leader_id: Union[Unset, str] = UNSET
    if not isinstance(leader_id, Unset):
        json_leader_id = str(leader_id)
    params["leader_id"] = json_leader_id

    json_kind: Union[Unset, list[str]] = UNSET
    if not isinstance(kind, Unset):
        json_kind = []
        for kind_item_data in kind:
            kind_item = kind_item_data.value
            json_kind.append(kind_item)

    params["kind"] = json_kind

    json_action: Union[Unset, list[str]] = UNSET
    if not isinstance(action, Unset):
        json_action = []
        for action_item_data in action:
            action_item = action_item_data.value
            json_action.append(action_item)

    params["action"] = json_action

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/copy/signals",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopySignalPage, Error]:
    if response.status_code == 200:
        response_200 = CopySignalPage.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopySignalPage, Error]]:
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
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    kind: Union[Unset, list[ListCopySignalsKindItem]] = UNSET,
    action: Union[Unset, list[ListCopySignalsActionItem]] = UNSET,
) -> Response[Union[CopySignalPage, Error]]:
    """Your leaders' signals over a window, newest first, each with what became of its copies

     Leader fills and external signals as MFX Hub recorded them, never a signature, a key id or the
    source's body: the console's own row, and `outcomes`, how many of the signal's own copies were
    filled, refused and skipped (a stop-out's close names the signal it closes but is not its copy).
    Every filter narrows the rows in the query, before the page is cut, and the stats row counts every
    signal the window and the filters match, by kind, on every page. The window is `from` to `to`, each
    inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours. As on
    the copy log, nothing older than the plan's log retention is listed.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        leader_id (Union[Unset, UUID]):
        kind (Union[Unset, list[ListCopySignalsKindItem]]):
        action (Union[Unset, list[ListCopySignalsActionItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopySignalPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        leader_id=leader_id,
        kind=kind,
        action=action,
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
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    kind: Union[Unset, list[ListCopySignalsKindItem]] = UNSET,
    action: Union[Unset, list[ListCopySignalsActionItem]] = UNSET,
) -> Optional[Union[CopySignalPage, Error]]:
    """Your leaders' signals over a window, newest first, each with what became of its copies

     Leader fills and external signals as MFX Hub recorded them, never a signature, a key id or the
    source's body: the console's own row, and `outcomes`, how many of the signal's own copies were
    filled, refused and skipped (a stop-out's close names the signal it closes but is not its copy).
    Every filter narrows the rows in the query, before the page is cut, and the stats row counts every
    signal the window and the filters match, by kind, on every page. The window is `from` to `to`, each
    inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours. As on
    the copy log, nothing older than the plan's log retention is listed.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        leader_id (Union[Unset, UUID]):
        kind (Union[Unset, list[ListCopySignalsKindItem]]):
        action (Union[Unset, list[ListCopySignalsActionItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopySignalPage, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        leader_id=leader_id,
        kind=kind,
        action=action,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    kind: Union[Unset, list[ListCopySignalsKindItem]] = UNSET,
    action: Union[Unset, list[ListCopySignalsActionItem]] = UNSET,
) -> Response[Union[CopySignalPage, Error]]:
    """Your leaders' signals over a window, newest first, each with what became of its copies

     Leader fills and external signals as MFX Hub recorded them, never a signature, a key id or the
    source's body: the console's own row, and `outcomes`, how many of the signal's own copies were
    filled, refused and skipped (a stop-out's close names the signal it closes but is not its copy).
    Every filter narrows the rows in the query, before the page is cut, and the stats row counts every
    signal the window and the filters match, by kind, on every page. The window is `from` to `to`, each
    inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours. As on
    the copy log, nothing older than the plan's log retention is listed.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        leader_id (Union[Unset, UUID]):
        kind (Union[Unset, list[ListCopySignalsKindItem]]):
        action (Union[Unset, list[ListCopySignalsActionItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopySignalPage, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        leader_id=leader_id,
        kind=kind,
        action=action,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    leader_id: Union[Unset, UUID] = UNSET,
    kind: Union[Unset, list[ListCopySignalsKindItem]] = UNSET,
    action: Union[Unset, list[ListCopySignalsActionItem]] = UNSET,
) -> Optional[Union[CopySignalPage, Error]]:
    """Your leaders' signals over a window, newest first, each with what became of its copies

     Leader fills and external signals as MFX Hub recorded them, never a signature, a key id or the
    source's body: the console's own row, and `outcomes`, how many of the signal's own copies were
    filled, refused and skipped (a stop-out's close names the signal it closes but is not its copy).
    Every filter narrows the rows in the query, before the page is cut, and the stats row counts every
    signal the window and the filters match, by kind, on every page. The window is `from` to `to`, each
    inclusive, at most 31 days (422 `window_too_wide`); without `from` it is the last 24 hours. As on
    the copy log, nothing older than the plan's log retention is listed.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        leader_id (Union[Unset, UUID]):
        kind (Union[Unset, list[ListCopySignalsKindItem]]):
        action (Union[Unset, list[ListCopySignalsActionItem]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopySignalPage, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            from_=from_,
            to=to,
            leader_id=leader_id,
            kind=kind,
            action=action,
        )
    ).parsed
