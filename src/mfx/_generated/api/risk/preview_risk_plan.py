from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.risk_preview import RiskPreview
from ...models.risk_preview_request import RiskPreviewRequest
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: RiskPreviewRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/risk/planner/preview",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, RiskPreview]:
    if response.status_code == 200:
        response_200 = RiskPreview.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RiskPreview]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPreviewRequest,
) -> Response[Union[Error, RiskPreview]]:
    """Size a trade from a risk budget with the broker's specification and check it against every rule;
    nothing is sent to the broker

     Read-only: no Idempotency-Key. The volume is rounded down to the symbol's step and never enlarges
    the budget; when the symbol's minimum volume costs more than the budget no volume is offered
    (`reason: volume_min_over_budget`). A cost the specification does not give is 422 `validation_error`
    with `details.reason = assumption_required` until the caller states it. The answer expires at
    `expires_at` or when the price moves `risk.preview_max_move_points`.

    Args:
        body (RiskPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPreview]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPreviewRequest,
) -> Optional[Union[Error, RiskPreview]]:
    """Size a trade from a risk budget with the broker's specification and check it against every rule;
    nothing is sent to the broker

     Read-only: no Idempotency-Key. The volume is rounded down to the symbol's step and never enlarges
    the budget; when the symbol's minimum volume costs more than the budget no volume is offered
    (`reason: volume_min_over_budget`). A cost the specification does not give is 422 `validation_error`
    with `details.reason = assumption_required` until the caller states it. The answer expires at
    `expires_at` or when the price moves `risk.preview_max_move_points`.

    Args:
        body (RiskPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPreview]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPreviewRequest,
) -> Response[Union[Error, RiskPreview]]:
    """Size a trade from a risk budget with the broker's specification and check it against every rule;
    nothing is sent to the broker

     Read-only: no Idempotency-Key. The volume is rounded down to the symbol's step and never enlarges
    the budget; when the symbol's minimum volume costs more than the budget no volume is offered
    (`reason: volume_min_over_budget`). A cost the specification does not give is 422 `validation_error`
    with `details.reason = assumption_required` until the caller states it. The answer expires at
    `expires_at` or when the price moves `risk.preview_max_move_points`.

    Args:
        body (RiskPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RiskPreview]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RiskPreviewRequest,
) -> Optional[Union[Error, RiskPreview]]:
    """Size a trade from a risk budget with the broker's specification and check it against every rule;
    nothing is sent to the broker

     Read-only: no Idempotency-Key. The volume is rounded down to the symbol's step and never enlarges
    the budget; when the symbol's minimum volume costs more than the budget no volume is offered
    (`reason: volume_min_over_budget`). A cost the specification does not give is 422 `validation_error`
    with `details.reason = assumption_required` until the caller states it. The answer expires at
    `expires_at` or when the price moves `risk.preview_max_move_points`.

    Args:
        body (RiskPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RiskPreview]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
