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

T = TypeVar("T", bound="Spread")


@_attrs_define
class Spread:
    """One instrument's spread as the tenant's own terminal sees it. A shared feed cannot answer this: the spread a user
    trades against is the one their broker gives *their* account, so it is read from their terminal and carries `age_s`
    — a spread is never returned without saying how old it is, because a stale spread reads as a live one and is acted
    on.

        Attributes:
            symbol (str):
            bid (str): decimal as a string
            ask (str):
            spread_points (int): ask − bid in points, as MT5 counts them
            digits (int):
            tick_time (datetime.datetime): UTC
            age_s (float): how old the tick is; a caller decides for itself what is too old
            spread_price (Union[Unset, str]): ask − bid in the quote currency, decimal as a string
            pip_value_per_lot (Union[None, Unset, str]): from the terminal, never derived; null until the terminal has
                reported it
    """

    symbol: str
    bid: str
    ask: str
    spread_points: int
    digits: int
    tick_time: datetime.datetime
    age_s: float
    spread_price: Union[Unset, str] = UNSET
    pip_value_per_lot: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        bid = self.bid

        ask = self.ask

        spread_points = self.spread_points

        digits = self.digits

        tick_time = self.tick_time.isoformat()

        age_s = self.age_s

        spread_price = self.spread_price

        pip_value_per_lot: Union[None, Unset, str]
        if isinstance(self.pip_value_per_lot, Unset):
            pip_value_per_lot = UNSET
        else:
            pip_value_per_lot = self.pip_value_per_lot

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "bid": bid,
                "ask": ask,
                "spread_points": spread_points,
                "digits": digits,
                "tick_time": tick_time,
                "age_s": age_s,
            }
        )
        if spread_price is not UNSET:
            field_dict["spread_price"] = spread_price
        if pip_value_per_lot is not UNSET:
            field_dict["pip_value_per_lot"] = pip_value_per_lot

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        bid = d.pop("bid")

        ask = d.pop("ask")

        spread_points = d.pop("spread_points")

        digits = d.pop("digits")

        tick_time = isoparse(d.pop("tick_time"))

        age_s = d.pop("age_s")

        spread_price = d.pop("spread_price", UNSET)

        def _parse_pip_value_per_lot(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pip_value_per_lot = _parse_pip_value_per_lot(d.pop("pip_value_per_lot", UNSET))

        spread = cls(
            symbol=symbol,
            bid=bid,
            ask=ask,
            spread_points=spread_points,
            digits=digits,
            tick_time=tick_time,
            age_s=age_s,
            spread_price=spread_price,
            pip_value_per_lot=pip_value_per_lot,
        )

        spread.additional_properties = d
        return spread

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
