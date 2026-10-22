from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.expert_advisor_attach import ExpertAdvisorAttach
from ...models.operation_accepted import OperationAccepted
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: ExpertAdvisorAttach,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/terminals/{id}/expert-advisor".format(
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
    body: ExpertAdvisorAttach,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Attach an approved version of your EA to a terminal - governed, followed as an operation; a trial
    with trading off comes first

     Refused before the operation's rules: 409 `ea_not_approved` with the version's state; 409
    `not_customer_code_farm`; 409 `build_mismatch` when the version was built for another MetaTrader
    build than the farm runs: after an operator moves the farm to a newer MetaTrader, the platform
    builds each approved version for it, and `details.build` says where that build stands - `queued`,
    `running` (attach again once it is done), or `failed` with `failure` in plain words (the version is
    not attachable on that build; the same bundle uploaded again tries once more); 409 `ea_attached`
    when the terminal already carries one (detach it first); 404 for another tenant's version, or a
    symbol the terminal's server does not list. Then the seven rules of a governed operation, as on
    restartTerminal. The operation succeeds when the terminal produces again with the build loaded and
    trading by experts off: the trial has started. A green trial goes live by itself on a demo account;
    on a real-money account it waits for confirmExpertAdvisor.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorAttach): Attach an approved version to a terminal. A governed operation
            of kind `attach`: the terminal is relaunched with the expert loaded and trading by experts
            off, and the operation succeeds when the terminal produces again, which is when the trial
            starts.

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
    body: ExpertAdvisorAttach,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Attach an approved version of your EA to a terminal - governed, followed as an operation; a trial
    with trading off comes first

     Refused before the operation's rules: 409 `ea_not_approved` with the version's state; 409
    `not_customer_code_farm`; 409 `build_mismatch` when the version was built for another MetaTrader
    build than the farm runs: after an operator moves the farm to a newer MetaTrader, the platform
    builds each approved version for it, and `details.build` says where that build stands - `queued`,
    `running` (attach again once it is done), or `failed` with `failure` in plain words (the version is
    not attachable on that build; the same bundle uploaded again tries once more); 409 `ea_attached`
    when the terminal already carries one (detach it first); 404 for another tenant's version, or a
    symbol the terminal's server does not list. Then the seven rules of a governed operation, as on
    restartTerminal. The operation succeeds when the terminal produces again with the build loaded and
    trading by experts off: the trial has started. A green trial goes live by itself on a demo account;
    on a real-money account it waits for confirmExpertAdvisor.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorAttach): Attach an approved version to a terminal. A governed operation
            of kind `attach`: the terminal is relaunched with the expert loaded and trading by experts
            off, and the operation succeeds when the terminal produces again, which is when the trial
            starts.

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
    body: ExpertAdvisorAttach,
    idempotency_key: str,
) -> Response[Union[Error, OperationAccepted]]:
    """Attach an approved version of your EA to a terminal - governed, followed as an operation; a trial
    with trading off comes first

     Refused before the operation's rules: 409 `ea_not_approved` with the version's state; 409
    `not_customer_code_farm`; 409 `build_mismatch` when the version was built for another MetaTrader
    build than the farm runs: after an operator moves the farm to a newer MetaTrader, the platform
    builds each approved version for it, and `details.build` says where that build stands - `queued`,
    `running` (attach again once it is done), or `failed` with `failure` in plain words (the version is
    not attachable on that build; the same bundle uploaded again tries once more); 409 `ea_attached`
    when the terminal already carries one (detach it first); 404 for another tenant's version, or a
    symbol the terminal's server does not list. Then the seven rules of a governed operation, as on
    restartTerminal. The operation succeeds when the terminal produces again with the build loaded and
    trading by experts off: the trial has started. A green trial goes live by itself on a demo account;
    on a real-money account it waits for confirmExpertAdvisor.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorAttach): Attach an approved version to a terminal. A governed operation
            of kind `attach`: the terminal is relaunched with the expert loaded and trading by experts
            off, and the operation succeeds when the terminal produces again, which is when the trial
            starts.

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
    body: ExpertAdvisorAttach,
    idempotency_key: str,
) -> Optional[Union[Error, OperationAccepted]]:
    """Attach an approved version of your EA to a terminal - governed, followed as an operation; a trial
    with trading off comes first

     Refused before the operation's rules: 409 `ea_not_approved` with the version's state; 409
    `not_customer_code_farm`; 409 `build_mismatch` when the version was built for another MetaTrader
    build than the farm runs: after an operator moves the farm to a newer MetaTrader, the platform
    builds each approved version for it, and `details.build` says where that build stands - `queued`,
    `running` (attach again once it is done), or `failed` with `failure` in plain words (the version is
    not attachable on that build; the same bundle uploaded again tries once more); 409 `ea_attached`
    when the terminal already carries one (detach it first); 404 for another tenant's version, or a
    symbol the terminal's server does not list. Then the seven rules of a governed operation, as on
    restartTerminal. The operation succeeds when the terminal produces again with the build loaded and
    trading by experts off: the trial has started. A green trial goes live by itself on a demo account;
    on a real-money account it waits for confirmExpertAdvisor.

    Args:
        id (UUID):
        idempotency_key (str):
        body (ExpertAdvisorAttach): Attach an approved version to a terminal. A governed operation
            of kind `attach`: the terminal is relaunched with the expert loaded and trading by experts
            off, and the operation succeeds when the terminal produces again, which is when the trial
            starts.

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
