from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...models.terminal_update import TerminalUpdate
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: TerminalUpdate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/terminals/{id}".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantTerminal]:
    if response.status_code == 200:
        response_200 = TenantTerminal.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TenantTerminal]]:
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
    body: TerminalUpdate,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Change a running terminal - today its refresh rate

     Written at once and applied by the terminal's cell within a minute, without a restart. A rate faster
    than the farm's is 422 with `details.allowed`. A faster rate that the terminal's cell no longer has
    room for is 409 `no_room` with `details.fastest_that_fits`: the terminal is never moved to make
    room. Another tenant's terminal is 404.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalUpdate): What a tenant may change on a running terminal. Send only the
            fields to change

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
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
    body: TerminalUpdate,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Change a running terminal - today its refresh rate

     Written at once and applied by the terminal's cell within a minute, without a restart. A rate faster
    than the farm's is 422 with `details.allowed`. A faster rate that the terminal's cell no longer has
    room for is 409 `no_room` with `details.fastest_that_fits`: the terminal is never moved to make
    room. Another tenant's terminal is 404.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalUpdate): What a tenant may change on a running terminal. Send only the
            fields to change

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminal]
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
    body: TerminalUpdate,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Change a running terminal - today its refresh rate

     Written at once and applied by the terminal's cell within a minute, without a restart. A rate faster
    than the farm's is 422 with `details.allowed`. A faster rate that the terminal's cell no longer has
    room for is 409 `no_room` with `details.fastest_that_fits`: the terminal is never moved to make
    room. Another tenant's terminal is 404.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalUpdate): What a tenant may change on a running terminal. Send only the
            fields to change

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
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
    body: TerminalUpdate,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Change a running terminal - today its refresh rate

     Written at once and applied by the terminal's cell within a minute, without a restart. A rate faster
    than the farm's is 422 with `details.allowed`. A faster rate that the terminal's cell no longer has
    room for is 409 `no_room` with `details.fastest_that_fits`: the terminal is never moved to make
    room. Another tenant's terminal is 404.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalUpdate): What a tenant may change on a running terminal. Send only the
            fields to change

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminal]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
