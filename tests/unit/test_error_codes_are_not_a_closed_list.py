"""The contract names its error codes and does not close the list.

Until 8 Oct 2026 `ErrorBody.code` was a fixed set of 21 values and the platform sent 35. A client
generated from the contract raised inside its own parser on any of the other fourteen - a restart
refused for its cooldown, for one. This SDK was saved by a fallback that reads the raw answer when
the generated parser fails; a customer generating a client in another language had none.

The contract now says the code is text, lists every code the platform sends beside it
(`x-known-values`), and tells a client to read a code it does not know as an error. This file
holds the SDK to the same sentence.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from mfx._generated.models.error_body import ErrorBody
from mfx.client import MfxClient
from mfx.errors import _BY_CODE, _BY_STATUS, MfxApiError, RateLimitError, UpstreamError

from .conftest import TERMINAL_ID, FakeMfx, error

SPEC = Path(__file__).resolve().parents[2] / "spec" / "openapi.yaml"


def _known() -> dict[str, list[int]]:
    """Each code the contract names, with the statuses its own words give it."""
    spec: dict[str, Any] = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    code = spec["components"]["schemas"]["ErrorBody"]["properties"]["code"]
    assert code["type"] == "string" and "enum" not in code, "the list is not closed"
    values: dict[str, str] = code["x-known-values"]
    return {
        name: [int(n) for n in re.findall(r"\b[45]\d\d\b", words.split(".")[0])]
        for name, words in values.items()
    }


async def test_every_error_code_the_contract_names_and_one_it_does_not_is_a_typed_error(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given every error code the contract lists beside `ErrorBody.code`, each with the HTTP
    status the contract gives it, and one code no contract has named yet
    When the platform answers a call with each
    Then the generated parser reads the body as it is, with no fixed set to fall outside of; the
    caller gets an MFX error whose `code` is the text that was sent and whose class follows the
    code where this SDK knows it and the status where it does not; a refusal that says when to
    come back carries the seconds; and nothing raised is a ValueError from a generated module.
    """
    known = _known()
    assert len(known) >= 35 and all(known.values()), "each known code names its status"
    for refusal in ("cooldown", "concurrency", "tenant_rate", "farm_capacity"):
        assert known[refusal] == [429], refusal

    cases = [(code, status) for code, statuses in known.items() for status in statuses]
    cases.append(("a_rule_written_next_year", 409))
    for code, status in cases:
        body = ErrorBody.from_dict({"code": code, "message": "refused"})
        assert body.code == code

        headers = {"Retry-After": "42"} if status == 429 else {}
        mfx.responses.append(error(status, code, "refused", **headers))
        with pytest.raises(MfxApiError) as raised:
            await client.terminals.restart(TERMINAL_ID, reason="stuck", idempotency_key=code)

        said = raised.value
        assert (said.code, said.status) == (code, status)
        assert type(said) is (_BY_CODE.get(code) or _BY_STATUS.get(status, MfxApiError)), code
        if status == 429:
            assert isinstance(said, RateLimitError) and said.retry_after_s == 42.0, code
        assert not isinstance(said.__cause__, ValueError), f"{code} went through the fallback"

    # A store the platform needs did not answer: its own class, and still an
    # upstream failure, so a caller that waits and retries on one does so on the other.
    assert issubclass(_BY_CODE["dependency_unavailable"], UpstreamError)
    assert _BY_CODE["dependency_unavailable"] is not UpstreamError is _BY_STATUS[503]
