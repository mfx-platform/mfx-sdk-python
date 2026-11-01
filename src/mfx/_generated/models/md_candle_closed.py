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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.md_candle_closed_timeframe import MdCandleClosedTimeframe
from ..types import UNSET, Unset

T = TypeVar("T", bound="MdCandleClosed")


@_attrs_define
class MdCandleClosed:
    """md.candle_closed on candles:{server_id}:{symbol}:{tf}: a closed bar, once, read by one of your own terminals. Never
    replayed; prev_ts tells you whether you missed one

        Attributes:
            schema_version (str):  Example: 1.
            server_id (UUID):
            symbol (str): The broker's own name
            timeframe (MdCandleClosedTimeframe):
            ts (datetime.datetime): Bar open time, UTC; a D1 bar opens at the broker's midnight
            o (str):
            h (str):
            l (str):
            c (str):
            v (int): Tick volume
            prev_ts (datetime.datetime): Open time of the bar before this one in the terminal's history. Not the ts of the
                last bar you hold: you missed bars; read GET /v1/md/candles from your last ts
    """

    schema_version: str
    server_id: UUID
    symbol: str
    timeframe: MdCandleClosedTimeframe
    ts: datetime.datetime
    o: str
    h: str
    l: str
    c: str
    v: int
    prev_ts: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        server_id = str(self.server_id)

        symbol = self.symbol

        timeframe = self.timeframe.value

        ts = self.ts.isoformat()

        o = self.o

        h = self.h

        l = self.l

        c = self.c

        v = self.v

        prev_ts = self.prev_ts.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "server_id": server_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "ts": ts,
                "o": o,
                "h": h,
                "l": l,
                "c": c,
                "v": v,
                "prev_ts": prev_ts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        server_id = UUID(d.pop("server_id"))

        symbol = d.pop("symbol")

        timeframe = MdCandleClosedTimeframe(d.pop("timeframe"))

        ts = isoparse(d.pop("ts"))

        o = d.pop("o")

        h = d.pop("h")

        l = d.pop("l")

        c = d.pop("c")

        v = d.pop("v")

        prev_ts = isoparse(d.pop("prev_ts"))

        md_candle_closed = cls(
            schema_version=schema_version,
            server_id=server_id,
            symbol=symbol,
            timeframe=timeframe,
            ts=ts,
            o=o,
            h=h,
            l=l,
            c=c,
            v=v,
            prev_ts=prev_ts,
        )

        md_candle_closed.additional_properties = d
        return md_candle_closed

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
