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

T = TypeVar("T", bound="Tick")


@_attrs_define
class Tick:
    """
    Attributes:
        ts (datetime.datetime): The tick's time, UTC, to the millisecond
        bid (str):
        ask (str):
        last (Union[None, str]): The last deal's price where the broker sends one; null otherwise (most FX)
        volume (Union[None, str]): The last deal's volume where the broker sends one
    """

    ts: datetime.datetime
    bid: str
    ask: str
    last: Union[None, str]
    volume: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ts = self.ts.isoformat()

        bid = self.bid

        ask = self.ask

        last: Union[None, str]
        last = self.last

        volume: Union[None, str]
        volume = self.volume

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ts": ts,
                "bid": bid,
                "ask": ask,
                "last": last,
                "volume": volume,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ts = isoparse(d.pop("ts"))

        bid = d.pop("bid")

        ask = d.pop("ask")

        def _parse_last(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last = _parse_last(d.pop("last"))

        def _parse_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume = _parse_volume(d.pop("volume"))

        tick = cls(
            ts=ts,
            bid=bid,
            ask=ask,
            last=last,
            volume=volume,
        )

        tick.additional_properties = d
        return tick

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
