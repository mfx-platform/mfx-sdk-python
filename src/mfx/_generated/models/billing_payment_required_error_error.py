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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_body_details import ErrorBodyDetails


T = TypeVar("T", bound="BillingPaymentRequiredErrorError")


@_attrs_define
class BillingPaymentRequiredErrorError:
    """
    Attributes:
        code (str): Which rule refused the request, or which failure this is: the kind of error, not the HTTP status.
            **`x-known-values` beside this lists every code the platform sends today, and the list is not closed**: a new
            rule brings a new code, and it is added here in the release that sends it. A client must read a code it does not
            know as an error, by the HTTP status and `message`, and must never fail on it. A client generated from this
            contract gets text here, not a fixed set, for that reason.
        message (str):
        details (ErrorBodyDetails): `details` of a 402 `billing_payment_required` Example: {'tenant_id':
            '6f1c2a0e-1b8d-4f7a-9a51-7d0c1a2b3c4d', 'billing_profile_id': '0b7e5c1a-3d2f-4e6a-8b9c-1d2e3f4a5b6c', 'stage':
            'reminder', 'cause': 'balance_used_up', 'since': '2026-11-20T00:05:00Z', 'suspends_at': '2026-11-23T00:05:00Z',
            'pay_by': '2026-11-23T00:04:59Z', 'action': {'kind': 'top_up', 'portal_path': '/billing/top-up', 'amount_usd':
            '10.00', 'invoice_id': None}}.
    """

    code: str
    message: str
    details: "ErrorBodyDetails"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.error_body_details import ErrorBodyDetails

        code = self.code

        message = self.message

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_body_details import ErrorBodyDetails

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        details = ErrorBodyDetails.from_dict(d.pop("details"))

        billing_payment_required_error_error = cls(
            code=code,
            message=message,
            details=details,
        )

        billing_payment_required_error_error.additional_properties = d
        return billing_payment_required_error_error

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
