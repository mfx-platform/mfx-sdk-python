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

T = TypeVar("T", bound="CopyPreviewRequestRowsItem")


@_attrs_define
class CopyPreviewRequestRowsItem:
    """
    Attributes:
        symbol (str):
        volume (str): A decimal as a string, never a JSON number
        price (Union[None, Unset, str]): fixed_risk: the entry; the current price when absent
        sl (Union[None, Unset, str]): fixed_risk: the leader's stop loss
    """

    symbol: str
    volume: str
    price: Union[None, Unset, str] = UNSET
    sl: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        volume = self.volume

        price: Union[None, Unset, str]
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        sl: Union[None, Unset, str]
        if isinstance(self.sl, Unset):
            sl = UNSET
        else:
            sl = self.sl

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "symbol": symbol,
                "volume": volume,
            }
        )
        if price is not UNSET:
            field_dict["price"] = price
        if sl is not UNSET:
            field_dict["sl"] = sl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        volume = d.pop("volume")

        def _parse_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_sl(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sl = _parse_sl(d.pop("sl", UNSET))

        copy_preview_request_rows_item = cls(
            symbol=symbol,
            volume=volume,
            price=price,
            sl=sl,
        )

        return copy_preview_request_rows_item
