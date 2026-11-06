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

from ..models.risk_daily_loss_basis import RiskDailyLossBasis
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_actions import RiskActions
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskDailyLoss")


@_attrs_define
class RiskDailyLoss:
    """
    Attributes:
        limit (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        basis (RiskDailyLossBasis):
        warn_at (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        act_at (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        check_entries (bool): Refuse an entry whose loss at its stop would take the day past act_at (risk_daily_loss)
        actions (RiskActions):
    """

    limit: "RiskAmount"
    basis: RiskDailyLossBasis
    warn_at: "RiskAmount"
    act_at: "RiskAmount"
    check_entries: bool
    actions: "RiskActions"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        limit = self.limit.to_dict()

        basis = self.basis.value

        warn_at = self.warn_at.to_dict()

        act_at = self.act_at.to_dict()

        check_entries = self.check_entries

        actions = self.actions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "basis": basis,
                "warn_at": warn_at,
                "act_at": act_at,
                "check_entries": check_entries,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        limit = RiskAmount.from_dict(d.pop("limit"))

        basis = RiskDailyLossBasis(d.pop("basis"))

        warn_at = RiskAmount.from_dict(d.pop("warn_at"))

        act_at = RiskAmount.from_dict(d.pop("act_at"))

        check_entries = d.pop("check_entries")

        actions = RiskActions.from_dict(d.pop("actions"))

        risk_daily_loss = cls(
            limit=limit,
            basis=basis,
            warn_at=warn_at,
            act_at=act_at,
            check_entries=check_entries,
            actions=actions,
        )

        risk_daily_loss.additional_properties = d
        return risk_daily_loss

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
