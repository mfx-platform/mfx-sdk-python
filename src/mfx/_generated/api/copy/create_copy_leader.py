from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_leader import CopyLeader
from ...models.copy_leader_create import CopyLeaderCreate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CopyLeaderCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/leaders",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyLeader, Error]:
    if response.status_code == 201:
        response_201 = CopyLeader.from_dict(response.json())

        return response_201

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyLeader, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyLeaderCreate,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Make one of your accounts, or an external signal source, a leader

     An account leads once: a second live leader on the same account is 409 `conflict` with
    `details.reason = account_already_leads` and `details.leader_id`. A leader's account never changes;
    a leader on another account is another leader. Over the plan's number of leaders is 409
    `quota_exceeded` with `details.reason = plan_limit` and `details.limit = copy_leaders`. An account
    that is not yours, or is retired, is 422 `unprocessable` with `details.reason = account_not_usable`.

    Args:
        idempotency_key (str):
        body (CopyLeaderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
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
    body: CopyLeaderCreate,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Make one of your accounts, or an external signal source, a leader

     An account leads once: a second live leader on the same account is 409 `conflict` with
    `details.reason = account_already_leads` and `details.leader_id`. A leader's account never changes;
    a leader on another account is another leader. Over the plan's number of leaders is 409
    `quota_exceeded` with `details.reason = plan_limit` and `details.limit = copy_leaders`. An account
    that is not yours, or is retired, is 422 `unprocessable` with `details.reason = account_not_usable`.

    Args:
        idempotency_key (str):
        body (CopyLeaderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeader, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyLeaderCreate,
    idempotency_key: str,
) -> Response[Union[CopyLeader, Error]]:
    """Make one of your accounts, or an external signal source, a leader

     An account leads once: a second live leader on the same account is 409 `conflict` with
    `details.reason = account_already_leads` and `details.leader_id`. A leader's account never changes;
    a leader on another account is another leader. Over the plan's number of leaders is 409
    `quota_exceeded` with `details.reason = plan_limit` and `details.limit = copy_leaders`. An account
    that is not yours, or is retired, is 422 `unprocessable` with `details.reason = account_not_usable`.

    Args:
        idempotency_key (str):
        body (CopyLeaderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyLeader, Error]]
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
    body: CopyLeaderCreate,
    idempotency_key: str,
) -> Optional[Union[CopyLeader, Error]]:
    """Make one of your accounts, or an external signal source, a leader

     An account leads once: a second live leader on the same account is 409 `conflict` with
    `details.reason = account_already_leads` and `details.leader_id`. A leader's account never changes;
    a leader on another account is another leader. Over the plan's number of leaders is 409
    `quota_exceeded` with `details.reason = plan_limit` and `details.limit = copy_leaders`. An account
    that is not yours, or is retired, is 422 `unprocessable` with `details.reason = account_not_usable`.

    Args:
        idempotency_key (str):
        body (CopyLeaderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyLeader, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
