from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EaTrialCount")


@_attrs_define
class EaTrialCount:
    """How this version's trials went, shown beside its colour: a trial colours the terminal's attachment, not the version,
    so the version says how many of its terminals' trials failed out of those judged. Every attachment of the version
    counts, on a terminal now or ended. Absent from older answers

        Attributes:
            failed (int): Trials judged amber, red or grey
            judged (int): Trials judged; one still running, or ended before it was judged, is not counted
    """

    failed: int
    judged: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed = self.failed

        judged = self.judged

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failed": failed,
                "judged": judged,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        failed = d.pop("failed")

        judged = d.pop("judged")

        ea_trial_count = cls(
            failed=failed,
            judged=judged,
        )

        ea_trial_count.additional_properties = d
        return ea_trial_count

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
