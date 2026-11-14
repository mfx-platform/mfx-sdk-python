from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_risk_account_close_scope_scope import GetRiskAccountCloseScopeScope
from ...models.risk_close_scope import RiskCloseScope
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    scope: GetRiskAccountCloseScopeScope,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_scope = scope.value
    params["scope"] = json_scope

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/risk/accounts/{id}/close-scope".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskCloseScope]:
    if response.status_code == 200:
        response_200 = RiskCloseScope.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskCloseScope]]:
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
    scope: GetRiskAccountCloseScopeScope,
) -> Response[Union[Error, RiskCloseScope]]:
    """The positions close_positions would close now on the account under a scope, before a rule that
    closes them is saved. Nothing is sent

    Args:
        id (UUID):
        scope (GetRiskAccountCloseScopeScope):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskCloseScope]]
    """

    kwargs = _get_kwargs(
        id=id,
        scope=scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    scope: GetRiskAccountCloseScopeScope,
) -> Optional[Union[Error, RiskCloseScope]]:
    """The positions close_positions would close now on the account under a scope, before a rule that
    closes them is saved. Nothing is sent

    Args:
        id (UUID):
        scope (GetRiskAccountCloseScopeScope):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskCloseScope]
    """

    return sync_detailed(
        id=id,
        client=client,
        scope=scope,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    scope: GetRiskAccountCloseScopeScope,
) -> Response[Union[Error, RiskCloseScope]]:
    """The positions close_positions would close now on the account under a scope, before a rule that
    closes them is saved. Nothing is sent

    Args:
        id (UUID):
        scope (GetRiskAccountCloseScopeScope):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskCloseScope]]
    """

    kwargs = _get_kwargs(
        id=id,
        scope=scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    scope: GetRiskAccountCloseScopeScope,
) -> Optional[Union[Error, RiskCloseScope]]:
    """The positions close_positions would close now on the account under a scope, before a rule that
    closes them is saved. Nothing is sent

    Args:
        id (UUID):
        scope (GetRiskAccountCloseScopeScope):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskCloseScope]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            scope=scope,
        )
    ).parsed
