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

T = TypeVar("T", bound="BillingInvoiceDetailPayByTransferType0")


@_attrs_define
class BillingInvoiceDetailPayByTransferType0:
    """
    Attributes:
        account_name (Union[Unset, str]):
        currency (Union[Unset, str]):
        account_number (Union[Unset, str]):
        routing (Union[Unset, str]):
        swift (Union[Unset, str]):
        reference (Union[Unset, str]):
    """

    account_name: Union[Unset, str] = UNSET
    currency: Union[Unset, str] = UNSET
    account_number: Union[Unset, str] = UNSET
    routing: Union[Unset, str] = UNSET
    swift: Union[Unset, str] = UNSET
    reference: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_name = self.account_name

        currency = self.currency

        account_number = self.account_number

        routing = self.routing

        swift = self.swift

        reference = self.reference

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_name is not UNSET:
            field_dict["account_name"] = account_name
        if currency is not UNSET:
            field_dict["currency"] = currency
        if account_number is not UNSET:
            field_dict["account_number"] = account_number
        if routing is not UNSET:
            field_dict["routing"] = routing
        if swift is not UNSET:
            field_dict["swift"] = swift
        if reference is not UNSET:
            field_dict["reference"] = reference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        account_name = d.pop("account_name", UNSET)

        currency = d.pop("currency", UNSET)

        account_number = d.pop("account_number", UNSET)

        routing = d.pop("routing", UNSET)

        swift = d.pop("swift", UNSET)

        reference = d.pop("reference", UNSET)

        billing_invoice_detail_pay_by_transfer_type_0 = cls(
            account_name=account_name,
            currency=currency,
            account_number=account_number,
            routing=routing,
            swift=swift,
            reference=reference,
        )

        billing_invoice_detail_pay_by_transfer_type_0.additional_properties = d
        return billing_invoice_detail_pay_by_transfer_type_0

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
