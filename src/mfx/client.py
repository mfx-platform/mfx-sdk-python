"""``MfxClient`` — the connection a tenant holds.

It owns one signed ``httpx.AsyncClient``, the remaining budget the platform reports on every
answer, and the read retry policy. It owns no business logic: ``client.terminals`` and its siblings
are thin objects that build requests from the generated core and hand them here.

Retries re-enter the signing layer rather than resending a built request, because every MFX request
carries a nonce that is good once (see :mod:`mfx.signing`). Reads retry on 429 honouring
``Retry-After`` with jitter; **writes never retry** — a retried write is a second order.
"""

from __future__ import annotations

import random
import time
import types
from collections.abc import Awaitable, Callable, Mapping
from contextvars import ContextVar
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Final, Self

import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mfx._generated.client import Client as GeneratedClient
from mfx._generated.types import Response as GeneratedResponse
from mfx.accounts import Accounts
from mfx.catalog import Catalog
from mfx.errors import (
    MfxApiError,
    MfxTimeout,
    MfxTransportError,
    raise_for,
    retry_after_seconds,
)
from mfx.execution import Execution
from mfx.expert_advisors import ExpertAdvisors, Tenant
from mfx.farms import Farms
from mfx.maintenance import Maintenance
from mfx.md import MarketData
from mfx.signing import MfxSignature, SigningKey
from mfx.streaming import Connector, MfxStream, websockets_connector
from mfx.terminals import Terminals
from mfx.usage import UsageReader
from mfx.webhooks import Webhooks

__all__ = ["Budget", "MfxClient"]

DEFAULT_TIMEOUT_S: Final = 30.0
#: Read retries on 429. Small: a budget that is out stays out, and a caller waiting on a client
#: that quietly retries for a minute has no way to know why nothing is happening.
DEFAULT_READ_RETRIES: Final = 3
#: Used when the server does not say. Doubles per attempt, with jitter so a fleet of clients that
#: hit the limit together do not come back together.
_BACKOFF_BASE_S: Final = 0.5
_BACKOFF_CAP_S: Final = 20.0

#: The raw answer to the call running in this context, so a body the generated parser cannot read
#: is still reported as the HTTP failure it was. Per-context, so concurrent calls never see each
#: other's answers.
_IN_FLIGHT: ContextVar[list[httpx.Response]] = ContextVar("mfx_in_flight")


@dataclass(frozen=True, slots=True)
class Budget:
    """What the key has left, as of the last answer (``X-MFX-Budget-*``)."""

    remaining: int
    #: ``counted`` when it is a measurement, ``configured`` when it is the key's allowance,
    #: ``unconfigured`` when the key has none. A number whose source is not ``counted`` is a
    #: ceiling, not a reading.
    source: str


class MfxClient:
    """A tenant's connection to MFX.

    ``base_url`` includes the version: ``https://api.mfxhub.com/v1``, or
    ``https://api.dev.mfxhub.com/v1`` for development.
    """

    def __init__(
        self,
        base_url: str,
        key_id: str,
        private_key: SigningKey | Ed25519PrivateKey | str | bytes,
        *,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        read_retries: int = DEFAULT_READ_RETRIES,
        transport: httpx.AsyncBaseTransport | None = None,
        sleep: Callable[[float], Awaitable[None]] | None = None,
        jitter: Callable[[float, float], float] = random.uniform,  # noqa: S311 - backoff, not crypto
        wall: Callable[[], float] = time.monotonic,
    ) -> None:
        self._wall = wall
        self._base_url = base_url.rstrip("/")
        self._auth = MfxSignature(key_id, private_key)
        self._read_retries = read_retries
        self._jitter = jitter
        self._sleep = sleep or self._default_sleep
        self._budget: Budget | None = None
        self._http = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            auth=self._auth,
            timeout=timeout_s,
            transport=transport,
            event_hooks={"response": [self._observe]},
        )
        # The generated core builds and parses; this client sends. It is handed our httpx client so
        # every generated call is signed, budgeted and retried by the same rules.
        self._generated = GeneratedClient(base_url=base_url.rstrip("/"))
        self._generated.set_async_httpx_client(self._http)
        self.terminals = Terminals(self)
        self.execution = Execution(self)
        self.catalog = Catalog(self)
        self.accounts = Accounts(self)
        self.md = MarketData(self)
        self.usage = UsageReader(self)
        self.webhooks = Webhooks(self)
        self.expert_advisors = ExpertAdvisors(self)
        self.tenant = Tenant(self)
        self.maintenance = Maintenance(self)
        self.farms = Farms(self)

    @staticmethod
    async def _default_sleep(seconds: float) -> None:
        import anyio

        await anyio.sleep(seconds)

    async def _observe(self, response: httpx.Response) -> None:
        """Every answer passes here: the budget is read, and the raw answer is kept for this call.

        The raw answer matters because the generated core parses eagerly — including error bodies.
        A 502 carrying a proxy's HTML makes its parser raise, and without the answer in hand the
        SDK could only say "unreadable" about something it knows perfectly well is a 502.
        """
        await response.aread()
        slot = _IN_FLIGHT.get(None)
        if slot is not None:
            slot.append(response)
        remaining = response.headers.get("X-MFX-Budget-Remaining")
        if remaining is None:
            return
        try:
            self._budget = Budget(int(remaining), response.headers.get("X-MFX-Budget-Source", ""))
        except ValueError:  # a header that is not a number tells us nothing; keep the last one
            return

    @property
    def budget(self) -> Budget | None:
        """What the key had left when MFX last answered; None before the first answer."""
        return self._budget

    @property
    def key_id(self) -> str:
        """The id of the API key this client signs with. Safe to log, unlike the private key."""
        return self._auth.key_id

    @property
    def base_url(self) -> str:
        """The REST base this client was pointed at. The stream's host is derived from it."""
        return self._base_url

    @property
    def signature(self) -> MfxSignature:
        """The signer, so the WebSocket upgrade is signed by the same code as every REST call."""
        return self._auth

    def backoff_for(self, attempt: int) -> float:
        """Jittered exponential backoff for an attempt, with no server-supplied delay in hand.

        Exposed so the stream's reconnects and the read path's retries lean on this tenant's quota
        at the same rate; two backoff policies in one client is one policy nobody tuned.
        """
        return self._wait_for(attempt, {})

    def stream(
        self,
        *,
        connect: Connector | None = None,
        url: str | None = None,
        max_reconnects: int | None = None,
    ) -> MfxStream:
        """The multiplexed WebSocket stream. Opened with ``async with``.

        ``connect`` replaces the transport, which is how a test drives reconnects without a server.
        """
        return MfxStream(
            self,
            connect=connect or websockets_connector,
            url=url,
            max_reconnects=max_reconnects,
        )

    @property
    def generated(self) -> GeneratedClient:
        """The generated client, for the endpoint modules. Not part of the public surface."""
        return self._generated

    def wall(self) -> float:
        """This client's clock, so latency is measured the same way everywhere and can be faked."""
        return self._wall()

    async def pause(self, seconds: float) -> None:
        """This client's sleep — the one the retry policy uses, so a test waits for nothing."""
        await self._sleep(seconds)

    def raise_for_answer(self, response: GeneratedResponse[Any], what: str) -> None:
        """Raise the typed error for a failed answer, for a caller that wants to catch rather than
        check. ``execution`` uses it to turn a refusal into a result rather than an exception."""
        raise_for(int(response.status_code), response.headers, response.content, what)

    def _wait_for(self, attempt: int, headers: Mapping[str, str]) -> float:
        """The server's own answer when it gave one; otherwise jittered exponential backoff."""
        told = retry_after_seconds(headers)
        if told is not None:
            return told
        ceiling = min(_BACKOFF_BASE_S * 2**attempt, _BACKOFF_CAP_S)
        return self._jitter(0.0, ceiling)

    async def read(self, call: Callable[[], Awaitable[GeneratedResponse[Any]]], what: str) -> Any:  # noqa: ANN401 - the generated union
        """Run a generated read and return what the generated core parsed."""
        return (await self.read_raw(call, what)).parsed

    async def read_raw(
        self, call: Callable[[], Awaitable[GeneratedResponse[Any]]], what: str
    ) -> GeneratedResponse[Any]:
        """Run a generated read, retrying 429 with the server's own delay.

        Each attempt calls ``call()`` again, so it is signed again: a retried request is a new
        request with a new nonce, never the same bytes twice.

        Returns the whole answer, for the one caller that must read the body itself while the page
        schemas generate without their contents.
        """
        for attempt in range(self._read_retries + 1):
            response = await self.send(call, what)
            rate_limited = int(response.status_code) == HTTPStatus.TOO_MANY_REQUESTS
            if rate_limited and attempt < self._read_retries:
                await self._sleep(self._wait_for(attempt, response.headers))
                continue
            raise_for(int(response.status_code), response.headers, response.content, what)
            return response
        raise AssertionError("unreachable: the loop returns or raises")  # pragma: no cover

    async def write(self, call: Callable[[], Awaitable[GeneratedResponse[Any]]], what: str) -> Any:  # noqa: ANN401 - the generated union
        """Run a generated write. Never retried: a retried write is a second order."""
        response = await self.send(call, what)
        raise_for(int(response.status_code), response.headers, response.content, what)
        return response.parsed

    async def send(
        self, call: Callable[[], Awaitable[GeneratedResponse[Any]]], what: str = "the request"
    ) -> GeneratedResponse[Any]:
        """One attempt, with transport faults and unreadable answers turned into MFX errors."""
        slot: list[httpx.Response] = []
        token = _IN_FLIGHT.set(slot)
        try:
            return await call()
        except httpx.TimeoutException as exc:
            raise MfxTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise MfxTransportError(str(exc)) from exc
        except (ValueError, KeyError, TypeError) as exc:
            # The generated parser assumes the answer matches the spec, and parses error bodies
            # too. A failure it cannot read is still a failure the caller must see as itself: a
            # gateway's HTML 502 is UpstreamError, not "unreadable".
            if slot:
                answer = slot[-1]
                raise_for(answer.status_code, answer.headers, answer.content, what)
            raise MfxApiError(
                f"{what} answered something this SDK could not read: {type(exc).__name__}: {exc}",
                status=slot[-1].status_code if slot else 0,
                code="contract_breach",
            ) from exc
        finally:
            _IN_FLIGHT.reset(token)

    async def aclose(self) -> None:
        """Close the client's connections. ``async with MfxClient(...)`` does this for you."""
        await self._http.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: types.TracebackType | None,
    ) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"MfxClient(base_url={self._base_url!r}, key_id={self.key_id!r})"
