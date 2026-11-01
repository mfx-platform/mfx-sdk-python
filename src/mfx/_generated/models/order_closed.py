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

from ..models.order_closed_order_type import OrderClosedOrderType
from ..models.order_closed_reason import OrderClosedReason
from ..models.order_closed_side import OrderClosedSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderClosed")


@_attrs_define
class OrderClosed:
    """`data` of an `order.closed` message on the `events` channel: sent once when a pending order leaves the account's
    pending list, for whatever reason. `reason` is the order's own state in the terminal's order history (MT5
    `ORDER_STATE`): `filled`, `cancelled`, `expired`, `rejected`; `unknown` when the terminal did not find it in its
    history within 60 s, or MT5 gave a state outside that list. The platform never infers it from the expiry or from a
    nearby position. A fill carries `position_ticket`, the position it opened or, on a netting account, went into;
    `position.opened` carries the same order's ticket as `order_ticket`. The order as it stood when it left. On the
    stream every value is text, and a field with no value is left out.

        Example:
            {'schema_version': '1', 'terminal_id': '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101', 'event_id':
                '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101:58190240:order:closed', 'ticket': '58190240', 'symbol': 'EURUSD', 'side':
                'buy', 'order_type': 'limit', 'volume': '0.10', 'price': '1.07950', 'sl': '1.07700', 'tp': '1.08600',
                'placed_time': '2026-10-23T09:20:00Z', 'expires_at': '2026-10-23T21:00:00Z', 'magic': '0', 'comment': '',
                'reason': 'filled', 'order_state_raw': '4', 'position_ticket': '58190240', 'ts': '2026-10-23T10:02:47Z'}

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID): The join key: the terminal whose account holds the order
            event_id (str): Deterministic per order: a replay after a cell restart carries the same one and is sent once
            ticket (str): The order's MT5 ticket, an integer as text: the key the pending list and the other order events
                carry for it
            symbol (str):
            side (OrderClosedSide):
            order_type (OrderClosedOrderType):
            volume (str): Lots still to fill, a decimal as text
            price (str): The order's price, a decimal as text; on a stop-limit order the stop price
            placed_time (datetime.datetime): When it was placed, UTC
            magic (str): The MT5 magic number, an integer as text; 0 when none
            comment (str): The MT5 comment; empty when none
            reason (OrderClosedReason): Why it left the pending list: MT5 ORDER_STATE in plain words; unknown when it could
                not be read
            ts (datetime.datetime): When it left, UTC: the order's time done in the history, or when the terminal saw it
                gone
            stop_limit_price (Union[Unset, str]): A stop-limit order's second price, the limit placed when the market
                reaches `price`; absent on every other order
            sl (Union[Unset, str]): The stop loss; absent when none
            tp (Union[Unset, str]): The take profit; absent when none
            expires_at (Union[Unset, datetime.datetime]): When it expires, UTC; absent when good till cancelled
            order_state_raw (Union[Unset, str]): MT5's own ORDER_STATE code, an integer as text; absent when the order was
                not found in the history
            position_ticket (Union[Unset, str]): On a fill, the MT5 ticket of the position it opened or went into, an
                integer as text; absent otherwise
            idempotency_key (Union[Unset, str]): On a cancel, the Idempotency-Key of the platform command that cancelled it
                (cancelOrder): the newest such command on this terminal recorded SUCCEEDED naming this order within the last 30
                s. Absent on a fill, an expiry or a rejection, and on a cancel the platform did not make
    """

    schema_version: str
    terminal_id: UUID
    event_id: str
    ticket: str
    symbol: str
    side: OrderClosedSide
    order_type: OrderClosedOrderType
    volume: str
    price: str
    placed_time: datetime.datetime
    magic: str
    comment: str
    reason: OrderClosedReason
    ts: datetime.datetime
    stop_limit_price: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    order_state_raw: Union[Unset, str] = UNSET
    position_ticket: Union[Unset, str] = UNSET
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

        reason = self.reason.value

        ts = self.ts.isoformat()

        stop_limit_price = self.stop_limit_price

        sl = self.sl

        tp = self.tp

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        order_state_raw = self.order_state_raw

        position_ticket = self.position_ticket

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
                "reason": reason,
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
        if order_state_raw is not UNSET:
            field_dict["order_state_raw"] = order_state_raw
        if position_ticket is not UNSET:
            field_dict["position_ticket"] = position_ticket
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

        side = OrderClosedSide(d.pop("side"))

        order_type = OrderClosedOrderType(d.pop("order_type"))

        volume = d.pop("volume")

        price = d.pop("price")

        placed_time = isoparse(d.pop("placed_time"))

        magic = d.pop("magic")

        comment = d.pop("comment")

        reason = OrderClosedReason(d.pop("reason"))

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

        order_state_raw = d.pop("order_state_raw", UNSET)

        position_ticket = d.pop("position_ticket", UNSET)

        idempotency_key = d.pop("idempotency_key", UNSET)

        order_closed = cls(
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
            reason=reason,
            ts=ts,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            expires_at=expires_at,
            order_state_raw=order_state_raw,
            position_ticket=position_ticket,
            idempotency_key=idempotency_key,
        )

        order_closed.additional_properties = d
        return order_closed

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
