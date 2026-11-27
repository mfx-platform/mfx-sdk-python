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

T = TypeVar("T", bound="BillingInvoicePageStats")


@_attrs_define
class BillingInvoicePageStats:
    """Totals for the filtered set: the portal's tiles, and available to the tenant API on the same filters

    Attributes:
        open_ (Union[Unset, int]):
        open_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        overdue (Union[Unset, int]):
        overdue_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        in_progress (Union[Unset, int]):
        in_progress_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        due_in_7_days_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        due_in_7_days_count (Union[Unset, int]): How many invoices due_in_7_days_usd sums
        settled_12m_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        average_days_to_settle (Union[None, Unset, float]):
        next_invoice_on (Union[None, Unset, datetime.date]):
    """

    open_: Union[Unset, int] = UNSET
    open_usd: Union[Unset, str] = UNSET
    overdue: Union[Unset, int] = UNSET
    overdue_usd: Union[Unset, str] = UNSET
    in_progress: Union[Unset, int] = UNSET
    in_progress_usd: Union[Unset, str] = UNSET
    due_in_7_days_usd: Union[Unset, str] = UNSET
    due_in_7_days_count: Union[Unset, int] = UNSET
    settled_12m_usd: Union[Unset, str] = UNSET
    average_days_to_settle: Union[None, Unset, float] = UNSET
    next_invoice_on: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        open_ = self.open_

        open_usd = self.open_usd

        overdue = self.overdue

        overdue_usd = self.overdue_usd

        in_progress = self.in_progress

        in_progress_usd = self.in_progress_usd

        due_in_7_days_usd = self.due_in_7_days_usd

        due_in_7_days_count = self.due_in_7_days_count

        settled_12m_usd = self.settled_12m_usd

        average_days_to_settle: Union[None, Unset, float]
        if isinstance(self.average_days_to_settle, Unset):
            average_days_to_settle = UNSET
        else:
            average_days_to_settle = self.average_days_to_settle

        next_invoice_on: Union[None, Unset, str]
        if isinstance(self.next_invoice_on, Unset):
            next_invoice_on = UNSET
        elif isinstance(self.next_invoice_on, datetime.date):
            next_invoice_on = self.next_invoice_on.isoformat()
        else:
            next_invoice_on = self.next_invoice_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if open_ is not UNSET:
            field_dict["open"] = open_
        if open_usd is not UNSET:
            field_dict["open_usd"] = open_usd
        if overdue is not UNSET:
            field_dict["overdue"] = overdue
        if overdue_usd is not UNSET:
            field_dict["overdue_usd"] = overdue_usd
        if in_progress is not UNSET:
            field_dict["in_progress"] = in_progress
        if in_progress_usd is not UNSET:
            field_dict["in_progress_usd"] = in_progress_usd
        if due_in_7_days_usd is not UNSET:
            field_dict["due_in_7_days_usd"] = due_in_7_days_usd
        if due_in_7_days_count is not UNSET:
            field_dict["due_in_7_days_count"] = due_in_7_days_count
        if settled_12m_usd is not UNSET:
            field_dict["settled_12m_usd"] = settled_12m_usd
        if average_days_to_settle is not UNSET:
            field_dict["average_days_to_settle"] = average_days_to_settle
        if next_invoice_on is not UNSET:
            field_dict["next_invoice_on"] = next_invoice_on

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        open_ = d.pop("open", UNSET)

        open_usd = d.pop("open_usd", UNSET)

        overdue = d.pop("overdue", UNSET)

        overdue_usd = d.pop("overdue_usd", UNSET)

        in_progress = d.pop("in_progress", UNSET)

        in_progress_usd = d.pop("in_progress_usd", UNSET)

        due_in_7_days_usd = d.pop("due_in_7_days_usd", UNSET)

        due_in_7_days_count = d.pop("due_in_7_days_count", UNSET)

        settled_12m_usd = d.pop("settled_12m_usd", UNSET)

        def _parse_average_days_to_settle(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_days_to_settle = _parse_average_days_to_settle(
            d.pop("average_days_to_settle", UNSET)
        )

        def _parse_next_invoice_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_invoice_on_type_0 = isoparse(data).date()

                return next_invoice_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        next_invoice_on = _parse_next_invoice_on(d.pop("next_invoice_on", UNSET))

        billing_invoice_page_stats = cls(
            open_=open_,
            open_usd=open_usd,
            overdue=overdue,
            overdue_usd=overdue_usd,
            in_progress=in_progress,
            in_progress_usd=in_progress_usd,
            due_in_7_days_usd=due_in_7_days_usd,
            due_in_7_days_count=due_in_7_days_count,
            settled_12m_usd=settled_12m_usd,
            average_days_to_settle=average_days_to_settle,
            next_invoice_on=next_invoice_on,
        )

        billing_invoice_page_stats.additional_properties = d
        return billing_invoice_page_stats

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
