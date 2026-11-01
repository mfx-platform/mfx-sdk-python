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

from ..models.position_opened_side import PositionOpenedSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionOpened")


@_attrs_define
class PositionOpened:
    """`data` of a `position.opened` message on the `events` channel: sent once when a position opens on the terminal's
    account, by anyone (MFX Hub, an expert advisor, the broker's own apps). The terminal reads its positions and tells
    what changed since it last read them, so a position that opened and closed between two reads is told as
    `position.opened` then `position.closed`. On the stream every value is text, as on every event, and a field with no
    value is left out.

        Example:
            {'schema_version': '1', 'terminal_id': '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101', 'event_id':
                '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101:58190233:open', 'ticket': '58190233', 'symbol': 'EURUSD', 'side': 'buy',
                'volume': '0.10', 'open_price': '1.08412', 'price_current': '1.08420', 'sl': '1.08100', 'tp': '1.09000',
                'profit': '0.80', 'swap': '0.00', 'open_time': '2026-10-23T09:15:02Z', 'magic': '0', 'comment': '', 'ts':
                '2026-10-23T09:15:02Z', 'idempotency_key': 'client-order-0001', 'order_ticket': '58190233'}

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID): The join key: the terminal whose account holds the position
            event_id (str): Deterministic per position: a replay after a cell restart carries the same one and is sent once
            ticket (str): The position's MT5 ticket, an integer as text: the key `position.modified` and `position.closed`
                carry for it
            symbol (str):
            side (PositionOpenedSide):
            volume (str): Lots, a decimal as text
            open_price (str): A decimal as text
            open_time (datetime.datetime): When it opened, UTC
            magic (str): The MT5 magic number, an integer as text; 0 when none
            comment (str): The MT5 comment; empty when none
            ts (datetime.datetime): When it opened, UTC: the same instant as `open_time`
            price_current (Union[Unset, str]): The last price the terminal read for it; absent when not known
            sl (Union[Unset, str]): The stop loss; absent when none
            tp (Union[Unset, str]): The take profit; absent when none
            profit (Union[Unset, str]): The floating profit in the account currency when it was read; absent when not known
            swap (Union[Unset, str]): Absent when not known
            idempotency_key (Union[Unset, str]): The Idempotency-Key of the platform command that opened it (placeOrder):
                the newest such command on this terminal recorded SUCCEEDED naming this position within the last 30 s. Absent
                for a position the platform did not open (an expert advisor, the broker's apps) or whose command outcome was not
                yet recorded
            order_ticket (Union[Unset, str]): The MT5 ticket of the order whose deal opened the position, an integer as
                text: for a position opened by a pending order, that order's ticket, the same order `position_ticket` names on
                its `order.closed`. Absent from a terminal whose agent does not report it yet
    """

    schema_version: str
    terminal_id: UUID
    event_id: str
    ticket: str
    symbol: str
    side: PositionOpenedSide
    volume: str
    open_price: str
    open_time: datetime.datetime
    magic: str
    comment: str
    ts: datetime.datetime
    price_current: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET
    profit: Union[Unset, str] = UNSET
    swap: Union[Unset, str] = UNSET
    idempotency_key: Union[Unset, str] = UNSET
    order_ticket: Union[Unset, str] = UNSET
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

        ts = self.ts.isoformat()

        price_current = self.price_current

        sl = self.sl

        tp = self.tp

        profit = self.profit

        swap = self.swap

        idempotency_key = self.idempotency_key

        order_ticket = self.order_ticket

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
                "ts": ts,
            }
        )
        if price_current is not UNSET:
            field_dict["price_current"] = price_current
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if profit is not UNSET:
            field_dict["profit"] = profit
        if swap is not UNSET:
            field_dict["swap"] = swap
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if order_ticket is not UNSET:
            field_dict["order_ticket"] = order_ticket

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        event_id = d.pop("event_id")

        ticket = d.pop("ticket")

        symbol = d.pop("symbol")

        side = PositionOpenedSide(d.pop("side"))

        volume = d.pop("volume")

        open_price = d.pop("open_price")

        open_time = isoparse(d.pop("open_time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        ts = isoparse(d.pop("ts"))

        price_current = d.pop("price_current", UNSET)

        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        profit = d.pop("profit", UNSET)

        swap = d.pop("swap", UNSET)

        idempotency_key = d.pop("idempotency_key", UNSET)

        order_ticket = d.pop("order_ticket", UNSET)

        position_opened = cls(
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
            ts=ts,
            price_current=price_current,
            sl=sl,
            tp=tp,
            profit=profit,
            swap=swap,
            idempotency_key=idempotency_key,
            order_ticket=order_ticket,
        )

        position_opened.additional_properties = d
        return position_opened

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
