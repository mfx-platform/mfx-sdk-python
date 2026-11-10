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

T = TypeVar("T", bound="CommandResultDealsType0Item")


@_attrs_define
class CommandResultDealsType0Item:
    """
    Attributes:
        deal (int):
        order (Union[None, int]):
        position (Union[None, int]):
        volume_units (str): Decimal as a string: the deal's volume in units of the instrument (100,000 for one lot of
            EURUSD at a lot size of 100,000)
        price (str): Decimal as a string: the deal's price
    """

    deal: int
    order: Union[None, int]
    position: Union[None, int]
    volume_units: str
    price: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deal = self.deal

        order: Union[None, int]
        order = self.order

        position: Union[None, int]
        position = self.position

        volume_units = self.volume_units

        price = self.price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deal": deal,
                "order": order,
                "position": position,
                "volume_units": volume_units,
                "price": price,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deal = d.pop("deal")

        def _parse_order(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        order = _parse_order(d.pop("order"))

        def _parse_position(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        position = _parse_position(d.pop("position"))

        volume_units = d.pop("volume_units")

        price = d.pop("price")

        command_result_deals_type_0_item = cls(
            deal=deal,
            order=order,
            position=position,
            volume_units=volume_units,
            price=price,
        )

        command_result_deals_type_0_item.additional_properties = d
        return command_result_deals_type_0_item

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
