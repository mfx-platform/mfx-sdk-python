from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_action import BulkAction
from ...models.bulk_terminal_ask import BulkTerminalAsk
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: BulkTerminalAsk,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals:restart",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BulkAction, Error]:
    if response.status_code == 202:
        response_202 = BulkAction.from_dict(response.json())

        return response_202

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BulkAction, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BulkTerminalAsk,
    idempotency_key: str,
) -> Response[Union[BulkAction, Error]]:
    """Restart many of your terminals at once - accepted at once, carried out at the pace of their cells

     One request for many terminals. Each terminal the filter names is judged by the same rules as `POST
    /terminals/{id}/restart`; a refused one is listed in `refused` with its rule's code and the rest are
    taken. Each taken terminal is one operation in its cell's line, and each cell carries them at its
    own pace, so the terminals already running on it are not slowed. The answer is 202 with the action
    and its expected finish; follow it at `GET /bulk-actions/{id}`, or each operation as usual. The
    items never expire. The same Idempotency-Key returns the same action. 422 `validation_error` when no
    filter is given.

    Args:
        idempotency_key (str):
        body (BulkTerminalAsk): Which of your terminals a bulk restart or retire takes, and why.
            At least one of the filters; given together they narrow each other

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BulkAction, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BulkTerminalAsk,
    idempotency_key: str,
) -> Optional[Union[BulkAction, Error]]:
    """Restart many of your terminals at once - accepted at once, carried out at the pace of their cells

     One request for many terminals. Each terminal the filter names is judged by the same rules as `POST
    /terminals/{id}/restart`; a refused one is listed in `refused` with its rule's code and the rest are
    taken. Each taken terminal is one operation in its cell's line, and each cell carries them at its
    own pace, so the terminals already running on it are not slowed. The answer is 202 with the action
    and its expected finish; follow it at `GET /bulk-actions/{id}`, or each operation as usual. The
    items never expire. The same Idempotency-Key returns the same action. 422 `validation_error` when no
    filter is given.

    Args:
        idempotency_key (str):
        body (BulkTerminalAsk): Which of your terminals a bulk restart or retire takes, and why.
            At least one of the filters; given together they narrow each other

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BulkAction, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BulkTerminalAsk,
    idempotency_key: str,
) -> Response[Union[BulkAction, Error]]:
    """Restart many of your terminals at once - accepted at once, carried out at the pace of their cells

     One request for many terminals. Each terminal the filter names is judged by the same rules as `POST
    /terminals/{id}/restart`; a refused one is listed in `refused` with its rule's code and the rest are
    taken. Each taken terminal is one operation in its cell's line, and each cell carries them at its
    own pace, so the terminals already running on it are not slowed. The answer is 202 with the action
    and its expected finish; follow it at `GET /bulk-actions/{id}`, or each operation as usual. The
    items never expire. The same Idempotency-Key returns the same action. 422 `validation_error` when no
    filter is given.

    Args:
        idempotency_key (str):
        body (BulkTerminalAsk): Which of your terminals a bulk restart or retire takes, and why.
            At least one of the filters; given together they narrow each other

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BulkAction, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BulkTerminalAsk,
    idempotency_key: str,
) -> Optional[Union[BulkAction, Error]]:
    """Restart many of your terminals at once - accepted at once, carried out at the pace of their cells

     One request for many terminals. Each terminal the filter names is judged by the same rules as `POST
    /terminals/{id}/restart`; a refused one is listed in `refused` with its rule's code and the rest are
    taken. Each taken terminal is one operation in its cell's line, and each cell carries them at its
    own pace, so the terminals already running on it are not slowed. The answer is 202 with the action
    and its expected finish; follow it at `GET /bulk-actions/{id}`, or each operation as usual. The
    items never expire. The same Idempotency-Key returns the same action. 422 `validation_error` when no
    filter is given.

    Args:
        idempotency_key (str):
        body (BulkTerminalAsk): Which of your terminals a bulk restart or retire takes, and why.
            At least one of the filters; given together they narrow each other

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BulkAction, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
