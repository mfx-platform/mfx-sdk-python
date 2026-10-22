from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.expert_advisor_upload import ExpertAdvisorUpload
from ...models.tenant_expert_advisor import TenantExpertAdvisor
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: ExpertAdvisorUpload,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/expert-advisors",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Error, TenantExpertAdvisor]:
    if response.status_code == 200:
        response_200 = TenantExpertAdvisor.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = TenantExpertAdvisor.from_dict(response.json())

        return response_202

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
) -> Response[Union[Error, TenantExpertAdvisor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExpertAdvisorUpload,
    idempotency_key: str,
) -> Response[Union[Error, TenantExpertAdvisor]]:
    """Upload an expert advisor's source to be checked

     Stores the bundle where no cell can reach it and starts the checks; the answer is the new version in
    state `uploaded`. Read the version until `verdict` is set, then the report. The same bundle uploaded
    again answers the version it already made (200) and nothing is checked twice, unless the tenant
    withdrew that version. For an approved version it also starts a build for each MetaTrader build of
    the tenant's customer-code farms that the version has no build for and none running (a farm moved to
    a newer MetaTrader, or such a build failed); an attach's 409 `build_mismatch` says where it stands.
    Refused with 409 `conflict` and `details.why`: `no_customer_code_farm` (the tenant has no farm that
    runs customer code) or `uploads_off` (an operator has switched uploads off). A tenant already
    keeping as many versions as it may is 409 `quota_exceeded` with `details {quota, in_use}`: withdraw
    one.

    Args:
        idempotency_key (str):
        body (ExpertAdvisorUpload): One expert advisor's source: its `.mq5` and its own includes
            (`.mqh`). The platform reads it, checks it and builds it, so what runs is what was
            checked. A compiled `.ex5` is refused: it cannot be read. The size of the whole bundle and
            the number of files are bounded (8 MiB and 30 files unless an operator has changed them).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantExpertAdvisor]]
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
    body: ExpertAdvisorUpload,
    idempotency_key: str,
) -> Optional[Union[Error, TenantExpertAdvisor]]:
    """Upload an expert advisor's source to be checked

     Stores the bundle where no cell can reach it and starts the checks; the answer is the new version in
    state `uploaded`. Read the version until `verdict` is set, then the report. The same bundle uploaded
    again answers the version it already made (200) and nothing is checked twice, unless the tenant
    withdrew that version. For an approved version it also starts a build for each MetaTrader build of
    the tenant's customer-code farms that the version has no build for and none running (a farm moved to
    a newer MetaTrader, or such a build failed); an attach's 409 `build_mismatch` says where it stands.
    Refused with 409 `conflict` and `details.why`: `no_customer_code_farm` (the tenant has no farm that
    runs customer code) or `uploads_off` (an operator has switched uploads off). A tenant already
    keeping as many versions as it may is 409 `quota_exceeded` with `details {quota, in_use}`: withdraw
    one.

    Args:
        idempotency_key (str):
        body (ExpertAdvisorUpload): One expert advisor's source: its `.mq5` and its own includes
            (`.mqh`). The platform reads it, checks it and builds it, so what runs is what was
            checked. A compiled `.ex5` is refused: it cannot be read. The size of the whole bundle and
            the number of files are bounded (8 MiB and 30 files unless an operator has changed them).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantExpertAdvisor]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ExpertAdvisorUpload,
    idempotency_key: str,
) -> Response[Union[Error, TenantExpertAdvisor]]:
    """Upload an expert advisor's source to be checked

     Stores the bundle where no cell can reach it and starts the checks; the answer is the new version in
    state `uploaded`. Read the version until `verdict` is set, then the report. The same bundle uploaded
    again answers the version it already made (200) and nothing is checked twice, unless the tenant
    withdrew that version. For an approved version it also starts a build for each MetaTrader build of
    the tenant's customer-code farms that the version has no build for and none running (a farm moved to
    a newer MetaTrader, or such a build failed); an attach's 409 `build_mismatch` says where it stands.
    Refused with 409 `conflict` and `details.why`: `no_customer_code_farm` (the tenant has no farm that
    runs customer code) or `uploads_off` (an operator has switched uploads off). A tenant already
    keeping as many versions as it may is 409 `quota_exceeded` with `details {quota, in_use}`: withdraw
    one.

    Args:
        idempotency_key (str):
        body (ExpertAdvisorUpload): One expert advisor's source: its `.mq5` and its own includes
            (`.mqh`). The platform reads it, checks it and builds it, so what runs is what was
            checked. A compiled `.ex5` is refused: it cannot be read. The size of the whole bundle and
            the number of files are bounded (8 MiB and 30 files unless an operator has changed them).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TenantExpertAdvisor]]
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
    body: ExpertAdvisorUpload,
    idempotency_key: str,
) -> Optional[Union[Error, TenantExpertAdvisor]]:
    """Upload an expert advisor's source to be checked

     Stores the bundle where no cell can reach it and starts the checks; the answer is the new version in
    state `uploaded`. Read the version until `verdict` is set, then the report. The same bundle uploaded
    again answers the version it already made (200) and nothing is checked twice, unless the tenant
    withdrew that version. For an approved version it also starts a build for each MetaTrader build of
    the tenant's customer-code farms that the version has no build for and none running (a farm moved to
    a newer MetaTrader, or such a build failed); an attach's 409 `build_mismatch` says where it stands.
    Refused with 409 `conflict` and `details.why`: `no_customer_code_farm` (the tenant has no farm that
    runs customer code) or `uploads_off` (an operator has switched uploads off). A tenant already
    keeping as many versions as it may is 409 `quota_exceeded` with `details {quota, in_use}`: withdraw
    one.

    Args:
        idempotency_key (str):
        body (ExpertAdvisorUpload): One expert advisor's source: its `.mq5` and its own includes
            (`.mqh`). The platform reads it, checks it and builds it, so what runs is what was
            checked. A compiled `.ex5` is refused: it cannot be read. The size of the whole bundle and
            the number of files are bounded (8 MiB and 30 files unless an operator has changed them).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TenantExpertAdvisor]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
