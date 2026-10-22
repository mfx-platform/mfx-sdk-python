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

from ..models.position_closed_close_reason import PositionClosedCloseReason
from ..models.position_closed_side import PositionClosedSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionClosed")


@_attrs_define
class PositionClosed:
    """`data` of a `position.closed` message on the `events` channel: sent once when a position closes, at the broker or by
    anyone. `close_reason` says why in MT5's own `DEAL_REASON` words, the same as `Deal.close_reason`, read from the
    closing deal's code (`deal_reason_raw`); the platform never infers it from a comment. `unknown` when the terminal
    did not find the closing deal, or MT5 gave a code outside its list; the code is then in `deal_reason_raw` where
    there was one. On the stream every value is text, as on every event, and a field with no value is left out.

        Attributes:
            schema_version (str):
            terminal_id (UUID): The join key: the terminal whose position closed
            event_id (str): Deterministic per close: a replay after a cell restart carries the same one and is sent once
            ticket (str): The position's MT5 ticket, an integer as text, as on `position.opened`
            symbol (str):
            side (PositionClosedSide):
            volume (str): Lots
            open_price (str):
            open_time (datetime.datetime):
            magic (str): The MT5 magic number, an integer as text; 0 when none
            comment (str): The MT5 comment; empty when none
            close_reason (PositionClosedCloseReason): MT5 DEAL_REASON of the closing deal: client (desktop), mobile, web,
                expert (a program, MFX included), sl, tp, stop_out, rollover, vmargin, split; unknown when it could not be read
            ts (datetime.datetime): When it closed, UTC: the closing deal's time, or when the cell saw it gone
            sl (Union[None, Unset, str]): The stop loss it closed with; absent when none
            tp (Union[None, Unset, str]): The take profit it closed with; absent when none
            price_current (Union[None, Unset, str]): The last price the cell held for it; absent when not known
            swap (Union[None, Unset, str]): Absent when not known
            close_price (Union[None, Unset, str]): The closing deal's price; absent when the closing deal was not found
            profit (Union[None, Unset, str]): The closing deal's profit in the account currency; absent when the closing
                deal was not found
            deal_reason_raw (Union[Unset, str]): MT5's own DEAL_REASON code of the closing deal, an integer as text; absent
                when the closing deal was not found
            idempotency_key (Union[None, Unset, str]): The Idempotency-Key of the platform command that closed it
                (closePosition or closePositionBy): the newest such command on this terminal whose outcome is recorded
                SUCCEEDED, names this position and was recorded within the last 30 s. Absent for a close nobody asked the
                platform for (sl, tp, stop-out, a person at the terminal), and when the command's outcome was not yet recorded
                when the close was told; `magic` and `comment` here are the position's own
    """

    schema_version: str
    terminal_id: UUID
    event_id: str
    ticket: str
    symbol: str
    side: PositionClosedSide
    volume: str
    open_price: str
    open_time: datetime.datetime
    magic: str
    comment: str
    close_reason: PositionClosedCloseReason
    ts: datetime.datetime
    sl: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    price_current: Union[None, Unset, str] = UNSET
    swap: Union[None, Unset, str] = UNSET
    close_price: Union[None, Unset, str] = UNSET
    profit: Union[None, Unset, str] = UNSET
    deal_reason_raw: Union[Unset, str] = UNSET
    idempotency_key: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        event_id = self.event_id

        ticket = self.ticket

        symbol = self.symbol

        side = self.side.value

        volume = self.volume

        open_price = self.open_price

        open_time = self.open_time.isoformat()

        magic = self.magic

        comment = self.comment

        close_reason = self.close_reason.value

        ts = self.ts.isoformat()

        sl: Union[None, Unset, str]
        if isinstance(self.sl, Unset):
            sl = UNSET
        else:
            sl = self.sl

        tp: Union[None, Unset, str]
        if isinstance(self.tp, Unset):
            tp = UNSET
        else:
            tp = self.tp

        price_current: Union[None, Unset, str]
        if isinstance(self.price_current, Unset):
            price_current = UNSET
        else:
            price_current = self.price_current

        swap: Union[None, Unset, str]
        if isinstance(self.swap, Unset):
            swap = UNSET
        else:
            swap = self.swap

        close_price: Union[None, Unset, str]
        if isinstance(self.close_price, Unset):
            close_price = UNSET
        else:
            close_price = self.close_price

        profit: Union[None, Unset, str]
        if isinstance(self.profit, Unset):
            profit = UNSET
        else:
            profit = self.profit

        deal_reason_raw = self.deal_reason_raw

        idempotency_key: Union[None, Unset, str]
        if isinstance(self.idempotency_key, Unset):
            idempotency_key = UNSET
        else:
            idempotency_key = self.idempotency_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "event_id": event_id,
                "ticket": ticket,
                "symbol": symbol,
                "side": side,
                "volume": volume,
                "open_price": open_price,
                "open_time": open_time,
                "magic": magic,
                "comment": comment,
                "close_reason": close_reason,
                "ts": ts,
            }
        )
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if price_current is not UNSET:
            field_dict["price_current"] = price_current
        if swap is not UNSET:
            field_dict["swap"] = swap
        if close_price is not UNSET:
            field_dict["close_price"] = close_price
        if profit is not UNSET:
            field_dict["profit"] = profit
        if deal_reason_raw is not UNSET:
            field_dict["deal_reason_raw"] = deal_reason_raw
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        event_id = d.pop("event_id")

        ticket = d.pop("ticket")

        symbol = d.pop("symbol")

        side = PositionClosedSide(d.pop("side"))

        volume = d.pop("volume")

        open_price = d.pop("open_price")

        open_time = isoparse(d.pop("open_time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        close_reason = PositionClosedCloseReason(d.pop("close_reason"))

        ts = isoparse(d.pop("ts"))

        def _parse_sl(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sl = _parse_sl(d.pop("sl", UNSET))

        def _parse_tp(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tp = _parse_tp(d.pop("tp", UNSET))

        def _parse_price_current(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        price_current = _parse_price_current(d.pop("price_current", UNSET))

        def _parse_swap(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        swap = _parse_swap(d.pop("swap", UNSET))

        def _parse_close_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        close_price = _parse_close_price(d.pop("close_price", UNSET))

        def _parse_profit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profit = _parse_profit(d.pop("profit", UNSET))

        deal_reason_raw = d.pop("deal_reason_raw", UNSET)

        def _parse_idempotency_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        idempotency_key = _parse_idempotency_key(d.pop("idempotency_key", UNSET))

        position_closed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            event_id=event_id,
            ticket=ticket,
            symbol=symbol,
            side=side,
            volume=volume,
            open_price=open_price,
            open_time=open_time,
            magic=magic,
            comment=comment,
            close_reason=close_reason,
            ts=ts,
            sl=sl,
            tp=tp,
            price_current=price_current,
            swap=swap,
            close_price=close_price,
            profit=profit,
            deal_reason_raw=deal_reason_raw,
            idempotency_key=idempotency_key,
        )

        position_closed.additional_properties = d
        return position_closed

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
