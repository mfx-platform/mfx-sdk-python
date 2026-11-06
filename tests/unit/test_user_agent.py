"""The SDK names itself on every call, so the platform can tell which SDK and version made it."""

from __future__ import annotations

import tomllib
from pathlib import Path

import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import mfx
from mfx.client import MfxClient
from mfx.sync import SyncMfxClient

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx, terminal_body
from .test_streaming import FakeTransport

#: The Story these cases are Tested By: the SDKs name themselves in the call log.

NAMED = f"mfx-sdk-python/{mfx.__version__}"


async def test_every_rest_call_names_the_sdk_and_its_version(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a client / When it reads and when it retries / Then every request carries
    `User-Agent: mfx-sdk-python/<version>`, not the HTTP library's own name, so the platform's call
    log can say which SDK and which version made each call."""
    mfx.responses.extend(
        [
            httpx.Response(
                429,
                json={"error": {"code": "rate_limited", "message": "slow"}},
                headers={"Retry-After": "0"},
            ),
            httpx.Response(200, json=terminal_body("ACTIVE")),
        ]
    )

    await client.terminals.get(TERMINAL_ID)

    assert [r.headers["User-Agent"] for r in mfx.requests] == [NAMED, NAMED], "a retry too"
    assert "python-httpx" not in mfx.last.headers["User-Agent"]


def test_the_blocking_client_names_the_sdk_the_same_way(
    mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given the blocking client, which is the same client underneath / When it reads / Then the
    request carries the same `User-Agent: mfx-sdk-python/<version>`."""
    mfx.responses.append(httpx.Response(200, json=terminal_body("ACTIVE")))

    with SyncMfxClient(BASE_URL, KEY_ID, private_key, transport=mfx.transport) as blocking:
        blocking.get_terminal(TERMINAL_ID)

    assert mfx.last.headers["User-Agent"] == NAMED


async def test_the_stream_upgrade_names_the_sdk_beside_its_signature(client: MfxClient) -> None:
    """Given a client / When it opens the stream / Then the upgrade request carries the same name
    beside the four signing headers, whatever transport opens the socket."""
    transport = FakeTransport([])

    async with client.stream(connect=transport):
        pass

    assert transport.headers[0]["User-Agent"] == NAMED


def test_the_version_named_is_the_packages_own() -> None:
    """Given the package as released / When its name is built / Then the version in it is the
    package's own, never typed twice, so the version a user installed is the one the platform
    records."""
    pyproject = tomllib.loads((Path(__file__).parents[2] / "pyproject.toml").read_text("utf-8"))

    assert mfx.__version__ == pyproject["project"]["version"]
    assert "mfx-sdk-python/" + pyproject["project"]["version"] == NAMED
