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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.spread import Spread


T = TypeVar("T", bound="SpreadList")


@_attrs_define
class SpreadList:
    """Every instrument this terminal streams, not a page: a terminal carries at most instruments_max (100 Windows, 65
    Linux).

        Attributes:
            terminal_id (UUID):
            items (list['Spread']):
            as_of (datetime.datetime): when the platform last heard from the terminal
    """

    terminal_id: UUID
    items: list["Spread"]
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.spread import Spread

        terminal_id = str(self.terminal_id)

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "items": items,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.spread import Spread

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Spread.from_dict(items_item_data)

            items.append(items_item)

        as_of = isoparse(d.pop("as_of"))

        spread_list = cls(
            terminal_id=terminal_id,
            items=items,
            as_of=as_of,
        )

        spread_list.additional_properties = d
        return spread_list

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
