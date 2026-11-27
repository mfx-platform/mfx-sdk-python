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
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_agreement_ref_payment_mode import BillingAgreementRefPaymentMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingAgreementRef")


@_attrs_define
class BillingAgreementRef:
    """The Enterprise agreement in force: its number, term, renewal and how it pays. Where it is used it is null when none
    is in force, which is always the case on Standard.

        Attributes:
            id (UUID):
            number (str): e.g. AGR-2026-0003
            starts_on (datetime.date):
            ends_on (datetime.date): The last UTC day of the term
            auto_renew (bool): On: at the end of the term it runs again for a term of the same length, with the same
                entitlements and prices
            payment_mode (BillingAgreementRefPaymentMode): How every billing profile of the organisation pays while the
                agreement is in force
    """

    id: UUID
    number: str
    starts_on: datetime.date
    ends_on: datetime.date
    auto_renew: bool
    payment_mode: BillingAgreementRefPaymentMode
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        number = self.number

        starts_on = self.starts_on.isoformat()

        ends_on = self.ends_on.isoformat()

        auto_renew = self.auto_renew

        payment_mode = self.payment_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "number": number,
                "starts_on": starts_on,
                "ends_on": ends_on,
                "auto_renew": auto_renew,
                "payment_mode": payment_mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        number = d.pop("number")

        starts_on = isoparse(d.pop("starts_on")).date()

        ends_on = isoparse(d.pop("ends_on")).date()

        auto_renew = d.pop("auto_renew")

        payment_mode = BillingAgreementRefPaymentMode._read(d.pop("payment_mode"))

        billing_agreement_ref = cls(
            id=id,
            number=number,
            starts_on=starts_on,
            ends_on=ends_on,
            auto_renew=auto_renew,
            payment_mode=payment_mode,
        )

        billing_agreement_ref.additional_properties = d
        return billing_agreement_ref

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
