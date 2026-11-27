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

from ..models.billing_verification_ref_status import BillingVerificationRefStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingVerificationRef")


@_attrs_define
class BillingVerificationRef:
    """Where the organisation's verification stands. Only verified unlocks what waits for it, such as invoices

    Attributes:
        status (BillingVerificationRefStatus):
        verified (bool): True when status is verified
        verified_at (Union[None, Unset, datetime.datetime]): When it was last verified; null when it is not
        renewal_due (Union[None, Unset, datetime.date]): A verified organisation is verified again every 12 months
    """

    status: BillingVerificationRefStatus
    verified: bool
    verified_at: Union[None, Unset, datetime.datetime] = UNSET
    renewal_due: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        verified = self.verified

        verified_at: Union[None, Unset, str]
        if isinstance(self.verified_at, Unset):
            verified_at = UNSET
        elif isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        renewal_due: Union[None, Unset, str]
        if isinstance(self.renewal_due, Unset):
            renewal_due = UNSET
        elif isinstance(self.renewal_due, datetime.date):
            renewal_due = self.renewal_due.isoformat()
        else:
            renewal_due = self.renewal_due

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "verified": verified,
            }
        )
        if verified_at is not UNSET:
            field_dict["verified_at"] = verified_at
        if renewal_due is not UNSET:
            field_dict["renewal_due"] = renewal_due

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = BillingVerificationRefStatus._read(d.pop("status"))

        verified = d.pop("verified")

        def _parse_verified_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verified_at_type_0 = isoparse(data)

                return verified_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        verified_at = _parse_verified_at(d.pop("verified_at", UNSET))

        def _parse_renewal_due(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                renewal_due_type_0 = isoparse(data).date()

                return renewal_due_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        renewal_due = _parse_renewal_due(d.pop("renewal_due", UNSET))

        billing_verification_ref = cls(
            status=status,
            verified=verified,
            verified_at=verified_at,
            renewal_due=renewal_due,
        )

        billing_verification_ref.additional_properties = d
        return billing_verification_ref

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
