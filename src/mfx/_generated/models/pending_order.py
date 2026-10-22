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
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.pending_order_order_type import PendingOrderOrderType
from ..models.pending_order_side import PendingOrderSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingOrder")


@_attrs_define
class PendingOrder:
    """
    Attributes:
        ticket (int):
        symbol (str):
        side (PendingOrderSide):
        order_type (PendingOrderOrderType):
        volume (str):
        price (str): On a stop-limit order, the stop price
        sl (Union[None, str]):
        tp (Union[None, str]):
        placed_time (datetime.datetime):
        expires_at (Union[None, datetime.datetime]): Null means good till cancelled
        magic (int):
        comment (str):
        stop_limit_price (Union[None, Unset, str]): A stop-limit order's second price, the limit order placed when the
            market reaches `price`; null on every other order
    """

    ticket: int
    symbol: str
    side: PendingOrderSide
    order_type: PendingOrderOrderType
    volume: str
    price: str
    sl: Union[None, str]
    tp: Union[None, str]
    placed_time: datetime.datetime
    expires_at: Union[None, datetime.datetime]
    magic: int
    comment: str
    stop_limit_price: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket = self.ticket

        symbol = self.symbol

        side = self.side.value

        order_type = self.order_type.value

        volume = self.volume

        price = self.price

        sl: Union[None, str]
        sl = self.sl

        tp: Union[None, str]
        tp = self.tp

        placed_time = self.placed_time.isoformat()

        expires_at: Union[None, str]
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        magic = self.magic

        comment = self.comment

        stop_limit_price: Union[None, Unset, str]
        if isinstance(self.stop_limit_price, Unset):
            stop_limit_price = UNSET
        else:
            stop_limit_price = self.stop_limit_price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
                "symbol": symbol,
                "side": side,
                "order_type": order_type,
                "volume": volume,
                "price": price,
                "sl": sl,
                "tp": tp,
                "placed_time": placed_time,
                "expires_at": expires_at,
                "magic": magic,
                "comment": comment,
            }
        )
        if stop_limit_price is not UNSET:
            field_dict["stop_limit_price"] = stop_limit_price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ticket = d.pop("ticket")

        symbol = d.pop("symbol")

        side = PendingOrderSide(d.pop("side"))

        order_type = PendingOrderOrderType(d.pop("order_type"))

        volume = d.pop("volume")

        price = d.pop("price")

        def _parse_sl(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sl = _parse_sl(d.pop("sl"))

        def _parse_tp(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tp = _parse_tp(d.pop("tp"))

        placed_time = isoparse(d.pop("placed_time"))

        def _parse_expires_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        def _parse_stop_limit_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stop_limit_price = _parse_stop_limit_price(d.pop("stop_limit_price", UNSET))

        pending_order = cls(
            ticket=ticket,
            symbol=symbol,
            side=side,
            order_type=order_type,
            volume=volume,
            price=price,
            sl=sl,
            tp=tp,
            placed_time=placed_time,
            expires_at=expires_at,
            magic=magic,
            comment=comment,
            stop_limit_price=stop_limit_price,
        )

        pending_order.additional_properties = d
        return pending_order

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
