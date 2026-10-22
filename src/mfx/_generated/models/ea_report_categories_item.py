from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ea_colour import EaColour
from ..models.ea_rule_group import EaRuleGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="EaReportCategoriesItem")


@_attrs_define
class EaReportCategoriesItem:
    """
    Attributes:
        group (EaRuleGroup):
        colour (EaColour): A verdict's colour. green: nothing found, or notes only. amber: needs a person. red: refused.
            grey: nothing could be judged yet. The verdict of a version is its worst finding under the policy version it was
            judged by.
        findings (int):
    """

    group: EaRuleGroup
    colour: EaColour
    findings: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group = self.group.value

        colour = self.colour.value

        findings = self.findings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group": group,
                "colour": colour,
                "findings": findings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group = EaRuleGroup(d.pop("group"))

        colour = EaColour(d.pop("colour"))

        findings = d.pop("findings")

        ea_report_categories_item = cls(
            group=group,
            colour=colour,
            findings=findings,
        )

        ea_report_categories_item.additional_properties = d
        return ea_report_categories_item

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
