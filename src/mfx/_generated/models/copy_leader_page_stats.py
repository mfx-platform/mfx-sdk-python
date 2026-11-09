from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyLeaderPageStats")


@_attrs_define
class CopyLeaderPageStats:
    """Over every leader the filters match, not this page

    Attributes:
        leaders (int):
        active (int):
        paused (int):
        retired (int):
    """

    leaders: int
    active: int
    paused: int
    retired: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        leaders = self.leaders

        active = self.active

        paused = self.paused

        retired = self.retired

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "leaders": leaders,
                "active": active,
                "paused": paused,
                "retired": retired,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        leaders = d.pop("leaders")

        active = d.pop("active")

        paused = d.pop("paused")

        retired = d.pop("retired")

        copy_leader_page_stats = cls(
            leaders=leaders,
            active=active,
            paused=paused,
            retired=retired,
        )

        copy_leader_page_stats.additional_properties = d
        return copy_leader_page_stats

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
