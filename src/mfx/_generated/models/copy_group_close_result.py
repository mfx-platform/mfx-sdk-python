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

T = TypeVar("T", bound="CopyGroupCloseResult")


@_attrs_define
class CopyGroupCloseResult:
    """
    Attributes:
        group_id (UUID):
        batch_id (UUID): GET /copy/closes?batch_id= lists them
        paused (bool): Whether the group is paused now
        followers (int): The live members a close was asked for
        closes (list[UUID]): Each member's close, in member id order
    """

    group_id: UUID
    batch_id: UUID
    paused: bool
    followers: int
    closes: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_id = str(self.group_id)

        batch_id = str(self.batch_id)

        paused = self.paused

        followers = self.followers

        closes = []
        for closes_item_data in self.closes:
            closes_item = str(closes_item_data)
            closes.append(closes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_id": group_id,
                "batch_id": batch_id,
                "paused": paused,
                "followers": followers,
                "closes": closes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_id = UUID(d.pop("group_id"))

        batch_id = UUID(d.pop("batch_id"))

        paused = d.pop("paused")

        followers = d.pop("followers")

        closes = []
        _closes = d.pop("closes")
        for closes_item_data in _closes:
            closes_item = UUID(closes_item_data)

            closes.append(closes_item)

        copy_group_close_result = cls(
            group_id=group_id,
            batch_id=batch_id,
            paused=paused,
            followers=followers,
            closes=closes,
        )

        copy_group_close_result.additional_properties = d
        return copy_group_close_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
