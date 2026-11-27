from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_price_list_items_item_plans_additional_property import (
    BillingPriceListItemsItemPlansAdditionalProperty,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingPriceListItemsItemPlans")


@_attrs_define
class BillingPriceListItemsItemPlans:
    """ """

    additional_properties: dict[str, BillingPriceListItemsItemPlansAdditionalProperty] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_price_list_items_item_plans = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = BillingPriceListItemsItemPlansAdditionalProperty._read(prop_dict)

            additional_properties[prop_name] = additional_property

        billing_price_list_items_item_plans.additional_properties = additional_properties
        return billing_price_list_items_item_plans

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> BillingPriceListItemsItemPlansAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: BillingPriceListItemsItemPlansAdditionalProperty
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
