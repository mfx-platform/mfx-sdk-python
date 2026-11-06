from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_plan import RiskPlan
from ...models.risk_plan_create import RiskPlanCreate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: RiskPlanCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/risk/plans",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskPlan]:
    if response.status_code == 201:
        response_201 = RiskPlan.from_dict(response.json())

        return response_201

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskPlan]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPlanCreate,
    idempotency_key: str,
) -> Response[Union[Error, RiskPlan]]:
    """An exit plan on an open position, or an order placed with its plan (checked as any entry; managing
    when the position opens)

     A position has one manager. A plan on a position that already has one (a plan or a standalone
    trailing stop) needs `replace: true`, or is 409 `conflict` with `details.reason = position_managed`
    and `details.manager`. A plan with a trailing step owns its trailing stop. With `order`, the answer
    carries the command that places it.

    Args:
        idempotency_key (str):
        body (RiskPlanCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlan]]
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
    body: RiskPlanCreate,
    idempotency_key: str,
) -> Optional[Union[Error, RiskPlan]]:
    """An exit plan on an open position, or an order placed with its plan (checked as any entry; managing
    when the position opens)

     A position has one manager. A plan on a position that already has one (a plan or a standalone
    trailing stop) needs `replace: true`, or is 409 `conflict` with `details.reason = position_managed`
    and `details.manager`. A plan with a trailing step owns its trailing stop. With `order`, the answer
    carries the command that places it.

    Args:
        idempotency_key (str):
        body (RiskPlanCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPlan]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPlanCreate,
    idempotency_key: str,
) -> Response[Union[Error, RiskPlan]]:
    """An exit plan on an open position, or an order placed with its plan (checked as any entry; managing
    when the position opens)

     A position has one manager. A plan on a position that already has one (a plan or a standalone
    trailing stop) needs `replace: true`, or is 409 `conflict` with `details.reason = position_managed`
    and `details.manager`. A plan with a trailing step owns its trailing stop. With `order`, the answer
    carries the command that places it.

    Args:
        idempotency_key (str):
        body (RiskPlanCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPlan]]
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
    body: RiskPlanCreate,
    idempotency_key: str,
) -> Optional[Union[Error, RiskPlan]]:
    """An exit plan on an open position, or an order placed with its plan (checked as any entry; managing
    when the position opens)

     A position has one manager. A plan on a position that already has one (a plan or a standalone
    trailing stop) needs `replace: true`, or is 409 `conflict` with `details.reason = position_managed`
    and `details.manager`. A plan with a trailing step owns its trailing stop. With `order`, the answer
    carries the command that places it.

    Args:
        idempotency_key (str):
        body (RiskPlanCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPlan]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
