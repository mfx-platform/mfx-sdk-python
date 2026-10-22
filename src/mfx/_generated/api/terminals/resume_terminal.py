from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/resume".format(
            id=id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantTerminal]:
    if response.status_code == 202:
        response_202 = TenantTerminal.from_dict(response.json())

        return response_202

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
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Resume a drained terminal - placed and logged in again exactly as a new terminal is

     Place a DRAINED terminal again. It keeps its id and goes back to REQUESTED, and from there it is
    placed and logged in exactly as a new terminal is. What can never work is refused now, before
    anything is written: its farm not taking terminals (409 `state_error`), its broker or server no
    longer supported (422 `unprocessable`, or 409 `broker_not_supported`), a usage or an instrument
    count its farm no longer offers (422). Otherwise it waits in REQUESTED until its farm has room, as a
    new terminal does, and becomes ACTIVE through the normal login. It is billed again from when it is
    ACTIVE. A terminal already REQUESTED, PROVISIONING, LOGGING_IN or ACTIVE is answered as it is: a
    resume sent twice is one resume. A DRAINING terminal is 409 `state_error` (resume it once it is
    DRAINED); so is any other state, and a suspended tenant's resume. No quota is counted: a DRAINED
    terminal never left the terminal quota.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
    """

    kwargs = _get_kwargs(
        id=id,
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
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Resume a drained terminal - placed and logged in again exactly as a new terminal is

     Place a DRAINED terminal again. It keeps its id and goes back to REQUESTED, and from there it is
    placed and logged in exactly as a new terminal is. What can never work is refused now, before
    anything is written: its farm not taking terminals (409 `state_error`), its broker or server no
    longer supported (422 `unprocessable`, or 409 `broker_not_supported`), a usage or an instrument
    count its farm no longer offers (422). Otherwise it waits in REQUESTED until its farm has room, as a
    new terminal does, and becomes ACTIVE through the normal login. It is billed again from when it is
    ACTIVE. A terminal already REQUESTED, PROVISIONING, LOGGING_IN or ACTIVE is answered as it is: a
    resume sent twice is one resume. A DRAINING terminal is 409 `state_error` (resume it once it is
    DRAINED); so is any other state, and a suspended tenant's resume. No quota is counted: a DRAINED
    terminal never left the terminal quota.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminal]
    """

    return sync_detailed(
        id=id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Resume a drained terminal - placed and logged in again exactly as a new terminal is

     Place a DRAINED terminal again. It keeps its id and goes back to REQUESTED, and from there it is
    placed and logged in exactly as a new terminal is. What can never work is refused now, before
    anything is written: its farm not taking terminals (409 `state_error`), its broker or server no
    longer supported (422 `unprocessable`, or 409 `broker_not_supported`), a usage or an instrument
    count its farm no longer offers (422). Otherwise it waits in REQUESTED until its farm has room, as a
    new terminal does, and becomes ACTIVE through the normal login. It is billed again from when it is
    ACTIVE. A terminal already REQUESTED, PROVISIONING, LOGGING_IN or ACTIVE is answered as it is: a
    resume sent twice is one resume. A DRAINING terminal is 409 `state_error` (resume it once it is
    DRAINED); so is any other state, and a suspended tenant's resume. No quota is counted: a DRAINED
    terminal never left the terminal quota.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
    """

    kwargs = _get_kwargs(
        id=id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Resume a drained terminal - placed and logged in again exactly as a new terminal is

     Place a DRAINED terminal again. It keeps its id and goes back to REQUESTED, and from there it is
    placed and logged in exactly as a new terminal is. What can never work is refused now, before
    anything is written: its farm not taking terminals (409 `state_error`), its broker or server no
    longer supported (422 `unprocessable`, or 409 `broker_not_supported`), a usage or an instrument
    count its farm no longer offers (422). Otherwise it waits in REQUESTED until its farm has room, as a
    new terminal does, and becomes ACTIVE through the normal login. It is billed again from when it is
    ACTIVE. A terminal already REQUESTED, PROVISIONING, LOGGING_IN or ACTIVE is answered as it is: a
    resume sent twice is one resume. A DRAINING terminal is 409 `state_error` (resume it once it is
    DRAINED); so is any other state, and a suspended tenant's resume. No quota is counted: a DRAINED
    terminal never left the terminal quota.

    Args:
        id (UUID):
        idempotency_key (str):

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
            idempotency_key=idempotency_key,
        )
    ).parsed
