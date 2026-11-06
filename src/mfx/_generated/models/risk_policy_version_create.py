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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_reset import RiskReset
    from ..models.risk_rules import RiskRules


T = TypeVar("T", bound="RiskPolicyVersionCreate")


@_attrs_define
class RiskPolicyVersionCreate:
    """
    Attributes:
        rules (RiskRules): Every rule is optional; a rule present is evaluated. Nothing has a default the platform chose
        reset (RiskReset):
        reason (Union[None, Unset, str]):
    """

    rules: "RiskRules"
    reset: "RiskReset"
    reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_reset import RiskReset
        from ..models.risk_rules import RiskRules

        rules = self.rules.to_dict()

        reset = self.reset.to_dict()

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rules": rules,
                "reset": reset,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_reset import RiskReset
        from ..models.risk_rules import RiskRules

        d = dict(src_dict)
        rules = RiskRules.from_dict(d.pop("rules"))

        reset = RiskReset.from_dict(d.pop("reset"))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        risk_policy_version_create = cls(
            rules=rules,
            reset=reset,
            reason=reason,
        )

        risk_policy_version_create.additional_properties = d
        return risk_policy_version_create

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
