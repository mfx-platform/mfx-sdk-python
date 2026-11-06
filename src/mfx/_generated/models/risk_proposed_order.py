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

from ..models.risk_proposed_order_side import RiskProposedOrderSide
from ..models.risk_proposed_order_type import RiskProposedOrderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskProposedOrder")


@_attrs_define
class RiskProposedOrder:
    """
    Attributes:
        symbol (str):
        side (RiskProposedOrderSide):
        type_ (RiskProposedOrderType):
        volume (str):
        price (Union[None, Unset, str]):
        sl (Union[None, Unset, str]):
        tp (Union[None, Unset, str]):
    """

    symbol: str
    side: RiskProposedOrderSide
    type_: RiskProposedOrderType
    volume: str
    price: Union[None, Unset, str] = UNSET
    sl: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        side = self.side.value

        type_ = self.type_.value

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

        tp: Union[None, Unset, str]
        if isinstance(self.tp, Unset):
            tp = UNSET
        else:
            tp = self.tp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "side": side,
                "type": type_,
                "volume": volume,
            }
        )
        if price is not UNSET:
            field_dict["price"] = price
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        side = RiskProposedOrderSide(d.pop("side"))

        type_ = RiskProposedOrderType(d.pop("type"))

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

        def _parse_tp(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tp = _parse_tp(d.pop("tp", UNSET))

        risk_proposed_order = cls(
            symbol=symbol,
            side=side,
            type_=type_,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
        )

        risk_proposed_order.additional_properties = d
        return risk_proposed_order

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
