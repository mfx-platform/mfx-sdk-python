"""Cursor pagination, in one place.

Every list in this API is cursor-paginated and there is no total, no page number and no offset —
deliberately, because the API cannot answer those without a COUNT(\\*) over a partitioned table
(guardrail 7). So the SDK follows the cursor and never pretends to know how many there are.

:class:`Page` exists for ergonomics only: it gives the generated page model a length and makes it
iterable, so a caller writes ``for terminal in page`` instead of ``for terminal in page.items``.
It parses nothing.

**What used to be here.** Until 2026-09-26 this module re-parsed the raw response body by hand,
because the spec wrote every page schema as ``allOf: [PageMeta]`` with the page's own
``properties`` as a sibling and openapi-python-client drops the siblings — so every generated list
model had a cursor and *no items*. The schemas were restructured in the contract on
2026-09-21 and the fix has been in the contract since; this SDK had simply never re-vendored the
spec, so it went on working around a bug that no longer existed. The parser is gone and the items
come from the generated model, which is the only thing that can keep up with the schema.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

__all__ = ["Page", "page_of"]


@dataclass(frozen=True, slots=True)
class Page[T]:
    """One page, and the cursor for the next. ``next_cursor`` is None on the last.

    Iterate it, or read ``items``. To walk every page, pass ``next_cursor`` back as ``cursor``, or
    use the method that iterates for you where there is one (``all_brokers()``, ``farms.list()``).
    """

    items: list[T] = field(default_factory=list)
    next_cursor: str | None = None
    #: How many are in THIS page. Not a total, and never to be shown as one.
    returned: int | None = None

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)


def page_of[T](parsed: Any) -> Page[T]:  # noqa: ANN401 - one of the generated page models
    """Wrap a generated page model.

    ``next_cursor`` is normalised to None on the last page: the spec types it as nullable, and an
    empty string would otherwise read as a cursor and fetch the first page again for ever.
    ``returned`` is absent rather than null when the server omits it, which the generator models as
    ``UNSET`` — not an integer, so it comes through as None rather than as a count of nothing.
    """
    cursor = getattr(parsed, "next_cursor", None)
    returned = getattr(parsed, "returned", None)
    return Page(
        items=list(getattr(parsed, "items", None) or ()),
        next_cursor=cursor if isinstance(cursor, str) and cursor else None,
        returned=returned if isinstance(returned, int) else None,
    )
