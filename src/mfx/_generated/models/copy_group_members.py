from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyGroupMembers")


@_attrs_define
class CopyGroupMembers:
    """
    Attributes:
        follower_ids (list[UUID]):
    """

    follower_ids: list[UUID]

    def to_dict(self) -> dict[str, Any]:
        follower_ids = []
        for follower_ids_item_data in self.follower_ids:
            follower_ids_item = str(follower_ids_item_data)
            follower_ids.append(follower_ids_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "follower_ids": follower_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        follower_ids = []
        _follower_ids = d.pop("follower_ids")
        for follower_ids_item_data in _follower_ids:
            follower_ids_item = UUID(follower_ids_item_data)

            follower_ids.append(follower_ids_item)

        copy_group_members = cls(
            follower_ids=follower_ids,
        )

        return copy_group_members
