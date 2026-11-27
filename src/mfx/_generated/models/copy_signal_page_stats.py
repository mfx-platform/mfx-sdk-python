from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopySignalPageStats")


@_attrs_define
class CopySignalPageStats:
    """Over every signal the window and the filters match, not this page

    Attributes:
        signals (int):
        fill (int):
        external (int):
    """

    signals: int
    fill: int
    external: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        signals = self.signals

        fill = self.fill

        external = self.external

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signals": signals,
                "fill": fill,
                "external": external,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signals = d.pop("signals")

        fill = d.pop("fill")

        external = d.pop("external")

        copy_signal_page_stats = cls(
            signals=signals,
            fill=fill,
            external=external,
        )

        copy_signal_page_stats.additional_properties = d
        return copy_signal_page_stats

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
