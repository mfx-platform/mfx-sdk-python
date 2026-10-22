from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantExpertAdvisorFindings")


@_attrs_define
class TenantExpertAdvisorFindings:
    """How many findings of each colour, under the policy version it was judged by. All zero until it is judged

    Attributes:
        red (int):
        amber (int):
        note (int):
    """

    red: int
    amber: int
    note: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        red = self.red

        amber = self.amber

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "red": red,
                "amber": amber,
                "note": note,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        red = d.pop("red")

        amber = d.pop("amber")

        note = d.pop("note")

        tenant_expert_advisor_findings = cls(
            red=red,
            amber=amber,
            note=note,
        )

        tenant_expert_advisor_findings.additional_properties = d
        return tenant_expert_advisor_findings

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
