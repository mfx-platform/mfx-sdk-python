import datetime
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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.ea_colour import EaColour
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_finding import EaFinding
    from ..models.ea_trial_figure import EaTrialFigure


T = TypeVar("T", bound="EaReportTrial")


@_attrs_define
class EaReportTrial:
    """One judged trial, as the report carries it

    Attributes:
        terminal_id (UUID):
        ended_at (datetime.datetime): When it was judged
        verdict (EaColour): A verdict's colour. green: nothing found, or notes only. amber: needs a person. red:
            refused. grey: nothing could be judged yet. The verdict of a version is its worst finding under the policy
            version it was judged by.
        findings (list['EaFinding']): One for each trial rule its figures crossed, `found_by` trial, with the figure
            measured and the line in `evidence`. Empty on a green trial, and on one that failed because nothing was measured
            or the wrong build was loaded: `reason` says which
        reason (Union[None, str]): Why it was not green, in one line; null on a green trial
        figures (list['EaTrialFigure']): The seven, as judged
    """

    terminal_id: UUID
    ended_at: datetime.datetime
    verdict: EaColour
    findings: list["EaFinding"]
    reason: Union[None, str]
    figures: list["EaTrialFigure"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_finding import EaFinding
        from ..models.ea_trial_figure import EaTrialFigure

        terminal_id = str(self.terminal_id)

        ended_at = self.ended_at.isoformat()

        verdict = self.verdict.value

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        reason: Union[None, str]
        reason = self.reason

        figures = []
        for figures_item_data in self.figures:
            figures_item = figures_item_data.to_dict()
            figures.append(figures_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "ended_at": ended_at,
                "verdict": verdict,
                "findings": findings,
                "reason": reason,
                "figures": figures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_finding import EaFinding
        from ..models.ea_trial_figure import EaTrialFigure

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        ended_at = isoparse(d.pop("ended_at"))

        verdict = EaColour(d.pop("verdict"))

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = EaFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        figures = []
        _figures = d.pop("figures")
        for figures_item_data in _figures:
            figures_item = EaTrialFigure.from_dict(figures_item_data)

            figures.append(figures_item)

        ea_report_trial = cls(
            terminal_id=terminal_id,
            ended_at=ended_at,
            verdict=verdict,
            findings=findings,
            reason=reason,
            figures=figures,
        )

        ea_report_trial.additional_properties = d
        return ea_report_trial

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
