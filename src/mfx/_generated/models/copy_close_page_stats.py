from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyClosePageStats")


@_attrs_define
class CopyClosePageStats:
    """Over every close the filters and the window match, not this page

    Attributes:
        pending (int):
        done (int):
        incomplete (int):
        superseded (int):
    """

    pending: int
    done: int
    incomplete: int
    superseded: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pending = self.pending

        done = self.done

        incomplete = self.incomplete

        superseded = self.superseded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pending": pending,
                "done": done,
                "incomplete": incomplete,
                "superseded": superseded,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pending = d.pop("pending")

        done = d.pop("done")

        incomplete = d.pop("incomplete")

        superseded = d.pop("superseded")

        copy_close_page_stats = cls(
            pending=pending,
            done=done,
            incomplete=incomplete,
            superseded=superseded,
        )

        copy_close_page_stats.additional_properties = d
        return copy_close_page_stats

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
