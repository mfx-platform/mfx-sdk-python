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

from ..models.copy_copied_as_side import CopyCopiedAsSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyCopiedAs")


@_attrs_define
class CopyCopiedAs:
    """What the copy became on the follower account

    Attributes:
        symbol (str):
        side (CopyCopiedAsSide):
        volume (str): In the follower venue's unit
        price (Union[None, str]):
    """

    symbol: str
    side: CopyCopiedAsSide
    volume: str
    price: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        side = self.side.value

        volume = self.volume

        price: Union[None, str]
        price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "side": side,
                "volume": volume,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        side = CopyCopiedAsSide(d.pop("side"))

        volume = d.pop("volume")

        def _parse_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        price = _parse_price(d.pop("price"))

        copy_copied_as = cls(
            symbol=symbol,
            side=side,
            volume=volume,
            price=price,
        )

        copy_copied_as.additional_properties = d
        return copy_copied_as

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
