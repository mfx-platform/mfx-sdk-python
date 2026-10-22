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

        state = SymbolState(d.pop("state"))

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
