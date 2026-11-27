from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopySignalEntryOutcomes")


@_attrs_define
class CopySignalEntryOutcomes:
    """How many of the signal's own copies, one a follower, were filled, refused and skipped; 0 where none. A stop-out's
    close names the signal it closes but is not its copy

        Attributes:
            filled (int):
            refused (int):
            skipped (int):
    """

    filled: int
    refused: int
    skipped: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filled = self.filled

        refused = self.refused

        skipped = self.skipped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filled": filled,
                "refused": refused,
                "skipped": skipped,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filled = d.pop("filled")

        refused = d.pop("refused")

        skipped = d.pop("skipped")

        copy_signal_entry_outcomes = cls(
            filled=filled,
            refused=refused,
            skipped=skipped,
        )

        copy_signal_entry_outcomes.additional_properties = d
        return copy_signal_entry_outcomes

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
