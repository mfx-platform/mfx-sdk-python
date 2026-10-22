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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pending_order import PendingOrder


T = TypeVar("T", bound="PendingOrderList")


@_attrs_define
class PendingOrderList:
    """
    Attributes:
        as_of (datetime.datetime): When the cell last read the pending orders: on a position change, or every 5 s
        stale (bool): As Account.stale
        items (list['PendingOrder']):
    """

    as_of: datetime.datetime
    stale: bool
    items: list["PendingOrder"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pending_order import PendingOrder

        as_of = self.as_of.isoformat()

        stale = self.stale

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "as_of": as_of,
                "stale": stale,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pending_order import PendingOrder

        d = dict(src_dict)
        as_of = isoparse(d.pop("as_of"))

        stale = d.pop("stale")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = PendingOrder.from_dict(items_item_data)

            items.append(items_item)

        pending_order_list = cls(
            as_of=as_of,
            stale=stale,
            items=items,
        )

        pending_order_list.additional_properties = d
        return pending_order_list

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
