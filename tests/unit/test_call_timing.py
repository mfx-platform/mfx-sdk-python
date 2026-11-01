"""Each HTTP call the client makes is timed and handed to whoever asked.

The platform's checks show how long a sample's calls took: their count, median and slowest. A
sample runs as its own process, so the timings leave it through a file named by ``MFX_CALL_LOG``;
code that holds the client can pass ``on_call`` instead.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx import CallTiming, MfxClient
from mfx.errors import MfxTransportError, NotFoundError

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx, error, terminal_body

#: The Story these cases are Tested By: the platform's checks, their per-call latency.


class Clock:
    """A clock that moves only when a call is answered, by a set step each time."""

    def __init__(self, steps_ms: list[float]) -> None:
        self.now = 100.0
        self._steps = iter(steps_ms)

    def __call__(self) -> float:
        return self.now

    def advance(self) -> None:
        self.now += next(self._steps) / 1000


def _timed(mfx: FakeMfx, key: Ed25519PrivateKey, clock: Clock, **kwargs: object) -> MfxClient:
    def handle(request: httpx.Request) -> httpx.Response:
        clock.advance()
        return mfx.handle(request)

    return MfxClient(
        BASE_URL, KEY_ID, key, transport=httpx.MockTransport(handle), wall=clock,
        sleep=_no_sleep, **kwargs,  # type: ignore[arg-type]
    )  # fmt: skip


async def _no_sleep(_seconds: float) -> None:
    return None


@pytest.fixture
def no_call_log(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.delenv("MFX_CALL_LOG", raising=False)
    yield


async def test_every_call_is_timed_and_handed_to_on_call_with_its_status(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, no_call_log: None
) -> None:
    """Given a client with ``on_call``, a read that answers 200 and one that answers 404
    When both are made
    Then ``on_call`` is told each call once, with what was asked, the HTTP status and how long it
    took in milliseconds, measured on the client's own clock; a refused call is timed too."""
    clock = Clock([120.0, 35.0])
    seen: list[CallTiming] = []
    client = _timed(mfx, private_key, clock, on_call=seen.append)
    mfx.responses.extend(
        [httpx.Response(200, json=terminal_body("ACTIVE")), error(404, "not_found", "no such")]
    )

    await client.terminals.get(TERMINAL_ID)
    with pytest.raises(NotFoundError):
        await client.terminals.get(TERMINAL_ID)

    assert [(c.status, round(c.ms)) for c in seen] == [(200, 120), (404, 35)]
    assert all(TERMINAL_ID in c.what for c in seen)


async def test_each_retried_attempt_is_its_own_call(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, no_call_log: None
) -> None:
    """Given a read rate limited once, then answered
    When it is made
    Then two calls are timed, 429 then 200: each attempt reached the platform and cost its time."""
    clock = Clock([10.0, 20.0])
    seen: list[CallTiming] = []
    client = _timed(mfx, private_key, clock, on_call=seen.append)
    mfx.responses.extend(
        [
            error(429, "rate_limited", "slow down", **{"Retry-After": "0"}),
            httpx.Response(200, json=terminal_body("ACTIVE")),
        ]
    )

    await client.terminals.get(TERMINAL_ID)

    assert [(c.status, round(c.ms)) for c in seen] == [(429, 10), (200, 20)]


async def test_a_call_that_never_reached_an_answer_is_timed_with_no_status(
    private_key: Ed25519PrivateKey, no_call_log: None
) -> None:
    """Given a transport that fails to connect
    When a read is made
    Then the caller gets the SDK's transport error, and the call is still timed, status None."""
    seen: list[CallTiming] = []

    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    client = MfxClient(
        BASE_URL, KEY_ID, private_key, transport=httpx.MockTransport(refuse), on_call=seen.append
    )

    with pytest.raises(MfxTransportError):
        await client.terminals.get(TERMINAL_ID)

    assert [c.status for c in seen] == [None]
    assert seen[0].ms >= 0


async def test_mfx_call_log_names_a_file_that_gets_one_line_a_call(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Given ``MFX_CALL_LOG`` naming a file, as the platform's check runner sets for a sample
    When the client makes two calls
    Then the file holds two JSON lines, each the status and milliseconds and nothing else: no
    path, id, header or key, so the file can be read by a process that should see none of them."""
    log = tmp_path / "calls.jsonl"
    monkeypatch.setenv("MFX_CALL_LOG", str(log))
    clock = Clock([50.0, 70.0])
    client = _timed(mfx, private_key, clock)
    mfx.responses.extend([httpx.Response(200, json=terminal_body("ACTIVE"))] * 2)

    await client.terminals.get(TERMINAL_ID)
    await client.terminals.get(TERMINAL_ID)

    lines = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert lines == [{"status": 200, "ms": 50.0}, {"status": 200, "ms": 70.0}]


async def test_a_failing_listener_or_log_never_fails_the_call(
    mfx: FakeMfx, private_key: Ed25519PrivateKey, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Given an ``on_call`` that raises and an ``MFX_CALL_LOG`` that cannot be written
    When a read is made
    Then the read returns its answer: timing is an observation, never a reason for a call to
    fail."""
    monkeypatch.setenv("MFX_CALL_LOG", str(tmp_path / "no-such-dir" / "calls.jsonl"))

    def broken(_timing: CallTiming) -> None:
        raise RuntimeError("listener bug")

    client = _timed(mfx, private_key, Clock([5.0]), on_call=broken)
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))

    terminal = await client.terminals.get(TERMINAL_ID)

    assert terminal.state.value == "ACTIVE"
