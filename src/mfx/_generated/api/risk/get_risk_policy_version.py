from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_policy_version import RiskPolicyVersion
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    version: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/policies/{id}/versions/{version}".format(
            id=id,
            version=version,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskPolicyVersion]:
    if response.status_code == 200:
        response_200 = RiskPolicyVersion.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskPolicyVersion]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    version: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, RiskPolicyVersion]]:
    """One version of a policy

    Args:
        id (UUID):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPolicyVersion]]
    """

    kwargs = _get_kwargs(
        id=id,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    version: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, RiskPolicyVersion]]:
    """One version of a policy

    Args:
        id (UUID):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPolicyVersion]
    """

    return sync_detailed(
        id=id,
        version=version,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    version: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, RiskPolicyVersion]]:
    """One version of a policy

    Args:
        id (UUID):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPolicyVersion]]
    """

    kwargs = _get_kwargs(
        id=id,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    version: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, RiskPolicyVersion]]:
    """One version of a policy

    Args:
        id (UUID):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPolicyVersion]
    """

    return (
        await asyncio_detailed(
            id=id,
            version=version,
            client=client,
        )
    ).parsed
