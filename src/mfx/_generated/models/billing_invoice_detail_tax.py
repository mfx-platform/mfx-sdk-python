from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_invoice_detail_tax_rule import BillingInvoiceDetailTaxRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingInvoiceDetailTax")


@_attrs_define
class BillingInvoiceDetailTax:
    """
    Attributes:
        rule (BillingInvoiceDetailTaxRule):
        rate_pct (int):
        tax_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
    """

    rule: BillingInvoiceDetailTaxRule
    rate_pct: int
    tax_usd: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule = self.rule.value

        rate_pct = self.rate_pct

        tax_usd = self.tax_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
                "rate_pct": rate_pct,
                "tax_usd": tax_usd,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule = BillingInvoiceDetailTaxRule._read(d.pop("rule"))

        rate_pct = d.pop("rate_pct")

        tax_usd = d.pop("tax_usd")

        billing_invoice_detail_tax = cls(
            rule=rule,
            rate_pct=rate_pct,
            tax_usd=tax_usd,
        )

        billing_invoice_detail_tax.additional_properties = d
        return billing_invoice_detail_tax

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
