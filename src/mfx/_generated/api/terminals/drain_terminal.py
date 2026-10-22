from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...models.terminal_drain import TerminalDrain
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: TerminalDrain,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/drain".format(
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
    body: TerminalDrain,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Drain a terminal - it is closed gracefully and kept, holding no cell and not billed, until you
    resume it

     Close the terminal gracefully and keep it. A drain is a governed operation under the rules of
    restartTerminal: one lifecycle operation per terminal at a time (409 `operation_in_progress`), a
    cooldown per terminal (429 `cooldown`), open positions need `confirm_open_positions` (409
    `positions_open`) while the platform's open-position confirmation setting is on, the tenant rate and
    concurrency, counted with moves and retires (429 `tenant_rate`, `concurrency`), and the farm blast
    radius (429 `farm_capacity`). A refusal names its rule in `error.code` and carries `Retry-After`
    when waiting helps. A drain is never queued. Offered for an ACTIVE or OFFLINE terminal; any other
    state is 409 `state_error`. The answer is the terminal DRAINING. Its cell stops it as it stops a
    retired terminal; it is then DRAINED (`terminal.state_changed`) and the operation, kind `drain`,
    succeeds (`terminal.operation_changed`). A DRAINED terminal keeps its id, broker account and
    credential, instruments, depth instruments, labels, refresh rate and expert-advisor attachment
    record; it runs nothing (no MT5 session, no expert advisor), holds no cell slot, and is not billed
    from the moment it is DRAINED. It still counts toward the terminal quota (terminals that are not
    RETIRED) and toward its login's terminal and session limits, because it keeps its account and logs
    in again when resumed. Resume it with POST /terminals/{id}/resume; retire it with DELETE
    /terminals/{id}, at once since it holds nothing. A DELETE while it is DRAINING makes the drain end
    in RETIRED instead. The same Idempotency-Key answers the terminal as it now is; a different body
    under it is 409 `conflict`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalDrain): A drain. The body is optional; omitted, the reason is recorded as
            not given

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
    body: TerminalDrain,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Drain a terminal - it is closed gracefully and kept, holding no cell and not billed, until you
    resume it

     Close the terminal gracefully and keep it. A drain is a governed operation under the rules of
    restartTerminal: one lifecycle operation per terminal at a time (409 `operation_in_progress`), a
    cooldown per terminal (429 `cooldown`), open positions need `confirm_open_positions` (409
    `positions_open`) while the platform's open-position confirmation setting is on, the tenant rate and
    concurrency, counted with moves and retires (429 `tenant_rate`, `concurrency`), and the farm blast
    radius (429 `farm_capacity`). A refusal names its rule in `error.code` and carries `Retry-After`
    when waiting helps. A drain is never queued. Offered for an ACTIVE or OFFLINE terminal; any other
    state is 409 `state_error`. The answer is the terminal DRAINING. Its cell stops it as it stops a
    retired terminal; it is then DRAINED (`terminal.state_changed`) and the operation, kind `drain`,
    succeeds (`terminal.operation_changed`). A DRAINED terminal keeps its id, broker account and
    credential, instruments, depth instruments, labels, refresh rate and expert-advisor attachment
    record; it runs nothing (no MT5 session, no expert advisor), holds no cell slot, and is not billed
    from the moment it is DRAINED. It still counts toward the terminal quota (terminals that are not
    RETIRED) and toward its login's terminal and session limits, because it keeps its account and logs
    in again when resumed. Resume it with POST /terminals/{id}/resume; retire it with DELETE
    /terminals/{id}, at once since it holds nothing. A DELETE while it is DRAINING makes the drain end
    in RETIRED instead. The same Idempotency-Key answers the terminal as it now is; a different body
    under it is 409 `conflict`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalDrain): A drain. The body is optional; omitted, the reason is recorded as
            not given

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
    body: TerminalDrain,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Drain a terminal - it is closed gracefully and kept, holding no cell and not billed, until you
    resume it

     Close the terminal gracefully and keep it. A drain is a governed operation under the rules of
    restartTerminal: one lifecycle operation per terminal at a time (409 `operation_in_progress`), a
    cooldown per terminal (429 `cooldown`), open positions need `confirm_open_positions` (409
    `positions_open`) while the platform's open-position confirmation setting is on, the tenant rate and
    concurrency, counted with moves and retires (429 `tenant_rate`, `concurrency`), and the farm blast
    radius (429 `farm_capacity`). A refusal names its rule in `error.code` and carries `Retry-After`
    when waiting helps. A drain is never queued. Offered for an ACTIVE or OFFLINE terminal; any other
    state is 409 `state_error`. The answer is the terminal DRAINING. Its cell stops it as it stops a
    retired terminal; it is then DRAINED (`terminal.state_changed`) and the operation, kind `drain`,
    succeeds (`terminal.operation_changed`). A DRAINED terminal keeps its id, broker account and
    credential, instruments, depth instruments, labels, refresh rate and expert-advisor attachment
    record; it runs nothing (no MT5 session, no expert advisor), holds no cell slot, and is not billed
    from the moment it is DRAINED. It still counts toward the terminal quota (terminals that are not
    RETIRED) and toward its login's terminal and session limits, because it keeps its account and logs
    in again when resumed. Resume it with POST /terminals/{id}/resume; retire it with DELETE
    /terminals/{id}, at once since it holds nothing. A DELETE while it is DRAINING makes the drain end
    in RETIRED instead. The same Idempotency-Key answers the terminal as it now is; a different body
    under it is 409 `conflict`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalDrain): A drain. The body is optional; omitted, the reason is recorded as
            not given

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
    body: TerminalDrain,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Drain a terminal - it is closed gracefully and kept, holding no cell and not billed, until you
    resume it

     Close the terminal gracefully and keep it. A drain is a governed operation under the rules of
    restartTerminal: one lifecycle operation per terminal at a time (409 `operation_in_progress`), a
    cooldown per terminal (429 `cooldown`), open positions need `confirm_open_positions` (409
    `positions_open`) while the platform's open-position confirmation setting is on, the tenant rate and
    concurrency, counted with moves and retires (429 `tenant_rate`, `concurrency`), and the farm blast
    radius (429 `farm_capacity`). A refusal names its rule in `error.code` and carries `Retry-After`
    when waiting helps. A drain is never queued. Offered for an ACTIVE or OFFLINE terminal; any other
    state is 409 `state_error`. The answer is the terminal DRAINING. Its cell stops it as it stops a
    retired terminal; it is then DRAINED (`terminal.state_changed`) and the operation, kind `drain`,
    succeeds (`terminal.operation_changed`). A DRAINED terminal keeps its id, broker account and
    credential, instruments, depth instruments, labels, refresh rate and expert-advisor attachment
    record; it runs nothing (no MT5 session, no expert advisor), holds no cell slot, and is not billed
    from the moment it is DRAINED. It still counts toward the terminal quota (terminals that are not
    RETIRED) and toward its login's terminal and session limits, because it keeps its account and logs
    in again when resumed. Resume it with POST /terminals/{id}/resume; retire it with DELETE
    /terminals/{id}, at once since it holds nothing. A DELETE while it is DRAINING makes the drain end
    in RETIRED instead. The same Idempotency-Key answers the terminal as it now is; a different body
    under it is 409 `conflict`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalDrain): A drain. The body is optional; omitted, the reason is recorded as
            not given

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
