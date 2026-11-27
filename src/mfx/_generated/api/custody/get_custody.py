from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custody import Custody
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/custody",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Custody, Error]:
    if response.status_code == 200:
        response_200 = Custody.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Custody, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Custody, Error]]:
    """Data custody - what of your trading data is held where, who can read it, the stated limit and your
    key's state (Enterprise)

     Read only. Enterprise only, and always on: a key whose plan is not Enterprise is 403
    `feature_not_entitled` with `details.feature = data_custody`. Nobody at MFX Hub can read your broker
    password, login, account name, server, orders, fills, positions or balances; instrument names are
    held in clear because quotes are routed by symbol. The stated limit says where the promise ends.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Custody, Error]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Custody, Error]]:
    """Data custody - what of your trading data is held where, who can read it, the stated limit and your
    key's state (Enterprise)

     Read only. Enterprise only, and always on: a key whose plan is not Enterprise is 403
    `feature_not_entitled` with `details.feature = data_custody`. Nobody at MFX Hub can read your broker
    password, login, account name, server, orders, fills, positions or balances; instrument names are
    held in clear because quotes are routed by symbol. The stated limit says where the promise ends.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Custody, Error]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Custody, Error]]:
    """Data custody - what of your trading data is held where, who can read it, the stated limit and your
    key's state (Enterprise)

     Read only. Enterprise only, and always on: a key whose plan is not Enterprise is 403
    `feature_not_entitled` with `details.feature = data_custody`. Nobody at MFX Hub can read your broker
    password, login, account name, server, orders, fills, positions or balances; instrument names are
    held in clear because quotes are routed by symbol. The stated limit says where the promise ends.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Custody, Error]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Custody, Error]]:
    """Data custody - what of your trading data is held where, who can read it, the stated limit and your
    key's state (Enterprise)

     Read only. Enterprise only, and always on: a key whose plan is not Enterprise is 403
    `feature_not_entitled` with `details.feature = data_custody`. Nobody at MFX Hub can read your broker
    password, login, account name, server, orders, fills, positions or balances; instrument names are
    held in clear because quotes are routed by symbol. The stated limit says where the promise ends.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Custody, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
