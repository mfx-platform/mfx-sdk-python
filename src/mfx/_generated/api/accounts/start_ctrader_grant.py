from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ctrader_grant_create import CtraderGrantCreate
from ...models.ctrader_grant_started import CtraderGrantStarted
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CtraderGrantCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/accounts/ctrader/grants",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CtraderGrantStarted, Error]:
    if response.status_code == 201:
        response_201 = CtraderGrantStarted.from_dict(response.json())

        return response_201

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CtraderGrantStarted, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderGrantCreate,
    idempotency_key: str,
) -> Response[Union[CtraderGrantStarted, Error]]:
    """Start connecting a trader's cTrader accounts; answers the consent URL to send them to

     The trader signs in at cTrader with their cTrader ID and chooses which of their accounts to share.
    MFX Hub never sees their password. After consent the trader is sent to `return_url` with `grant_id`,
    `result` and your `tenant_state`; then read the grant for the accounts it lists and choose which to
    connect. The consent link lives 15 minutes. A tenant whose plan does not include cTrader is 403
    `feature_not_entitled`.

    Args:
        idempotency_key (str):
        body (CtraderGrantCreate): Start connecting a trader's cTrader accounts. Send the trader
            to `consent_url`: they sign in at cTrader, choose the accounts to share, and come back to
            `return_url`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderGrantStarted, Error]]
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
    body: CtraderGrantCreate,
    idempotency_key: str,
) -> Optional[Union[CtraderGrantStarted, Error]]:
    """Start connecting a trader's cTrader accounts; answers the consent URL to send them to

     The trader signs in at cTrader with their cTrader ID and chooses which of their accounts to share.
    MFX Hub never sees their password. After consent the trader is sent to `return_url` with `grant_id`,
    `result` and your `tenant_state`; then read the grant for the accounts it lists and choose which to
    connect. The consent link lives 15 minutes. A tenant whose plan does not include cTrader is 403
    `feature_not_entitled`.

    Args:
        idempotency_key (str):
        body (CtraderGrantCreate): Start connecting a trader's cTrader accounts. Send the trader
            to `consent_url`: they sign in at cTrader, choose the accounts to share, and come back to
            `return_url`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderGrantStarted, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CtraderGrantCreate,
    idempotency_key: str,
) -> Response[Union[CtraderGrantStarted, Error]]:
    """Start connecting a trader's cTrader accounts; answers the consent URL to send them to

     The trader signs in at cTrader with their cTrader ID and chooses which of their accounts to share.
    MFX Hub never sees their password. After consent the trader is sent to `return_url` with `grant_id`,
    `result` and your `tenant_state`; then read the grant for the accounts it lists and choose which to
    connect. The consent link lives 15 minutes. A tenant whose plan does not include cTrader is 403
    `feature_not_entitled`.

    Args:
        idempotency_key (str):
        body (CtraderGrantCreate): Start connecting a trader's cTrader accounts. Send the trader
            to `consent_url`: they sign in at cTrader, choose the accounts to share, and come back to
            `return_url`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CtraderGrantStarted, Error]]
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
    body: CtraderGrantCreate,
    idempotency_key: str,
) -> Optional[Union[CtraderGrantStarted, Error]]:
    """Start connecting a trader's cTrader accounts; answers the consent URL to send them to

     The trader signs in at cTrader with their cTrader ID and chooses which of their accounts to share.
    MFX Hub never sees their password. After consent the trader is sent to `return_url` with `grant_id`,
    `result` and your `tenant_state`; then read the grant for the accounts it lists and choose which to
    connect. The consent link lives 15 minutes. A tenant whose plan does not include cTrader is 403
    `feature_not_entitled`.

    Args:
        idempotency_key (str):
        body (CtraderGrantCreate): Start connecting a trader's cTrader accounts. Send the trader
            to `consent_url`: they sign in at cTrader, choose the accounts to share, and come back to
            `return_url`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CtraderGrantStarted, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
