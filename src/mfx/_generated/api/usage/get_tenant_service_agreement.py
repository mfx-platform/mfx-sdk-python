from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tenant_service_agreement import TenantServiceAgreement
from ...types import UNSET, Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tenant/service-agreement",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantServiceAgreement]:
    if response.status_code == 200:
        response_200 = TenantServiceAgreement.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, TenantServiceAgreement]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, TenantServiceAgreement]]:
    """What your organisation must accept before it can add terminals, expert advisors or keys

     Any key may read it, whatever its scopes. `due` is true while a plan change awaits acceptance of the
    new plan's Service Agreement, or a version of a Service Agreement, the Terms of Service or the
    MetaTrader 5 licence asks to be accepted. While a plan change waits, the plan in force stays as it
    is. `held` is true while additions are refused 409 `service_agreement_not_accepted` or
    `terms_not_accepted`; reads, orders, positions and anything running are never refused. An owner or
    admin accepts at `accept_url`. Every answer carries the `MFX-Service-Agreement` header while
    something is due.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantServiceAgreement]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TenantServiceAgreement]]:
    """What your organisation must accept before it can add terminals, expert advisors or keys

     Any key may read it, whatever its scopes. `due` is true while a plan change awaits acceptance of the
    new plan's Service Agreement, or a version of a Service Agreement, the Terms of Service or the
    MetaTrader 5 licence asks to be accepted. While a plan change waits, the plan in force stays as it
    is. `held` is true while additions are refused 409 `service_agreement_not_accepted` or
    `terms_not_accepted`; reads, orders, positions and anything running are never refused. An owner or
    admin accepts at `accept_url`. Every answer carries the `MFX-Service-Agreement` header while
    something is due.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantServiceAgreement]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, TenantServiceAgreement]]:
    """What your organisation must accept before it can add terminals, expert advisors or keys

     Any key may read it, whatever its scopes. `due` is true while a plan change awaits acceptance of the
    new plan's Service Agreement, or a version of a Service Agreement, the Terms of Service or the
    MetaTrader 5 licence asks to be accepted. While a plan change waits, the plan in force stays as it
    is. `held` is true while additions are refused 409 `service_agreement_not_accepted` or
    `terms_not_accepted`; reads, orders, positions and anything running are never refused. An owner or
    admin accepts at `accept_url`. Every answer carries the `MFX-Service-Agreement` header while
    something is due.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantServiceAgreement]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, TenantServiceAgreement]]:
    """What your organisation must accept before it can add terminals, expert advisors or keys

     Any key may read it, whatever its scopes. `due` is true while a plan change awaits acceptance of the
    new plan's Service Agreement, or a version of a Service Agreement, the Terms of Service or the
    MetaTrader 5 licence asks to be accepted. While a plan change waits, the plan in force stays as it
    is. `held` is true while additions are refused 409 `service_agreement_not_accepted` or
    `terms_not_accepted`; reads, orders, positions and anything running are never refused. An owner or
    admin accepts at `accept_url`. Every answer carries the `MFX-Service-Agreement` header while
    something is due.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantServiceAgreement]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
