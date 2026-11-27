from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyTenantStopoutPageStats")


@_attrs_define
class CopyTenantStopoutPageStats:
    """Over every stop-out the window and the filters match, not this page

    Attributes:
        stopouts (int):
        active (int):
        reset (int):
        expired (int):
    """

    stopouts: int
    active: int
    reset: int
    expired: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stopouts = self.stopouts

        active = self.active

        reset = self.reset

        expired = self.expired

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stopouts": stopouts,
                "active": active,
                "reset": reset,
                "expired": expired,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stopouts = d.pop("stopouts")

        active = d.pop("active")

        reset = d.pop("reset")

        expired = d.pop("expired")

        copy_tenant_stopout_page_stats = cls(
            stopouts=stopouts,
            active=active,
            reset=reset,
            expired=expired,
        )

        copy_tenant_stopout_page_stats.additional_properties = d
        return copy_tenant_stopout_page_stats

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
