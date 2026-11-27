from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ctrader_return_origins import CtraderReturnOrigins
from ...models.ctrader_return_origins_set import CtraderReturnOriginsSet
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CtraderReturnOriginsSet,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/accounts/ctrader/return-origins",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CtraderReturnOrigins, Error]:
    if response.status_code == 200:
        response_200 = CtraderReturnOrigins.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CtraderReturnOrigins, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderReturnOriginsSet,
    idempotency_key: str,
) -> Response[Union[CtraderReturnOrigins, Error]]:
    """Replace the https origins a cTrader grant may send the trader back to

     Replaces the whole list. Each origin is a scheme and host, and a port when it is not 443, with no
    path, query or fragment: `https://app.example.com`. MFX Hub stores each one with its host lower-
    cased and `:443` dropped, removes duplicates, and answers the list sorted, so what GET returns may
    differ in form from what you sent. An origin that does not match is 422 `validation_error` naming
    the item's index, and nothing is replaced. Once the list is not empty, starting a grant whose
    `return_url` has another origin is 400 `validation_error` with `details.reason`
    `return_url_unregistered`, before the trader is sent anywhere. An empty list removes them all.
    Grants already started are not checked again.

    Args:
        idempotency_key (str):
        body (CtraderReturnOriginsSet):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderReturnOrigins, Error]]
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
    body: CtraderReturnOriginsSet,
    idempotency_key: str,
) -> Optional[Union[CtraderReturnOrigins, Error]]:
    """Replace the https origins a cTrader grant may send the trader back to

     Replaces the whole list. Each origin is a scheme and host, and a port when it is not 443, with no
    path, query or fragment: `https://app.example.com`. MFX Hub stores each one with its host lower-
    cased and `:443` dropped, removes duplicates, and answers the list sorted, so what GET returns may
    differ in form from what you sent. An origin that does not match is 422 `validation_error` naming
    the item's index, and nothing is replaced. Once the list is not empty, starting a grant whose
    `return_url` has another origin is 400 `validation_error` with `details.reason`
    `return_url_unregistered`, before the trader is sent anywhere. An empty list removes them all.
    Grants already started are not checked again.

    Args:
        idempotency_key (str):
        body (CtraderReturnOriginsSet):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderReturnOrigins, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderReturnOriginsSet,
    idempotency_key: str,
) -> Response[Union[CtraderReturnOrigins, Error]]:
    """Replace the https origins a cTrader grant may send the trader back to

     Replaces the whole list. Each origin is a scheme and host, and a port when it is not 443, with no
    path, query or fragment: `https://app.example.com`. MFX Hub stores each one with its host lower-
    cased and `:443` dropped, removes duplicates, and answers the list sorted, so what GET returns may
    differ in form from what you sent. An origin that does not match is 422 `validation_error` naming
    the item's index, and nothing is replaced. Once the list is not empty, starting a grant whose
    `return_url` has another origin is 400 `validation_error` with `details.reason`
    `return_url_unregistered`, before the trader is sent anywhere. An empty list removes them all.
    Grants already started are not checked again.

    Args:
        idempotency_key (str):
        body (CtraderReturnOriginsSet):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderReturnOrigins, Error]]
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
    body: CtraderReturnOriginsSet,
    idempotency_key: str,
) -> Optional[Union[CtraderReturnOrigins, Error]]:
    """Replace the https origins a cTrader grant may send the trader back to

     Replaces the whole list. Each origin is a scheme and host, and a port when it is not 443, with no
    path, query or fragment: `https://app.example.com`. MFX Hub stores each one with its host lower-
    cased and `:443` dropped, removes duplicates, and answers the list sorted, so what GET returns may
    differ in form from what you sent. An origin that does not match is 422 `validation_error` naming
    the item's index, and nothing is replaced. Once the list is not empty, starting a grant whose
    `return_url` has another origin is 400 `validation_error` with `details.reason`
    `return_url_unregistered`, before the trader is sent anywhere. An empty list removes them all.
    Grants already started are not checked again.

    Args:
        idempotency_key (str):
        body (CtraderReturnOriginsSet):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderReturnOrigins, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
