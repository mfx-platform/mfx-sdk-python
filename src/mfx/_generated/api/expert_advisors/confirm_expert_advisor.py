from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.expert_advisor_attachment import ExpertAdvisorAttachment
from ...models.expert_advisor_confirm import ExpertAdvisorConfirm
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    body: ExpertAdvisorConfirm,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/terminals/{id}/expert-advisor/confirm".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, ExpertAdvisorAttachment]:
    if response.status_code == 200:
        response_200 = ExpertAdvisorAttachment.from_dict(response.json())

        return response_200

    response_default = Error.from_dict(response.json())

    return response_default


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, ExpertAdvisorAttachment]]:
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
    body: ExpertAdvisorConfirm,
) -> Response[Union[Error, ExpertAdvisorAttachment]]:
    """Turn on live trading for an EA on a real-money account after a green trial, with the one-time code
    from the trial email

     409 `not_awaiting_confirmation` unless the terminal's attachment is waiting for it. A code that is
    wrong, used or expired is 403 `confirmation_refused`, and the answer does not say which. Five
    refusals in a row lock the confirmation for that attachment until an operator looks. A key alone
    confirms nothing: the code reaches only the representative's mailbox.

    Args:
        id (UUID):
        body (ExpertAdvisorConfirm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ExpertAdvisorAttachment]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExpertAdvisorConfirm,
) -> Optional[Union[Error, ExpertAdvisorAttachment]]:
    """Turn on live trading for an EA on a real-money account after a green trial, with the one-time code
    from the trial email

     409 `not_awaiting_confirmation` unless the terminal's attachment is waiting for it. A code that is
    wrong, used or expired is 403 `confirmation_refused`, and the answer does not say which. Five
    refusals in a row lock the confirmation for that attachment until an operator looks. A key alone
    confirms nothing: the code reaches only the representative's mailbox.

    Args:
        id (UUID):
        body (ExpertAdvisorConfirm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ExpertAdvisorAttachment]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExpertAdvisorConfirm,
) -> Response[Union[Error, ExpertAdvisorAttachment]]:
    """Turn on live trading for an EA on a real-money account after a green trial, with the one-time code
    from the trial email

     409 `not_awaiting_confirmation` unless the terminal's attachment is waiting for it. A code that is
    wrong, used or expired is 403 `confirmation_refused`, and the answer does not say which. Five
    refusals in a row lock the confirmation for that attachment until an operator looks. A key alone
    confirms nothing: the code reaches only the representative's mailbox.

    Args:
        id (UUID):
        body (ExpertAdvisorConfirm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ExpertAdvisorAttachment]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExpertAdvisorConfirm,
) -> Optional[Union[Error, ExpertAdvisorAttachment]]:
    """Turn on live trading for an EA on a real-money account after a green trial, with the one-time code
    from the trial email

     409 `not_awaiting_confirmation` unless the terminal's attachment is waiting for it. A code that is
    wrong, used or expired is 403 `confirmation_refused`, and the answer does not say which. Five
    refusals in a row lock the confirmation for that attachment until an operator looks. A key alone
    confirms nothing: the code reaches only the representative's mailbox.

    Args:
        id (UUID):
        body (ExpertAdvisorConfirm):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ExpertAdvisorAttachment]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
