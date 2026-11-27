from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.billing_payment_required_error import BillingPaymentRequiredError
from ...models.error import Error
from ...models.risk_plan import RiskPlan
from ...models.risk_plan_amend import RiskPlanAmend
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: RiskPlanAmend,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/risk/plans/{id}/amend".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[BillingPaymentRequiredError, Error, RiskPlan]:
    if response.status_code == 200:
        response_200 = RiskPlan.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = BillingPaymentRequiredError.from_dict(response.json())

        return response_402

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BillingPaymentRequiredError, Error, RiskPlan]]:
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
    body: RiskPlanAmend,
    idempotency_key: str,
) -> Response[Union[BillingPaymentRequiredError, Error, RiskPlan]]:
    """A new version of the plan's steps; the protection in place stays until it is accepted

    Args:
        id (UUID):
        idempotency_key (str):
        body (RiskPlanAmend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, Error, RiskPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
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
    body: RiskPlanAmend,
    idempotency_key: str,
) -> Optional[Union[BillingPaymentRequiredError, Error, RiskPlan]]:
    """A new version of the plan's steps; the protection in place stays until it is accepted

    Args:
        id (UUID):
        idempotency_key (str):
        body (RiskPlanAmend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, Error, RiskPlan]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPlanAmend,
    idempotency_key: str,
) -> Response[Union[BillingPaymentRequiredError, Error, RiskPlan]]:
    """A new version of the plan's steps; the protection in place stays until it is accepted

    Args:
        id (UUID):
        idempotency_key (str):
        body (RiskPlanAmend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BillingPaymentRequiredError, Error, RiskPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPlanAmend,
    idempotency_key: str,
) -> Optional[Union[BillingPaymentRequiredError, Error, RiskPlan]]:
    """A new version of the plan's steps; the protection in place stays until it is accepted

    Args:
        id (UUID):
        idempotency_key (str):
        body (RiskPlanAmend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BillingPaymentRequiredError, Error, RiskPlan]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
