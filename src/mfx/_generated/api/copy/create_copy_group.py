from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.copy_group import CopyGroup
from ...models.copy_group_create import CopyGroupCreate
from ...models.error import Error
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CopyGroupCreate,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/copy/groups",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CopyGroup, Error]:
    if response.status_code == 201:
        response_201 = CopyGroup.from_dict(response.json())

        return response_201

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CopyGroup, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyGroupCreate,
    idempotency_key: str,
) -> Response[Union[CopyGroup, Error]]:
    """A group of followers managed together under one template and one exposure cap (Enterprise)

     Followers join with `group_id` on create, or through the group's followers route. A tenant whose
    plan is not Enterprise is 403 `feature_not_entitled` with `details.part = groups`

    Args:
        idempotency_key (str):
        body (CopyGroupCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroup, Error]]
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
    body: CopyGroupCreate,
    idempotency_key: str,
) -> Optional[Union[CopyGroup, Error]]:
    """A group of followers managed together under one template and one exposure cap (Enterprise)

     Followers join with `group_id` on create, or through the group's followers route. A tenant whose
    plan is not Enterprise is 403 `feature_not_entitled` with `details.part = groups`

    Args:
        idempotency_key (str):
        body (CopyGroupCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroup, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CopyGroupCreate,
    idempotency_key: str,
) -> Response[Union[CopyGroup, Error]]:
    """A group of followers managed together under one template and one exposure cap (Enterprise)

     Followers join with `group_id` on create, or through the group's followers route. A tenant whose
    plan is not Enterprise is 403 `feature_not_entitled` with `details.part = groups`

    Args:
        idempotency_key (str):
        body (CopyGroupCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CopyGroup, Error]]
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
    body: CopyGroupCreate,
    idempotency_key: str,
) -> Optional[Union[CopyGroup, Error]]:
    """A group of followers managed together under one template and one exposure cap (Enterprise)

     Followers join with `group_id` on create, or through the group's followers route. A tenant whose
    plan is not Enterprise is 403 `feature_not_entitled` with `details.part = groups`

    Args:
        idempotency_key (str):
        body (CopyGroupCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CopyGroup, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
