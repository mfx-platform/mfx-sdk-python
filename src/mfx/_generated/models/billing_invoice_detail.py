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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_invoice import BillingInvoice
    from ..models.billing_invoice_detail_history_item import (
        BillingInvoiceDetailHistoryItem,
    )
    from ..models.billing_invoice_detail_pay_by_transfer_type_0 import (
        BillingInvoiceDetailPayByTransferType0,
    )
    from ..models.billing_invoice_detail_receipts_item import (
        BillingInvoiceDetailReceiptsItem,
    )
    from ..models.billing_invoice_detail_summary_item import (
        BillingInvoiceDetailSummaryItem,
    )
    from ..models.billing_invoice_detail_tax import BillingInvoiceDetailTax
    from ..models.billing_invoice_settlement import BillingInvoiceSettlement
    from ..models.billing_standing import BillingStanding


T = TypeVar("T", bound="BillingInvoiceDetail")


@_attrs_define
class BillingInvoiceDetail:
    """One invoice with its lines summary, its tax, what is matched, how to pay and its history

    Attributes:
        invoice (BillingInvoice):
        tax (BillingInvoiceDetailTax):
        matched_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        lines_total (int):
        history (list['BillingInvoiceDetailHistoryItem']):
        summary (Union[Unset, list['BillingInvoiceDetailSummaryItem']]): One line per product, quantities in account-
            months or block-months
        pay_by_transfer (Union['BillingInvoiceDetailPayByTransferType0', None, Unset]):
        receipts (Union[Unset, list['BillingInvoiceDetailReceiptsItem']]):
        standing (Union[Unset, BillingStanding]): Where a billing profile stands on payment. `ok`: nothing is due.
            `notice`: a prepaid balance will last fewer days than the notice setting, or an invoice is due within it.
            `reminder`: the balance is used up or the invoice is past due; `suspends_at` is the first suspended moment and
            `pay_by` the last moment a payment avoids it, and requests that add something billed are refused with 402
            `billing_payment_required`. `suspended`: the profile's MT5 terminals are disabled and its cTrader connections
            stopped, nothing deleted, and suspended days are not billed. Paying releases them.
        settlement (Union['BillingInvoiceSettlement', None, Unset]): The same as invoice.settlement: who paid it, when,
            and the receipt; null until it is settled
    """

    invoice: "BillingInvoice"
    tax: "BillingInvoiceDetailTax"
    matched_usd: str
    lines_total: int
    history: list["BillingInvoiceDetailHistoryItem"]
    summary: Union[Unset, list["BillingInvoiceDetailSummaryItem"]] = UNSET
    pay_by_transfer: Union["BillingInvoiceDetailPayByTransferType0", None, Unset] = UNSET
    receipts: Union[Unset, list["BillingInvoiceDetailReceiptsItem"]] = UNSET
    standing: Union[Unset, "BillingStanding"] = UNSET
    settlement: Union["BillingInvoiceSettlement", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_invoice import BillingInvoice
        from ..models.billing_invoice_detail_history_item import (
            BillingInvoiceDetailHistoryItem,
        )
        from ..models.billing_invoice_detail_pay_by_transfer_type_0 import (
            BillingInvoiceDetailPayByTransferType0,
        )
        from ..models.billing_invoice_detail_receipts_item import (
            BillingInvoiceDetailReceiptsItem,
        )
        from ..models.billing_invoice_detail_summary_item import (
            BillingInvoiceDetailSummaryItem,
        )
        from ..models.billing_invoice_detail_tax import BillingInvoiceDetailTax
        from ..models.billing_invoice_settlement import BillingInvoiceSettlement
        from ..models.billing_standing import BillingStanding

        invoice = self.invoice.to_dict()

        tax = self.tax.to_dict()

        matched_usd = self.matched_usd

        lines_total = self.lines_total

        history = []
        for history_item_data in self.history:
            history_item = history_item_data.to_dict()
            history.append(history_item)

        summary: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.summary, Unset):
            summary = []
            for summary_item_data in self.summary:
                summary_item = summary_item_data.to_dict()
                summary.append(summary_item)

        pay_by_transfer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.pay_by_transfer, Unset):
            pay_by_transfer = UNSET
        elif isinstance(self.pay_by_transfer, BillingInvoiceDetailPayByTransferType0):
            pay_by_transfer = self.pay_by_transfer.to_dict()
        else:
            pay_by_transfer = self.pay_by_transfer

        receipts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.receipts, Unset):
            receipts = []
            for receipts_item_data in self.receipts:
                receipts_item = receipts_item_data.to_dict()
                receipts.append(receipts_item)

        standing: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.standing, Unset):
            standing = self.standing.to_dict()

        settlement: Union[None, Unset, dict[str, Any]]
        if isinstance(self.settlement, Unset):
            settlement = UNSET
        elif isinstance(self.settlement, BillingInvoiceSettlement):
            settlement = self.settlement.to_dict()
        else:
            settlement = self.settlement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invoice": invoice,
                "tax": tax,
                "matched_usd": matched_usd,
                "lines_total": lines_total,
                "history": history,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if pay_by_transfer is not UNSET:
            field_dict["pay_by_transfer"] = pay_by_transfer
        if receipts is not UNSET:
            field_dict["receipts"] = receipts
        if standing is not UNSET:
            field_dict["standing"] = standing
        if settlement is not UNSET:
            field_dict["settlement"] = settlement

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice import BillingInvoice
        from ..models.billing_invoice_detail_history_item import (
            BillingInvoiceDetailHistoryItem,
        )
        from ..models.billing_invoice_detail_pay_by_transfer_type_0 import (
            BillingInvoiceDetailPayByTransferType0,
        )
        from ..models.billing_invoice_detail_receipts_item import (
            BillingInvoiceDetailReceiptsItem,
        )
        from ..models.billing_invoice_detail_summary_item import (
            BillingInvoiceDetailSummaryItem,
        )
        from ..models.billing_invoice_detail_tax import BillingInvoiceDetailTax
        from ..models.billing_invoice_settlement import BillingInvoiceSettlement
        from ..models.billing_standing import BillingStanding

        d = dict(src_dict)
        invoice = BillingInvoice.from_dict(d.pop("invoice"))

        tax = BillingInvoiceDetailTax.from_dict(d.pop("tax"))

        matched_usd = d.pop("matched_usd")

        lines_total = d.pop("lines_total")

        history = []
        _history = d.pop("history")
        for history_item_data in _history:
            history_item = BillingInvoiceDetailHistoryItem.from_dict(history_item_data)

            history.append(history_item)

        summary = []
        _summary = d.pop("summary", UNSET)
        for summary_item_data in _summary or []:
            summary_item = BillingInvoiceDetailSummaryItem.from_dict(summary_item_data)

            summary.append(summary_item)

        def _parse_pay_by_transfer(
            data: object,
        ) -> Union["BillingInvoiceDetailPayByTransferType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pay_by_transfer_type_0 = BillingInvoiceDetailPayByTransferType0.from_dict(data)

                return pay_by_transfer_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingInvoiceDetailPayByTransferType0", None, Unset], data)

        pay_by_transfer = _parse_pay_by_transfer(d.pop("pay_by_transfer", UNSET))

        receipts = []
        _receipts = d.pop("receipts", UNSET)
        for receipts_item_data in _receipts or []:
            receipts_item = BillingInvoiceDetailReceiptsItem.from_dict(receipts_item_data)

            receipts.append(receipts_item)

        _standing = d.pop("standing", UNSET)
        standing: Union[Unset, BillingStanding]
        if isinstance(_standing, Unset):
            standing = UNSET
        else:
            standing = BillingStanding.from_dict(_standing)

        def _parse_settlement(data: object) -> Union["BillingInvoiceSettlement", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settlement_type_0 = BillingInvoiceSettlement.from_dict(data)

                return settlement_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingInvoiceSettlement", None, Unset], data)

        settlement = _parse_settlement(d.pop("settlement", UNSET))

        billing_invoice_detail = cls(
            invoice=invoice,
            tax=tax,
            matched_usd=matched_usd,
            lines_total=lines_total,
            history=history,
            summary=summary,
            pay_by_transfer=pay_by_transfer,
            receipts=receipts,
            standing=standing,
            settlement=settlement,
        )

        billing_invoice_detail.additional_properties = d
        return billing_invoice_detail

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
