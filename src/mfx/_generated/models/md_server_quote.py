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
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MdServerQuote")


@_attrs_define
class MdServerQuote:
    """One symbol's newest quote in an `md.quotes` message: the symbol, and the fields of that tick as its own channel
    sends them (`MdTickMessage`). `broker_ts` is this symbol's own time on the broker's clock. The message's `sent_at`
    minus `source_sent_at` is the time this quote spent inside the platform, the wait for the interval included.

        Attributes:
            symbol (str): In the broker's own name, as the terminal lists it
            bid (str): decimal as a string
            ask (str): decimal as a string
            broker_ts (str): The tick's time on the broker's clock, to the millisecond, no offset, e.g.
                2026-11-20T08:16:53.187
            last (Union[Unset, str]): The last deal price, decimal as a string; 0.0 where the broker sends none
            volume (Union[Unset, float]): The tick's volume as the terminal reported it
            source_terminal_id (Union[Unset, UUID]): The tenant's terminal that read this tick. For a terminal with MFX Hub
                HA it is the tenant's terminal, never a pair member
            source_sent_at (Union[Unset, str]): When the host of the terminal that read the tick sent it to the platform:
                seconds since 1970 UTC with milliseconds, as text
    """

    symbol: str
    bid: str
    ask: str
    broker_ts: str
    last: Union[Unset, str] = UNSET
    volume: Union[Unset, float] = UNSET
    source_terminal_id: Union[Unset, UUID] = UNSET
    source_sent_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        bid = self.bid

        ask = self.ask

        broker_ts = self.broker_ts

        last = self.last

        volume = self.volume

        source_terminal_id: Union[Unset, str] = UNSET
        if not isinstance(self.source_terminal_id, Unset):
            source_terminal_id = str(self.source_terminal_id)

        source_sent_at = self.source_sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "bid": bid,
                "ask": ask,
                "broker_ts": broker_ts,
            }
        )
        if last is not UNSET:
            field_dict["last"] = last
        if volume is not UNSET:
            field_dict["volume"] = volume
        if source_terminal_id is not UNSET:
            field_dict["source_terminal_id"] = source_terminal_id
        if source_sent_at is not UNSET:
            field_dict["source_sent_at"] = source_sent_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        bid = d.pop("bid")

        ask = d.pop("ask")

        broker_ts = d.pop("broker_ts")

        last = d.pop("last", UNSET)

        volume = d.pop("volume", UNSET)

        _source_terminal_id = d.pop("source_terminal_id", UNSET)
        source_terminal_id: Union[Unset, UUID]
        if isinstance(_source_terminal_id, Unset):
            source_terminal_id = UNSET
        else:
            source_terminal_id = UUID(_source_terminal_id)

        source_sent_at = d.pop("source_sent_at", UNSET)

        md_server_quote = cls(
            symbol=symbol,
            bid=bid,
            ask=ask,
            broker_ts=broker_ts,
            last=last,
            volume=volume,
            source_terminal_id=source_terminal_id,
            source_sent_at=source_sent_at,
        )

        md_server_quote.additional_properties = d
        return md_server_quote

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
