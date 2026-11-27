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

T = TypeVar("T", bound="MdTickMessage")


@_attrs_define
class MdTickMessage:
    """`data` of a tick on `md:{server_id}:{symbol}` (a msg with no `type`): one quote as one of the tenant's own terminals
    read it. Every terminal of the tenant on that server that lists the symbol feeds the channel, and a tick is sent
    once, when its broker time is newer than the newest already sent; `source_terminal_id` says which terminal brought
    it. Ticks published together are sent with the same `seq`; they are usually one terminal's one read, and can be
    several terminals' when the stream was held to its rate, so read `source_terminal_id` and `source_sent_at` on each
    tick. The four times are in order: the tick's own (`broker_ts`, on the broker's clock), `source_sent_at`,
    `fanned_at`, `sent_at`; the last three are on the platform's clock, so `sent_at` minus `source_sent_at` is the time
    the tick spent inside the platform after the terminal's host sent it, with no clock of the client's in it. Ticks are
    never replayed.

        Attributes:
            bid (str): decimal as a string
            ask (str): decimal as a string
            broker_ts (str): The tick's time on the broker's clock, to the millisecond, no offset, e.g.
                2026-11-20T08:16:53.187
            last (Union[Unset, str]): The last deal price, decimal as a string; 0.0 where the broker sends none
            volume (Union[Unset, float]): The tick's volume as the terminal reported it
            fanned_at (Union[Unset, str]): When the platform published the tick to the tenant's stream: seconds since 1970
                UTC with milliseconds, as text, e.g. 1795155413.660
            source_terminal_id (Union[Unset, UUID]): The tenant's terminal that read this tick. For a terminal with MFX Hub
                HA it is the tenant's terminal, never a pair member. Absent on a cTrader account's channel
                (`md:{account_id}:{symbol}`), where no terminal of the tenant's reads the price, and wherever the platform does
                not know it; never sent empty
            source_sent_at (Union[Unset, str]): When the host of the terminal that read the tick sent it to the platform, in
                the form of `fanned_at`
            sent_at (Union[Unset, str]): When the gateway put the message on this connection, in the form of `fanned_at`
    """

    bid: str
    ask: str
    broker_ts: str
    last: Union[Unset, str] = UNSET
    volume: Union[Unset, float] = UNSET
    fanned_at: Union[Unset, str] = UNSET
    source_terminal_id: Union[Unset, UUID] = UNSET
    source_sent_at: Union[Unset, str] = UNSET
    sent_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bid = self.bid

        ask = self.ask

        broker_ts = self.broker_ts

        last = self.last

        volume = self.volume

        fanned_at = self.fanned_at

        source_terminal_id: Union[Unset, str] = UNSET
        if not isinstance(self.source_terminal_id, Unset):
            source_terminal_id = str(self.source_terminal_id)

        source_sent_at = self.source_sent_at

        sent_at = self.sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bid": bid,
                "ask": ask,
                "broker_ts": broker_ts,
            }
        )
        if last is not UNSET:
            field_dict["last"] = last
        if volume is not UNSET:
            field_dict["volume"] = volume
        if fanned_at is not UNSET:
            field_dict["fanned_at"] = fanned_at
        if source_terminal_id is not UNSET:
            field_dict["source_terminal_id"] = source_terminal_id
        if source_sent_at is not UNSET:
            field_dict["source_sent_at"] = source_sent_at
        if sent_at is not UNSET:
            field_dict["sent_at"] = sent_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bid = d.pop("bid")

        ask = d.pop("ask")

        broker_ts = d.pop("broker_ts")

        last = d.pop("last", UNSET)

        volume = d.pop("volume", UNSET)

        fanned_at = d.pop("fanned_at", UNSET)

        _source_terminal_id = d.pop("source_terminal_id", UNSET)
        source_terminal_id: Union[Unset, UUID]
        if isinstance(_source_terminal_id, Unset):
            source_terminal_id = UNSET
        else:
            source_terminal_id = UUID(_source_terminal_id)

        source_sent_at = d.pop("source_sent_at", UNSET)

        sent_at = d.pop("sent_at", UNSET)

        md_tick_message = cls(
            bid=bid,
            ask=ask,
            broker_ts=broker_ts,
            last=last,
            volume=volume,
            fanned_at=fanned_at,
            source_terminal_id=source_terminal_id,
            source_sent_at=source_sent_at,
            sent_at=sent_at,
        )

        md_tick_message.additional_properties = d
        return md_tick_message

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
