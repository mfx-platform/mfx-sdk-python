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

from ..models.billing_invoice_state import BillingInvoiceState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_invoice_paid_by_type_0 import BillingInvoicePaidByType0
    from ..models.billing_invoice_replaced_by_type_0 import BillingInvoiceReplacedByType0
    from ..models.billing_invoice_settlement import BillingInvoiceSettlement


T = TypeVar("T", bound="BillingInvoice")


@_attrs_define
class BillingInvoice:
    """
    Attributes:
        id (UUID):
        number (str): Gap-free per year, e.g. INV-2026-1104
        billing_profile_id (UUID):
        period (str):
        total_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
        open_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
        issued_on (datetime.date):
        due_on (datetime.date):
        state (BillingInvoiceState):
        overdue (bool):
        profile_name (Union[Unset, str]):
        subtotal_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        tax_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        overdue_days (Union[None, Unset, int]):
        suspends_at (Union[None, Unset, datetime.datetime]): From the reminder: the first suspended moment if this stays
            unpaid
        pay_by (Union[None, Unset, datetime.datetime]): From the reminder: the last moment a payment avoids the
            suspension
        paid_by (Union['BillingInvoicePaidByType0', None, Unset]): How it was paid; null while nothing is paid
        replaced_by (Union['BillingInvoiceReplacedByType0', None, Unset]): A void invoice: the invoice that replaced it
        pdf_url (Union[None, Unset, str]):
        usage_csv_url (Union[None, Unset, str]):
        settlement (Union['BillingInvoiceSettlement', None, Unset]): Who paid it, when, and the receipt; null until it
            is settled
    """

    id: UUID
    number: str
    billing_profile_id: UUID
    period: str
    total_usd: str
    open_usd: str
    issued_on: datetime.date
    due_on: datetime.date
    state: BillingInvoiceState
    overdue: bool
    profile_name: Union[Unset, str] = UNSET
    subtotal_usd: Union[Unset, str] = UNSET
    tax_usd: Union[Unset, str] = UNSET
    overdue_days: Union[None, Unset, int] = UNSET
    suspends_at: Union[None, Unset, datetime.datetime] = UNSET
    pay_by: Union[None, Unset, datetime.datetime] = UNSET
    paid_by: Union["BillingInvoicePaidByType0", None, Unset] = UNSET
    replaced_by: Union["BillingInvoiceReplacedByType0", None, Unset] = UNSET
    pdf_url: Union[None, Unset, str] = UNSET
    usage_csv_url: Union[None, Unset, str] = UNSET
    settlement: Union["BillingInvoiceSettlement", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_invoice_paid_by_type_0 import BillingInvoicePaidByType0
        from ..models.billing_invoice_replaced_by_type_0 import (
            BillingInvoiceReplacedByType0,
        )
        from ..models.billing_invoice_settlement import BillingInvoiceSettlement

        id = str(self.id)

        number = self.number

        billing_profile_id = str(self.billing_profile_id)

        period = self.period

        total_usd = self.total_usd

        open_usd = self.open_usd

        issued_on = self.issued_on.isoformat()

        due_on = self.due_on.isoformat()

        state = self.state.value

        overdue = self.overdue

        profile_name = self.profile_name

        subtotal_usd = self.subtotal_usd

        tax_usd = self.tax_usd

        overdue_days: Union[None, Unset, int]
        if isinstance(self.overdue_days, Unset):
            overdue_days = UNSET
        else:
            overdue_days = self.overdue_days

        suspends_at: Union[None, Unset, str]
        if isinstance(self.suspends_at, Unset):
            suspends_at = UNSET
        elif isinstance(self.suspends_at, datetime.datetime):
            suspends_at = self.suspends_at.isoformat()
        else:
            suspends_at = self.suspends_at

        pay_by: Union[None, Unset, str]
        if isinstance(self.pay_by, Unset):
            pay_by = UNSET
        elif isinstance(self.pay_by, datetime.datetime):
            pay_by = self.pay_by.isoformat()
        else:
            pay_by = self.pay_by

        paid_by: Union[None, Unset, dict[str, Any]]
        if isinstance(self.paid_by, Unset):
            paid_by = UNSET
        elif isinstance(self.paid_by, BillingInvoicePaidByType0):
            paid_by = self.paid_by.to_dict()
        else:
            paid_by = self.paid_by

        replaced_by: Union[None, Unset, dict[str, Any]]
        if isinstance(self.replaced_by, Unset):
            replaced_by = UNSET
        elif isinstance(self.replaced_by, BillingInvoiceReplacedByType0):
            replaced_by = self.replaced_by.to_dict()
        else:
            replaced_by = self.replaced_by

        pdf_url: Union[None, Unset, str]
        if isinstance(self.pdf_url, Unset):
            pdf_url = UNSET
        else:
            pdf_url = self.pdf_url

        usage_csv_url: Union[None, Unset, str]
        if isinstance(self.usage_csv_url, Unset):
            usage_csv_url = UNSET
        else:
            usage_csv_url = self.usage_csv_url

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
                "id": id,
                "number": number,
                "billing_profile_id": billing_profile_id,
                "period": period,
                "total_usd": total_usd,
                "open_usd": open_usd,
                "issued_on": issued_on,
                "due_on": due_on,
                "state": state,
                "overdue": overdue,
            }
        )
        if profile_name is not UNSET:
            field_dict["profile_name"] = profile_name
        if subtotal_usd is not UNSET:
            field_dict["subtotal_usd"] = subtotal_usd
        if tax_usd is not UNSET:
            field_dict["tax_usd"] = tax_usd
        if overdue_days is not UNSET:
            field_dict["overdue_days"] = overdue_days
        if suspends_at is not UNSET:
            field_dict["suspends_at"] = suspends_at
        if pay_by is not UNSET:
            field_dict["pay_by"] = pay_by
        if paid_by is not UNSET:
            field_dict["paid_by"] = paid_by
        if replaced_by is not UNSET:
            field_dict["replaced_by"] = replaced_by
        if pdf_url is not UNSET:
            field_dict["pdf_url"] = pdf_url
        if usage_csv_url is not UNSET:
            field_dict["usage_csv_url"] = usage_csv_url
        if settlement is not UNSET:
            field_dict["settlement"] = settlement

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice_paid_by_type_0 import BillingInvoicePaidByType0
        from ..models.billing_invoice_replaced_by_type_0 import (
            BillingInvoiceReplacedByType0,
        )
        from ..models.billing_invoice_settlement import BillingInvoiceSettlement

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        number = d.pop("number")

        billing_profile_id = UUID(d.pop("billing_profile_id"))

        period = d.pop("period")

        total_usd = d.pop("total_usd")

        open_usd = d.pop("open_usd")

        issued_on = isoparse(d.pop("issued_on")).date()

        due_on = isoparse(d.pop("due_on")).date()

        state = BillingInvoiceState._read(d.pop("state"))

        overdue = d.pop("overdue")

        profile_name = d.pop("profile_name", UNSET)

        subtotal_usd = d.pop("subtotal_usd", UNSET)

        tax_usd = d.pop("tax_usd", UNSET)

        def _parse_overdue_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        overdue_days = _parse_overdue_days(d.pop("overdue_days", UNSET))

        def _parse_suspends_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                suspends_at_type_0 = isoparse(data)

                return suspends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        suspends_at = _parse_suspends_at(d.pop("suspends_at", UNSET))

        def _parse_pay_by(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pay_by_type_0 = isoparse(data)

                return pay_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        pay_by = _parse_pay_by(d.pop("pay_by", UNSET))

        def _parse_paid_by(data: object) -> Union["BillingInvoicePaidByType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                paid_by_type_0 = BillingInvoicePaidByType0.from_dict(data)

                return paid_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingInvoicePaidByType0", None, Unset], data)

        paid_by = _parse_paid_by(d.pop("paid_by", UNSET))

        def _parse_replaced_by(data: object) -> Union["BillingInvoiceReplacedByType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                replaced_by_type_0 = BillingInvoiceReplacedByType0.from_dict(data)

                return replaced_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingInvoiceReplacedByType0", None, Unset], data)

        replaced_by = _parse_replaced_by(d.pop("replaced_by", UNSET))

        def _parse_pdf_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pdf_url = _parse_pdf_url(d.pop("pdf_url", UNSET))

        def _parse_usage_csv_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        usage_csv_url = _parse_usage_csv_url(d.pop("usage_csv_url", UNSET))

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

        billing_invoice = cls(
            id=id,
            number=number,
            billing_profile_id=billing_profile_id,
            period=period,
            total_usd=total_usd,
            open_usd=open_usd,
            issued_on=issued_on,
            due_on=due_on,
            state=state,
            overdue=overdue,
            profile_name=profile_name,
            subtotal_usd=subtotal_usd,
            tax_usd=tax_usd,
            overdue_days=overdue_days,
            suspends_at=suspends_at,
            pay_by=pay_by,
            paid_by=paid_by,
            replaced_by=replaced_by,
            pdf_url=pdf_url,
            usage_csv_url=usage_csv_url,
            settlement=settlement,
        )

        billing_invoice.additional_properties = d
        return billing_invoice

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
