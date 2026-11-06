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

from ..models.risk_challenge_rules_daily_loss_basis import (
    RiskChallengeRulesDailyLossBasis,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskChallengeRulesDailyLoss")


@_attrs_define
class RiskChallengeRulesDailyLoss:
    """
    Attributes:
        limit (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        basis (RiskChallengeRulesDailyLossBasis):
    """

    limit: "RiskAmount"
    basis: RiskChallengeRulesDailyLossBasis
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_amount import RiskAmount

        limit = self.limit.to_dict()

        basis = self.basis.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "basis": basis,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        limit = RiskAmount.from_dict(d.pop("limit"))

        basis = RiskChallengeRulesDailyLossBasis(d.pop("basis"))

        risk_challenge_rules_daily_loss = cls(
            limit=limit,
            basis=basis,
        )

        risk_challenge_rules_daily_loss.additional_properties = d
        return risk_challenge_rules_daily_loss

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
