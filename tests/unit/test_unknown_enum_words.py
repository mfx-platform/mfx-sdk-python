"""A response enum word this SDK was not generated with reads as UNKNOWN, never a failed call.

A later version of the API may add a word to a list it answers with: a close's cause, a leader's
state. Until now the generated parser built each enum field by calling the class, and a word
outside it raised ValueError from inside the parser, failing the whole call and every other row
of the page with it. Now a model read from a response builds its enum fields with
the class's ``_read``: a known word is its member, and any other word is an ``UNKNOWN``
pseudo-member whose value is the word as sent, so nothing is lost and ``to_dict`` writes it back.
A caller's own word is still refused: only what the platform answers is read this way.
"""

from __future__ import annotations

import enum
import inspect
from typing import Any

import pytest

import mfx._generated.models as generated
from mfx._generated.models.copy_close import CopyClose
from mfx._generated.models.copy_close_cause import CopyCloseCause
from mfx._generated.models.copy_leader_source import CopyLeaderSource
from mfx._generated.models.copy_leader_state import CopyLeaderState
from mfx.client import MfxClient

from .conftest import FakeMfx
from .test_copy_trading import CLOSE_STATS, LEADER_STATS, close_row, copy_page, leader

LATER = "a_word_from_a_later_version"


def _enums() -> list[type[enum.Enum]]:
    return [
        cls
        for _, cls in inspect.getmembers(generated, inspect.isclass)
        if issubclass(cls, enum.Enum)
    ]


def test_every_generated_enum_reads_a_word_it_does_not_know_as_unknown_keeping_the_word() -> None:
    """Given every enum the SDK was generated with, and a word or number none of them lists
    When each reads it as a response field, and reads each of its own members' values
    Then the unknown value is an UNKNOWN pseudo-member of that enum whose value and text are what
    was sent, equal to it, and not one of the enum's members; each known value is its own member;
    and something of the wrong kind altogether is still refused."""
    enums = _enums()
    assert len(enums) > 100
    for cls in enums:
        later: Any = 987654 if issubclass(cls, int) else LATER
        unknown = cls._read(later)  # type: ignore[attr-defined]
        assert isinstance(unknown, cls), cls
        assert (unknown.name, unknown.value, unknown) == ("UNKNOWN", later, later), cls
        assert str(unknown) == str(later), cls
        assert unknown not in list(cls), cls
        for member in cls:
            assert cls._read(member.value) is member, cls  # type: ignore[attr-defined]
        with pytest.raises(ValueError):
            cls._read(None)  # type: ignore[attr-defined]


def test_a_model_with_an_unknown_word_reads_and_writes_the_word_back() -> None:
    """Given a requested close whose cause is a word the SDK does not know and whose state it knows
    When it is read from the answer and written back with to_dict
    Then the cause is CopyCloseCause's UNKNOWN keeping the word, the state is its own member, and
    to_dict carries the word exactly as it was sent."""
    row = close_row()
    row["cause"] = LATER
    close = CopyClose.from_dict(row)
    assert isinstance(close.cause, CopyCloseCause)
    assert (close.cause.name, close.cause.value) == ("UNKNOWN", LATER)
    assert close.state.name == "PENDING"
    assert close.to_dict()["cause"] == LATER
    assert CopyClose.from_dict({**row, "cause": "group_close"}).cause is CopyCloseCause.GROUP_CLOSE


async def test_a_page_with_unknown_words_is_returned_and_a_callers_unknown_word_is_refused(
    client: MfxClient, mfx: FakeMfx
) -> None:
    """Given the platform answers a page of closes and a page of leaders, one row of each carrying
    words a later version of the API added
    When the caller lists them, and then passes such a word as its own filter
    Then each page is returned whole with the unknown words read as UNKNOWN and the other rows as
    they were; but the caller's own word is refused before anything is sent."""
    later_close = {**close_row(), "id": "06abfa00-0000-7000-8000-0000000000a3", "cause": LATER}
    mfx.responses.append(copy_page([close_row(), later_close], None, CLOSE_STATS))
    closes = await client.copy.closes()
    assert [c.cause.name for c in closes.items] == ["GROUP_CLOSE", "UNKNOWN"]
    assert closes.items[1].cause.value == LATER

    later_leader = leader(state=LATER, id="06abfa00-0000-7000-8000-0000000000c2", source=LATER)
    mfx.responses.append(copy_page([leader(), later_leader], None, LEADER_STATS))
    leaders = await client.copy.leaders()
    assert [(x.source.name, x.state.name) for x in leaders.items] == [
        ("ACCOUNT", "ACTIVE"),
        ("UNKNOWN", "UNKNOWN"),
    ]
    assert (leaders.items[1].source.value, leaders.items[1].state.value) == (LATER, LATER)
    assert len(mfx.requests) == 2

    with pytest.raises(ValueError, match=LATER):
        CopyLeaderSource(LATER)
    with pytest.raises(ValueError):
        await client.copy.leaders(state=LATER)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        await client.copy.leaders(source=LATER)  # type: ignore[arg-type]
    assert CopyLeaderState("active") is CopyLeaderState.ACTIVE
    assert len(mfx.requests) == 2
