from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_coverage_summary_counts import RiskCoverageSummaryCounts
    from ..models.risk_coverage_summary_not_healthy_item import (
        RiskCoverageSummaryNotHealthyItem,
    )


T = TypeVar("T", bound="RiskCoverageSummary")


@_attrs_define
class RiskCoverageSummary:
    """
    Attributes:
        counts (RiskCoverageSummaryCounts): For each kind (monitoring, pre_trade, broker_held, managed_actions), how
            many accounts are in each state
        not_healthy (list['RiskCoverageSummaryNotHealthyItem']):
    """

    counts: "RiskCoverageSummaryCounts"
    not_healthy: list["RiskCoverageSummaryNotHealthyItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_coverage_summary_counts import RiskCoverageSummaryCounts
        from ..models.risk_coverage_summary_not_healthy_item import (
            RiskCoverageSummaryNotHealthyItem,
        )

        counts = self.counts.to_dict()

        not_healthy = []
        for not_healthy_item_data in self.not_healthy:
            not_healthy_item = not_healthy_item_data.to_dict()
            not_healthy.append(not_healthy_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "counts": counts,
                "not_healthy": not_healthy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_coverage_summary_counts import RiskCoverageSummaryCounts
        from ..models.risk_coverage_summary_not_healthy_item import (
            RiskCoverageSummaryNotHealthyItem,
        )

        d = dict(src_dict)
        counts = RiskCoverageSummaryCounts.from_dict(d.pop("counts"))

        not_healthy = []
        _not_healthy = d.pop("not_healthy")
        for not_healthy_item_data in _not_healthy:
            not_healthy_item = RiskCoverageSummaryNotHealthyItem.from_dict(not_healthy_item_data)

            not_healthy.append(not_healthy_item)

        risk_coverage_summary = cls(
            counts=counts,
            not_healthy=not_healthy,
        )

        risk_coverage_summary.additional_properties = d
        return risk_coverage_summary

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
