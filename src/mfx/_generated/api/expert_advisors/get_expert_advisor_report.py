from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ea_report import EaReport
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/expert-advisors/{id}/report".format(
            id=id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[EaReport, Error]:
    if response.status_code == 200:
        response_200 = EaReport.from_dict(response.json())

        return response_200

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[EaReport, Error]]:
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
) -> Response[Union[EaReport, Error]]:
    """The report of one version - the verdict, one colour for each group of rules, every finding with its
    lines and what to change

     The same report an operator reads and the tenant's representative is emailed. A found secret is
    masked wherever it appears, and no source is in it beyond the lines a finding quotes.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EaReport, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[EaReport, Error]]:
    """The report of one version - the verdict, one colour for each group of rules, every finding with its
    lines and what to change

     The same report an operator reads and the tenant's representative is emailed. A found secret is
    masked wherever it appears, and no source is in it beyond the lines a finding quotes.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EaReport, Error]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[EaReport, Error]]:
    """The report of one version - the verdict, one colour for each group of rules, every finding with its
    lines and what to change

     The same report an operator reads and the tenant's representative is emailed. A found secret is
    masked wherever it appears, and no source is in it beyond the lines a finding quotes.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EaReport, Error]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[EaReport, Error]]:
    """The report of one version - the verdict, one colour for each group of rules, every finding with its
    lines and what to change

     The same report an operator reads and the tenant's representative is emailed. A found secret is
    masked wherever it appears, and no source is in it beyond the lines a finding quotes.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EaReport, Error]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
