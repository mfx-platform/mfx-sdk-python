from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_terminal import TenantTerminal
from ...models.terminal_ha import TerminalHa
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: TerminalHa,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/ha".format(
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
    body: TerminalHa,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Turn MFX Hub HA on or off for a terminal, or change its mode

     On, MFX Hub creates a second terminal on the same broker login, on separate hardware in the
    terminal's farm, and keeps it ready (`ha.fallback_state`); the terminal's id answers as before. Off,
    the second terminal is retired. Sent again, the same ask changes nothing. Refused: a plan that does
    not include HA (403 `forbidden`, `details.reason` `ha_not_in_plan`); a terminal that is not
    REQUESTED, PROVISIONING, LOGGING_IN, ACTIVE or OFFLINE (409 `state_error`); a terminal carrying an
    expert advisor, or on a farm that runs customer code (409 `conflict`, `details.reason` `ea_attached`
    or `customer_code_farm`); a login whose broker is not known to allow one more session (409
    `placement_error`, `details.reason` `login_session_limit`); warm mode, not offered yet (422
    `unprocessable`). While HA is on, attaching an expert advisor is 409 `conflict` with
    `details.reason` `ha_on`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalHa): MFX Hub HA for one terminal. On, MFX Hub runs a second terminal on the
            same broker login, on separate hardware, ready to take over; you keep this terminal's id
            for everything and never see the second one. It is not in your terminal quota, your usage
            or your terminals per login, and it is not billed while HA is not priced. It is one more
            session on the login, so the broker's limit of sessions applies.

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
    body: TerminalHa,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Turn MFX Hub HA on or off for a terminal, or change its mode

     On, MFX Hub creates a second terminal on the same broker login, on separate hardware in the
    terminal's farm, and keeps it ready (`ha.fallback_state`); the terminal's id answers as before. Off,
    the second terminal is retired. Sent again, the same ask changes nothing. Refused: a plan that does
    not include HA (403 `forbidden`, `details.reason` `ha_not_in_plan`); a terminal that is not
    REQUESTED, PROVISIONING, LOGGING_IN, ACTIVE or OFFLINE (409 `state_error`); a terminal carrying an
    expert advisor, or on a farm that runs customer code (409 `conflict`, `details.reason` `ea_attached`
    or `customer_code_farm`); a login whose broker is not known to allow one more session (409
    `placement_error`, `details.reason` `login_session_limit`); warm mode, not offered yet (422
    `unprocessable`). While HA is on, attaching an expert advisor is 409 `conflict` with
    `details.reason` `ha_on`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalHa): MFX Hub HA for one terminal. On, MFX Hub runs a second terminal on the
            same broker login, on separate hardware, ready to take over; you keep this terminal's id
            for everything and never see the second one. It is not in your terminal quota, your usage
            or your terminals per login, and it is not billed while HA is not priced. It is one more
            session on the login, so the broker's limit of sessions applies.

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
    body: TerminalHa,
    idempotency_key: str,
) -> Response[Union[Error, TenantTerminal]]:
    """Turn MFX Hub HA on or off for a terminal, or change its mode

     On, MFX Hub creates a second terminal on the same broker login, on separate hardware in the
    terminal's farm, and keeps it ready (`ha.fallback_state`); the terminal's id answers as before. Off,
    the second terminal is retired. Sent again, the same ask changes nothing. Refused: a plan that does
    not include HA (403 `forbidden`, `details.reason` `ha_not_in_plan`); a terminal that is not
    REQUESTED, PROVISIONING, LOGGING_IN, ACTIVE or OFFLINE (409 `state_error`); a terminal carrying an
    expert advisor, or on a farm that runs customer code (409 `conflict`, `details.reason` `ea_attached`
    or `customer_code_farm`); a login whose broker is not known to allow one more session (409
    `placement_error`, `details.reason` `login_session_limit`); warm mode, not offered yet (422
    `unprocessable`). While HA is on, attaching an expert advisor is 409 `conflict` with
    `details.reason` `ha_on`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalHa): MFX Hub HA for one terminal. On, MFX Hub runs a second terminal on the
            same broker login, on separate hardware, ready to take over; you keep this terminal's id
            for everything and never see the second one. It is not in your terminal quota, your usage
            or your terminals per login, and it is not billed while HA is not priced. It is one more
            session on the login, so the broker's limit of sessions applies.

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
    body: TerminalHa,
    idempotency_key: str,
) -> Optional[Union[Error, TenantTerminal]]:
    """Turn MFX Hub HA on or off for a terminal, or change its mode

     On, MFX Hub creates a second terminal on the same broker login, on separate hardware in the
    terminal's farm, and keeps it ready (`ha.fallback_state`); the terminal's id answers as before. Off,
    the second terminal is retired. Sent again, the same ask changes nothing. Refused: a plan that does
    not include HA (403 `forbidden`, `details.reason` `ha_not_in_plan`); a terminal that is not
    REQUESTED, PROVISIONING, LOGGING_IN, ACTIVE or OFFLINE (409 `state_error`); a terminal carrying an
    expert advisor, or on a farm that runs customer code (409 `conflict`, `details.reason` `ea_attached`
    or `customer_code_farm`); a login whose broker is not known to allow one more session (409
    `placement_error`, `details.reason` `login_session_limit`); warm mode, not offered yet (422
    `unprocessable`). While HA is on, attaching an expert advisor is 409 `conflict` with
    `details.reason` `ha_on`.

    Args:
        id (UUID):
        idempotency_key (str):
        body (TerminalHa): MFX Hub HA for one terminal. On, MFX Hub runs a second terminal on the
            same broker login, on separate hardware, ready to take over; you keep this terminal's id
            for everything and never see the second one. It is not in your terminal quota, your usage
            or your terminals per login, and it is not billed while HA is not priced. It is one more
            session on the login, so the broker's limit of sessions applies.

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
