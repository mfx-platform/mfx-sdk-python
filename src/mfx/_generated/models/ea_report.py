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

from ..models.ea_colour import EaColour
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_finding import EaFinding
    from ..models.ea_report_categories_item import EaReportCategoriesItem
    from ..models.ea_report_trial import EaReportTrial


T = TypeVar("T", bound="EaReport")


@_attrs_define
class EaReport:
    """The report of one version: the same one the tenant reads through the API and receives by email.

    Attributes:
        policy_version (int): The policy version it was judged by
        verdict (EaColour): A verdict's colour. green: nothing found, or notes only. amber: needs a person. red:
            refused. grey: nothing could be judged yet. The verdict of a version is its worst finding under the policy
            version it was judged by.
        categories (list['EaReportCategoriesItem']): One entry for each rule group, in the register's order
        findings (list['EaFinding']):
        summary (Union[None, str]): The AI review's paragraph for the tenant; null where it did not run
        trial (Union['EaReportTrial', None, Unset]): The newest judged trial of this version: its verdict, what it found
            and its figures. The version's own verdict, findings and categories stay those of its checks; a trial is judged
            on one terminal. Null until a trial has been judged, and absent from older answers
    """

    policy_version: int
    verdict: EaColour
    categories: list["EaReportCategoriesItem"]
    findings: list["EaFinding"]
    summary: Union[None, str]
    trial: Union["EaReportTrial", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_finding import EaFinding
        from ..models.ea_report_categories_item import EaReportCategoriesItem
        from ..models.ea_report_trial import EaReportTrial

        policy_version = self.policy_version

        verdict = self.verdict.value

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        summary: Union[None, str]
        summary = self.summary

        trial: Union[None, Unset, dict[str, Any]]
        if isinstance(self.trial, Unset):
            trial = UNSET
        elif isinstance(self.trial, EaReportTrial):
            trial = self.trial.to_dict()
        else:
            trial = self.trial

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_version": policy_version,
                "verdict": verdict,
                "categories": categories,
                "findings": findings,
                "summary": summary,
            }
        )
        if trial is not UNSET:
            field_dict["trial"] = trial

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_finding import EaFinding
        from ..models.ea_report_categories_item import EaReportCategoriesItem
        from ..models.ea_report_trial import EaReportTrial

        d = dict(src_dict)
        policy_version = d.pop("policy_version")

        verdict = EaColour(d.pop("verdict"))

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = EaReportCategoriesItem.from_dict(categories_item_data)

            categories.append(categories_item)

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = EaFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        def _parse_summary(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        summary = _parse_summary(d.pop("summary"))

        def _parse_trial(data: object) -> Union["EaReportTrial", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                trial_type_0 = EaReportTrial.from_dict(data)

                return trial_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EaReportTrial", None, Unset], data)

        trial = _parse_trial(d.pop("trial", UNSET))

        ea_report = cls(
            policy_version=policy_version,
            verdict=verdict,
            categories=categories,
            findings=findings,
            summary=summary,
            trial=trial,
        )

        ea_report.additional_properties = d
        return ea_report

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
