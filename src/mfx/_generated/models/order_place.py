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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.order_place_order_type import OrderPlaceOrderType
from ..models.order_place_side import OrderPlaceSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderPlace")


@_attrs_define
class OrderPlace:
    """Place an order. Refused before it reaches the broker — never rounded or trimmed: a volume off the symbol's step, a
    comment MT5 would truncate, a pending order with no price. Every decimal here is a **string**, exactly as every
    decimal the API returns already is, because a float price is a wrong price in either direction: a computed size is
    the ordinary path for a strategy, and `0.07 * 3` is `0.21000000000000002` as a JSON number. Send what `Decimal`
    gives you. The one thing the platform changes is binary float noise that arrives anyway — a decimal within 1e-6 of a
    multiple of the symbol's own increment, its `volume_step` for a volume or its tick size for a price, is put exactly
    onto that multiple. A value further off than that is what you asked for and is sent unchanged: the platform never
    moves a price you chose. **When the command is SUCCEEDED.** The outcome is the broker's answer to the one
    `order_send`, never a later event. A market order is SUCCEEDED when the broker reports the deal: `mt5_retcode` 10009
    (TRADE_RETCODE_DONE) or 10010 (DONE_PARTIAL); `tickets.order`, `tickets.deal` and `tickets.position` are set and
    `exec_price` and `exec_volume` are the fill (a broker on exchange execution that answers a market order 10008
    instead gives the same SUCCEEDED with `tickets.deal` null). A pending order (limit, stop, stop_limit) is SUCCEEDED
    when the broker accepts it onto its book: `mt5_retcode` 10008 (TRADE_RETCODE_PLACED), `retcode_text` placed. Then
    `tickets.order` is the pending order's ticket - the one to cancel or amend it by - and `tickets.deal` and
    `tickets.position` are null, because nothing has filled; `exec_price` is null, and `exec_volume`, when present, is
    the order's volume as the broker echoed it, not a fill. A placement interrupted and then reconciled from the
    terminal's order history reads the same (10008, `tickets.order` set). **The fill of a pending order is not a command
    outcome**: no second `command.completed` is sent. When the order triggers and fills, it leaves the pending orders
    (`GET /terminals/{id}/orders/pending` and the `pending` of `account.snapshot`), a deal whose `order` is that ticket
    appears in `GET /terminals/{id}/history/deals`, and the position arrives as `position.opened` on `events`
    (`position.modified` when a netting account adds it to a position already open). Match a fill to its order by the
    deal's `order`: MT5 usually gives the position the order's ticket, but not always. An order that lapses at its
    `expires_at` or is cancelled leaves the pending orders with no deal.

        Attributes:
            symbol (str): The broker's own name, e.g. EURUSD.sd
            side (OrderPlaceSide):
            volume (str): Lots, as a decimal string: above zero, inside the symbol's volume_min..volume_max and on its
                volume_step. A string because a computed size is the ordinary path and 0.07 * 3 is 0.21000000000000002 as a JSON
                number. Float noise that does arrive is snapped onto the step; a volume genuinely off it is refused
            order_type (Union[Unset, OrderPlaceOrderType]): A `stop_limit` order waits for the market to reach `price` and
                then places a limit order at `stop_limit_price` Default: OrderPlaceOrderType.MARKET.
            price (Union[Unset, str]): Decimal string above zero. Required for limit, stop and stop_limit (where it is the
                stop price: where the order wakes up); ignored for market (the current bid/ask is used). Float noise is snapped
                onto the symbol's tick; a price deliberately finer than the tick is sent as given, for the broker to accept or
                refuse
            stop_limit_price (Union[Unset, str]): stop_limit only, and required with it: the price of the limit order placed
                when the market reaches `price`. A decimal string above zero. Refused with any other order_type
            sl (Union[Unset, str]): Stop loss price as a decimal string; "0" or absent means none
            tp (Union[Unset, str]): Take profit price as a decimal string; "0" or absent means none
            deviation_points (Union[Unset, int]): Slippage allowed on a market order Default: 20.
            expires_at (Union[Unset, datetime.datetime]): Pending orders only: when the order lapses at the broker if it has
                not filled; absent means good till cancelled. Not the command's own deadline, which is `expires_in_ms`
            expires_in_ms (Union[Unset, int]): How long the command may take to reach the broker, from the moment it is
                accepted: the response's `expires_at` is then that much later. Absent is 10 s, as for every execution command.
                Past it the command is EXPIRED and the order is never sent; it is not how long a pending order stays on the book
                (that is `expires_at`). Outside 1000 to 60000 is refused with 400 validation_error, `details` naming the bounds.
                A replay under the same Idempotency-Key must send the same value (a different one is 409 conflict)
            magic (Union[Unset, int]):  Default: 0.
            comment (Union[Unset, str]): MT5 cuts anything longer without saying so, so longer is refused
    """

    symbol: str
    side: OrderPlaceSide
    volume: str
    order_type: Union[Unset, OrderPlaceOrderType] = OrderPlaceOrderType.MARKET
    price: Union[Unset, str] = UNSET
    stop_limit_price: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    tp: Union[Unset, str] = UNSET
    deviation_points: Union[Unset, int] = 20
    expires_at: Union[Unset, datetime.datetime] = UNSET
    expires_in_ms: Union[Unset, int] = UNSET
    magic: Union[Unset, int] = 0
    comment: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        side = self.side.value

        volume = self.volume

        order_type: Union[Unset, str] = UNSET
        if not isinstance(self.order_type, Unset):
            order_type = self.order_type.value

        price = self.price

        stop_limit_price = self.stop_limit_price

        sl = self.sl

        tp = self.tp

        deviation_points = self.deviation_points

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        expires_in_ms = self.expires_in_ms

        magic = self.magic

        comment = self.comment

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "symbol": symbol,
                "side": side,
                "volume": volume,
            }
        )
        if order_type is not UNSET:
            field_dict["order_type"] = order_type
        if price is not UNSET:
            field_dict["price"] = price
        if stop_limit_price is not UNSET:
            field_dict["stop_limit_price"] = stop_limit_price
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if deviation_points is not UNSET:
            field_dict["deviation_points"] = deviation_points
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if expires_in_ms is not UNSET:
            field_dict["expires_in_ms"] = expires_in_ms
        if magic is not UNSET:
            field_dict["magic"] = magic
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        side = OrderPlaceSide(d.pop("side"))

        volume = d.pop("volume")

        _order_type = d.pop("order_type", UNSET)
        order_type: Union[Unset, OrderPlaceOrderType]
        if isinstance(_order_type, Unset):
            order_type = UNSET
        else:
            order_type = OrderPlaceOrderType(_order_type)

        price = d.pop("price", UNSET)

        stop_limit_price = d.pop("stop_limit_price", UNSET)

        sl = d.pop("sl", UNSET)

        tp = d.pop("tp", UNSET)

        deviation_points = d.pop("deviation_points", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        expires_in_ms = d.pop("expires_in_ms", UNSET)

        magic = d.pop("magic", UNSET)

        comment = d.pop("comment", UNSET)

        order_place = cls(
            symbol=symbol,
            side=side,
            volume=volume,
            order_type=order_type,
            price=price,
            stop_limit_price=stop_limit_price,
            sl=sl,
            tp=tp,
            deviation_points=deviation_points,
            expires_at=expires_at,
            expires_in_ms=expires_in_ms,
            magic=magic,
            comment=comment,
        )

        return order_place
