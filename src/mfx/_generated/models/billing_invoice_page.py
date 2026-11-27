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
    from ..models.billing_invoice import BillingInvoice
    from ..models.billing_invoice_page_stats import BillingInvoicePageStats


T = TypeVar("T", bound="BillingInvoicePage")


@_attrs_define
class BillingInvoicePage:
    """
    Attributes:
        items (list['BillingInvoice']):
        next_cursor (Union[None, str]):
        returned (Union[Unset, int]): How many items are in this page; not a total
        stats (Union[Unset, BillingInvoicePageStats]): Totals for the filtered set: the portal's tiles, and available to
            the tenant API on the same filters
    """

    items: list["BillingInvoice"]
    next_cursor: Union[None, str]
    returned: Union[Unset, int] = UNSET
    stats: Union[Unset, "BillingInvoicePageStats"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_invoice import BillingInvoice
        from ..models.billing_invoice_page_stats import BillingInvoicePageStats

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_cursor: Union[None, str]
        next_cursor = self.next_cursor

        returned = self.returned

        stats: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "next_cursor": next_cursor,
            }
        )
        if returned is not UNSET:
            field_dict["returned"] = returned
        if stats is not UNSET:
            field_dict["stats"] = stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_invoice import BillingInvoice
        from ..models.billing_invoice_page_stats import BillingInvoicePageStats

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = BillingInvoice.from_dict(items_item_data)

            items.append(items_item)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        returned = d.pop("returned", UNSET)

        _stats = d.pop("stats", UNSET)
        stats: Union[Unset, BillingInvoicePageStats]
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = BillingInvoicePageStats.from_dict(_stats)

        billing_invoice_page = cls(
            items=items,
            next_cursor=next_cursor,
            returned=returned,
            stats=stats,
        )

        billing_invoice_page.additional_properties = d
        return billing_invoice_page

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
