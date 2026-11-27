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

T = TypeVar("T", bound="BillingPriceListAccountsType0")


@_attrs_define
class BillingPriceListAccountsType0:
    """Your own prices only (GET /billing/prices): the accounts the Standard prices tile reads. Absent from the public list

    Attributes:
        running_accounts (int):
        paused_accounts (int):
        max_running_accounts (Union[None, int]): The plan's running-account limit; null when it has none
    """

    running_accounts: int
    paused_accounts: int
    max_running_accounts: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        running_accounts = self.running_accounts

        paused_accounts = self.paused_accounts

        max_running_accounts: Union[None, int]
        max_running_accounts = self.max_running_accounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "running_accounts": running_accounts,
                "paused_accounts": paused_accounts,
                "max_running_accounts": max_running_accounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        running_accounts = d.pop("running_accounts")

        paused_accounts = d.pop("paused_accounts")

        def _parse_max_running_accounts(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_running_accounts = _parse_max_running_accounts(d.pop("max_running_accounts"))

        billing_price_list_accounts_type_0 = cls(
            running_accounts=running_accounts,
            paused_accounts=paused_accounts,
            max_running_accounts=max_running_accounts,
        )

        billing_price_list_accounts_type_0.additional_properties = d
        return billing_price_list_accounts_type_0

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
