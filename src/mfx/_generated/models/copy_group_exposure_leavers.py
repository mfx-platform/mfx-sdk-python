from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyGroupExposureLeavers")


@_attrs_define
class CopyGroupExposureLeavers:
    """The open copied positions of followers that left the group (unfollowed without close_copied, or removed): copied
    under it, no longer counted in used or against the cap

        Attributes:
            used (str): Their exposure, in US dollars
            unpriced (int): Of those rows, the ones with no exposure or in another currency
    """

    used: str
    unpriced: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used = self.used

        unpriced = self.unpriced

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "unpriced": unpriced,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used = d.pop("used")

        unpriced = d.pop("unpriced")

        copy_group_exposure_leavers = cls(
            used=used,
            unpriced=unpriced,
        )

        copy_group_exposure_leavers.additional_properties = d
        return copy_group_exposure_leavers

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
