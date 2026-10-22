"""A failure upstream of the platform reaches the caller whole: 503 by code, never lost at the
edge."""

from __future__ import annotations

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import UpstreamError

from .conftest import TERMINAL_ID, FakeMfx


def _error(status: int, code: str, reason: str | None = None, **headers: str) -> httpx.Response:
    details = {} if reason is None else {"reason": reason}
    body = {"error": {"code": code, "message": f"{code} happened", "details": details}}
    return httpx.Response(status, json=body, headers=headers)


async def test_an_upstream_failure_is_a_503_with_its_reason_and_an_edge_page_says_it_is_the_edge(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given the platform answering 503 upstream_error when the tenant's terminal does not answer,
    503 dependency_unavailable with Retry-After when a store of its own does not, and the edge in
    between answering 502 or 504 with a page of its own and no MFX body
    When the caller reads a terminal
    Then each is an UpstreamError: the platform's carry their code, the reason it gave and no
    invented retry time, the store's carries its Retry-After, and the edge's say they came from the
    edge (the platform answers neither 502 nor 504), with no reason it did not give."""
    mfx.responses.append(_error(503, "upstream_error", "terminal_timeout"))
    with pytest.raises(UpstreamError) as timed_out:
        await client.terminals.get(TERMINAL_ID)
    said = timed_out.value
    assert (said.status, said.code, said.reason) == (503, "upstream_error", "terminal_timeout")
    assert said.retry_after_s is None and said.from_edge is False

    mfx.responses.append(_error(503, "dependency_unavailable", **{"Retry-After": "7"}))
    with pytest.raises(UpstreamError) as store:
        await client.terminals.get(TERMINAL_ID)
    assert (store.value.code, store.value.retry_after_s, store.value.reason) == (
        "dependency_unavailable", 7.0, None,
    )  # fmt: skip

    for status in (502, 504):
        mfx.responses.append(
            httpx.Response(
                status, text="<html>error code: 5xx</html>", headers={"content-type": "text/html"}
            )
        )
        with pytest.raises(UpstreamError) as edge:
            await client.terminals.get(TERMINAL_ID)
        assert edge.value.status == status and edge.value.from_edge is True
        assert edge.value.reason is None
