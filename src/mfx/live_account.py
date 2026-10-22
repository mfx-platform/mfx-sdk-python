"""Following one terminal's account live, snapshot then marks.

``account:{terminal_id}`` does not send you the whole account every time a price moves. It sends a
full ``account.snapshot`` when the position set changes and once a minute, and an ``account.marks``
in between carrying only the positions whose floating values moved. For a tenant with 197 positions
open that is the difference between ~42 KB per message and ~8 KB, and at a 250 ms refresh rate it is
the difference between following an account and flooding yourself.

The arithmetic for putting the two back together is four rules, and
getting any of them subtly wrong gives you an account that looks plausible and is wrong - a position
showing a profit from a minute ago, or a view that quietly stops updating. :class:`LiveAccount`
applies them for you::

    live = LiveAccount(terminal_id)
    async with client.stream() as stream:
        await stream.subscribe(Channel.account(terminal_id))
        async for event in stream:
            if live.apply(event) is not None:
                show(live.view)
            elif live.behind:
                await stream.resume(Channel.account(terminal_id))

**It never guesses.** A message it cannot apply is dropped whole and :attr:`LiveAccount.behind` goes
true; it does not half-apply, and it does not patch a position it has never seen. ``behind`` is
cleared only by a snapshot, which arrives within 60 s on its own, or at once if you ``resume``.

**It takes the whole stream.** Events for another channel or another terminal are ignored, so one
connection can follow many terminals with a :class:`LiveAccount` each and the same ``for`` loop.

**The figures are copied by whatever name they arrive under**, because the platform renames them on
the way through: the cell sends ``free_margin`` where the tenant-facing message says
``margin_free``.
Nothing here enumerates them, so a figure the platform adds later is carried rather than dropped.

**A mark, though, is positional and must be read by position.** ``AccountMarksMessage`` makes each
one a four-element array - ``[ticket, price_current, profit, swap]``, the ticket an integer and the
rest decimal strings - so the three names it sets are written out here. An earlier draft of this
module treated a mark as an object with four keys, which is what the *cell* sends to the platform
and not what the platform sends on. That version type-checked, passed
its tests against its own fixtures, and would have **silently dropped every mark**: an unreadable
mark would have left the list empty, which on this channel is a keep-alive and not an error, so the
view would simply have stopped updating without ever reporting itself behind.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final
from uuid import UUID

from mfx.streaming import ChannelRefused, Resync, StreamEvent, StreamMessage

__all__ = [
    "MARKS",
    "SNAPSHOT",
    "AccountView",
    "LiveAccount",
]

SNAPSHOT: Final = "account.snapshot"
MARKS: Final = "account.marks"

#: Carried by a message but not part of the account: either protocol (``kind``, ``type``, ``seq``,
#: ``base``), already a field of the view (``as_of``, ``terminal_id``), or the delta itself
#: (``marks``). Everything else a message carries is treated as a figure, including one the platform
#: adds after this SDK ships.
_NOT_A_FIGURE: Final = frozenset(
    {"kind", "type", "seq", "base", "as_of", "terminal_id", "schema_version", "marks"}
)
#: A snapshot's fields that belong to the position *set* rather than to the figures: the two lists,
#: when the orders were last read, and the count. Only another snapshot replaces them, never a mark.
_SET: Final = ("positions", "pending", "pending_as_of", "open_positions_count")

#: What a mark carries, in the order ``AccountMarksMessage.marks[]`` carries it. The ticket names
#: the position; the other three are the fields set on it.
_MARKED: Final = ("price_current", "profit", "swap")


@dataclass(frozen=True, slots=True)
class AccountView:
    """One terminal's account as the stream last said it was: a snapshot, with the marks applied.

    ``positions`` is keyed by ticket because that is how a mark names the position it moves, and
    because a caller drawing a table wants to find a row rather than scan for it. The order is the
    snapshot's own - dicts keep insertion order - so rendering it twice reads the same way.
    """

    terminal_id: str
    #: The ``as_of`` of the last message applied, not of the snapshot: the figures are that fresh.
    as_of: str | None
    #: The ``seq`` of the last message applied. A jump between this and the next message's is what
    #: the stream's ordering rules call a gap.
    seq: int | None
    #: The ``seq`` of the snapshot this view is drawn from, which every marks message names.
    base: int | None
    figures: dict[str, Any] = field(default_factory=dict)
    positions: dict[int, dict[str, Any]] = field(default_factory=dict)
    pending: tuple[dict[str, Any], ...] = ()


class LiveAccount:
    """The stream's ordering rules, applied to the events you hand it.

    Not a subscriber: it holds no socket and asks for nothing. The caller drives the stream, which
    is what lets one connection follow several terminals and lets a caller who already has an event
    loop keep it.
    """

    def __init__(self, terminal_id: str | UUID) -> None:
        self._terminal_id = str(terminal_id)
        self._view: AccountView | None = None
        self._behind = False

    @property
    def view(self) -> AccountView | None:
        """The account, or ``None`` until the first snapshot arrives.

        ``None`` rather than an empty view: an account with no positions and a zero balance is a
        statement about a tenant's money, and "we have not been told yet" is not that statement.
        """
        return self._view

    @property
    def behind(self) -> bool:
        """True when a message could not be applied, so this view is not the account.

        The remedy is ``resume``, which answers with a snapshot. Waiting is also
        correct - a snapshot comes within 60 s by itself - but until one does, do not show these
        figures as live.
        """
        return self._behind

    def apply(self, event: StreamEvent) -> AccountView | None:
        """Take one stream event. Returns the new view, or ``None`` if nothing was applied.

        ``None`` deliberately covers several things, because a caller does the same for all of
        them - draw nothing new, then check :attr:`behind`: an event for another channel, terminal
        or kind; a marks message that does not apply; a resync; and a sequence gap.
        """
        if isinstance(event, ChannelRefused):
            if not self._mine(event.channel, None):
                return None
            # The channel this view is fed by is gone - the terminal was retired, or was never
            # ours. What we hold is the account as it was, and nothing will correct it again, so
            # the view is dropped rather than left to be drawn as if it were current.
            self._view, self._behind = None, True
            return None
        if isinstance(event, Resync):
            if not self._mine(event.channel, None):
                return None
            # The replay window has passed. What we hold may be arbitrarily old and the platform
            # has said it cannot help; only a snapshot can.
            self._view, self._behind = None, True
            return None
        if not self._mine(event.channel, event.data.get("terminal_id")):
            return None
        kind = event.type or str(event.data.get("kind") or "")
        if kind == SNAPSHOT:
            return self._draw(event)
        if kind != MARKS:
            return None
        return self._mark(event)

    def _mine(self, channel: str, terminal_id: Any) -> bool:
        """Is this event about this terminal?

        Two independent answers, because either may be missing and they cannot disagree: the
        channel key ends in the terminal id, and the message says whose account it is. A message
        that names a *different* terminal is not ours whatever the channel said - that way round a
        mark can never be applied to the wrong tenant's positions, which is the one mistake here
        that would be worse than showing nothing.
        """
        if terminal_id is not None and str(terminal_id) != self._terminal_id:
            return False
        return not channel or channel.endswith(self._terminal_id)

    # -- rule 1 --------------------------------------------------------------------------------

    def _draw(self, message: StreamMessage) -> AccountView:
        """Replace the whole view with every snapshot.

        Every snapshot - not only the first, and not only one with a newer seq. A snapshot is the
        platform's current answer, and preferring what we hold to what we have just been told is
        exactly how a view gets stuck; the channel's ``seq`` also restarts from 1 when a terminal
        has been quiet for 180 s, so a newer snapshot can legitimately carry a smaller one.

        ``base`` is taken from the message and **not** inferred from ``seq``. A snapshot the cell
        sent has them equal, but one served from the platform's hot copy on ``subscribe`` or
        ``resume`` already includes every mark up to its ``seq``, so its ``base`` names the snapshot
        it grew from. Synthesising it from ``seq`` would make every following mark unapplicable
        after a resume - which is the one moment a caller resumes *because* it is already behind.
        """
        data = message.data
        self._behind = False
        base = _base_of(message)
        self._view = AccountView(
            terminal_id=self._terminal_id,
            as_of=_text(data.get("as_of")),
            seq=message.seq,
            base=message.seq if base is None else base,
            figures=_figures(data),
            positions={
                _int(row["ticket"]): dict(row)
                for row in _rows(data.get("positions"))
                if "ticket" in row
            },
            pending=tuple(dict(row) for row in _rows(data.get("pending"))),
        )
        return self._view

    # -- rules 2 and 3 -------------------------------------------------------------------------

    def _mark(self, message: StreamMessage) -> AccountView | None:
        """Apply a marks message, or drop it whole and fall behind (the stream's ordering rules).

        Four reasons to refuse, and every one of them means the same thing - this view is not the
        account any more, so patching it would be inventing:

        * nothing held, so there is no snapshot to apply it to;
        * its ``base`` is not the snapshot we hold, so it describes an account whose position set we
          never saw;
        * a gap: its ``seq`` is not the next one, so a message in between went missing and some
          position's figures are older than this one assumes;
        * it names a ticket we do not have, which rule 2 calls out by name as "your view is behind";
        * or a mark is not the four-element array the contract defines, which means this SDK and the
          platform disagree about the wire. Refusing is the only safe answer: a mark that cannot be
          read is **not** an empty mark, and on this channel an empty list is a keep-alive, so
          treating the two alike would stop the view updating while reporting nothing wrong.

        The last drops the **whole** message rather than the unknown mark. A message is one account
        at one instant: applying the half we recognise would produce an account that never existed,
        and the figures - which ride the same message - would then disagree with the positions they
        were measured against.
        """
        view = self._view
        if view is None:
            self._behind = True
            return None
        base = _base_of(message)
        marks = _marks(message.data.get("marks"))
        if (
            (base is not None and base != view.base)
            or _gapped(view.seq, message.seq)
            or marks is None
            or any(ticket not in view.positions for ticket, _ in marks)
        ):
            self._behind = True
            return None

        positions = {ticket: dict(row) for ticket, row in view.positions.items()}
        for ticket, values in marks:
            positions[ticket].update(dict(zip(_MARKED, values, strict=True)))
        self._view = AccountView(
            terminal_id=view.terminal_id,
            as_of=_text(message.data.get("as_of")) or view.as_of,
            seq=view.seq if message.seq is None else message.seq,
            base=view.base,
            # The figures the message carried replace the ones held, and a keep-alive carries them
            # too - so an account whose positions are still but whose balance moved stays current.
            figures={**view.figures, **_figures(message.data)},
            positions=positions,
            pending=view.pending,
        )
        return self._view


def _marks(value: Any) -> list[tuple[int, list[Any]]] | None:
    """``marks`` as ``(ticket, [price_current, profit, swap])`` pairs, or ``None`` if unreadable.

    ``AccountMarksMessage`` gives each mark as a four-element array, ticket first
    (``prefixItems``). ``None`` and ``[]`` are deliberately different answers: an empty list is a
    keep-alive and applies cleanly, while a mark of the wrong shape means this SDK is reading a wire
    it does not understand, and the caller must be told it is behind rather than shown a view that
    has quietly stopped moving.
    """
    if not isinstance(value, list):
        return None
    out: list[tuple[int, list[Any]]] = []
    for mark in value:
        if not isinstance(mark, list | tuple) or len(mark) != 1 + len(_MARKED):
            return None
        ticket = _int(mark[0])
        if ticket < 0:
            return None
        out.append((ticket, list(mark[1:])))
    return out


def _base_of(message: StreamMessage) -> int | None:
    """The ``seq`` of the snapshot this message applies to, from wherever the platform put it.

    The stream makes ``base`` a property of the channel, like ``seq``, so the envelope is where it
    belongs and where :class:`StreamMessage` carries it. The payload is read as well because the
    channel's schema is still open and the ingest may yet forward it inside ``data``;
    reading both costs a dict lookup and means this SDK does not have to be reissued to find out.

    ``None`` means the platform did not say. That is not treated as a mismatch - see
    :meth:`LiveAccount._mark` - because an older gateway that stamps no ``base`` would otherwise
    make every marks message unapplicable, which looks to a caller like a quiet account rather than
    like a platform too old to follow.
    """
    for value in (message.base, message.data.get("base")):
        if value is not None:
            return _int(value)
    return None


def _figures(data: Any) -> dict[str, Any]:
    return {
        name: value
        for name, value in dict(data).items()
        if name not in _NOT_A_FIGURE and name not in _SET
    }


def _rows(value: Any) -> list[dict[str, Any]]:
    """The dict rows of a list-valued field, and nothing from a field that is not a list of them.

    Used for a snapshot's ``positions`` and ``pending``, which are objects
    (``Position``/``PendingOrder``). Marks are not objects and go through :func:`_marks`.
    """
    if not isinstance(value, list):
        return []
    return [row for row in value if isinstance(row, dict)]


def _gapped(held: int | None, arriving: int | None) -> bool:
    """Is ``arriving`` past the next seq after ``held``? (the stream's gap rule.)

    Unknown on either side is not a gap. A stream that numbers nothing cannot prove a loss, and
    calling it one would make every message on it unapplicable - a worse failure than the one being
    guarded against, because it reads as a quiet account rather than as an error.
    """
    if held is None or arriving is None:
        return False
    return arriving > held + 1


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1


def _text(value: Any) -> str | None:
    return None if value is None else str(value)
