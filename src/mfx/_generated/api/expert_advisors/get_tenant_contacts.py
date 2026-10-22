from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.own_contacts import OwnContacts
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenant/contacts",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, OwnContacts]:
    if response.status_code == 200:
        response_200 = OwnContacts.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, OwnContacts]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, OwnContacts]]:
    """Who at your company is told about your expert advisors - the contacts and their roles

     Read only. The representative is emailed each verdict and confirms live trading on a real-money
    account; the technical contacts are emailed what to change. Contacts are set by the platform's
    operators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OwnContacts]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, OwnContacts]]:
    """Who at your company is told about your expert advisors - the contacts and their roles

     Read only. The representative is emailed each verdict and confirms live trading on a real-money
    account; the technical contacts are emailed what to change. Contacts are set by the platform's
    operators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OwnContacts]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, OwnContacts]]:
    """Who at your company is told about your expert advisors - the contacts and their roles

     Read only. The representative is emailed each verdict and confirms live trading on a real-money
    account; the technical contacts are emailed what to change. Contacts are set by the platform's
    operators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, OwnContacts]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, OwnContacts]]:
    """Who at your company is told about your expert advisors - the contacts and their roles

     Read only. The representative is emailed each verdict and confirms live trading on a real-money
    account; the technical contacts are emailed what to change. Contacts are set by the platform's
    operators.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, OwnContacts]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
