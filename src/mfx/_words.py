"""A request never carries an enum word the contract does not list.

A generated model read with ``from_dict`` reads a word it does not know as an ``UNKNOWN``
pseudo-member keeping the word, so an answer from a later version of the API never fails the call.
Some calls also build their request body with ``from_dict``, from what the caller gave; there the
same word is a mistake, and :func:`refuse_unknown_words` refuses it before anything is sent, as
calling the enum itself would.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

import attrs


def is_unknown(value: Enum) -> bool:
    """Whether ``value`` is a pseudo-member read from a word its enum does not list."""
    return type(value)._value2member_map_.get(value.value) is not value


def refuse_unknown_words[M](model: M) -> M:
    """Return ``model`` unchanged, or raise ValueError naming the first word its enums lack."""
    _walk(model)
    return model


def _walk(value: Any) -> None:  # noqa: ANN401 - any part of a generated model
    if isinstance(value, Enum):
        if is_unknown(value):
            raise ValueError(f"{value.value!r} is not a valid {type(value).__name__}")
    elif attrs.has(type(value)):
        for field in attrs.fields(type(value)):
            _walk(getattr(value, field.name))
    elif isinstance(value, dict):
        for item in value.values():
            _walk(item)
    elif isinstance(value, list | tuple):
        for item in value:
            _walk(item)
