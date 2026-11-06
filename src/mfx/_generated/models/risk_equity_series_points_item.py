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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskEquitySeriesPointsItem")


@_attrs_define
class RiskEquitySeriesPointsItem:
    """
    Attributes:
        at (datetime.datetime):
        equity (str):
        balance (str):
    """

    at: datetime.datetime
    equity: str
    balance: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        equity = self.equity

        balance = self.balance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "equity": equity,
                "balance": balance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = isoparse(d.pop("at"))

        equity = d.pop("equity")

        balance = d.pop("balance")

        risk_equity_series_points_item = cls(
            at=at,
            equity=equity,
            balance=balance,
        )

        risk_equity_series_points_item.additional_properties = d
        return risk_equity_series_points_item

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
