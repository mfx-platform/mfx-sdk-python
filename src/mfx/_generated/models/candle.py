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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Candle")


@_attrs_define
class Candle:
    """
    Attributes:
        ts (datetime.datetime): Bar open time, UTC
        o (str):
        h (str):
        l (str):
        c (str):
        v (int): Tick volume
    """

    ts: datetime.datetime
    o: str
    h: str
    l: str
    c: str
    v: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ts = self.ts.isoformat()

        o = self.o

        h = self.h

        l = self.l

        c = self.c

        v = self.v

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ts": ts,
                "o": o,
                "h": h,
                "l": l,
                "c": c,
                "v": v,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ts = isoparse(d.pop("ts"))

        o = d.pop("o")

        h = d.pop("h")

        l = d.pop("l")

        c = d.pop("c")

        v = d.pop("v")

        candle = cls(
            ts=ts,
            o=o,
            h=h,
            l=l,
            c=c,
            v=v,
        )

        candle.additional_properties = d
        return candle

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
