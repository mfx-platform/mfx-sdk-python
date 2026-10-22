"""One fake MFX for the unit suite: a transport that records what was signed and answers to order.

Nothing here reaches a network. The conformance suite (tests/conformance) is what runs against a
real deployment; these tests are about what the SDK *sends* and how it reads what comes back.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx.client import MfxClient

BASE_URL = "https://api.dev.mfxhub.com/v1"
KEY_ID = "key_01J8Z4Q"
TERMINAL_ID = "0191f0c2-aaaa-7bbb-8ccc-000000000001"
FARM_ID = "1c2d3e4f-5a6b-7c8d-9e0f-102030405060"
BROKER_ID = "2c2d3e4f-5a6b-7c8d-9e0f-102030405060"
SERVER_ID = "3c2d3e4f-5a6b-7c8d-9e0f-102030405060"


def terminal_body(state: str = "REQUESTED", **overrides: Any) -> dict[str, Any]:
    """A TenantTerminal as the API answers one, with only its required fields."""
    body: dict[str, Any] = {
        "id": TERMINAL_ID,
        "farm": {"id": FARM_ID, "label": "dev-uk-west"},
        "broker": {"id": BROKER_ID, "label": "Equiti"},
        "server": {"id": SERVER_ID, "label": "EquitiSecurities-Demo"},
        "streaming": True,
        "execution": False,
        "state": state,
        "instruments": ["EURUSD"],
        "created_at": "2026-09-21T09:00:00Z",
    }
    body.update(overrides)
    return body


@dataclass
class FakeMfx:
    """Answers the SDK, and keeps every request it was asked to sign."""

    responses: list[httpx.Response] = field(default_factory=list)
    requests: list[httpx.Request] = field(default_factory=list)
    #: Budget headers put on every answer, as the API promises (openapi.yaml info).
    budget: tuple[str, str] | None = ("999", "counted")

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        response = (
            self.responses.pop(0) if self.responses else httpx.Response(200, json={"ok": True})
        )
        if self.budget is not None:
            remaining, source = self.budget
            response.headers["X-MFX-Budget-Remaining"] = remaining
            response.headers["X-MFX-Budget-Source"] = source
        return response

    @property
    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def signed(self, index: int = -1) -> dict[str, str]:
        headers = self.requests[index].headers
        return {
            name: headers[name]
            for name in ("X-MFX-Key", "X-MFX-Timestamp", "X-MFX-Nonce", "X-MFX-Signature")
        }


def error(status: int, code: str, message: str, **headers: str) -> httpx.Response:
    return httpx.Response(
        status, json={"error": {"code": code, "message": message}}, headers=headers
    )


def accepted(state: str = "REQUESTED") -> httpx.Response:
    return httpx.Response(202, json=terminal_body(state))


def page(items: list[dict[str, Any]], next_cursor: str | None) -> httpx.Response:
    return httpx.Response(
        200, json={"items": items, "next_cursor": next_cursor, "returned": len(items)}
    )


@pytest.fixture
def private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


@pytest.fixture
def raw_key(private_key: Ed25519PrivateKey) -> str:
    """The key as MFX hands it over: base64 of the 32 raw bytes."""
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
    )

    raw = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    return base64.b64encode(raw).decode("ascii")


@pytest.fixture
def mfx() -> FakeMfx:
    return FakeMfx()


@pytest.fixture
def client(mfx: FakeMfx, private_key: Ed25519PrivateKey, sleeps: list[float]) -> MfxClient:
    return MfxClient(
        BASE_URL,
        KEY_ID,
        private_key,
        transport=mfx.transport,
        sleep=_record(sleeps),
        jitter=lambda _low, high: high,  # deterministic: the whole ceiling, never a random slice
    )


@pytest.fixture
def sleeps() -> list[float]:
    """Every wait the client would have taken, instead of taking it."""
    return []


def _record(sleeps: list[float]) -> Callable[[float], Any]:
    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    return sleep


def body_of(request: httpx.Request) -> dict[str, Any]:
    return json.loads(request.content)
