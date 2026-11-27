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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_invoice_detail_receipts_item_state import (
    BillingInvoiceDetailReceiptsItemState,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_invoice_detail_receipts_item_uploaded_by import (
        BillingInvoiceDetailReceiptsItemUploadedBy,
    )


T = TypeVar("T", bound="BillingInvoiceDetailReceiptsItem")


@_attrs_define
class BillingInvoiceDetailReceiptsItem:
    """
    Attributes:
        id (UUID):
        file (str): The file name as uploaded
        file_path (str): Where the portal downloads it:
            /portal/v1/billing/invoices/{invoice_id}/receipts/{receipt_id}/file
        amount_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        sent_on (datetime.date):
        uploaded_by (BillingInvoiceDetailReceiptsItemUploadedBy):
        state (BillingInvoiceDetailReceiptsItemState):
        bank_reference (Union[None, Unset, str]):
        matched_on (Union[None, Unset, datetime.date]):
        reason (Union[None, Unset, str]): Why it was rejected, as the customer reads it; null unless rejected
    """

    id: UUID
    file: str
    file_path: str
    amount_usd: str
    sent_on: datetime.date
    uploaded_by: "BillingInvoiceDetailReceiptsItemUploadedBy"
    state: BillingInvoiceDetailReceiptsItemState
    bank_reference: Union[None, Unset, str] = UNSET
    matched_on: Union[None, Unset, datetime.date] = UNSET
    reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_invoice_detail_receipts_item_uploaded_by import (
            BillingInvoiceDetailReceiptsItemUploadedBy,
        )

        id = str(self.id)

        file = self.file

        file_path = self.file_path

        amount_usd = self.amount_usd

        sent_on = self.sent_on.isoformat()

        uploaded_by = self.uploaded_by.to_dict()

        state = self.state.value

        bank_reference: Union[None, Unset, str]
        if isinstance(self.bank_reference, Unset):
            bank_reference = UNSET
        else:
            bank_reference = self.bank_reference

        matched_on: Union[None, Unset, str]
        if isinstance(self.matched_on, Unset):
            matched_on = UNSET
        elif isinstance(self.matched_on, datetime.date):
            matched_on = self.matched_on.isoformat()
        else:
            matched_on = self.matched_on

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "file": file,
                "file_path": file_path,
                "amount_usd": amount_usd,
                "sent_on": sent_on,
                "uploaded_by": uploaded_by,
                "state": state,
            }
        )
        if bank_reference is not UNSET:
            field_dict["bank_reference"] = bank_reference
        if matched_on is not UNSET:
            field_dict["matched_on"] = matched_on
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice_detail_receipts_item_uploaded_by import (
            BillingInvoiceDetailReceiptsItemUploadedBy,
        )

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        file = d.pop("file")

        file_path = d.pop("file_path")

        amount_usd = d.pop("amount_usd")

        sent_on = isoparse(d.pop("sent_on")).date()

        uploaded_by = BillingInvoiceDetailReceiptsItemUploadedBy.from_dict(d.pop("uploaded_by"))

        state = BillingInvoiceDetailReceiptsItemState._read(d.pop("state"))

        def _parse_bank_reference(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bank_reference = _parse_bank_reference(d.pop("bank_reference", UNSET))

        def _parse_matched_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                matched_on_type_0 = isoparse(data).date()

                return matched_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        matched_on = _parse_matched_on(d.pop("matched_on", UNSET))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        billing_invoice_detail_receipts_item = cls(
            id=id,
            file=file,
            file_path=file_path,
            amount_usd=amount_usd,
            sent_on=sent_on,
            uploaded_by=uploaded_by,
            state=state,
            bank_reference=bank_reference,
            matched_on=matched_on,
            reason=reason,
        )

        billing_invoice_detail_receipts_item.additional_properties = d
        return billing_invoice_detail_receipts_item

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
