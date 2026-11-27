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

T = TypeVar("T", bound="BillingPriceListTalkToSalesWhenType0")


@_attrs_define
class BillingPriceListTalkToSalesWhenType0:
    """
    Attributes:
        running_accounts_over (Union[Unset, int]):
        estimate_usd_over (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        items (Union[Unset, list[str]]):
    """

    running_accounts_over: Union[Unset, int] = UNSET
    estimate_usd_over: Union[Unset, str] = UNSET
    items: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        running_accounts_over = self.running_accounts_over

        estimate_usd_over = self.estimate_usd_over

        items: Union[Unset, list[str]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if running_accounts_over is not UNSET:
            field_dict["running_accounts_over"] = running_accounts_over
        if estimate_usd_over is not UNSET:
            field_dict["estimate_usd_over"] = estimate_usd_over
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        running_accounts_over = d.pop("running_accounts_over", UNSET)

        estimate_usd_over = d.pop("estimate_usd_over", UNSET)

        items = cast(list[str], d.pop("items", UNSET))

        billing_price_list_talk_to_sales_when_type_0 = cls(
            running_accounts_over=running_accounts_over,
            estimate_usd_over=estimate_usd_over,
            items=items,
        )

        billing_price_list_talk_to_sales_when_type_0.additional_properties = d
        return billing_price_list_talk_to_sales_when_type_0

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
