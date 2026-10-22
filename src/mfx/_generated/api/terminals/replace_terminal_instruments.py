from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...models.terminal_instruments import TerminalInstruments
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: TerminalInstruments,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/terminals/{id}/instruments".format(
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
    body: TerminalInstruments,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Replace a terminal's instrument list in place — same terminal, same credential, same history

     A tenant who mistyped a symbol, or whose broker renamed one, changes the list here instead of
    retiring the terminal and creating another. The list is written at once, and the terminal's cell re-
    subscribes within a minute. Names are checked against the tenant's own catalogue for the terminal's
    server: the account types this terminal has reported, or, before it has reported any, every name the
    tenant's terminals on that server have. A server the tenant has no catalogue for yet cannot be
    checked; the list is accepted and the response carries `X-MFX-Warning: instruments_unchecked`. The
    same list again changes nothing. `depth_instruments` names the symbols whose order book the terminal
    reads; the cell starts or stops reading them within the same minute.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalInstruments): The whole list, replacing the one the terminal has. Not a
            patch: send every instrument the terminal should watch. An empty list is allowed (an
            execution-only terminal watches nothing).

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
    body: TerminalInstruments,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Replace a terminal's instrument list in place — same terminal, same credential, same history

     A tenant who mistyped a symbol, or whose broker renamed one, changes the list here instead of
    retiring the terminal and creating another. The list is written at once, and the terminal's cell re-
    subscribes within a minute. Names are checked against the tenant's own catalogue for the terminal's
    server: the account types this terminal has reported, or, before it has reported any, every name the
    tenant's terminals on that server have. A server the tenant has no catalogue for yet cannot be
    checked; the list is accepted and the response carries `X-MFX-Warning: instruments_unchecked`. The
    same list again changes nothing. `depth_instruments` names the symbols whose order book the terminal
    reads; the cell starts or stops reading them within the same minute.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalInstruments): The whole list, replacing the one the terminal has. Not a
            patch: send every instrument the terminal should watch. An empty list is allowed (an
            execution-only terminal watches nothing).

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
    body: TerminalInstruments,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Replace a terminal's instrument list in place — same terminal, same credential, same history

     A tenant who mistyped a symbol, or whose broker renamed one, changes the list here instead of
    retiring the terminal and creating another. The list is written at once, and the terminal's cell re-
    subscribes within a minute. Names are checked against the tenant's own catalogue for the terminal's
    server: the account types this terminal has reported, or, before it has reported any, every name the
    tenant's terminals on that server have. A server the tenant has no catalogue for yet cannot be
    checked; the list is accepted and the response carries `X-MFX-Warning: instruments_unchecked`. The
    same list again changes nothing. `depth_instruments` names the symbols whose order book the terminal
    reads; the cell starts or stops reading them within the same minute.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalInstruments): The whole list, replacing the one the terminal has. Not a
            patch: send every instrument the terminal should watch. An empty list is allowed (an
            execution-only terminal watches nothing).

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
    body: TerminalInstruments,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Replace a terminal's instrument list in place — same terminal, same credential, same history

     A tenant who mistyped a symbol, or whose broker renamed one, changes the list here instead of
    retiring the terminal and creating another. The list is written at once, and the terminal's cell re-
    subscribes within a minute. Names are checked against the tenant's own catalogue for the terminal's
    server: the account types this terminal has reported, or, before it has reported any, every name the
    tenant's terminals on that server have. A server the tenant has no catalogue for yet cannot be
    checked; the list is accepted and the response carries `X-MFX-Warning: instruments_unchecked`. The
    same list again changes nothing. `depth_instruments` names the symbols whose order book the terminal
    reads; the cell starts or stops reading them within the same minute.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalInstruments): The whole list, replacing the one the terminal has. Not a
            patch: send every instrument the terminal should watch. An empty list is allowed (an
            execution-only terminal watches nothing).

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
