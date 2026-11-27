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

T = TypeVar("T", bound="BillingForecastLinesItem")


@_attrs_define
class BillingForecastLinesItem:
    """
    Attributes:
        key (str): The price-list item, e.g. account.mt5
        account_days (int): Account-days charged to date
        to_date_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        forecast_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        daily_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
    """

    key: str
    account_days: int
    to_date_usd: str
    forecast_usd: str
    daily_usd: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        account_days = self.account_days

        to_date_usd = self.to_date_usd

        forecast_usd = self.forecast_usd

        daily_usd = self.daily_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "account_days": account_days,
                "to_date_usd": to_date_usd,
                "forecast_usd": forecast_usd,
            }
        )
        if daily_usd is not UNSET:
            field_dict["daily_usd"] = daily_usd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        account_days = d.pop("account_days")

        to_date_usd = d.pop("to_date_usd")

        forecast_usd = d.pop("forecast_usd")

        daily_usd = d.pop("daily_usd", UNSET)

        billing_forecast_lines_item = cls(
            key=key,
            account_days=account_days,
            to_date_usd=to_date_usd,
            forecast_usd=forecast_usd,
            daily_usd=daily_usd,
        )

        billing_forecast_lines_item.additional_properties = d
        return billing_forecast_lines_item

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
