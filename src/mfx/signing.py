"""The four headers every MFX request carries, and the key that makes them.

An MFX request is signed, not bearing a token: ``X-MFX-Key`` names the key, ``X-MFX-Timestamp`` and
``X-MFX-Nonce`` make each request usable once, and ``X-MFX-Signature`` is an **Ed25519** signature
over::

    timestamp_ms\\nnonce\\nMETHOD\\npath_with_query\\nsha256_hex(body)

base64-encoded. The timestamp is epoch milliseconds and must be within ±30 s of the server's clock;
the nonce must be unique per key for five minutes. A retry is therefore a *new* signature, never the
same one sent twice — which is why every retry in this SDK re-enters the signing layer rather than
resending a built request.

**The nonce is inside the signature.** It used to sit
beside it: the signature covered the timestamp, method, path and body but not the nonce, so anyone
holding a captured request could put a fresh nonce on it and replay it for the 30 seconds the
timestamp stayed valid — the replay guard was the one part of the request nobody had signed. A
changed nonce is now a broken signature. Because the nonce is a line in a newline-delimited string,
it is restricted to ``^[A-Za-z0-9_-]{16,64}$``: a nonce containing a newline could otherwise move
the line boundaries and sign one request as another.

This is a hard cut-over with no dual acceptance — accepting both strings would keep the hole open
exactly as long as the old one worked. No tenant key exists yet, so nothing breaks.

The private key is returned once when the key is issued and the platform never stores it. This
module never writes it anywhere: :class:`SigningKey` renders as ``***`` in a repr, an f-string, a
log line and a traceback, so a key cannot reach a log by being printed.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
import secrets
import time
from collections.abc import Callable, Generator
from typing import Any, Final

import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

__all__ = [
    "KEY_HEADER",
    "NONCE_HEADER",
    "SIGNATURE_HEADER",
    "TIMESTAMP_HEADER",
    "MfxSignature",
    "SigningKey",
    "signing_message",
]

KEY_HEADER: Final = "X-MFX-Key"
TIMESTAMP_HEADER: Final = "X-MFX-Timestamp"
NONCE_HEADER: Final = "X-MFX-Nonce"
SIGNATURE_HEADER: Final = "X-MFX-Signature"

#: Ed25519 private keys are 32 bytes. Anything else is not one, whatever it decodes to.
_SEED_BYTES: Final = 32

#: What the platform accepts as a nonce. token_urlsafe(16) conforms, and so does a
#: uuid4 in either form.
_NONCE_RE: Final = re.compile(r"[A-Za-z0-9_-]{16,64}")


def _load(key: Ed25519PrivateKey | str | bytes) -> Ed25519PrivateKey:
    if isinstance(key, Ed25519PrivateKey):
        return key
    material = key.encode("ascii") if isinstance(key, str) else key
    material = material.strip()
    if material.startswith(b"-----BEGIN"):
        loaded = load_pem_private_key(material, password=None)
        if not isinstance(loaded, Ed25519PrivateKey):
            raise TypeError(f"an MFX key is Ed25519, not {type(loaded).__name__}")
        return loaded
    try:
        raw = base64.b64decode(material, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(
            "a signing key is a PEM private key or the base64 of its 32 raw bytes"
        ) from exc
    if len(raw) != _SEED_BYTES:
        raise ValueError(
            f"an Ed25519 private key is {_SEED_BYTES} bytes; this decoded to {len(raw)}"
        )
    return Ed25519PrivateKey.from_private_bytes(raw)


class SigningKey:
    """A tenant's Ed25519 private key, which renders as ``***`` everywhere it could be printed.

    Accepts the key as PEM, as the base64 of its 32 raw bytes, or as an already-loaded
    ``Ed25519PrivateKey``.
    """

    __slots__ = ("_key",)

    _key: Ed25519PrivateKey

    def __init__(self, key: Ed25519PrivateKey | str | bytes | SigningKey) -> None:
        self._key = key._key if isinstance(key, SigningKey) else _load(key)

    def sign(self, message: bytes) -> str:
        """The base64 signature of ``message``."""
        return base64.b64encode(self._key.sign(message)).decode("ascii")

    def __repr__(self) -> str:
        return "SigningKey(***)"

    __str__ = __repr__

    def __format__(self, spec: str) -> str:
        return "***"

    def __reduce__(self) -> tuple[Any, ...]:
        """Unpicklable on purpose: a pickled key is a key written to a file by accident."""
        raise TypeError("a SigningKey is never serialised; load it from your own secret store")


def signing_message(
    timestamp: str, nonce: str, method: str, path_with_query: str, body: bytes
) -> bytes:
    """The exact bytes an MFX signature covers — one place, so the client and the tests agree.

    Raises when the nonce is not ``^[A-Za-z0-9_-]{16,64}$``. Refusing here rather than sending it is
    deliberate: the server answers 401 to a bad nonce, and "auth_error" is a poor way to learn that
    a custom nonce generator emits something with a newline in it.
    """
    if not _NONCE_RE.fullmatch(nonce):
        raise ValueError(
            f"a nonce is 16-64 characters of A-Z a-z 0-9 _ - ; got {len(nonce)} characters. "
            "It is a line of the signed message, so anything else could move the line boundaries."
        )
    digest = hashlib.sha256(body).hexdigest()
    return "\n".join((timestamp, nonce, method.upper(), path_with_query, digest)).encode("utf-8")


class MfxSignature(httpx.Auth):
    """Signs every request as it goes out, with a fresh timestamp and nonce each time."""

    #: The signature covers the body, so httpx must have it before ``auth_flow`` runs.
    requires_request_body = True

    def __init__(
        self,
        key_id: str,
        key: SigningKey | Ed25519PrivateKey | str | bytes,
        *,
        clock: Callable[[], float] = time.time,
        nonce: Callable[[], str] = lambda: secrets.token_urlsafe(16),
    ) -> None:
        self.key_id = key_id
        self._key = SigningKey(key)
        self._clock = clock
        self._nonce = nonce

    def headers_for(self, method: str, path_with_query: str, body: bytes = b"") -> dict[str, str]:
        """The four headers for one request, with a fresh timestamp and nonce.

        The WebSocket upgrade is signed through here too, so the stream and every REST call put
        the same bytes under the same signature. A second implementation for the upgrade is how
        the two drift until one of them is a 401 nobody can explain.
        """
        timestamp = str(int(self._clock() * 1000))
        nonce = self._nonce()
        return {
            KEY_HEADER: self.key_id,
            TIMESTAMP_HEADER: timestamp,
            NONCE_HEADER: nonce,
            SIGNATURE_HEADER: self._key.sign(
                signing_message(timestamp, nonce, method, path_with_query, body)
            ),
        }

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # raw_path is the path with its query exactly as it goes on the wire; rebuilding it from
        # the parsed parts is where a client and a server stop agreeing about escaping.
        """Sign each request as it is sent. This is httpx's auth hook; it is not called directly."""
        path_with_query = request.url.raw_path.decode("ascii")
        request.headers.update(self.headers_for(request.method, path_with_query, request.content))
        yield request

    def __repr__(self) -> str:
        return f"MfxSignature(key_id={self.key_id!r}, key=***)"
