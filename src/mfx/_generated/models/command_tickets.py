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

T = TypeVar("T", bound="CommandTickets")


@_attrs_define
class CommandTickets:
    """MT5 relates exactly one order, one deal and one position per fill; a field is null where MT5 has none yet. A
    SUCCEEDED market order_place carries all three; a SUCCEEDED pending order_place (limit, stop, stop_limit) carries
    `order` only, the pending order's ticket, with `deal` and `position` null: the fill comes later and is seen in deals
    and positions, not here (OrderPlace)

        Attributes:
            order (Union[None, int]):
            deal (Union[None, int]):
            position (Union[None, int]):
    """

    order: Union[None, int]
    deal: Union[None, int]
    position: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order: Union[None, int]
        order = self.order

        deal: Union[None, int]
        deal = self.deal

        position: Union[None, int]
        position = self.position

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "order": order,
                "deal": deal,
                "position": position,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_order(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        order = _parse_order(d.pop("order"))

        def _parse_deal(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        deal = _parse_deal(d.pop("deal"))

        def _parse_position(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        position = _parse_position(d.pop("position"))

        command_tickets = cls(
            order=order,
            deal=deal,
            position=position,
        )

        command_tickets.additional_properties = d
        return command_tickets

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
