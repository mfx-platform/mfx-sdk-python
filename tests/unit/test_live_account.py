"""Merging a snapshot and the marks that follow it.

What goes wrong here is a tenant's view of its own money being *plausible* and wrong: a position
whose profit is a minute stale while everything around it is live, a mark applied to a position set
it was never measured against, or a view that quietly stops updating and looks like a still market.

Every refusal in `LiveAccount` is a case here, because a refusal is the only thing standing between
a lost message and an invented account.
"""

from __future__ import annotations

from typing import Any

from mfx import AccountView, ChannelRefused, LiveAccount, Resync, StreamMessage

TERMINAL = "0191f0c2-aaaa-7bbb-8ccc-000000000001"
OTHER = "0191f0c2-bbbb-7ccc-8ddd-000000000002"
CHANNEL = f"account:{TERMINAL}"


def _snapshot(
    seq: int, *, positions: list[dict[str, Any]], base: int | None = None, **figures: Any
) -> StreamMessage:
    """`AccountSnapshotMessage` as the gateway serves it: decimals as strings, rows under
    `positions`. `base` defaults to the snapshot's own seq, which is what a cell-sent one carries;
    a hot-copy one names the snapshot it grew from, so the tests set it."""
    return StreamMessage(
        channel=CHANNEL,
        seq=seq,
        type="account.snapshot",
        data={
            "terminal_id": TERMINAL,
            "schema_version": "1",
            "as_of": f"2026-10-01T12:00:{seq:02d}.000Z",
            "balance": "10000.00",
            "equity": "10050.00",
            "margin": "110.00",
            "margin_free": "9940.00",
            "margin_level": "9136.30",
            "open_positions_count": len(positions),
            "positions": positions,
            "pending": [],
            "pending_as_of": None,
            **figures,
        },
        base=seq if base is None else base,
    )


def _marks(seq: int, base: int, marks: list[Any], **figures: Any) -> StreamMessage:
    """`AccountMarksMessage`: each mark is the four-element array `[ticket, price_current, profit,
    swap]`, the ticket an integer and the rest decimal strings (prefixItems)."""
    return StreamMessage(
        channel=CHANNEL,
        seq=seq,
        type="account.marks",
        data={
            "terminal_id": TERMINAL,
            "schema_version": "1",
            "as_of": f"2026-10-01T12:00:{seq:02d}.000Z",
            "balance": "10000.00",
            "equity": "10050.00",
            "margin": "110.00",
            "margin_free": "9940.00",
            "margin_level": "9136.30",
            "open_positions_count": 1,
            "marks": marks,
            **figures,
        },
        base=base,
    )


def _position(ticket: int, **fields: Any) -> dict[str, Any]:
    """A `Position` as the API defines it: decimals as strings, `open_price` not `price_open`."""
    return {
        "ticket": ticket,
        "symbol": "EURUSD.sd",
        "side": "buy",
        "volume": "0.10",
        "open_price": "1.10415",
        "sl": None,
        "tp": None,
        "price_current": "1.10415",
        "profit": "0.00",
        "swap": "0.00",
        "open_time": "2026-10-01T11:00:00.000Z",
        "magic": 778201,
        "comment": "fx-scalp-v3",
        **fields,
    }


def test_marks_are_merged_into_the_snapshot_and_a_new_snapshot_replaces_it() -> None:
    """Given a live account drawn from a snapshot of two positions
    When marks arrive for one of them, then for the other, then a new snapshot
    Then each mark sets only its own position's figures and leaves the rest of that position alone,
    the account figures follow every message, and a snapshot replaces the whole view.

    The "leaves the rest alone" half is the one worth a test: a
    mark carries four fields and a position has ten, so a merge that replaced the row rather than
    updating it would lose the symbol, volume and opening price and look like a position that had
    just been opened at the current price.
    """
    live = LiveAccount(TERMINAL)
    assert live.view is None, "an account nobody has been told about is not an empty account"
    assert live.apply(_snapshot(10, positions=[_position(1), _position(2)])) is live.view

    view = live.view
    assert view is not None
    assert (view.seq, view.base) == (10, 10)
    assert set(view.positions) == {1, 2}
    assert view.figures["balance"] == "10000.00" and view.figures["margin_free"] == "9940.00"
    assert not {"positions", "pending", "pending_as_of", "open_positions_count", "marks"} & set(
        view.figures
    ), "the set and its count are not figures; only a snapshot changes them"

    applied = live.apply(_marks(11, 10, [[1, "1.10500", "8.50", "-0.20"]]))
    assert applied is not None and not live.behind
    assert applied.positions[1]["profit"] == "8.50"
    assert applied.positions[1]["price_current"] == "1.10500"
    assert applied.positions[1]["swap"] == "-0.20"
    assert applied.positions[1]["symbol"] == "EURUSD.sd", "a mark updates, it does not replace"
    assert applied.positions[1]["volume"] == "0.10"
    assert applied.positions[1]["open_price"] == "1.10415"
    assert applied.positions[2]["profit"] == "0.00", "and touches nothing it did not name"
    assert (applied.seq, applied.base) == (11, 10), "base stays the snapshot's"

    # The figures ride every message, including one whose marks are empty.
    moved = live.apply(_marks(12, 10, [], balance="10500.00", equity="10558.50"))
    assert moved is not None and moved.figures["balance"] == "10500.00"
    assert moved.positions[1]["profit"] == "8.50", "a keep-alive is not a reset"

    redrawn = live.apply(_snapshot(13, positions=[_position(3, profit="1.25")]))
    assert redrawn is not None
    assert set(redrawn.positions) == {3}, "every snapshot replaces the whole view"
    assert (redrawn.seq, redrawn.base) == (13, 13), "a snapshot's base is its own seq"
    assert redrawn.figures["balance"] == "10000.00", "including the figures it corrects"


def test_a_mark_that_cannot_be_applied_is_dropped_whole_and_says_so() -> None:
    """Given a live account
    When a marks message arrives before any snapshot, against a different snapshot, with a seq gap,
    or naming a ticket the view does not hold, and when the platform sends a resync
    Then none of them is applied even in part, the view keeps its last good state except after a
    resync which clears it, and `behind` is true until a snapshot arrives.

    Each of these is a lost or out-of-order message, and the
    failure they all guard against is the same: a delta merged into a position set it was never
    measured against is an account that never existed, and it is wrong in the one direction nobody
    checks - it looks fine.
    """
    live = LiveAccount(TERMINAL)

    # Nothing held: there is no snapshot to apply it to.
    assert live.apply(_marks(5, 4, [[1, "1.1", "3.00", "0.00"]])) is None
    assert live.behind and live.view is None

    live.apply(_snapshot(10, positions=[_position(1), _position(2)]))
    assert not live.behind, "a snapshot clears it"

    # A different snapshot's marks: the position set they were measured against is not ours.
    assert live.apply(_marks(11, 7, [[1, "1.1", "3.00", "0.00"]])) is None
    assert live.behind
    held = live.view
    assert held is not None and held.positions[1]["profit"] == "0.00", "nothing was half-applied"

    # A gap: 11 never arrived, so position 2's figures are older than 12 assumes.
    live.apply(_snapshot(10, positions=[_position(1), _position(2)]))
    assert live.apply(_marks(12, 10, [[1, "1.1", "3.00", "0.00"]])) is None
    assert live.behind

    # A ticket we do not hold: rule 2 names this one - "your view is behind".
    live.apply(_snapshot(20, positions=[_position(1)]))
    assert (
        live.apply(
            _marks(
                21,
                20,
                [[1, "1.1", "4.00", "0.00"], [99, "1.1", "1.00", "0.00"]],
            )
        )
        is None
    )
    assert live.behind
    after = live.view
    assert after is not None
    assert after.positions[1]["profit"] == "0.00", (
        "the whole message is dropped, not the unknown mark: the figures were measured "
        "against a set we do not have"
    )
    assert 99 not in after.positions, "and an unknown ticket is never invented"

    # A resync says the replay window has passed, so what we hold may be arbitrarily old.
    live.apply(_snapshot(30, positions=[_position(1)]))
    assert live.apply(Resync(CHANNEL)) is None
    assert live.behind and live.view is None

    # And it recovers from exactly one thing.
    assert live.apply(_snapshot(40, positions=[_position(1)])) is not None
    assert not live.behind


def test_one_stream_follows_many_terminals_without_crossing_them() -> None:
    """Given two LiveAccounts on one stream, and a platform that stamps no base
    When each is handed every event, including the other terminal's and an unrelated channel's
    Then each applies only its own terminal's messages, and a message with no base is applied
    rather than refused.

    Crossing two tenants' positions is the worst failure available here, so the terminal
    is checked from the message as well as from the channel key and the stricter answer wins. The
    missing `base` is the compatibility case: `base` is still being added to the contract,
    and an SDK that refused every message without one would read as a quiet account
    rather than as a platform too old to follow.
    """
    mine, theirs = LiveAccount(TERMINAL), LiveAccount(OTHER)
    events: list[Any] = [
        _snapshot(10, positions=[_position(1)]),
        StreamMessage(
            channel=f"account:{OTHER}",
            seq=11,
            type="account.snapshot",
            data={"terminal_id": OTHER, "balance": "50.00", "positions": [_position(7)]},
            base=11,
        ),
        # No base at all, and the kind only in the payload: an older gateway. Seq 11 and not 12:
        # `seq` is per channel, so the other terminal's message above consumed none of ours.
        StreamMessage(
            channel=CHANNEL,
            seq=11,
            type=None,
            data={
                "kind": "account.marks",
                "terminal_id": TERMINAL,
                "balance": "11000.00",
                "marks": [[1, "1.10500", "2.50", "0.00"]],
            },
        ),
        StreamMessage(channel="events", seq=13, type="position.opened", data={"ticket": 1}),
        Resync(f"account:{OTHER}"),
    ]
    for event in events:
        mine.apply(event)
        theirs.apply(event)

    assert mine.view is not None
    assert mine.view.positions[1]["profit"] == "2.50", "no base is not a mismatch"
    assert mine.view.figures["balance"] == "11000.00"
    assert not mine.behind, "another terminal's resync is not ours"
    assert 7 not in mine.view.positions, "and its positions are never ours"
    assert theirs.view is None and theirs.behind, "while the resync for theirs did land"


def test_a_snapshot_without_a_position_list_or_a_seq_is_still_usable() -> None:
    """Given a platform that numbers nothing and a snapshot whose `open` and `pending` are absent
    When marks follow it
    Then the view holds the figures with no positions, a mark naming any ticket is refused rather
    than inventing one, and an unnumbered stream is not treated as one long gap.

    `pending` absent means "we did not look", not "there are none",
    and a stream with no seq cannot prove a loss - calling that a gap would make every message
    unapplicable, which is a worse failure than the one being guarded against because it looks
    like a still market.
    """
    live = LiveAccount(TERMINAL)
    bare = StreamMessage(
        channel=CHANNEL,
        seq=None,
        type="account.snapshot",
        data={"terminal_id": TERMINAL, "balance": "10000.00", "positions": "not a list"},
    )
    view = live.apply(bare)
    assert isinstance(view, AccountView)
    assert view.positions == {} and view.pending == ()
    assert (view.seq, view.base) == (None, None)
    assert view.figures["balance"] == "10000.00"

    assert live.apply(_marks(99, 10, [[1, "1.1", "1.00", "0.00"]])) is None, "no such ticket"
    live.apply(bare)
    unnumbered = StreamMessage(
        channel=CHANNEL, seq=None, type="account.marks", data={"marks": [], "equity": "42.00"}
    )
    applied = live.apply(unnumbered)
    assert applied is not None and applied.figures["equity"] == "42.00"
    assert applied.as_of is None, "nothing said when, and nothing was invented"

    # A kind this SDK has never heard of, on our own channel: ignored, not fatal and not `behind`.
    # The channel is the platform's to extend, and a client that fell over on a new kind would
    # have to be reissued every time one was added.
    future = StreamMessage(
        channel=CHANNEL, seq=None, type="account.something_later", data={"terminal_id": TERMINAL}
    )
    assert live.apply(future) is None and not live.behind

    # A mark that is not the four-element array the contract defines. Refused, and emphatically
    # not read as an empty list: an empty `marks` is a keep-alive on this channel, so treating a
    # mark we cannot parse as "nothing moved" would stop the view updating and report nothing.
    live.apply(_snapshot(50, positions=[_position(1)]))
    assert live.apply(_marks(51, 50, [[1, "1.1", "9.00"]])) is None
    assert live.behind


def test_the_wire_shapes_the_contract_defines_are_the_ones_read() -> None:
    """Given messages in exactly the shapes AccountSnapshotMessage and AccountMarksMessage define
    When a mark is the four-element array, a snapshot carries rows under `positions`, and a resume
    serves a snapshot whose `base` names the snapshot it grew from rather than its own seq
    Then each is read correctly, and a mark of any other shape is refused rather than treated as an
    empty one.

    This is the regression test for a bug that passed its own suite. An earlier version of this
    module read a mark as an object with four keys - which is what the *cell* sends to the platform
    and not what the platform sends on - and read positions from `open`.
    Both were wrong against the published contract and neither test caught it, because the fixtures
    were written from the same misunderstanding as the code.

    The failure it would have caused in production is the quiet kind: an unreadable mark left the
    list empty, an empty `marks` is a keep-alive on this channel, so the view would have stopped
    updating while reporting itself perfectly healthy.
    """
    live = LiveAccount(TERMINAL)

    # The array form, ticket first, the rest decimal strings (prefixItems).
    live.apply(_snapshot(10, positions=[_position(1), _position(2)]))
    applied = live.apply(_marks(11, 10, [[2, "2402.90", "-14.25", "-0.75"]]))
    assert applied is not None and not live.behind
    assert applied.positions[2]["price_current"] == "2402.90"
    assert applied.positions[2]["profit"] == "-14.25"
    assert applied.positions[2]["swap"] == "-0.75"
    assert applied.positions[1]["profit"] == "0.00", "and only the ticket it named"

    # A resume is answered from the hot copy: its `base` names the snapshot it grew from, so it is
    # not the seq. Marks that follow carry that same base, and must still apply.
    resumed = live.apply(_snapshot(40, positions=[_position(1)], base=10))
    assert resumed is not None and (resumed.seq, resumed.base) == (40, 10)
    after = live.apply(_marks(41, 10, [[1, "1.10700", "25.00", "0.00"]]))
    assert after is not None, "a resumed snapshot's base is the one its marks name"
    assert after.positions[1]["profit"] == "25.00"

    # Anything that is not that array is refused, and is never read as "nothing moved": too short,
    # the cell's object form, too long, a ticket that is not a number, and `marks` not a list.
    broken_marks: list[Any] = [
        [[1, "1.1", "9.00"]],
        [{"ticket": 1, "profit": "9.00"}],
        [[1, "1.1", "9", "0", "x"]],
        [["EURUSD", "1.1", "9.00", "0.00"]],
        "not a list at all",
    ]
    for broken in broken_marks:
        live.apply(_snapshot(50, positions=[_position(1)]))
        assert live.apply(_marks(51, 50, broken)) is None, f"refused: {broken}"
        assert live.behind, "and the caller is told, rather than shown a view that stopped moving"


def test_a_refused_account_channel_drops_the_view_rather_than_leaving_it_to_be_drawn() -> None:
    """Given a view built from a snapshot
    When the platform refuses the channel it is fed by, and then refuses someone else's
    Then this terminal's refusal drops the view and marks it behind, and another channel's is
    ignored.

    A refusal on the account channel means the terminal is gone, or was never ours:
    nothing will correct this view again. Keeping it would leave a caller drawing an account as if
    it were current - balances and open positions, frozen at the moment the feed died, with
    nothing to say so. None plus `behind` is the honest answer, and it is the same answer as a
    resync whose replay window has passed.
    """
    account = LiveAccount(TERMINAL)
    opened = {
        "ticket": 1,
        "symbol": "EURUSD.sd",
        "side": "buy",
        "volume": "0.10",
        "open_price": "1.09",
        "price_current": "1.10",
        "profit": "10.00",
        "swap": "0.00",
    }
    assert account.apply(_snapshot(1, positions=[opened])) is not None
    assert account.view is not None and not account.behind

    # Another terminal's channel: not ours, so it says nothing about this view.
    assert (
        account.apply(ChannelRefused(f"account:{OTHER}", "not_found", "no such terminal")) is None
    )
    assert account.view is not None, "someone else's refusal is not ours"
    assert not account.behind

    assert account.apply(ChannelRefused(CHANNEL, "not_found", "no such terminal")) is None
    assert account.view is None, "the feed is gone; what we held is not the account any more"
    assert account.behind
