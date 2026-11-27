from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingProfileSummaryCoversSummary")


@_attrs_define
class BillingProfileSummaryCoversSummary:
    """
    Attributes:
        farms (int):
        accounts (int):
    """

    farms: int
    accounts: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        farms = self.farms

        accounts = self.accounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "farms": farms,
                "accounts": accounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        farms = d.pop("farms")

        accounts = d.pop("accounts")

        billing_profile_summary_covers_summary = cls(
            farms=farms,
            accounts=accounts,
        )

        billing_profile_summary_covers_summary.additional_properties = d
        return billing_profile_summary_covers_summary

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
