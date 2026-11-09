from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyLeaderRetire")


@_attrs_define
class CopyLeaderRetire:
    """
    Attributes:
        close_copied (bool): Close every follower's copied volume of this leader. False leaves those positions open, as
            the accounts' own
        reason (str):
    """

    close_copied: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        close_copied = self.close_copied

        reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "close_copied": close_copied,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        close_copied = d.pop("close_copied")

        reason = d.pop("reason")

        copy_leader_retire = cls(
            close_copied=close_copied,
            reason=reason,
        )

        return copy_leader_retire
