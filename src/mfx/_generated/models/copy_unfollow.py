from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyUnfollow")


@_attrs_define
class CopyUnfollow:
    """
    Attributes:
        close_copied (bool): Close the volume copied from this leader. False leaves it open, as the account's own
    """

    close_copied: bool

    def to_dict(self) -> dict[str, Any]:
        close_copied = self.close_copied

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "close_copied": close_copied,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        close_copied = d.pop("close_copied")

        copy_unfollow = cls(
            close_copied=close_copied,
        )

        return copy_unfollow
