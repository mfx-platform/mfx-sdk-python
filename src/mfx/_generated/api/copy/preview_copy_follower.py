from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_preview import CopyPreview
from ...models.copy_preview_request import CopyPreviewRequest
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CopyPreviewRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/followers/preview",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyPreview, Error]:
    if response.status_code == 200:
        response_200 = CopyPreview.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyPreview, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyPreviewRequest,
) -> Response[Union[CopyPreview, Error]]:
    """What a follow would do before it is made - each leader symbol's follower symbol, how it was matched,
    and what a leader volume becomes

     Read-only: nothing is created and no Idempotency-Key is needed. The mandate is checked and compiled
    exactly as a follow would be, against the follower account's own symbols and figures now: for each
    row, the follower symbol, how it was found (`own_map`, `instrument_key`, `same_name` or
    `automatic`), and the follower's volume for the leader volume given, rounded down to the follower
    symbol's step; or the reason it would be refused (`mapping`, `min_volume`, `no_stop`,
    `no_conversion`). A follow the venue cannot honour is answered here too, in `refusal`, with the same
    reason a follow would get. The figures are the accounts' at `inputs.read_at` and change as they do.

    Args:
        body (CopyPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyPreview, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyPreviewRequest,
) -> Optional[Union[CopyPreview, Error]]:
    """What a follow would do before it is made - each leader symbol's follower symbol, how it was matched,
    and what a leader volume becomes

     Read-only: nothing is created and no Idempotency-Key is needed. The mandate is checked and compiled
    exactly as a follow would be, against the follower account's own symbols and figures now: for each
    row, the follower symbol, how it was found (`own_map`, `instrument_key`, `same_name` or
    `automatic`), and the follower's volume for the leader volume given, rounded down to the follower
    symbol's step; or the reason it would be refused (`mapping`, `min_volume`, `no_stop`,
    `no_conversion`). A follow the venue cannot honour is answered here too, in `refusal`, with the same
    reason a follow would get. The figures are the accounts' at `inputs.read_at` and change as they do.

    Args:
        body (CopyPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyPreview, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyPreviewRequest,
) -> Response[Union[CopyPreview, Error]]:
    """What a follow would do before it is made - each leader symbol's follower symbol, how it was matched,
    and what a leader volume becomes

     Read-only: nothing is created and no Idempotency-Key is needed. The mandate is checked and compiled
    exactly as a follow would be, against the follower account's own symbols and figures now: for each
    row, the follower symbol, how it was found (`own_map`, `instrument_key`, `same_name` or
    `automatic`), and the follower's volume for the leader volume given, rounded down to the follower
    symbol's step; or the reason it would be refused (`mapping`, `min_volume`, `no_stop`,
    `no_conversion`). A follow the venue cannot honour is answered here too, in `refusal`, with the same
    reason a follow would get. The figures are the accounts' at `inputs.read_at` and change as they do.

    Args:
        body (CopyPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyPreview, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyPreviewRequest,
) -> Optional[Union[CopyPreview, Error]]:
    """What a follow would do before it is made - each leader symbol's follower symbol, how it was matched,
    and what a leader volume becomes

     Read-only: nothing is created and no Idempotency-Key is needed. The mandate is checked and compiled
    exactly as a follow would be, against the follower account's own symbols and figures now: for each
    row, the follower symbol, how it was found (`own_map`, `instrument_key`, `same_name` or
    `automatic`), and the follower's volume for the leader volume given, rounded down to the follower
    symbol's step; or the reason it would be refused (`mapping`, `min_volume`, `no_stop`,
    `no_conversion`). A follow the venue cannot honour is answered here too, in `refusal`, with the same
    reason a follow would get. The figures are the accounts' at `inputs.read_at` and change as they do.

    Args:
        body (CopyPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyPreview, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
