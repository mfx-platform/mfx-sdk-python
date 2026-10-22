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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ea_finding_colour import EaFindingColour
from ..models.ea_finding_found_by import EaFindingFoundBy
from ..models.ea_rule_group import EaRuleGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="EaFinding")


@_attrs_define
class EaFinding:
    """One finding of a report. `evidence` is quoted from the source at the lines named; a finding of the AI review whose
    evidence is not there is dropped before the report is made. A found secret is masked wherever it appears.

        Attributes:
            rule_id (str): e.g. SEC-06
            group (EaRuleGroup):
            name (str): The rule in an operator's words
            colour (EaFindingColour): Under the report's policy version. grey: the check could not be made on this file
            found_by (EaFindingFoundBy):
            file (Union[None, str]): The file of the bundle; null for a finding of the scan or the trial
            line_from (Union[None, int]):
            line_to (Union[None, int]):
            evidence (Union[None, str]): The lines quoted, or the figure measured
            why (str): Why it matters, in plain words
            change (Union[None, str]): What the tenant should change
    """

    rule_id: str
    group: EaRuleGroup
    name: str
    colour: EaFindingColour
    found_by: EaFindingFoundBy
    file: Union[None, str]
    line_from: Union[None, int]
    line_to: Union[None, int]
    evidence: Union[None, str]
    why: str
    change: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule_id = self.rule_id

        group = self.group.value

        name = self.name

        colour = self.colour.value

        found_by = self.found_by.value

        file: Union[None, str]
        file = self.file

        line_from: Union[None, int]
        line_from = self.line_from

        line_to: Union[None, int]
        line_to = self.line_to

        evidence: Union[None, str]
        evidence = self.evidence

        why = self.why

        change: Union[None, str]
        change = self.change

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule_id": rule_id,
                "group": group,
                "name": name,
                "colour": colour,
                "found_by": found_by,
                "file": file,
                "line_from": line_from,
                "line_to": line_to,
                "evidence": evidence,
                "why": why,
                "change": change,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule_id = d.pop("rule_id")

        group = EaRuleGroup(d.pop("group"))

        name = d.pop("name")

        colour = EaFindingColour(d.pop("colour"))

        found_by = EaFindingFoundBy(d.pop("found_by"))

        def _parse_file(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        file = _parse_file(d.pop("file"))

        def _parse_line_from(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        line_from = _parse_line_from(d.pop("line_from"))

        def _parse_line_to(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        line_to = _parse_line_to(d.pop("line_to"))

        def _parse_evidence(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        evidence = _parse_evidence(d.pop("evidence"))

        why = d.pop("why")

        def _parse_change(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        change = _parse_change(d.pop("change"))

        ea_finding = cls(
            rule_id=rule_id,
            group=group,
            name=name,
            colour=colour,
            found_by=found_by,
            file=file,
            line_from=line_from,
            line_to=line_to,
            evidence=evidence,
            why=why,
            change=change,
        )

        ea_finding.additional_properties = d
        return ea_finding

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
