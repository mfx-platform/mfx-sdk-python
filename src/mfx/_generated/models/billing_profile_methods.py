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
    from ..models.billing_payment_method import BillingPaymentMethod


T = TypeVar("T", bound="BillingProfileMethods")


@_attrs_define
class BillingProfileMethods:
    """Portal only

    Attributes:
        primary (Union['BillingPaymentMethod', None, Unset]):
        backup (Union['BillingPaymentMethod', None, Unset]):
    """

    primary: Union["BillingPaymentMethod", None, Unset] = UNSET
    backup: Union["BillingPaymentMethod", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_payment_method import BillingPaymentMethod

        primary: Union[None, Unset, dict[str, Any]]
        if isinstance(self.primary, Unset):
            primary = UNSET
        elif isinstance(self.primary, BillingPaymentMethod):
            primary = self.primary.to_dict()
        else:
            primary = self.primary

        backup: Union[None, Unset, dict[str, Any]]
        if isinstance(self.backup, Unset):
            backup = UNSET
        elif isinstance(self.backup, BillingPaymentMethod):
            backup = self.backup.to_dict()
        else:
            backup = self.backup

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if primary is not UNSET:
            field_dict["primary"] = primary
        if backup is not UNSET:
            field_dict["backup"] = backup

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_payment_method import BillingPaymentMethod

        d = dict(src_dict)

        def _parse_primary(data: object) -> Union["BillingPaymentMethod", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                primary_type_0 = BillingPaymentMethod.from_dict(data)

                return primary_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingPaymentMethod", None, Unset], data)

        primary = _parse_primary(d.pop("primary", UNSET))

        def _parse_backup(data: object) -> Union["BillingPaymentMethod", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                backup_type_0 = BillingPaymentMethod.from_dict(data)

                return backup_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingPaymentMethod", None, Unset], data)

        backup = _parse_backup(d.pop("backup", UNSET))

        billing_profile_methods = cls(
            primary=primary,
            backup=backup,
        )

        billing_profile_methods.additional_properties = d
        return billing_profile_methods

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
