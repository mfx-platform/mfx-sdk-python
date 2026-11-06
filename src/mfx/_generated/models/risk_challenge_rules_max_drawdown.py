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

from ..models.risk_challenge_rules_max_drawdown_kind import (
    RiskChallengeRulesMaxDrawdownKind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskChallengeRulesMaxDrawdown")


@_attrs_define
class RiskChallengeRulesMaxDrawdown:
    """
    Attributes:
        kind (RiskChallengeRulesMaxDrawdownKind):
        limit (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
    """

    kind: RiskChallengeRulesMaxDrawdownKind
    limit: "RiskAmount"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_amount import RiskAmount

        kind = self.kind.value

        limit = self.limit.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "limit": limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        kind = RiskChallengeRulesMaxDrawdownKind(d.pop("kind"))

        limit = RiskAmount.from_dict(d.pop("limit"))

        risk_challenge_rules_max_drawdown = cls(
            kind=kind,
            limit=limit,
        )

        risk_challenge_rules_max_drawdown.additional_properties = d
        return risk_challenge_rules_max_drawdown

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
