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

from ..models.order_modified_order_type import OrderModifiedOrderType
from ..models.order_modified_side import OrderModifiedSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderModified")


@_attrs_define
class OrderModified:
    """`data` of an `order.modified` message on the `events` channel: sent once each time the terminal reads a pending
    order with a different price, stop-limit price, stop loss, take profit, expiry or volume than it last read, set by
    anyone; a partial fill that leaves the rest pending is one. Each message is the order as it now stands, not the
    difference. On the stream every value is text, and a field with no value is left out.

        Example:
            {'schema_version': '1', 'terminal_id': '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101', 'event_id':
                '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101:58190240:order:modify:1.07950:1.07700:1.08600:2026-10-23T21:00:00Z:0.10',
                'ticket': '58190240', 'symbol': 'EURUSD', 'side': 'buy', 'order_type': 'limit', 'volume': '0.10', 'price':
                '1.07950', 'sl': '1.07700', 'tp': '1.08600', 'placed_time': '2026-10-23T09:20:00Z', 'expires_at':
                '2026-10-23T21:00:00Z', 'magic': '0', 'comment': '', 'ts': '2026-10-23T09:31:12Z', 'idempotency_key': 'client-
                modify-0001'}

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID): The join key: the terminal whose account holds the order
            event_id (str): Deterministic per change (the ticket with its new price, stop loss, take profit, expiry and
                volume): a replay after a cell restart carries the same one and is sent once
            ticket (str): The order's MT5 ticket, an integer as text: the key the pending list and the other order events
                carry for it
            symbol (str):
            side (OrderModifiedSide):
            order_type (OrderModifiedOrderType):
            volume (str): Lots still to fill, a decimal as text
            price (str): The order's price, a decimal as text; on a stop-limit order the stop price
            placed_time (datetime.datetime): When it was placed, UTC
            magic (str): The MT5 magic number, an integer as text; 0 when none
            comment (str): The MT5 comment; empty when none
            ts (datetime.datetime): When the terminal saw the change, UTC
            stop_limit_price (Union[Unset, str]): A stop-limit order's second price, the limit placed when the market
                reaches `price`; absent on every other order
            sl (Union[Unset, str]): The stop loss; absent when none
            tp (Union[Unset, str]): The take profit; absent when none
            expires_at (Union[Unset, datetime.datetime]): When it expires, UTC; absent when good till cancelled
            idempotency_key (Union[Unset, str]): The Idempotency-Key of the platform command that changed it (modifyOrder):
                the newest such command on this terminal recorded SUCCEEDED naming this order within the last 30 s. Absent for a
                change the platform did not make
    """

    schema_version: str
    terminal_id: UUID
    event_id: str
    ticket: str
    symbol: str
    side: OrderModifiedSide
    order_type: OrderModifiedOrderType
    volume: str
    price: str
    placed_time: datetime.datetime
    magic: str
    comment: str
    ts: datetime.datetime
    stop_limit_price: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    idempotency_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        event_id = self.event_id

        ticket = self.ticket

        symbol = self.symbol

        side = self.side.value

        order_type = self.order_type.value

        volume = self.volume

        price = self.price

        placed_time = self.placed_time.isoformat()

        magic = self.magic

        comment = self.comment

        ts = self.ts.isoformat()

        stop_limit_price = self.stop_limit_price

        sl = self.sl

        tp = self.tp

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

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
                "order_type": order_type,
                "volume": volume,
                "price": price,
                "placed_time": placed_time,
                "magic": magic,
                "comment": comment,
                "ts": ts,
            }
        )
        if stop_limit_price is not UNSET:
            field_dict["stop_limit_price"] = stop_limit_price
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
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

        side = OrderModifiedSide(d.pop("side"))

        order_type = OrderModifiedOrderType(d.pop("order_type"))

        volume = d.pop("volume")

        price = d.pop("price")

        placed_time = isoparse(d.pop("placed_time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        ts = isoparse(d.pop("ts"))

        stop_limit_price = d.pop("stop_limit_price", UNSET)

        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        idempotency_key = d.pop("idempotency_key", UNSET)

        order_modified = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            event_id=event_id,
            ticket=ticket,
            symbol=symbol,
            side=side,
            order_type=order_type,
            volume=volume,
            price=price,
            placed_time=placed_time,
            magic=magic,
            comment=comment,
            ts=ts,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            expires_at=expires_at,
            idempotency_key=idempotency_key,
        )

        order_modified.additional_properties = d
        return order_modified

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
