import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deal_page import DealPage
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    from_: datetime.datetime,
    to: datetime.datetime,
    position: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params["position"] = position

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/terminals/{id}/history/deals".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DealPage, Error]:
    if response.status_code == 200:
        response_200 = DealPage.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DealPage, Error]]:
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
    from_: datetime.datetime,
    to: datetime.datetime,
    position: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[DealPage, Error]]:
    """Deals in a window, newest first by (time, deal), optionally of one position

     Read from the broker on demand with a read-only request through the terminal, bounded at 10 s.
    Nothing is stored: the broker is the book of record for history. `to - from` is at most 31 days;
    `next_cursor` continues the window before the oldest deal returned. With `position`, only that
    position's deals are returned: the window is still read from the broker and the other deals are left
    out, so a page can hold fewer than `limit`, and even none, while `next_cursor` is not null. Keep
    asking until it is null.

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (datetime.datetime):
        position (Union[Unset, int]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DealPage, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        from_=from_,
        to=to,
        position=position,
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
    from_: datetime.datetime,
    to: datetime.datetime,
    position: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[DealPage, Error]]:
    """Deals in a window, newest first by (time, deal), optionally of one position

     Read from the broker on demand with a read-only request through the terminal, bounded at 10 s.
    Nothing is stored: the broker is the book of record for history. `to - from` is at most 31 days;
    `next_cursor` continues the window before the oldest deal returned. With `position`, only that
    position's deals are returned: the window is still read from the broker and the other deals are left
    out, so a page can hold fewer than `limit`, and even none, while `next_cursor` is not null. Keep
    asking until it is null.

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (datetime.datetime):
        position (Union[Unset, int]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DealPage, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        from_=from_,
        to=to,
        position=position,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    position: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Response[Union[DealPage, Error]]:
    """Deals in a window, newest first by (time, deal), optionally of one position

     Read from the broker on demand with a read-only request through the terminal, bounded at 10 s.
    Nothing is stored: the broker is the book of record for history. `to - from` is at most 31 days;
    `next_cursor` continues the window before the oldest deal returned. With `position`, only that
    position's deals are returned: the window is still read from the broker and the other deals are left
    out, so a page can hold fewer than `limit`, and even none, while `next_cursor` is not null. Keep
    asking until it is null.

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (datetime.datetime):
        position (Union[Unset, int]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DealPage, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        from_=from_,
        to=to,
        position=position,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime,
    to: datetime.datetime,
    position: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[DealPage, Error]]:
    """Deals in a window, newest first by (time, deal), optionally of one position

     Read from the broker on demand with a read-only request through the terminal, bounded at 10 s.
    Nothing is stored: the broker is the book of record for history. `to - from` is at most 31 days;
    `next_cursor` continues the window before the oldest deal returned. With `position`, only that
    position's deals are returned: the window is still read from the broker and the other deals are left
    out, so a page can hold fewer than `limit`, and even none, while `next_cursor` is not null. Keep
    asking until it is null.

    Args:
        id (UUID):
        from_ (datetime.datetime):
        to (datetime.datetime):
        position (Union[Unset, int]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DealPage, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            from_=from_,
            to=to,
            position=position,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
