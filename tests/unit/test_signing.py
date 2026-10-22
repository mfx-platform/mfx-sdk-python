"""The four headers, and the key that makes them.

If any of this is wrong the platform answers 401 to everything and no other test in this repo means
anything, so these assert the signature bytes themselves rather than that a request was sent.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
import uuid

import httpx
import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

from mfx.client import MfxClient
from mfx.signing import MfxSignature, SigningKey, signing_message

from .conftest import BASE_URL, KEY_ID, TERMINAL_ID, FakeMfx

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.


async def test_every_request_carries_the_four_headers_and_a_signature_that_verifies(
    client: MfxClient, mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given a client holding a tenant's key / When it makes a request / Then the request carries
    X-MFX-Key, X-MFX-Timestamp, X-MFX-Nonce and X-MFX-Signature, and the signature verifies against
    the public key over timestamp\\nnonce\\nMETHOD\\npath_with_query\\nsha256_hex(body).

    Asserted as bytes, not as "a header is present": a signature over the wrong string is a header
    that is present and a platform that answers 401 to everything."""
    mfx.responses.append(httpx.Response(200, json={"items": [], "next_cursor": None}))
    await client.terminals.page(limit=25)

    signed = mfx.signed()
    assert signed["X-MFX-Key"] == KEY_ID
    assert signed["X-MFX-Timestamp"].isdigit(), "epoch milliseconds, not an ISO date"
    assert len(signed["X-MFX-Nonce"]) >= 16

    request = mfx.last
    expected = signing_message(
        signed["X-MFX-Timestamp"],
        signed["X-MFX-Nonce"],
        "GET",
        "/v1/terminals?limit=25",
        request.content,
    )
    private_key.public_key().verify(base64.b64decode(signed["X-MFX-Signature"]), expected)


async def test_the_signature_covers_the_query_and_the_body_so_neither_can_be_changed(
    client: MfxClient, mfx: FakeMfx, private_key: Ed25519PrivateKey
) -> None:
    """Given a signed request / When its query string or its body is altered in flight / Then the
    signature no longer verifies, because both are inside the signed message.

    The body is covered as sha256 hex, and the path is covered *with* its query — a signature over
    the path alone would let a proxy change limit=25 to limit=200 and still verify."""
    mfx.responses.append(httpx.Response(200, json={"items": [], "next_cursor": None}))
    await client.terminals.page(limit=25)
    signed, request = mfx.signed(), mfx.last

    tampered_query = signing_message(
        signed["X-MFX-Timestamp"],
        signed["X-MFX-Nonce"],
        "GET",
        "/v1/terminals?limit=200",
        request.content,
    )
    tampered_body = signing_message(
        signed["X-MFX-Timestamp"],
        signed["X-MFX-Nonce"],
        "GET",
        "/v1/terminals?limit=25",
        b'{"not":"what was sent"}',
    )
    # The one this fix is about: a captured request with a fresh nonce on it.
    tampered_nonce = signing_message(
        signed["X-MFX-Timestamp"],
        "ffffffffffffffffffffffffffffffff",
        "GET",
        "/v1/terminals?limit=25",
        request.content,
    )
    signature = base64.b64decode(signed["X-MFX-Signature"])
    for message in (tampered_query, tampered_body, tampered_nonce):
        with pytest.raises(InvalidSignature):
            private_key.public_key().verify(signature, message)


async def test_each_request_is_signed_again_with_a_new_nonce_and_timestamp(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given a nonce that a key may use once in five minutes / When the client makes two requests /
    Then each carries its own nonce, its own timestamp and its own signature.

    This is why nothing in this SDK resends a built request: a replayed nonce is rejected, so a
    retry has to re-enter the signing layer (see the read-retry test).

    The signatures differ even for two identical requests in the same millisecond, because the
    nonce is inside the signed message. Once they did not, and that was the symptom of
    the hole: what the signature does not cover, an attacker may change."""
    mfx.responses.extend([httpx.Response(200, json={"items": [], "next_cursor": None})] * 2)
    await client.terminals.page()
    await client.terminals.page()

    first, second = mfx.signed(0), mfx.signed(1)
    assert first["X-MFX-Nonce"] != second["X-MFX-Nonce"], "a nonce is used once"
    assert int(second["X-MFX-Timestamp"]) >= int(first["X-MFX-Timestamp"])
    assert first["X-MFX-Signature"] != second["X-MFX-Signature"], (
        "the nonce is inside the signature"
    )
    assert len({first["X-MFX-Key"], second["X-MFX-Key"]}) == 1, "the same key signed both"


#: The shared anchor for the signed string. The platform asserts the same vector
#: against the server, so neither repo can drift alone. The seed is a published test value
#: (bytes 00..1f) and is never a key anything is issued with.
VECTOR_SEED = "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="
VECTOR_PUBLIC = "A6EHv/POEL4dcN0Y50vAmWfk1jCbpQ1fHdyGZBJVMbg="
VECTOR_TIMESTAMP = "1790000000000"
VECTOR_NONCE = "3f0c9a4e5b7d4c1e9a2b6d8f0a1c2e3f"
VECTOR_PATH = "/v1/terminals?dry_run=false"
VECTOR_BODY = b'{"farm_id":"00000000-0000-0000-0000-000000000001"}'
VECTOR_BODY_SHA = "a04da5e634e2ba32644e749dfec7f24186828312a8f3c0fa6bc48585d502ff79"
VECTOR_SIGNATURE = (
    "OLOeJhRskf6kvodIyvrrpI/Hwlg3MXn//TTc64zpcl0qACk3BOhNfMV8yrVthZUdUXlOCntJAIrfgHTNK6faDg=="
)


def test_the_signature_matches_the_agreed_test_vector_byte_for_byte() -> None:
    """Given the published test seed, timestamp, nonce, method, path and body / When they are
    signed / Then the signature is exactly the one the platform asserts on its own side.

    Ed25519 is deterministic, so this is an equality, not a shape. It is the one test that would
    catch the two repos disagreeing about the signed string — a disagreement whose only other
    symptom is the platform answering 401 to everything."""
    key = SigningKey(VECTOR_SEED)
    public = base64.b64encode(
        key._key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)  # noqa: SLF001
    ).decode("ascii")
    assert public == VECTOR_PUBLIC, "a different key would make every other assertion meaningless"

    message = signing_message(VECTOR_TIMESTAMP, VECTOR_NONCE, "POST", VECTOR_PATH, VECTOR_BODY)
    assert message == "\n".join(
        (VECTOR_TIMESTAMP, VECTOR_NONCE, "POST", VECTOR_PATH, VECTOR_BODY_SHA)
    ).encode("ascii")
    assert key.sign(message) == VECTOR_SIGNATURE


def test_the_signed_message_is_the_one_the_spec_writes_down() -> None:
    """timestamp\\nnonce\\nMETHOD\\npath\\nsha256_hex(body), and an empty body still has a hash."""
    nonce = "0123456789abcdef"
    message = signing_message("1789999999999", nonce, "post", "/v1/terminals", b'{"a":1}')
    assert message == f"1789999999999\n{nonce}\nPOST\n/v1/terminals\n".encode() + hashlib.sha256(
        b'{"a":1}'
    ).hexdigest().encode("ascii")
    empty = signing_message("1", nonce, "GET", "/v1/terminals", b"")
    assert empty.endswith(hashlib.sha256(b"").hexdigest().encode("ascii"))


def test_a_nonce_that_could_move_the_line_boundaries_is_refused_here_not_by_a_401() -> None:
    """Given a nonce outside ^[A-Za-z0-9_-]{16,64}$ / When a message is signed with it / Then the
    SDK refuses it.

    The nonce is a *line* of the signed message now. One containing a newline could move the line
    boundaries and sign one request as another, which is why the platform restricts the alphabet
    and answers 401 otherwise — a poor way to learn that a custom nonce generator has a bug."""
    for bad in ("short", "", "a" * 65, "has a space 1234", "line\nbreak123456", "semi;colon12345"):
        with pytest.raises(ValueError, match="nonce"):
            signing_message("1790000000000", bad, "GET", "/v1/terminals", b"")

    for good in ("0123456789abcdef", "a" * 64, secrets.token_urlsafe(16), uuid.uuid4().hex):
        signing_message("1790000000000", good, "GET", "/v1/terminals", b"")


def test_a_key_is_accepted_as_pem_or_as_its_raw_bytes_and_nothing_else(
    private_key: Ed25519PrivateKey, raw_key: str
) -> None:
    """MFX hands the key over once, and a tenant may keep it either way."""
    pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode(
        "ascii"
    )
    message = b"anything"
    from_pem = SigningKey(pem).sign(message)
    from_raw = SigningKey(raw_key).sign(message)
    from_object = SigningKey(private_key).sign(message)
    assert from_pem == from_raw == from_object, "the same key, however it was written down"
    assert SigningKey(SigningKey(private_key)).sign(message) == from_pem

    with pytest.raises(ValueError, match="PEM private key or the base64"):
        SigningKey("not a key at all!!")
    with pytest.raises(ValueError, match="32 bytes"):
        SigningKey(base64.b64encode(b"too short").decode("ascii"))


def test_an_rsa_key_is_refused_rather_than_used(private_key: Ed25519PrivateKey) -> None:
    """MFX signs with Ed25519 only: an Argon2id hash cannot verify an HMAC, and an RSA key
    here would fail at the platform with a message about signatures, not about key types."""
    from cryptography.hazmat.primitives.asymmetric import rsa

    rsa_pem = (
        rsa.generate_private_key(public_exponent=65537, key_size=2048)
        .private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
        .decode("ascii")
    )
    with pytest.raises(TypeError, match="Ed25519"):
        SigningKey(rsa_pem)


def test_a_signing_key_cannot_be_printed_or_pickled(private_key: Ed25519PrivateKey) -> None:
    """A secret never reaches a log: the key renders as *** wherever it could reach a log."""
    import pickle

    key = SigningKey(private_key)
    assert repr(key) == "SigningKey(***)"
    assert f"{key}" == "***" and str(key) == "SigningKey(***)"
    assert repr(MfxSignature(KEY_ID, key)) == f"MfxSignature(key_id={KEY_ID!r}, key=***)"
    with pytest.raises(TypeError, match="never serialised"):
        pickle.dumps(key)


async def test_the_client_names_itself_without_naming_the_key(client: MfxClient) -> None:
    assert repr(client) == f"MfxClient(base_url={BASE_URL!r}, key_id={KEY_ID!r})"
    assert client.key_id == KEY_ID
    assert TERMINAL_ID not in repr(client)
