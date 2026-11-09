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

from ..models.copy_leader_deal_action import CopyLeaderDealAction
from ..models.copy_leader_deal_side import CopyLeaderDealSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyLeaderDeal")


@_attrs_define
class CopyLeaderDeal:
    """The leader's deal a copy came from, in venue-neutral terms

    Attributes:
        action (CopyLeaderDealAction):
        side (CopyLeaderDealSide):
        units (str): The leader's volume in base units
        price (Union[None, str]):
        instrument_key (Union[None, str]):
    """

    action: CopyLeaderDealAction
    side: CopyLeaderDealSide
    units: str
    price: Union[None, str]
    instrument_key: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        side = self.side.value

        units = self.units

        price: Union[None, str]
        price = self.price

        instrument_key: Union[None, str]
        instrument_key = self.instrument_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "side": side,
                "units": units,
                "price": price,
                "instrument_key": instrument_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = CopyLeaderDealAction(d.pop("action"))

        side = CopyLeaderDealSide(d.pop("side"))

        units = d.pop("units")

        def _parse_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        price = _parse_price(d.pop("price"))

        def _parse_instrument_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instrument_key = _parse_instrument_key(d.pop("instrument_key"))

        copy_leader_deal = cls(
            action=action,
            side=side,
            units=units,
            price=price,
            instrument_key=instrument_key,
        )

        copy_leader_deal.additional_properties = d
        return copy_leader_deal

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
