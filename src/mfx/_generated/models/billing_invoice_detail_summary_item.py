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

T = TypeVar("T", bound="BillingInvoiceDetailSummaryItem")


@_attrs_define
class BillingInvoiceDetailSummaryItem:
    """
    Attributes:
        key (Union[Unset, str]):
        quantity (Union[Unset, str]):
        unit (Union[Unset, str]):
        monthly_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        amount_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
    """

    key: Union[Unset, str] = UNSET
    quantity: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    monthly_usd: Union[Unset, str] = UNSET
    amount_usd: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        quantity = self.quantity

        unit = self.unit

        monthly_usd = self.monthly_usd

        amount_usd = self.amount_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if unit is not UNSET:
            field_dict["unit"] = unit
        if monthly_usd is not UNSET:
            field_dict["monthly_usd"] = monthly_usd
        if amount_usd is not UNSET:
            field_dict["amount_usd"] = amount_usd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        quantity = d.pop("quantity", UNSET)

        unit = d.pop("unit", UNSET)

        monthly_usd = d.pop("monthly_usd", UNSET)

        amount_usd = d.pop("amount_usd", UNSET)

        billing_invoice_detail_summary_item = cls(
            key=key,
            quantity=quantity,
            unit=unit,
            monthly_usd=monthly_usd,
            amount_usd=amount_usd,
        )

        billing_invoice_detail_summary_item.additional_properties = d
        return billing_invoice_detail_summary_item

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
