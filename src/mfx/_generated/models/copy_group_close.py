from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyGroupClose")


@_attrs_define
class CopyGroupClose:
    """
    Attributes:
        reason (str): Why, kept on each close and the audit row
        pause (bool): true pauses the group in the same act; false leaves its state. Required, no default
    """

    reason: str
    pause: bool

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        pause = self.pause

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "reason": reason,
                "pause": pause,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        pause = d.pop("pause")

        copy_group_close = cls(
            reason=reason,
            pause=pause,
        )

        return copy_group_close
