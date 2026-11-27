from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyFollowerPageStats")


@_attrs_define
class CopyFollowerPageStats:
    """Over every follower the filters match, not this page

    Attributes:
        followers (int):
        copying (int):
        paused (int):
        stopped_out (int):
        unfollowed (int):
        out_of_step (Union[Unset, int]): Of those, the ones out of step: not unfollowed, and their newest drift above 0
    """

    followers: int
    copying: int
    paused: int
    stopped_out: int
    unfollowed: int
    out_of_step: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        followers = self.followers

        copying = self.copying

        paused = self.paused

        stopped_out = self.stopped_out

        unfollowed = self.unfollowed

        out_of_step = self.out_of_step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "followers": followers,
                "copying": copying,
                "paused": paused,
                "stopped_out": stopped_out,
                "unfollowed": unfollowed,
            }
        )
        if out_of_step is not UNSET:
            field_dict["out_of_step"] = out_of_step

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        followers = d.pop("followers")

        copying = d.pop("copying")

        paused = d.pop("paused")

        stopped_out = d.pop("stopped_out")

        unfollowed = d.pop("unfollowed")

        out_of_step = d.pop("out_of_step", UNSET)

        copy_follower_page_stats = cls(
            followers=followers,
            copying=copying,
            paused=paused,
            stopped_out=stopped_out,
            unfollowed=unfollowed,
            out_of_step=out_of_step,
        )

        copy_follower_page_stats.additional_properties = d
        return copy_follower_page_stats

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
