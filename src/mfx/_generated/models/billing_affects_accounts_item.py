from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_affects_accounts_item_venue import BillingAffectsAccountsItemVenue
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingAffectsAccountsItem")


@_attrs_define
class BillingAffectsAccountsItem:
    """
    Attributes:
        id (UUID):
        name (str):
        venue (BillingAffectsAccountsItemVenue):
    """

    id: UUID
    name: str
    venue: BillingAffectsAccountsItemVenue
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        venue = self.venue.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "venue": venue,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        venue = BillingAffectsAccountsItemVenue._read(d.pop("venue"))

        billing_affects_accounts_item = cls(
            id=id,
            name=name,
            venue=venue,
        )

        billing_affects_accounts_item.additional_properties = d
        return billing_affects_accounts_item

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
