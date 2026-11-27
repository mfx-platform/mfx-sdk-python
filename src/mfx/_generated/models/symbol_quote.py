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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.symbol_state import SymbolState
from ..types import UNSET, Unset

T = TypeVar("T", bound="SymbolQuote")


@_attrs_define
class SymbolQuote:
    """
    Attributes:
        symbol (str):
        server_id (UUID):
        account_type (str):
        bid (str): decimal as a string
        ask (str):
        tick_time (datetime.datetime): UTC
        broker_time (str): the tick time on the broker's clock, no offset (MT5 server time), e.g.
            2026-09-17T17:07:10.612
        age_s (float):
        state (SymbolState): Checked in this order, first match wins: unknown (no terminal of the tenant on this server
            is connected, or the newest symbol report from one is older than 180 s by default — could-not-read is never
            reported as closed) → trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) → close_only → long_only /
            short_only → open.
        source_terminal_id (Union[Unset, UUID]): The tenant's terminal whose tick this is: the one named in
            `terminal_id`, else the one the platform chose. For a terminal with MFX Hub HA it is the tenant's terminal,
            never a pair member. Absent on an answer served from the stored tick, which does not record which terminal
            reported it, and on an answer from a platform older than this field.
    """

    symbol: str
    server_id: UUID
    account_type: str
    bid: str
    ask: str
    tick_time: datetime.datetime
    broker_time: str
    age_s: float
    state: SymbolState
    source_terminal_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        server_id = str(self.server_id)

        account_type = self.account_type

        bid = self.bid

        ask = self.ask

        tick_time = self.tick_time.isoformat()

        broker_time = self.broker_time

        age_s = self.age_s

        state = self.state.value

        source_terminal_id: Union[Unset, str] = UNSET
        if not isinstance(self.source_terminal_id, Unset):
            source_terminal_id = str(self.source_terminal_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "server_id": server_id,
                "account_type": account_type,
                "bid": bid,
                "ask": ask,
                "tick_time": tick_time,
                "broker_time": broker_time,
                "age_s": age_s,
                "state": state,
            }
        )
        if source_terminal_id is not UNSET:
            field_dict["source_terminal_id"] = source_terminal_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        server_id = UUID(d.pop("server_id"))

        account_type = d.pop("account_type")

        bid = d.pop("bid")

        ask = d.pop("ask")

        tick_time = isoparse(d.pop("tick_time"))

        broker_time = d.pop("broker_time")

        age_s = d.pop("age_s")

        state = SymbolState._read(d.pop("state"))

        _source_terminal_id = d.pop("source_terminal_id", UNSET)
        source_terminal_id: Union[Unset, UUID]
        if isinstance(_source_terminal_id, Unset):
            source_terminal_id = UNSET
        else:
            source_terminal_id = UUID(_source_terminal_id)

        symbol_quote = cls(
            symbol=symbol,
            server_id=server_id,
            account_type=account_type,
            bid=bid,
            ask=ask,
            tick_time=tick_time,
            broker_time=broker_time,
            age_s=age_s,
            state=state,
            source_terminal_id=source_terminal_id,
        )

        symbol_quote.additional_properties = d
        return symbol_quote

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
