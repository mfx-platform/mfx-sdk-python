from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_group_close import CopyGroupClose
from ...models.copy_group_close_result import CopyGroupCloseResult
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: CopyGroupClose,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/groups/{id}/close".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyGroupCloseResult, Error]:
    if response.status_code == 202:
        response_202 = CopyGroupCloseResult.from_dict(response.json())

        return response_202

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyGroupCloseResult, Error]]:
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
    body: CopyGroupClose,
    idempotency_key: str,
) -> Response[Union[CopyGroupCloseResult, Error]]:
    """Close the copied positions of every live member of the group (Enterprise); the follows are kept

     One requested close a member that has not unfollowed (`cause: group_close`), all under one
    `batch_id`, covering the copied positions opened by leader deals signalled at or before this request
    (`cutoff_at` is its moment); a position copied after it is not covered. Only the volume copied is
    closed, never the account's own. `pause` is required: `true` pauses the group in the same act, so
    each member's next mandate copies closes only and carries its close; `false` leaves the group's
    state as it is, and later leader deals are copied again. Progress is `GET /copy/closes?batch_id=`,
    and each close sends one `copy.closed`. A copy of a covered deal can still fill until that deal's
    signal expires, so each close stays `pending` until the cutoff plus the longest signal lifetime of
    the group's leaders plus two minutes, closing such late copies too, even when every position it
    listed is closed. A member that already had a close pending has it superseded, the wider cover kept.
    A repeated Idempotency-Key answers the same batch.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupClose):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroupCloseResult, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyGroupClose,
    idempotency_key: str,
) -> Optional[Union[CopyGroupCloseResult, Error]]:
    """Close the copied positions of every live member of the group (Enterprise); the follows are kept

     One requested close a member that has not unfollowed (`cause: group_close`), all under one
    `batch_id`, covering the copied positions opened by leader deals signalled at or before this request
    (`cutoff_at` is its moment); a position copied after it is not covered. Only the volume copied is
    closed, never the account's own. `pause` is required: `true` pauses the group in the same act, so
    each member's next mandate copies closes only and carries its close; `false` leaves the group's
    state as it is, and later leader deals are copied again. Progress is `GET /copy/closes?batch_id=`,
    and each close sends one `copy.closed`. A copy of a covered deal can still fill until that deal's
    signal expires, so each close stays `pending` until the cutoff plus the longest signal lifetime of
    the group's leaders plus two minutes, closing such late copies too, even when every position it
    listed is closed. A member that already had a close pending has it superseded, the wider cover kept.
    A repeated Idempotency-Key answers the same batch.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupClose):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroupCloseResult, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyGroupClose,
    idempotency_key: str,
) -> Response[Union[CopyGroupCloseResult, Error]]:
    """Close the copied positions of every live member of the group (Enterprise); the follows are kept

     One requested close a member that has not unfollowed (`cause: group_close`), all under one
    `batch_id`, covering the copied positions opened by leader deals signalled at or before this request
    (`cutoff_at` is its moment); a position copied after it is not covered. Only the volume copied is
    closed, never the account's own. `pause` is required: `true` pauses the group in the same act, so
    each member's next mandate copies closes only and carries its close; `false` leaves the group's
    state as it is, and later leader deals are copied again. Progress is `GET /copy/closes?batch_id=`,
    and each close sends one `copy.closed`. A copy of a covered deal can still fill until that deal's
    signal expires, so each close stays `pending` until the cutoff plus the longest signal lifetime of
    the group's leaders plus two minutes, closing such late copies too, even when every position it
    listed is closed. A member that already had a close pending has it superseded, the wider cover kept.
    A repeated Idempotency-Key answers the same batch.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupClose):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroupCloseResult, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyGroupClose,
    idempotency_key: str,
) -> Optional[Union[CopyGroupCloseResult, Error]]:
    """Close the copied positions of every live member of the group (Enterprise); the follows are kept

     One requested close a member that has not unfollowed (`cause: group_close`), all under one
    `batch_id`, covering the copied positions opened by leader deals signalled at or before this request
    (`cutoff_at` is its moment); a position copied after it is not covered. Only the volume copied is
    closed, never the account's own. `pause` is required: `true` pauses the group in the same act, so
    each member's next mandate copies closes only and carries its close; `false` leaves the group's
    state as it is, and later leader deals are copied again. Progress is `GET /copy/closes?batch_id=`,
    and each close sends one `copy.closed`. A copy of a covered deal can still fill until that deal's
    signal expires, so each close stays `pending` until the cutoff plus the longest signal lifetime of
    the group's leaders plus two minutes, closing such late copies too, even when every position it
    listed is closed. A member that already had a close pending has it superseded, the wider cover kept.
    A repeated Idempotency-Key answers the same batch.

    Args:
        id (UUID):
        idempotency_key (str):
        body (CopyGroupClose):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroupCloseResult, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
