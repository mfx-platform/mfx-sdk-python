from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_policy import RiskPolicy
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
        "url": "/risk/policies/{id}/archive".format(
            id=id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskPolicy]:
    if response.status_code == 200:
        response_200 = RiskPolicy.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskPolicy]]:
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
) -> Response[Union[Error, RiskPolicy]]:
    """Archive a policy that is in force on no account; it no longer counts toward the policies quota

     Refused 409 `state_error` while any account holds the policy, active or paused; `details.accounts`
    lists those accounts. Deactivate them first. An archived policy stays readable with its versions,
    and Activity keeps everything it did. It cannot be activated or given a new version (409
    `state_error`). Archiving an archived policy answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPolicy]]
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
) -> Optional[Union[Error, RiskPolicy]]:
    """Archive a policy that is in force on no account; it no longer counts toward the policies quota

     Refused 409 `state_error` while any account holds the policy, active or paused; `details.accounts`
    lists those accounts. Deactivate them first. An archived policy stays readable with its versions,
    and Activity keeps everything it did. It cannot be activated or given a new version (409
    `state_error`). Archiving an archived policy answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPolicy]
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
) -> Response[Union[Error, RiskPolicy]]:
    """Archive a policy that is in force on no account; it no longer counts toward the policies quota

     Refused 409 `state_error` while any account holds the policy, active or paused; `details.accounts`
    lists those accounts. Deactivate them first. An archived policy stays readable with its versions,
    and Activity keeps everything it did. It cannot be activated or given a new version (409
    `state_error`). Archiving an archived policy answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPolicy]]
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
) -> Optional[Union[Error, RiskPolicy]]:
    """Archive a policy that is in force on no account; it no longer counts toward the policies quota

     Refused 409 `state_error` while any account holds the policy, active or paused; `details.accounts`
    lists those accounts. Deactivate them first. An archived policy stays readable with its versions,
    and Activity keeps everything it did. It cannot be activated or given a new version (409
    `state_error`). Archiving an archived policy answers it as it is.

    Args:
        id (UUID):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPolicy]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed
