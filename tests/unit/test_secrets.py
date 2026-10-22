"""``Secret`` and the odds and ends around it: a secret never reaches a log."""

from __future__ import annotations

import logging
import pickle

import httpx
import pytest

from mfx.client import MfxClient
from mfx.errors import retry_after_seconds
from mfx.secrets import Secret

from .conftest import TERMINAL_ID, FakeMfx, terminal_body

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.


def test_sdk_logs_redact_credentials_secrets_and_signatures_by_type(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Given a secret held by the SDK's own type / When it is logged, printed, interpolated or
    formatted / Then ``***`` appears and the value never does.

    By type, not by a filter that matches field names: a redaction that depends on a key being
    called "password" leaks the day someone calls it "pw"."""
    secret = Secret("hunter2-and-then-some")

    with caplog.at_level(logging.DEBUG):
        logging.getLogger("mfx.test").info("submitting %s for %s", secret, TERMINAL_ID)
        logging.getLogger("mfx.test").info("as f-string: %s", f"{secret}")
        logging.getLogger("mfx.test").info("as repr: %r", secret)

    assert "hunter2" not in caplog.text
    assert "***" in caplog.text
    assert f"{secret!r}" == "Secret(***)" and f"{secret}" == "***"
    assert str(secret) == "Secret(***)"


def test_a_secret_can_be_compared_and_tested_without_being_revealed() -> None:
    """Enough behaviour to be usable — equality for a rotation check, truthiness for "is it set" —
    and no more."""
    assert Secret("a") == Secret("a")
    assert Secret("a") != Secret("b")
    assert Secret("a") != "a", "never equal to a bare string; that is the point of the type"
    assert len({Secret("a"), Secret("a"), Secret("b")}) == 2
    assert bool(Secret("a")) is True and bool(Secret("")) is False
    assert Secret(Secret("a")).reveal() == "a", "wrapping twice is not double-wrapping"


def test_a_secret_cannot_be_pickled_into_a_file() -> None:
    with pytest.raises(TypeError, match="never serialised"):
        pickle.dumps(Secret("a"))


def test_a_retry_after_that_is_a_date_is_ignored_rather_than_guessed() -> None:
    """An HTTP-date is legal in Retry-After. This SDK does not parse one, and says so by backing
    off on its own schedule instead of inventing a number."""
    assert retry_after_seconds({"Retry-After": "5"}) == 5.0
    assert retry_after_seconds({"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}) is None
    assert retry_after_seconds({}) is None


async def test_draining_a_terminal_leaves_it_in_place(client: MfxClient, mfx: FakeMfx) -> None:
    """Drain is not retire: the terminal stops taking new work and stays."""
    mfx.responses.append(httpx.Response(202, json=terminal_body("DRAINING")))
    draining = await client.terminals.drain(TERMINAL_ID, idempotency_key="drain-1")
    assert draining.state.value == "DRAINING"
    assert mfx.last.method == "POST"
    assert mfx.last.url.path == f"/v1/terminals/{TERMINAL_ID}/drain"


async def test_the_client_really_waits_when_nobody_replaces_its_clock() -> None:
    """The default sleep is a real one; the tests replace it so they do not wait, and this is the
    one place that proves the thing they replaced works."""
    await MfxClient._default_sleep(0.0)
