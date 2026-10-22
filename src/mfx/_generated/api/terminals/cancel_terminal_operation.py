from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.terminal_operation import TerminalOperation
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    operation_id: UUID,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/terminals/{id}/operations/{operation_id}".format(
            id=id,
            operation_id=operation_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TerminalOperation]:
    if response.status_code == 200:
        response_200 = TerminalOperation.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TerminalOperation]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Response[Union[Error, TerminalOperation]]:
    """Cancel a queued operation — only while it waits

     Settles a QUEUED operation CANCELLED; nothing ran and the terminal is untouched. An operation that
    has started is not cancelled here. Audited, and announced as `terminal.operation_changed`. A tenant
    cancels what one of its own keys asked for: an operation the platform's operators queued on its
    terminal is 403 `forbidden`. Cancelling an operation that is already CANCELLED answers it again
    (200), so a cancel sent twice is one cancel.

    Args:
        id (UUID):
        operation_id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalOperation]]
    """

    kwargs = _get_kwargs(
        id=id,
        operation_id=operation_id,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Optional[Union[Error, TerminalOperation]]:
    """Cancel a queued operation — only while it waits

     Settles a QUEUED operation CANCELLED; nothing ran and the terminal is untouched. An operation that
    has started is not cancelled here. Audited, and announced as `terminal.operation_changed`. A tenant
    cancels what one of its own keys asked for: an operation the platform's operators queued on its
    terminal is 403 `forbidden`. Cancelling an operation that is already CANCELLED answers it again
    (200), so a cancel sent twice is one cancel.

    Args:
        id (UUID):
        operation_id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalOperation]
    """

    return sync_detailed(
        id=id,
        operation_id=operation_id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Response[Union[Error, TerminalOperation]]:
    """Cancel a queued operation — only while it waits

     Settles a QUEUED operation CANCELLED; nothing ran and the terminal is untouched. An operation that
    has started is not cancelled here. Audited, and announced as `terminal.operation_changed`. A tenant
    cancels what one of its own keys asked for: an operation the platform's operators queued on its
    terminal is 403 `forbidden`. Cancelling an operation that is already CANCELLED answers it again
    (200), so a cancel sent twice is one cancel.

    Args:
        id (UUID):
        operation_id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TerminalOperation]]
    """

    kwargs = _get_kwargs(
        id=id,
        operation_id=operation_id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    operation_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Optional[Union[Error, TerminalOperation]]:
    """Cancel a queued operation — only while it waits

     Settles a QUEUED operation CANCELLED; nothing ran and the terminal is untouched. An operation that
    has started is not cancelled here. Audited, and announced as `terminal.operation_changed`. A tenant
    cancels what one of its own keys asked for: an operation the platform's operators queued on its
    terminal is 403 `forbidden`. Cancelling an operation that is already CANCELLED answers it again
    (200), so a cancel sent twice is one cancel.

    Args:
        id (UUID):
        operation_id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TerminalOperation]
    """

    return (
        await asyncio_detailed(
            id=id,
            operation_id=operation_id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed
