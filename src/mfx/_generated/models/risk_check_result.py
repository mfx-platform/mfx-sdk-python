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

from ..models.risk_check_result_verdict import RiskCheckResultVerdict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_rule_check import RiskRuleCheck


T = TypeVar("T", bound="RiskCheckResult")


@_attrs_define
class RiskCheckResult:
    """
    Attributes:
        verdict (RiskCheckResultVerdict):
        reason (Union[None, str]):
        checks (list['RiskRuleCheck']):
    """

    verdict: RiskCheckResultVerdict
    reason: Union[None, str]
    checks: list["RiskRuleCheck"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_rule_check import RiskRuleCheck

        verdict = self.verdict.value

        reason: Union[None, str]
        reason = self.reason

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "verdict": verdict,
                "reason": reason,
                "checks": checks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_rule_check import RiskRuleCheck

        d = dict(src_dict)
        verdict = RiskCheckResultVerdict(d.pop("verdict"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = RiskRuleCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        risk_check_result = cls(
            verdict=verdict,
            reason=reason,
            checks=checks,
        )

        risk_check_result.additional_properties = d
        return risk_check_result

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
