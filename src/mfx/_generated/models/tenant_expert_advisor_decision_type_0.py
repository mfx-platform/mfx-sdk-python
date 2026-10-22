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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tenant_expert_advisor_decision_type_0_decision import (
    TenantExpertAdvisorDecisionType0Decision,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantExpertAdvisorDecisionType0")


@_attrs_define
class TenantExpertAdvisorDecisionType0:
    """
    Attributes:
        decision (TenantExpertAdvisorDecisionType0Decision):
        reason (Union[None, str]): What the operator wrote for you
        at (datetime.datetime):
    """

    decision: TenantExpertAdvisorDecisionType0Decision
    reason: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        decision = self.decision.value

        reason: Union[None, str]
        reason = self.reason

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decision": decision,
                "reason": reason,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision = TenantExpertAdvisorDecisionType0Decision(d.pop("decision"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        at = isoparse(d.pop("at"))

        tenant_expert_advisor_decision_type_0 = cls(
            decision=decision,
            reason=reason,
            at=at,
        )

        tenant_expert_advisor_decision_type_0.additional_properties = d
        return tenant_expert_advisor_decision_type_0

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
