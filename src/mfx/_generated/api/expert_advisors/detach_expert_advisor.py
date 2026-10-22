from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.operation_accepted import OperationAccepted
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    reason: str,
    queue: Union[Unset, bool] = False,
    confirm_open_positions: Union[Unset, bool] = False,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    params["reason"] = reason

    params["queue"] = queue

    params["confirm_open_positions"] = confirm_open_positions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/terminals/{id}/expert-advisor".format(
            id=id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, OperationAccepted]:
    if response.status_code == 202:
        response_202 = OperationAccepted.from_dict(response.json())

        return response_202

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, OperationAccepted]]:
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
    reason: str,
    queue: Union[Unset, bool] = False,
    confirm_open_positions: Union[Unset, bool] = False,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Detach the EA from a terminal - governed; the terminal is relaunched from a fresh copy of its folder
    without it

     409 `no_ea_attached` when the terminal carries none. Then the seven rules of a governed operation,
    as on restartTerminal.

    Args:
        id (UUID):
        reason (str):
        queue (Union[Unset, bool]):  Default: False.
        confirm_open_positions (Union[Unset, bool]):  Default: False.
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OperationAccepted]]
    """

    kwargs = _get_kwargs(
        id=id,
        reason=reason,
        queue=queue,
        confirm_open_positions=confirm_open_positions,
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
    reason: str,
    queue: Union[Unset, bool] = False,
    confirm_open_positions: Union[Unset, bool] = False,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Detach the EA from a terminal - governed; the terminal is relaunched from a fresh copy of its folder
    without it

     409 `no_ea_attached` when the terminal carries none. Then the seven rules of a governed operation,
    as on restartTerminal.

    Args:
        id (UUID):
        reason (str):
        queue (Union[Unset, bool]):  Default: False.
        confirm_open_positions (Union[Unset, bool]):  Default: False.
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OperationAccepted]
    """

    return sync_detailed(
        id=id,
        client=client,
        reason=reason,
        queue=queue,
        confirm_open_positions=confirm_open_positions,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    reason: str,
    queue: Union[Unset, bool] = False,
    confirm_open_positions: Union[Unset, bool] = False,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Detach the EA from a terminal - governed; the terminal is relaunched from a fresh copy of its folder
    without it

     409 `no_ea_attached` when the terminal carries none. Then the seven rules of a governed operation,
    as on restartTerminal.

    Args:
        id (UUID):
        reason (str):
        queue (Union[Unset, bool]):  Default: False.
        confirm_open_positions (Union[Unset, bool]):  Default: False.
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OperationAccepted]]
    """

    kwargs = _get_kwargs(
        id=id,
        reason=reason,
        queue=queue,
        confirm_open_positions=confirm_open_positions,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    reason: str,
    queue: Union[Unset, bool] = False,
    confirm_open_positions: Union[Unset, bool] = False,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Detach the EA from a terminal - governed; the terminal is relaunched from a fresh copy of its folder
    without it

     409 `no_ea_attached` when the terminal carries none. Then the seven rules of a governed operation,
    as on restartTerminal.

    Args:
        id (UUID):
        reason (str):
        queue (Union[Unset, bool]):  Default: False.
        confirm_open_positions (Union[Unset, bool]):  Default: False.
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OperationAccepted]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            reason=reason,
            queue=queue,
            confirm_open_positions=confirm_open_positions,
            idempotency_key=idempotency_key,
        )
    ).parsed
