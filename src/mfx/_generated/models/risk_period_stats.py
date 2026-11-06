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

T = TypeVar("T", bound="RiskPeriodStats")


@_attrs_define
class RiskPeriodStats:
    """
    Attributes:
        start_equity (Union[None, str]):
        end_equity (Union[None, str]):
        start_balance (Union[None, str]):
        end_balance (Union[None, str]):
        profit (Union[None, str]):
        max_drawdown (Union[None, str]):
        max_drawdown_at (Union[None, datetime.datetime]):
        days_traded (int):
        worst_daily_loss (Union[None, str]):
    """

    start_equity: Union[None, str]
    end_equity: Union[None, str]
    start_balance: Union[None, str]
    end_balance: Union[None, str]
    profit: Union[None, str]
    max_drawdown: Union[None, str]
    max_drawdown_at: Union[None, datetime.datetime]
    days_traded: int
    worst_daily_loss: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_equity: Union[None, str]
        start_equity = self.start_equity

        end_equity: Union[None, str]
        end_equity = self.end_equity

        start_balance: Union[None, str]
        start_balance = self.start_balance

        end_balance: Union[None, str]
        end_balance = self.end_balance

        profit: Union[None, str]
        profit = self.profit

        max_drawdown: Union[None, str]
        max_drawdown = self.max_drawdown

        max_drawdown_at: Union[None, str]
        if isinstance(self.max_drawdown_at, datetime.datetime):
            max_drawdown_at = self.max_drawdown_at.isoformat()
        else:
            max_drawdown_at = self.max_drawdown_at

        days_traded = self.days_traded

        worst_daily_loss: Union[None, str]
        worst_daily_loss = self.worst_daily_loss

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_equity": start_equity,
                "end_equity": end_equity,
                "start_balance": start_balance,
                "end_balance": end_balance,
                "profit": profit,
                "max_drawdown": max_drawdown,
                "max_drawdown_at": max_drawdown_at,
                "days_traded": days_traded,
                "worst_daily_loss": worst_daily_loss,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_start_equity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        start_equity = _parse_start_equity(d.pop("start_equity"))

        def _parse_end_equity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        end_equity = _parse_end_equity(d.pop("end_equity"))

        def _parse_start_balance(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        start_balance = _parse_start_balance(d.pop("start_balance"))

        def _parse_end_balance(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        end_balance = _parse_end_balance(d.pop("end_balance"))

        def _parse_profit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profit = _parse_profit(d.pop("profit"))

        def _parse_max_drawdown(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        max_drawdown = _parse_max_drawdown(d.pop("max_drawdown"))

        def _parse_max_drawdown_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                max_drawdown_at_type_0 = isoparse(data)

                return max_drawdown_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        max_drawdown_at = _parse_max_drawdown_at(d.pop("max_drawdown_at"))

        days_traded = d.pop("days_traded")

        def _parse_worst_daily_loss(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        worst_daily_loss = _parse_worst_daily_loss(d.pop("worst_daily_loss"))

        risk_period_stats = cls(
            start_equity=start_equity,
            end_equity=end_equity,
            start_balance=start_balance,
            end_balance=end_balance,
            profit=profit,
            max_drawdown=max_drawdown,
            max_drawdown_at=max_drawdown_at,
            days_traded=days_traded,
            worst_daily_loss=worst_daily_loss,
        )

        risk_period_stats.additional_properties = d
        return risk_period_stats

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
