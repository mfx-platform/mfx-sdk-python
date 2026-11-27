from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingSummaryOpenInvoices")


@_attrs_define
class BillingSummaryOpenInvoices:
    """
    Attributes:
        count (int):
        open_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
        overdue_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
    """

    count: int
    open_usd: str
    overdue_usd: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        open_usd = self.open_usd

        overdue_usd = self.overdue_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "open_usd": open_usd,
                "overdue_usd": overdue_usd,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        open_usd = d.pop("open_usd")

        overdue_usd = d.pop("overdue_usd")

        billing_summary_open_invoices = cls(
            count=count,
            open_usd=open_usd,
            overdue_usd=overdue_usd,
        )

        billing_summary_open_invoices.additional_properties = d
        return billing_summary_open_invoices

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
