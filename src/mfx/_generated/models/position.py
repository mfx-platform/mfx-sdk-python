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

from ..models.position_side import PositionSide
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trailing_stop import TrailingStop


T = TypeVar("T", bound="Position")


@_attrs_define
class Position:
    """
    Attributes:
        ticket (int):
        symbol (str):
        side (PositionSide):
        volume (str): Lots
        open_price (str):
        sl (Union[None, str]): Null when none
        tp (Union[None, str]):
        profit (Union[None, str]): Floating, in the account currency; null when only position events are known
        swap (Union[None, str]):
        open_time (datetime.datetime):
        magic (int):
        comment (str):
        price_current (Union[None, Unset, str]): The price the floating profit is computed at; null when only position
            events are known
        commission (Union[None, Unset, str]): In the account currency: the commission the broker charged on the deals of
            this position so far, entry and any partial close (MT5 keeps it on the deals, not the position). Null when the
            broker reports none or the cell has not read the deals yet
        margin (Union[None, Unset, str]): In the account currency: the margin this position holds, as the terminal
            computes it for its volume at its open price (order_calc_margin). Null when the terminal cannot compute it; the
            account's `margin` is the total the broker applies, which hedging rules may make less than the sum
        trailing_stop (Union['TrailingStop', None, Unset]): The position's trailing stop, or null when it has none. The
            moving stop itself is `sl`
    """

    ticket: int
    symbol: str
    side: PositionSide
    volume: str
    open_price: str
    sl: Union[None, str]
    tp: Union[None, str]
    profit: Union[None, str]
    swap: Union[None, str]
    open_time: datetime.datetime
    magic: int
    comment: str
    price_current: Union[None, Unset, str] = UNSET
    commission: Union[None, Unset, str] = UNSET
    margin: Union[None, Unset, str] = UNSET
    trailing_stop: Union["TrailingStop", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trailing_stop import TrailingStop

        ticket = self.ticket

        symbol = self.symbol

        side = self.side.value

        volume = self.volume

        open_price = self.open_price

        sl: Union[None, str]
        sl = self.sl

        tp: Union[None, str]
        tp = self.tp

        profit: Union[None, str]
        profit = self.profit

        swap: Union[None, str]
        swap = self.swap

        open_time = self.open_time.isoformat()

        magic = self.magic

        comment = self.comment

        price_current: Union[None, Unset, str]
        if isinstance(self.price_current, Unset):
            price_current = UNSET
        else:
            price_current = self.price_current

        commission: Union[None, Unset, str]
        if isinstance(self.commission, Unset):
            commission = UNSET
        else:
            commission = self.commission

        margin: Union[None, Unset, str]
        if isinstance(self.margin, Unset):
            margin = UNSET
        else:
            margin = self.margin

        trailing_stop: Union[None, Unset, dict[str, Any]]
        if isinstance(self.trailing_stop, Unset):
            trailing_stop = UNSET
        elif isinstance(self.trailing_stop, TrailingStop):
            trailing_stop = self.trailing_stop.to_dict()
        else:
            trailing_stop = self.trailing_stop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
                "symbol": symbol,
                "side": side,
                "volume": volume,
                "open_price": open_price,
                "sl": sl,
                "tp": tp,
                "profit": profit,
                "swap": swap,
                "open_time": open_time,
                "magic": magic,
                "comment": comment,
            }
        )
        if price_current is not UNSET:
            field_dict["price_current"] = price_current
        if commission is not UNSET:
            field_dict["commission"] = commission
        if margin is not UNSET:
            field_dict["margin"] = margin
        if trailing_stop is not UNSET:
            field_dict["trailing_stop"] = trailing_stop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trailing_stop import TrailingStop

        d = dict(src_dict)
        ticket = d.pop("ticket")

        symbol = d.pop("symbol")

        side = PositionSide(d.pop("side"))

        volume = d.pop("volume")

        open_price = d.pop("open_price")

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

        def _parse_profit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profit = _parse_profit(d.pop("profit"))

        def _parse_swap(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        swap = _parse_swap(d.pop("swap"))

        open_time = isoparse(d.pop("open_time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        def _parse_price_current(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        price_current = _parse_price_current(d.pop("price_current", UNSET))

        def _parse_commission(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        commission = _parse_commission(d.pop("commission", UNSET))

        def _parse_margin(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        margin = _parse_margin(d.pop("margin", UNSET))

        def _parse_trailing_stop(data: object) -> Union["TrailingStop", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                trailing_stop_type_0 = TrailingStop.from_dict(data)

                return trailing_stop_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TrailingStop", None, Unset], data)

        trailing_stop = _parse_trailing_stop(d.pop("trailing_stop", UNSET))

        position = cls(
            ticket=ticket,
            symbol=symbol,
            side=side,
            volume=volume,
            open_price=open_price,
            sl=sl,
            tp=tp,
            profit=profit,
            swap=swap,
            open_time=open_time,
            magic=magic,
            comment=comment,
            price_current=price_current,
            commission=commission,
            margin=margin,
            trailing_stop=trailing_stop,
        )

        position.additional_properties = d
        return position

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
