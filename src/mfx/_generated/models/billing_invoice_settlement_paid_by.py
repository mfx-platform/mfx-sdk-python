from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_invoice_settlement_paid_by_rail import (
    BillingInvoiceSettlementPaidByRail,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingInvoiceSettlementPaidBy")


@_attrs_define
class BillingInvoiceSettlementPaidBy:
    """
    Attributes:
        rail (BillingInvoiceSettlementPaidByRail):
        label (str): e.g. Visa ending 4242, or Bank transfer, 8 Nov
    """

    rail: BillingInvoiceSettlementPaidByRail
    label: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rail = self.rail.value

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rail": rail,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rail = BillingInvoiceSettlementPaidByRail._read(d.pop("rail"))

        label = d.pop("label")

        billing_invoice_settlement_paid_by = cls(
            rail=rail,
            label=label,
        )

        billing_invoice_settlement_paid_by.additional_properties = d
        return billing_invoice_settlement_paid_by

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
