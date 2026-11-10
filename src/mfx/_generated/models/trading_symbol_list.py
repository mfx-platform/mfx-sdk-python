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
    from ..models.trading_symbol import TradingSymbol


T = TypeVar("T", bound="TradingSymbolList")


@_attrs_define
class TradingSymbolList:
    """
    Attributes:
        account_id (UUID):
        as_of (datetime.datetime): When the platform read the list from Spotware
        items (list['TradingSymbol']):
    """

    account_id: UUID
    as_of: datetime.datetime
    items: list["TradingSymbol"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trading_symbol import TradingSymbol

        account_id = str(self.account_id)

        as_of = self.as_of.isoformat()

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "as_of": as_of,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trading_symbol import TradingSymbol

        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        as_of = isoparse(d.pop("as_of"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = TradingSymbol.from_dict(items_item_data)

            items.append(items_item)

        trading_symbol_list = cls(
            account_id=account_id,
            as_of=as_of,
            items=items,
        )

        trading_symbol_list.additional_properties = d
        return trading_symbol_list

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
