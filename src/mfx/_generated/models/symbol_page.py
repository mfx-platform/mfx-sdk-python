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

from ..models.symbol_page_source import SymbolPageSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.symbol import Symbol


T = TypeVar("T", bound="SymbolPage")


@_attrs_define
class SymbolPage:
    """
    Attributes:
        next_cursor (Union[None, str]): Opaque (created_at, id) cursor for the following page; null on the last page
        items (list['Symbol']):
        source (Union[Unset, SymbolPageSource]): live: a terminal of yours runs on this server and account type.
            last_known: none does any more; the rows are the last your terminals reported, each with its refreshed_at
        returned (Union[Unset, int]): How many items are in THIS page; never a total
    """

    next_cursor: Union[None, str]
    items: list["Symbol"]
    source: Union[Unset, SymbolPageSource] = UNSET
    returned: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.symbol import Symbol

        next_cursor: Union[None, str]
        next_cursor = self.next_cursor

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        returned = self.returned

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "next_cursor": next_cursor,
                "items": items,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if returned is not UNSET:
            field_dict["returned"] = returned

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.symbol import Symbol

        d = dict(src_dict)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Symbol.from_dict(items_item_data)

            items.append(items_item)

        _source = d.pop("source", UNSET)
        source: Union[Unset, SymbolPageSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = SymbolPageSource(_source)

        returned = d.pop("returned", UNSET)

        symbol_page = cls(
            next_cursor=next_cursor,
            items=items,
            source=source,
            returned=returned,
        )

        symbol_page.additional_properties = d
        return symbol_page

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
