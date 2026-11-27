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
    from ..models.billing_payment_required_error_error import (
        BillingPaymentRequiredErrorError,
    )


T = TypeVar("T", bound="BillingPaymentRequiredError")


@_attrs_define
class BillingPaymentRequiredError:
    """The error envelope of a 402 billing_payment_required, with its details

    Attributes:
        error (BillingPaymentRequiredErrorError):
    """

    error: "BillingPaymentRequiredErrorError"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_payment_required_error_error import (
            BillingPaymentRequiredErrorError,
        )

        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_payment_required_error_error import (
            BillingPaymentRequiredErrorError,
        )

        d = dict(src_dict)
        error = BillingPaymentRequiredErrorError.from_dict(d.pop("error"))

        billing_payment_required_error = cls(
            error=error,
        )

        billing_payment_required_error.additional_properties = d
        return billing_payment_required_error

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
