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

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderModify")


@_attrs_define
class OrderModify:
    """Amend an order that is still pending: a limit or a stop the broker has not filled. Send only what changes; a field
    that is absent keeps the order's present value, so amending the price does not touch its stops. The ticket in the
    path is the order's. An order that is no longer pending - filled, cancelled, expired, or never on this account - is
    refused before the broker with `invalid_request`; a filled order is a position, and its stops are amended with
    modifyPosition. Every decimal is a string and is treated as on OrderPlace: float noise is snapped onto the symbol's
    tick, and a price deliberately finer than the tick is sent as given, for the broker to accept or refuse. The order's
    volume, side, type and symbol cannot be amended: cancel the order and place another.

        Attributes:
            price (Union[Unset, str]): The order's new price, a decimal string above zero. On a stop-limit order it is the
                stop price
            stop_limit_price (Union[Unset, str]): A stop-limit order's second price: the limit order placed when the market
                reaches `price`. On an order that is not a stop-limit it is refused with `invalid_request`
            sl (Union[Unset, str]): Stop loss as a decimal string; "0" clears it
            tp (Union[Unset, str]): Take profit as a decimal string; "0" clears it
            expires_at (Union[None, Unset, datetime.datetime]): When the order lapses if it has not filled. A time sets it;
                null makes the order good till cancelled; absent leaves it as it is. Read on the broker's clock by the terminal,
                as on OrderPlace
    """

    price: Union[Unset, str] = UNSET
    stop_limit_price: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET
    expires_at: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        price = self.price

        stop_limit_price = self.stop_limit_price

        sl = self.sl

        tp = self.tp

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if price is not UNSET:
            field_dict["price"] = price
        if stop_limit_price is not UNSET:
            field_dict["stop_limit_price"] = stop_limit_price
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        price = d.pop("price", UNSET)

        stop_limit_price = d.pop("stop_limit_price", UNSET)

        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        order_modify = cls(
            price=price,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            expires_at=expires_at,
        )

        return order_modify
