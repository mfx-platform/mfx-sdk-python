from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...models.terminal_create import TerminalCreate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: TerminalCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals",
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
    *,
    client: Union[AuthenticatedClient, Client],
    body: TerminalCreate,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Provision a terminal — answered at once in state REQUESTED; the move to a cell is asynchronous

     A broker whose permission is `unknown` is accepted in the development environment with the response
    header `X-MFX-Warning: broker_permission_unknown`, and refused `broker_not_supported` in production.
    Refused at request time, never passed to a terminal: an unsupported broker or server (422), a farm
    that does not carry the usages (409), a redundancy the farm does not offer (409). The credential is
    submitted separately (`POST /terminals/{id}/credentials`), so a terminal can exist before its login
    does. Several terminals may use the same broker login, on every plan: the limits are checked when
    the credential is submitted. `farm_id` is optional: omitted, the platform chooses a farm and says
    which on the answer; none fits is 409 `no_farm`, with `details.why` one of `no_usage` (no farm you
    can use offers what this terminal needs), `no_region` (none in the server's region) or `no_room`.
    `refresh_ms` faster than the farm's rate is 422 with `details.allowed`; with no farm named, only
    farms that allow the rate are considered. A changed rate a cell cannot carry is the PATCH's 409
    `no_room`; create queues the terminal for placement. The tenant's plan decides the farm: enterprise
    and system tenants' terminals go to their own farms, standard tenants' to the shared farms. A named
    farm outside the plan is 409 `farm_not_in_plan`; with no farm named the platform chooses within the
    plan. A tenant already at its terminal quota is 409 `quota_exceeded` with `details {quota, in_use}`.

    Args:
        idempotency_key (str):
        body (TerminalCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
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
    body: TerminalCreate,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Provision a terminal — answered at once in state REQUESTED; the move to a cell is asynchronous

     A broker whose permission is `unknown` is accepted in the development environment with the response
    header `X-MFX-Warning: broker_permission_unknown`, and refused `broker_not_supported` in production.
    Refused at request time, never passed to a terminal: an unsupported broker or server (422), a farm
    that does not carry the usages (409), a redundancy the farm does not offer (409). The credential is
    submitted separately (`POST /terminals/{id}/credentials`), so a terminal can exist before its login
    does. Several terminals may use the same broker login, on every plan: the limits are checked when
    the credential is submitted. `farm_id` is optional: omitted, the platform chooses a farm and says
    which on the answer; none fits is 409 `no_farm`, with `details.why` one of `no_usage` (no farm you
    can use offers what this terminal needs), `no_region` (none in the server's region) or `no_room`.
    `refresh_ms` faster than the farm's rate is 422 with `details.allowed`; with no farm named, only
    farms that allow the rate are considered. A changed rate a cell cannot carry is the PATCH's 409
    `no_room`; create queues the terminal for placement. The tenant's plan decides the farm: enterprise
    and system tenants' terminals go to their own farms, standard tenants' to the shared farms. A named
    farm outside the plan is 409 `farm_not_in_plan`; with no farm named the platform chooses within the
    plan. A tenant already at its terminal quota is 409 `quota_exceeded` with `details {quota, in_use}`.

    Args:
        idempotency_key (str):
        body (TerminalCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminal]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TerminalCreate,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Provision a terminal — answered at once in state REQUESTED; the move to a cell is asynchronous

     A broker whose permission is `unknown` is accepted in the development environment with the response
    header `X-MFX-Warning: broker_permission_unknown`, and refused `broker_not_supported` in production.
    Refused at request time, never passed to a terminal: an unsupported broker or server (422), a farm
    that does not carry the usages (409), a redundancy the farm does not offer (409). The credential is
    submitted separately (`POST /terminals/{id}/credentials`), so a terminal can exist before its login
    does. Several terminals may use the same broker login, on every plan: the limits are checked when
    the credential is submitted. `farm_id` is optional: omitted, the platform chooses a farm and says
    which on the answer; none fits is 409 `no_farm`, with `details.why` one of `no_usage` (no farm you
    can use offers what this terminal needs), `no_region` (none in the server's region) or `no_room`.
    `refresh_ms` faster than the farm's rate is 422 with `details.allowed`; with no farm named, only
    farms that allow the rate are considered. A changed rate a cell cannot carry is the PATCH's 409
    `no_room`; create queues the terminal for placement. The tenant's plan decides the farm: enterprise
    and system tenants' terminals go to their own farms, standard tenants' to the shared farms. A named
    farm outside the plan is 409 `farm_not_in_plan`; with no farm named the platform chooses within the
    plan. A tenant already at its terminal quota is 409 `quota_exceeded` with `details {quota, in_use}`.

    Args:
        idempotency_key (str):
        body (TerminalCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantTerminal]]
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
    body: TerminalCreate,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Provision a terminal — answered at once in state REQUESTED; the move to a cell is asynchronous

     A broker whose permission is `unknown` is accepted in the development environment with the response
    header `X-MFX-Warning: broker_permission_unknown`, and refused `broker_not_supported` in production.
    Refused at request time, never passed to a terminal: an unsupported broker or server (422), a farm
    that does not carry the usages (409), a redundancy the farm does not offer (409). The credential is
    submitted separately (`POST /terminals/{id}/credentials`), so a terminal can exist before its login
    does. Several terminals may use the same broker login, on every plan: the limits are checked when
    the credential is submitted. `farm_id` is optional: omitted, the platform chooses a farm and says
    which on the answer; none fits is 409 `no_farm`, with `details.why` one of `no_usage` (no farm you
    can use offers what this terminal needs), `no_region` (none in the server's region) or `no_room`.
    `refresh_ms` faster than the farm's rate is 422 with `details.allowed`; with no farm named, only
    farms that allow the rate are considered. A changed rate a cell cannot carry is the PATCH's 409
    `no_room`; create queues the terminal for placement. The tenant's plan decides the farm: enterprise
    and system tenants' terminals go to their own farms, standard tenants' to the shared farms. A named
    farm outside the plan is 409 `farm_not_in_plan`; with no farm named the platform chooses within the
    plan. A tenant already at its terminal quota is 409 `quota_exceeded` with `details {quota, in_use}`.

    Args:
        idempotency_key (str):
        body (TerminalCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantTerminal]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
