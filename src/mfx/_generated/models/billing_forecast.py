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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_forecast_lines_item import BillingForecastLinesItem


T = TypeVar("T", bound="BillingForecast")


@_attrs_define
class BillingForecast:
    """This month for one billing profile: to date by product, and the forecast to month end at today's accounts and add-
    ons. Quantities are account-days; a full month of one account is as many account-days as the month has days.

        Example:
            {'month': '2026-11', 'billing_profile_id': '0b7e5c1a-3d2f-4e6a-8b9c-1d2e3f4a5b6c', 'days_in_month': 30,
                'days_billed': 15, 'to_date_usd': '25.85', 'forecast_usd': '51.60', 'tax_forecast_usd': '5.16', 'lines':
                [{'key': 'account.mt5', 'account_days': 75, 'daily_usd': '0.250000', 'to_date_usd': '18.75', 'forecast_usd':
                '37.50'}, {'key': 'addon.expert_advisors', 'account_days': 30, 'daily_usd': '0.200000', 'to_date_usd': '6.00',
                'forecast_usd': '12.00'}, {'key': 'account.ctrader', 'account_days': 10, 'daily_usd': '0.083333', 'to_date_usd':
                '0.83', 'forecast_usd': '0.83'}, {'key': 'addon.risk_management', 'account_days': 4, 'daily_usd': '0.066667',
                'to_date_usd': '0.27', 'forecast_usd': '1.27'}], 'talk_to_sales': False}

        Attributes:
            month (str):
            billing_profile_id (UUID):
            days_in_month (int):
            days_billed (int): UTC days charged so far: a day is charged just after it ends
            to_date_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
                to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
                table; never rounded before it is summed.
            forecast_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
                to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
                table; never rounded before it is summed.
            lines (list['BillingForecastLinesItem']):
            talk_to_sales (bool):
            tax_forecast_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
                "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
                per-day rate in a table; never rounded before it is summed.
    """

    month: str
    billing_profile_id: UUID
    days_in_month: int
    days_billed: int
    to_date_usd: str
    forecast_usd: str
    lines: list["BillingForecastLinesItem"]
    talk_to_sales: bool
    tax_forecast_usd: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_forecast_lines_item import BillingForecastLinesItem

        month = self.month

        billing_profile_id = str(self.billing_profile_id)

        days_in_month = self.days_in_month

        days_billed = self.days_billed

        to_date_usd = self.to_date_usd

        forecast_usd = self.forecast_usd

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        talk_to_sales = self.talk_to_sales

        tax_forecast_usd = self.tax_forecast_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "month": month,
                "billing_profile_id": billing_profile_id,
                "days_in_month": days_in_month,
                "days_billed": days_billed,
                "to_date_usd": to_date_usd,
                "forecast_usd": forecast_usd,
                "lines": lines,
                "talk_to_sales": talk_to_sales,
            }
        )
        if tax_forecast_usd is not UNSET:
            field_dict["tax_forecast_usd"] = tax_forecast_usd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_forecast_lines_item import BillingForecastLinesItem

        d = dict(src_dict)
        month = d.pop("month")

        billing_profile_id = UUID(d.pop("billing_profile_id"))

        days_in_month = d.pop("days_in_month")

        days_billed = d.pop("days_billed")

        to_date_usd = d.pop("to_date_usd")

        forecast_usd = d.pop("forecast_usd")

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = BillingForecastLinesItem.from_dict(lines_item_data)

            lines.append(lines_item)

        talk_to_sales = d.pop("talk_to_sales")

        tax_forecast_usd = d.pop("tax_forecast_usd", UNSET)

        billing_forecast = cls(
            month=month,
            billing_profile_id=billing_profile_id,
            days_in_month=days_in_month,
            days_billed=days_billed,
            to_date_usd=to_date_usd,
            forecast_usd=forecast_usd,
            lines=lines,
            talk_to_sales=talk_to_sales,
            tax_forecast_usd=tax_forecast_usd,
        )

        billing_forecast.additional_properties = d
        return billing_forecast

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
