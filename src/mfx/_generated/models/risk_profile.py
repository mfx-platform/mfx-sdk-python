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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_actions import RiskActions
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskProfile")


@_attrs_define
class RiskProfile:
    """A template the tenant confirmed: it filled the rules and adds its own labelled rules. Updating a template never
    changes an active version

        Attributes:
            name (str):
            version (str):
            confirmed_at (datetime.datetime):
            profit_target (Union[Unset, RiskAmount]): A limit as money in the account currency, or as a percentage of the
                rule's reference; exactly one
            min_trading_days (Union[Unset, int]):
            consistency (Union[None, Unset, str]): The tenant's own words; shown, not evaluated
            on_target (Union[Unset, RiskActions]):
    """

    name: str
    version: str
    confirmed_at: datetime.datetime
    profit_target: Union[Unset, "RiskAmount"] = UNSET
    min_trading_days: Union[Unset, int] = UNSET
    consistency: Union[None, Unset, str] = UNSET
    on_target: Union[Unset, "RiskActions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        name = self.name

        version = self.version

        confirmed_at = self.confirmed_at.isoformat()

        profit_target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.profit_target, Unset):
            profit_target = self.profit_target.to_dict()

        min_trading_days = self.min_trading_days

        consistency: Union[None, Unset, str]
        if isinstance(self.consistency, Unset):
            consistency = UNSET
        else:
            consistency = self.consistency

        on_target: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.on_target, Unset):
            on_target = self.on_target.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "version": version,
                "confirmed_at": confirmed_at,
            }
        )
        if profit_target is not UNSET:
            field_dict["profit_target"] = profit_target
        if min_trading_days is not UNSET:
            field_dict["min_trading_days"] = min_trading_days
        if consistency is not UNSET:
            field_dict["consistency"] = consistency
        if on_target is not UNSET:
            field_dict["on_target"] = on_target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        confirmed_at = isoparse(d.pop("confirmed_at"))

        _profit_target = d.pop("profit_target", UNSET)
        profit_target: Union[Unset, RiskAmount]
        if isinstance(_profit_target, Unset):
            profit_target = UNSET
        else:
            profit_target = RiskAmount.from_dict(_profit_target)

        min_trading_days = d.pop("min_trading_days", UNSET)

        def _parse_consistency(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        consistency = _parse_consistency(d.pop("consistency", UNSET))

        _on_target = d.pop("on_target", UNSET)
        on_target: Union[Unset, RiskActions]
        if isinstance(_on_target, Unset):
            on_target = UNSET
        else:
            on_target = RiskActions.from_dict(_on_target)

        risk_profile = cls(
            name=name,
            version=version,
            confirmed_at=confirmed_at,
            profit_target=profit_target,
            min_trading_days=min_trading_days,
            consistency=consistency,
            on_target=on_target,
        )

        risk_profile.additional_properties = d
        return risk_profile

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
