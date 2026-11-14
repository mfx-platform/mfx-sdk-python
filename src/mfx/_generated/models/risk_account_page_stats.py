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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskAccountPageStats")


@_attrs_define
class RiskAccountPageStats:
    """
    Attributes:
        accounts (int):
        protected (int): Accounts with an active policy or an enrolled challenge
        restricted (int):
        degraded (int):
        actions_today (int):
        unresolved (int):
        warnings (Union[Unset, int]): Accounts with a rule at its warn level, short of acting
        active_plans (Union[Unset, int]): Exit plans armed, managing or paused, over every account
        gross_exposure (Union[Unset, str]): The open volume in lots over every account (gross exposure in money is per
            account, in its own currency)
    """

    accounts: int
    protected: int
    restricted: int
    degraded: int
    actions_today: int
    unresolved: int
    warnings: Union[Unset, int] = UNSET
    active_plans: Union[Unset, int] = UNSET
    gross_exposure: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts

        protected = self.protected

        restricted = self.restricted

        degraded = self.degraded

        actions_today = self.actions_today

        unresolved = self.unresolved

        warnings = self.warnings

        active_plans = self.active_plans

        gross_exposure = self.gross_exposure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "protected": protected,
                "restricted": restricted,
                "degraded": degraded,
                "actions_today": actions_today,
                "unresolved": unresolved,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if active_plans is not UNSET:
            field_dict["active_plans"] = active_plans
        if gross_exposure is not UNSET:
            field_dict["gross_exposure"] = gross_exposure

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accounts = d.pop("accounts")

        protected = d.pop("protected")

        restricted = d.pop("restricted")

        degraded = d.pop("degraded")

        actions_today = d.pop("actions_today")

        unresolved = d.pop("unresolved")

        warnings = d.pop("warnings", UNSET)

        active_plans = d.pop("active_plans", UNSET)

        gross_exposure = d.pop("gross_exposure", UNSET)

        risk_account_page_stats = cls(
            accounts=accounts,
            protected=protected,
            restricted=restricted,
            degraded=degraded,
            actions_today=actions_today,
            unresolved=unresolved,
            warnings=warnings,
            active_plans=active_plans,
            gross_exposure=gross_exposure,
        )

        risk_account_page_stats.additional_properties = d
        return risk_account_page_stats

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
