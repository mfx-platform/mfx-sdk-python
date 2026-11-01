from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.expert_advisor_parameters import ExpertAdvisorParameters
from ...models.expert_advisor_parameters_put import ExpertAdvisorParametersPut
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: ExpertAdvisorParametersPut,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/terminals/{id}/expert-advisor/parameters".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, ExpertAdvisorParameters]:
    if response.status_code == 202:
        response_202 = ExpertAdvisorParameters.from_dict(response.json())

        return response_202

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ExpertAdvisorParameters]]:
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
    body: ExpertAdvisorParametersPut,
    idempotency_key: str,
) -> Response[Union[Error, ExpertAdvisorParameters]]:
    """Send your EA a new parameter set - the platform numbers it, delivers it to the terminal, and keeps
    it for every later copy of the terminal

     The set replaces the one before. The platform gives it the next `version` (1 for the first), answers
    at once, and delivers it to the terminal's EA, which reads it from its parameter file. You never
    send a version: ordering is the platform's, so a retry or a race can never put an older set back.
    The newest set is also part of the terminal's desired state, so a terminal copied again (detach and
    attach, or a move to another cell) starts with it, not with the EA's defaults. `applied_version` on
    getExpertAdvisorParameters says when your EA runs it: your EA echoes the version it runs in every
    heartbeat line. Refused: 409 `no_ea_attached` when the terminal carries no expert; 400
    `validation_error` when the set is not an object, when the file it makes would exceed 256 KiB
    (`details.bytes`, `details.max`), or when a key anywhere in it is named like a credential
    (`details.key`) - your EA can read this file, so it must never hold one; 404 for another tenant's
    terminal. The same Idempotency-Key with the same body answers the same version again; with another
    body it is 409 `conflict` with `details.reason = idempotency_key_reused`. What the cell answered is
    kept on the platform: read the outcome on getExpertAdvisorParameters (`version`, `applied_version`,
    `converged`); getCommand shows only the command's own state.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorParametersPut): A parameter set for the terminal's EA. Your keys go in
            `params`; the platform writes them, with `enabled` and the version it assigns, to the EA's
            parameter file (`MQL5/Files/mfx/params.json`), so they never collide with the platform's
            own keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ExpertAdvisorParameters]]
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
    body: ExpertAdvisorParametersPut,
    idempotency_key: str,
) -> Optional[Union[Error, ExpertAdvisorParameters]]:
    """Send your EA a new parameter set - the platform numbers it, delivers it to the terminal, and keeps
    it for every later copy of the terminal

     The set replaces the one before. The platform gives it the next `version` (1 for the first), answers
    at once, and delivers it to the terminal's EA, which reads it from its parameter file. You never
    send a version: ordering is the platform's, so a retry or a race can never put an older set back.
    The newest set is also part of the terminal's desired state, so a terminal copied again (detach and
    attach, or a move to another cell) starts with it, not with the EA's defaults. `applied_version` on
    getExpertAdvisorParameters says when your EA runs it: your EA echoes the version it runs in every
    heartbeat line. Refused: 409 `no_ea_attached` when the terminal carries no expert; 400
    `validation_error` when the set is not an object, when the file it makes would exceed 256 KiB
    (`details.bytes`, `details.max`), or when a key anywhere in it is named like a credential
    (`details.key`) - your EA can read this file, so it must never hold one; 404 for another tenant's
    terminal. The same Idempotency-Key with the same body answers the same version again; with another
    body it is 409 `conflict` with `details.reason = idempotency_key_reused`. What the cell answered is
    kept on the platform: read the outcome on getExpertAdvisorParameters (`version`, `applied_version`,
    `converged`); getCommand shows only the command's own state.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorParametersPut): A parameter set for the terminal's EA. Your keys go in
            `params`; the platform writes them, with `enabled` and the version it assigns, to the EA's
            parameter file (`MQL5/Files/mfx/params.json`), so they never collide with the platform's
            own keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ExpertAdvisorParameters]
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
    body: ExpertAdvisorParametersPut,
    idempotency_key: str,
) -> Response[Union[Error, ExpertAdvisorParameters]]:
    """Send your EA a new parameter set - the platform numbers it, delivers it to the terminal, and keeps
    it for every later copy of the terminal

     The set replaces the one before. The platform gives it the next `version` (1 for the first), answers
    at once, and delivers it to the terminal's EA, which reads it from its parameter file. You never
    send a version: ordering is the platform's, so a retry or a race can never put an older set back.
    The newest set is also part of the terminal's desired state, so a terminal copied again (detach and
    attach, or a move to another cell) starts with it, not with the EA's defaults. `applied_version` on
    getExpertAdvisorParameters says when your EA runs it: your EA echoes the version it runs in every
    heartbeat line. Refused: 409 `no_ea_attached` when the terminal carries no expert; 400
    `validation_error` when the set is not an object, when the file it makes would exceed 256 KiB
    (`details.bytes`, `details.max`), or when a key anywhere in it is named like a credential
    (`details.key`) - your EA can read this file, so it must never hold one; 404 for another tenant's
    terminal. The same Idempotency-Key with the same body answers the same version again; with another
    body it is 409 `conflict` with `details.reason = idempotency_key_reused`. What the cell answered is
    kept on the platform: read the outcome on getExpertAdvisorParameters (`version`, `applied_version`,
    `converged`); getCommand shows only the command's own state.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorParametersPut): A parameter set for the terminal's EA. Your keys go in
            `params`; the platform writes them, with `enabled` and the version it assigns, to the EA's
            parameter file (`MQL5/Files/mfx/params.json`), so they never collide with the platform's
            own keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ExpertAdvisorParameters]]
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
    body: ExpertAdvisorParametersPut,
    idempotency_key: str,
) -> Optional[Union[Error, ExpertAdvisorParameters]]:
    """Send your EA a new parameter set - the platform numbers it, delivers it to the terminal, and keeps
    it for every later copy of the terminal

     The set replaces the one before. The platform gives it the next `version` (1 for the first), answers
    at once, and delivers it to the terminal's EA, which reads it from its parameter file. You never
    send a version: ordering is the platform's, so a retry or a race can never put an older set back.
    The newest set is also part of the terminal's desired state, so a terminal copied again (detach and
    attach, or a move to another cell) starts with it, not with the EA's defaults. `applied_version` on
    getExpertAdvisorParameters says when your EA runs it: your EA echoes the version it runs in every
    heartbeat line. Refused: 409 `no_ea_attached` when the terminal carries no expert; 400
    `validation_error` when the set is not an object, when the file it makes would exceed 256 KiB
    (`details.bytes`, `details.max`), or when a key anywhere in it is named like a credential
    (`details.key`) - your EA can read this file, so it must never hold one; 404 for another tenant's
    terminal. The same Idempotency-Key with the same body answers the same version again; with another
    body it is 409 `conflict` with `details.reason = idempotency_key_reused`. What the cell answered is
    kept on the platform: read the outcome on getExpertAdvisorParameters (`version`, `applied_version`,
    `converged`); getCommand shows only the command's own state.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorParametersPut): A parameter set for the terminal's EA. Your keys go in
            `params`; the platform writes them, with `enabled` and the version it assigns, to the EA's
            parameter file (`MQL5/Files/mfx/params.json`), so they never collide with the platform's
            own keys.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ExpertAdvisorParameters]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
