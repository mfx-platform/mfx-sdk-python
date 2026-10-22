from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.operation_accepted import OperationAccepted
from ...models.terminal_restart import TerminalRestart
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: TerminalRestart,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/restart".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
    body: TerminalRestart,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Restart a stuck terminal — governed, followed as an operation

     Close the terminal gracefully (60 s), stop it by force only if it will not close, relaunch it, and
    report SUCCEEDED only once it produces ticks again. Seven rules are checked in order before anything
    is written, the same guard the platform's automatic recovery takes: one lifecycle operation per
    terminal at a time (409 `operation_in_progress`), a cooldown per terminal (429 `cooldown`), open
    positions need `confirm_open_positions` (409 `positions_open`) while the platform's open-position
    confirmation setting is on (it is off unless an operator turns it on), a tenant rate (429
    `tenant_rate`), tenant concurrency (429 `concurrency`), a farm blast radius (429 `farm_capacity`),
    and the general budget. A refusal names its rule in `error.code` and carries `Retry-After` when
    waiting helps. With `queue: true` the four busy refusals (cooldown, tenant rate, concurrency, farm
    capacity) are held instead: 202 with `state: QUEUED` and where it waits, started by the platform
    when it can, and settled EXPIRED if it has not started by `queue.expires_at`. A terminal has at most
    one waiting operation: the same kind again returns it with `duplicate: true`; a stronger kind
    replaces it (it settles SUPERSEDED); a weaker one is 409 `superseded_by_waiting` with
    `details.operation_id`. The same Idempotency-Key returns the original operation; a different body
    under it is 409.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalRestart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OperationAccepted]]
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
    body: TerminalRestart,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Restart a stuck terminal — governed, followed as an operation

     Close the terminal gracefully (60 s), stop it by force only if it will not close, relaunch it, and
    report SUCCEEDED only once it produces ticks again. Seven rules are checked in order before anything
    is written, the same guard the platform's automatic recovery takes: one lifecycle operation per
    terminal at a time (409 `operation_in_progress`), a cooldown per terminal (429 `cooldown`), open
    positions need `confirm_open_positions` (409 `positions_open`) while the platform's open-position
    confirmation setting is on (it is off unless an operator turns it on), a tenant rate (429
    `tenant_rate`), tenant concurrency (429 `concurrency`), a farm blast radius (429 `farm_capacity`),
    and the general budget. A refusal names its rule in `error.code` and carries `Retry-After` when
    waiting helps. With `queue: true` the four busy refusals (cooldown, tenant rate, concurrency, farm
    capacity) are held instead: 202 with `state: QUEUED` and where it waits, started by the platform
    when it can, and settled EXPIRED if it has not started by `queue.expires_at`. A terminal has at most
    one waiting operation: the same kind again returns it with `duplicate: true`; a stronger kind
    replaces it (it settles SUPERSEDED); a weaker one is 409 `superseded_by_waiting` with
    `details.operation_id`. The same Idempotency-Key returns the original operation; a different body
    under it is 409.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalRestart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OperationAccepted]
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
    body: TerminalRestart,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Restart a stuck terminal — governed, followed as an operation

     Close the terminal gracefully (60 s), stop it by force only if it will not close, relaunch it, and
    report SUCCEEDED only once it produces ticks again. Seven rules are checked in order before anything
    is written, the same guard the platform's automatic recovery takes: one lifecycle operation per
    terminal at a time (409 `operation_in_progress`), a cooldown per terminal (429 `cooldown`), open
    positions need `confirm_open_positions` (409 `positions_open`) while the platform's open-position
    confirmation setting is on (it is off unless an operator turns it on), a tenant rate (429
    `tenant_rate`), tenant concurrency (429 `concurrency`), a farm blast radius (429 `farm_capacity`),
    and the general budget. A refusal names its rule in `error.code` and carries `Retry-After` when
    waiting helps. With `queue: true` the four busy refusals (cooldown, tenant rate, concurrency, farm
    capacity) are held instead: 202 with `state: QUEUED` and where it waits, started by the platform
    when it can, and settled EXPIRED if it has not started by `queue.expires_at`. A terminal has at most
    one waiting operation: the same kind again returns it with `duplicate: true`; a stronger kind
    replaces it (it settles SUPERSEDED); a weaker one is 409 `superseded_by_waiting` with
    `details.operation_id`. The same Idempotency-Key returns the original operation; a different body
    under it is 409.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalRestart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OperationAccepted]]
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
    body: TerminalRestart,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Restart a stuck terminal — governed, followed as an operation

     Close the terminal gracefully (60 s), stop it by force only if it will not close, relaunch it, and
    report SUCCEEDED only once it produces ticks again. Seven rules are checked in order before anything
    is written, the same guard the platform's automatic recovery takes: one lifecycle operation per
    terminal at a time (409 `operation_in_progress`), a cooldown per terminal (429 `cooldown`), open
    positions need `confirm_open_positions` (409 `positions_open`) while the platform's open-position
    confirmation setting is on (it is off unless an operator turns it on), a tenant rate (429
    `tenant_rate`), tenant concurrency (429 `concurrency`), a farm blast radius (429 `farm_capacity`),
    and the general budget. A refusal names its rule in `error.code` and carries `Retry-After` when
    waiting helps. With `queue: true` the four busy refusals (cooldown, tenant rate, concurrency, farm
    capacity) are held instead: 202 with `state: QUEUED` and where it waits, started by the platform
    when it can, and settled EXPIRED if it has not started by `queue.expires_at`. A terminal has at most
    one waiting operation: the same kind again returns it with `duplicate: true`; a stronger kind
    replaces it (it settles SUPERSEDED); a weaker one is 409 `superseded_by_waiting` with
    `details.operation_id`. The same Idempotency-Key returns the original operation; a different body
    under it is 409.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalRestart):

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
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
