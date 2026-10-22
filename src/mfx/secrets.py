"""``Secret`` — a value that cannot reach a log by being printed.

A broker password travels through a tenant's own code, this SDK, and an HTTP request. Along that
path it passes through repr, f-strings, ``print``, ``logging`` and any traceback that captures a
frame. This type renders as ``***`` in all of them, so revealing the value takes the one explicit
call that is easy to see in review: ``.reveal()``.
"""

from __future__ import annotations

from typing import Any

__all__ = ["Secret"]


class Secret:
    """A string that renders as ``***`` everywhere except :meth:`reveal`."""

    __slots__ = ("_value",)

    def __init__(self, value: str | Secret) -> None:
        self._value = value.reveal() if isinstance(value, Secret) else value

    def reveal(self) -> str:
        """The value itself. Every call site is a place a secret can escape — keep them few."""
        return self._value

    def __repr__(self) -> str:
        return "Secret(***)"

    __str__ = __repr__

    def __format__(self, spec: str) -> str:
        return "***"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Secret) and self._value == other._value

    def __hash__(self) -> int:
        return hash(("mfx.Secret", self._value))

    def __bool__(self) -> bool:
        return bool(self._value)

    def __reduce__(self) -> tuple[Any, ...]:
        """Unpicklable on purpose: a pickled secret is a secret written to a file by accident."""
        raise TypeError("a Secret is never serialised; read it from your own secret store")
