"""``client.webhooks`` and ``verify`` — MFX Hub calling a tenant's address."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

import httpx
import pytest

from mfx import Secret, WebhookSignatureError, verify
from mfx.client import MfxClient

from .conftest import FakeMfx, body_of

ENDPOINT_ID = "4c2d3e4f-5a6b-7c8d-9e0f-102030405060"
FAILURE_ID = "5c2d3e4f-5a6b-7c8d-9e0f-102030405060"
SECRET = "x" * 43  # a stand-in of the right length; never a real secret
BODY = b'{"type":"position.closed","schema_version":"1","id":"1792160000000-0","ticket":7}'


def _signed(body: bytes, at: int, *keys: str) -> str:
    """The platform's own construction (mfx-control-plane services/webhook_delivery.signature):
    HMAC-SHA256 keyed with the secret's UTF-8 text over `<t>.<body>`, newest secret first."""
    signed = str(at).encode() + b"." + body
    return ",".join(
        [f"t={at}"]
        + [f"v1={hmac.new(k.encode(), signed, hashlib.sha256).hexdigest()}" for k in keys]
    )


def _endpoint(**overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": ENDPOINT_ID, "url": "https://hooks.example.com/mfx",
        "event_types": ["position.closed"],
        "description": None, "status": "active", "paused_reason": None, "paused_by": None,
        "delivered": 0, "last_delivered_at": None, "last_failed_at": None, "retrying": 0,
        "dead": 0, "cursor": None, "previous_secret_until": None,
        "created_at": "2026-10-16T12:00:00Z",
    }  # fmt: skip
    body.update(overrides)
    return body


def _failure(n: int) -> dict[str, Any]:
    return {"id": FAILURE_ID, "event_id": f"1792160000000-{n}", "event_type": "position.closed",
            "state": "dead", "next_attempt_at": None, "prune_at": "2026-10-23T12:00:00Z",
            "attempts": [{"at": "2026-10-16T12:00:01Z", "outcome": "status", "status_code": 500,
                          "ms": 40}]}  # fmt: skip


def test_a_delivery_is_verified_over_the_body_as_received_within_five_minutes() -> None:
    """Given a delivery signed as the platform signs one
    When the receiver verifies it with the endpoint's secret
    Then it passes and the signed time is returned, as bytes, text or a Secret; for the day after
    a rotation either secret passes against a header carrying both; and a body changed by one
    byte, a secret that did not sign it, a time more than five minutes from the receiver's clock
    either way, or a header without t= or v1= is refused, each with its own reason."""
    at = 1_792_160_000
    header = _signed(BODY, at, SECRET)
    assert verify(BODY, header, SECRET, now=at + 10) == at
    assert verify(BODY.decode(), header, Secret(SECRET), now=at - 299) == at

    new = "Nw" + SECRET[2:]
    both = _signed(BODY, at, new, SECRET)
    assert verify(BODY, both, [new], now=at) == at
    assert verify(BODY, both, [Secret(SECRET)], now=at) == at, "the previous secret still signs"

    refusals = {
        "mismatch": lambda: verify(BODY.replace(b"7", b"8"), header, SECRET, now=at),
        "mismatch ": lambda: verify(BODY, header, new, now=at),
        "stale": lambda: verify(BODY, header, SECRET, now=at + 301),
        "stale ": lambda: verify(BODY, header, SECRET, now=at - 301),
        "malformed": lambda: verify(BODY, "v1=abc", SECRET, now=at),
        "malformed ": lambda: verify(BODY, f"t={at}", SECRET, now=at),
    }
    for reason, call in refusals.items():
        with pytest.raises(WebhookSignatureError) as raised:
            call()
        assert raised.value.reason == reason.strip()
    assert verify(BODY, _signed(BODY, int(__import__("time").time()), SECRET), SECRET)


async def test_an_endpoint_is_registered_with_its_types_and_its_secret_is_in_that_answer_only(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a tenant with hook:write
    When it registers an endpoint, lists its endpoints and reads one
    Then one POST /webhooks carries the address, the types, the description and the idempotency
    key, the answer carries the secret, and the list and the read are the endpoints as the
    platform describes them, with no secret."""
    mfx.responses.append(httpx.Response(201, json={**_endpoint(), "secret": SECRET}))
    created = await client.webhooks.create(
        "https://hooks.example.com/mfx", ["position.closed", "terminal.*"],
        description="desk one", idempotency_key="hook-1",
    )  # fmt: skip
    request = mfx.last
    assert (request.method, request.url.path) == ("POST", "/v1/webhooks")
    assert request.headers["Idempotency-Key"] == "hook-1"
    assert body_of(request) == {"url": "https://hooks.example.com/mfx",
                                "event_types": ["position.closed", "terminal.*"],
                                "description": "desk one"}  # fmt: skip
    assert created.secret == SECRET and str(created.id) == ENDPOINT_ID

    mfx.responses.append(httpx.Response(201, json={**_endpoint(), "secret": SECRET}))
    await client.webhooks.create("https://hooks.example.com/b", ["*"], idempotency_key="hook-2")
    assert body_of(mfx.last) == {"url": "https://hooks.example.com/b", "event_types": ["*"]}

    mfx.responses.append(httpx.Response(200, json={"items": [_endpoint(delivered=4)]}))
    [listed] = await client.webhooks.list()
    assert listed.delivered == 4 and not hasattr(listed, "secret")
    mfx.responses.append(httpx.Response(200, json=_endpoint(dead=1)))
    read = await client.webhooks.get(ENDPOINT_ID)
    assert mfx.last.url.path == f"/v1/webhooks/{ENDPOINT_ID}" and read.dead == 1


async def test_an_endpoint_is_changed_paused_resumed_rotated_tested_and_removed(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an endpoint
    When the tenant changes only its types, pauses it, resumes it, rotates its secret, asks for a
    test event and removes it
    Then each is one request to its route with only what was given in the body; pausing sends
    status paused and resuming active; the rotation answers the new secret and until when the old
    one also signs; the test answers the event's id; and the removal sends DELETE."""
    path = f"/v1/webhooks/{ENDPOINT_ID}"
    for _ in range(3):
        mfx.responses.append(httpx.Response(200, json=_endpoint()))
    await client.webhooks.update(ENDPOINT_ID, event_types=["terminal.*"], idempotency_key="u1")
    assert (mfx.last.method, mfx.last.url.path) == ("PATCH", path)
    assert body_of(mfx.last) == {"event_types": ["terminal.*"]}
    await client.webhooks.update(ENDPOINT_ID, paused=True, idempotency_key="u2")
    assert body_of(mfx.last) == {"status": "paused"}
    await client.webhooks.update(ENDPOINT_ID, paused=False, url="https://h.example.com/x",
                                 description="d", idempotency_key="u3")  # fmt: skip
    assert body_of(mfx.last) == {"status": "active", "url": "https://h.example.com/x",
                                 "description": "d"}  # fmt: skip

    mfx.responses.append(httpx.Response(200, json={
        "secret": "new", "previous_secret_until": "2026-10-17T12:00:00Z"}))  # fmt: skip
    rotated = await client.webhooks.rotate_secret(ENDPOINT_ID, idempotency_key="r1")
    assert (mfx.last.method, mfx.last.url.path) == ("POST", f"{path}/rotate-secret")
    assert mfx.last.headers["Idempotency-Key"] == "r1"
    assert rotated.secret == "new" and rotated.previous_secret_until.day == 17

    mfx.responses.append(httpx.Response(202, json={"event_id": "1792160000000-3"}))
    assert (await client.webhooks.test(ENDPOINT_ID)).event_id == "1792160000000-3"
    assert (mfx.last.method, mfx.last.url.path) == ("POST", f"{path}/test")

    mfx.responses.append(httpx.Response(204))
    assert await client.webhooks.delete(ENDPOINT_ID) is None
    assert (mfx.last.method, mfx.last.url.path) == ("DELETE", path)


async def test_what_did_not_arrive_is_read_page_by_page_and_events_are_asked_for_again(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given an endpoint with failed deliveries over two pages
    When the tenant reads its dead letters, then asks for events after a cursor and for one
    failure again
    Then the failures follow the cursor to the end, narrowed to the state asked, each with its
    attempts; a replay is one POST naming the cursor or the failure, never both and never neither;
    and the answer says how many events will be sent."""
    mfx.responses.append(httpx.Response(200, json={"items": [_failure(1)], "next_cursor": "c2"}))
    mfx.responses.append(httpx.Response(200, json={"items": [_failure(2)], "next_cursor": None}))
    failures = [f async for f in client.webhooks.failures(ENDPOINT_ID, state="dead", limit=1)]
    assert [f.event_id for f in failures] == ["1792160000000-1", "1792160000000-2"]
    assert failures[0].attempts[0].status_code == 500
    first, second = mfx.requests[-2], mfx.requests[-1]
    assert dict(first.url.params) == {"state": "dead", "limit": "1"}
    assert dict(second.url.params) == {"state": "dead", "limit": "1", "cursor": "c2"}

    mfx.responses.append(httpx.Response(202, json={"events": 12}))
    accepted = await client.webhooks.replay(
        ENDPOINT_ID, after="1792160000000-0", idempotency_key="p1"
    )
    assert (mfx.last.method, mfx.last.url.path) == ("POST", f"/v1/webhooks/{ENDPOINT_ID}/replay")
    assert body_of(mfx.last) == {"after": "1792160000000-0"} and accepted.events == 12
    mfx.responses.append(httpx.Response(202, json={"events": 1}))
    await client.webhooks.replay(ENDPOINT_ID, failure_id=FAILURE_ID, idempotency_key="p2")
    assert body_of(mfx.last) == {"failure_id": FAILURE_ID}
    for kwargs in ({}, {"after": "x", "failure_id": FAILURE_ID}):
        with pytest.raises(ValueError, match="exactly one"):
            await client.webhooks.replay(ENDPOINT_ID, idempotency_key="p3", **kwargs)
