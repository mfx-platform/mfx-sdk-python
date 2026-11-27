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

if TYPE_CHECKING:
    from ..models.billing_invoice_settlement_paid_by import BillingInvoiceSettlementPaidBy
    from ..models.billing_invoice_settlement_paid_by_person_type_0 import (
        BillingInvoiceSettlementPaidByPersonType0,
    )


T = TypeVar("T", bound="BillingInvoiceSettlement")


@_attrs_define
class BillingInvoiceSettlement:
    """How a settled invoice was paid. When several payments settled it, `paid_at` and the receipt are the last payment's
    and `paid_by.rail` is mixed; every receipt is in the documents.

        Attributes:
            paid_at (datetime.datetime): When the payment that settled it succeeded or was matched
            paid_by (BillingInvoiceSettlementPaidBy):
            receipt_number (Union[None, str]): The receipt issued for that payment, e.g. RCT-2026-000123; null when the last
                part was written off rather than paid
            receipt_document_id (Union[None, str]): The receipt in the documents list, as the document PDF route takes it;
                null with receipt_number
            paid_by_person (Union['BillingInvoiceSettlementPaidByPersonType0', None, Unset]): The portal member who paid the
                settling payment by card; null for a bank transfer or an automatic payment
    """

    paid_at: datetime.datetime
    paid_by: "BillingInvoiceSettlementPaidBy"
    receipt_number: Union[None, str]
    receipt_document_id: Union[None, str]
    paid_by_person: Union["BillingInvoiceSettlementPaidByPersonType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_invoice_settlement_paid_by import (
            BillingInvoiceSettlementPaidBy,
        )
        from ..models.billing_invoice_settlement_paid_by_person_type_0 import (
            BillingInvoiceSettlementPaidByPersonType0,
        )

        paid_at = self.paid_at.isoformat()

        paid_by = self.paid_by.to_dict()

        receipt_number: Union[None, str]
        receipt_number = self.receipt_number

        receipt_document_id: Union[None, str]
        receipt_document_id = self.receipt_document_id

        paid_by_person: Union[None, Unset, dict[str, Any]]
        if isinstance(self.paid_by_person, Unset):
            paid_by_person = UNSET
        elif isinstance(self.paid_by_person, BillingInvoiceSettlementPaidByPersonType0):
            paid_by_person = self.paid_by_person.to_dict()
        else:
            paid_by_person = self.paid_by_person

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paid_at": paid_at,
                "paid_by": paid_by,
                "receipt_number": receipt_number,
                "receipt_document_id": receipt_document_id,
            }
        )
        if paid_by_person is not UNSET:
            field_dict["paid_by_person"] = paid_by_person

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice_settlement_paid_by import (
            BillingInvoiceSettlementPaidBy,
        )
        from ..models.billing_invoice_settlement_paid_by_person_type_0 import (
            BillingInvoiceSettlementPaidByPersonType0,
        )

        d = dict(src_dict)
        paid_at = isoparse(d.pop("paid_at"))

        paid_by = BillingInvoiceSettlementPaidBy.from_dict(d.pop("paid_by"))

        def _parse_receipt_number(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        receipt_number = _parse_receipt_number(d.pop("receipt_number"))

        def _parse_receipt_document_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        receipt_document_id = _parse_receipt_document_id(d.pop("receipt_document_id"))

        def _parse_paid_by_person(
            data: object,
        ) -> Union["BillingInvoiceSettlementPaidByPersonType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                paid_by_person_type_0 = BillingInvoiceSettlementPaidByPersonType0.from_dict(data)

                return paid_by_person_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingInvoiceSettlementPaidByPersonType0", None, Unset], data)

        paid_by_person = _parse_paid_by_person(d.pop("paid_by_person", UNSET))

        billing_invoice_settlement = cls(
            paid_at=paid_at,
            paid_by=paid_by,
            receipt_number=receipt_number,
            receipt_document_id=receipt_document_id,
            paid_by_person=paid_by_person,
        )

        billing_invoice_settlement.additional_properties = d
        return billing_invoice_settlement

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
