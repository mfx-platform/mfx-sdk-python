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

from ..models.command_result_venue import CommandResultVenue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_result_deals_type_0_item import CommandResultDealsType0Item
    from ..models.command_tickets import CommandTickets


T = TypeVar("T", bound="CommandResult")


@_attrs_define
class CommandResult:
    """What happened at the broker, once the command has an outcome. `retryable` is set on every reason, so an SDK decides
    from the result and not from a table that can drift. It is written once, from the broker's answer to the command:
    for a pending order_place that is the placement (`mt5_retcode` 10008, `tickets.order` set, no deal, no
    `exec_price`), and the later fill never rewrites it (OrderPlace says where the fill is seen).

        Attributes:
            ok (bool):
            reason (Union[None, str]): Granular reason; null when ok. Every reason, with whether it is retryable, its
                typical cause and what to do, is in the error catalogue at the root of this document
            retryable (bool): Whether sending the same order again, under a NEW Idempotency-Key, can succeed. Always false
                while the state is UNKNOWN
            tickets (CommandTickets): MT5 relates exactly one order, one deal and one position per fill; a field is null
                where MT5 has none yet. A SUCCEEDED market order_place carries all three; a SUCCEEDED pending order_place
                (limit, stop, stop_limit) carries `order` only, the pending order's ticket, with `deal` and `position` null: the
                fill comes later and is seen in deals and positions, not here (OrderPlace)
            attempts (int):
            mt5_retcode (Union[None, Unset, int]): MT5 TRADE_RETCODE_*; null when the command never reached the terminal
            retcode_text (Union[None, Unset, str]):
            comment_raw (Union[None, Unset, str]): The broker's own comment, verbatim
            terminal_state (Union[None, Unset, str]): The terminal's lifecycle state when the outcome was recorded: when the
                cell's result arrived, or when the platform expired the command; null only when the terminal no longer exists
            exec_price (Union[None, Unset, str]): Decimal as a string: the fill price of a market order or close; on an
                amended pending order, its new price; null for a pending order's placement
            exec_volume (Union[None, Unset, str]): Lots, decimal as a string: the filled volume of a market order or close;
                on a pending order's placement, the order's volume as the broker echoed it, or null - never a fill
            broker_latency_ms (Union[None, Unset, int]):
            agent_latency_ms (Union[None, Unset, int]):
            rerouted_from (Union[None, UUID, Unset]): The terminal the command was first sent to, when a failover moved it
            idempotency_key (Union[Unset, str]): The Idempotency-Key the command was sent with, so an outcome is joined to
                its intent without a lookup. Always served
            magic (Union[None, Unset, int]): The magic number the command sent to the broker: the one asked for on
                OrderPlace, 0 when none was. Null for a command that carries none (a close keeps the position's own magic, which
                the platform does not hold), and for a command that is not an order. Always served
            comment (Union[None, Unset, str]): The comment the command sent to the broker: the one asked for on OrderPlace,
                PositionClose or PositionClosePartial, empty for an order placed without one. Null when the command carried none
                (a close without a comment, on which the closing deal takes the position's own). Always served
            venue (Union[Unset, CommandResultVenue]): The venue that answered: the runner's. A result from an MT5 cell is
                mt5
            venue_code (Union[None, Unset, str]): The venue's own code for a refusal, verbatim, beside the classified
                `reason` (cTrader: its error code, such as NOT_ENOUGH_MONEY). Null on MT5, whose code is `mt5_retcode`, and when
                the venue gave none
            deals (Union[None, Unset, list['CommandResultDealsType0Item']]): Every deal the command made, in the order they
                were made: two for an emulated close-by (`close_by_emulated`), one for an order filled at once. Null on MT5,
                where `tickets.deal` is the one deal of the fill
            volume_units (Union[None, Unset, str]): Decimal as a string: the volume the command filled, in units of the
                instrument (the sum of `deals`). `exec_volume` stays in lots. Null on MT5 and when nothing filled
            close_by_emulated (Union[Unset, bool]): True for a close-by the venue has no equivalent for, done as two closes
                (cTrader); false otherwise
            protection_not_set (Union[Unset, bool]): True when a market order filled but its stop loss or take profit could
                not be set on the new position (cTrader sets them after the fill): the position is open without them. False
                otherwise
    """

    ok: bool
    reason: Union[None, str]
    retryable: bool
    tickets: "CommandTickets"
    attempts: int
    mt5_retcode: Union[None, Unset, int] = UNSET
    retcode_text: Union[None, Unset, str] = UNSET
    comment_raw: Union[None, Unset, str] = UNSET
    terminal_state: Union[None, Unset, str] = UNSET
    exec_price: Union[None, Unset, str] = UNSET
    exec_volume: Union[None, Unset, str] = UNSET
    broker_latency_ms: Union[None, Unset, int] = UNSET
    agent_latency_ms: Union[None, Unset, int] = UNSET
    rerouted_from: Union[None, UUID, Unset] = UNSET
    idempotency_key: Union[Unset, str] = UNSET
    magic: Union[None, Unset, int] = UNSET
    comment: Union[None, Unset, str] = UNSET
    venue: Union[Unset, CommandResultVenue] = UNSET
    venue_code: Union[None, Unset, str] = UNSET
    deals: Union[None, Unset, list["CommandResultDealsType0Item"]] = UNSET
    volume_units: Union[None, Unset, str] = UNSET
    close_by_emulated: Union[Unset, bool] = UNSET
    protection_not_set: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.command_result_deals_type_0_item import (
            CommandResultDealsType0Item,
        )
        from ..models.command_tickets import CommandTickets

        ok = self.ok

        reason: Union[None, str]
        reason = self.reason

        retryable = self.retryable

        tickets = self.tickets.to_dict()

        attempts = self.attempts

        mt5_retcode: Union[None, Unset, int]
        if isinstance(self.mt5_retcode, Unset):
            mt5_retcode = UNSET
        else:
            mt5_retcode = self.mt5_retcode

        retcode_text: Union[None, Unset, str]
        if isinstance(self.retcode_text, Unset):
            retcode_text = UNSET
        else:
            retcode_text = self.retcode_text

        comment_raw: Union[None, Unset, str]
        if isinstance(self.comment_raw, Unset):
            comment_raw = UNSET
        else:
            comment_raw = self.comment_raw

        terminal_state: Union[None, Unset, str]
        if isinstance(self.terminal_state, Unset):
            terminal_state = UNSET
        else:
            terminal_state = self.terminal_state

        exec_price: Union[None, Unset, str]
        if isinstance(self.exec_price, Unset):
            exec_price = UNSET
        else:
            exec_price = self.exec_price

        exec_volume: Union[None, Unset, str]
        if isinstance(self.exec_volume, Unset):
            exec_volume = UNSET
        else:
            exec_volume = self.exec_volume

        broker_latency_ms: Union[None, Unset, int]
        if isinstance(self.broker_latency_ms, Unset):
            broker_latency_ms = UNSET
        else:
            broker_latency_ms = self.broker_latency_ms

        agent_latency_ms: Union[None, Unset, int]
        if isinstance(self.agent_latency_ms, Unset):
            agent_latency_ms = UNSET
        else:
            agent_latency_ms = self.agent_latency_ms

        rerouted_from: Union[None, Unset, str]
        if isinstance(self.rerouted_from, Unset):
            rerouted_from = UNSET
        elif isinstance(self.rerouted_from, UUID):
            rerouted_from = str(self.rerouted_from)
        else:
            rerouted_from = self.rerouted_from

        idempotency_key = self.idempotency_key

        magic: Union[None, Unset, int]
        if isinstance(self.magic, Unset):
            magic = UNSET
        else:
            magic = self.magic

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        venue: Union[Unset, str] = UNSET
        if not isinstance(self.venue, Unset):
            venue = self.venue.value

        venue_code: Union[None, Unset, str]
        if isinstance(self.venue_code, Unset):
            venue_code = UNSET
        else:
            venue_code = self.venue_code

        deals: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.deals, Unset):
            deals = UNSET
        elif isinstance(self.deals, list):
            deals = []
            for deals_type_0_item_data in self.deals:
                deals_type_0_item = deals_type_0_item_data.to_dict()
                deals.append(deals_type_0_item)

        else:
            deals = self.deals

        volume_units: Union[None, Unset, str]
        if isinstance(self.volume_units, Unset):
            volume_units = UNSET
        else:
            volume_units = self.volume_units

        close_by_emulated = self.close_by_emulated

        protection_not_set = self.protection_not_set

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "reason": reason,
                "retryable": retryable,
                "tickets": tickets,
                "attempts": attempts,
            }
        )
        if mt5_retcode is not UNSET:
            field_dict["mt5_retcode"] = mt5_retcode
        if retcode_text is not UNSET:
            field_dict["retcode_text"] = retcode_text
        if comment_raw is not UNSET:
            field_dict["comment_raw"] = comment_raw
        if terminal_state is not UNSET:
            field_dict["terminal_state"] = terminal_state
        if exec_price is not UNSET:
            field_dict["exec_price"] = exec_price
        if exec_volume is not UNSET:
            field_dict["exec_volume"] = exec_volume
        if broker_latency_ms is not UNSET:
            field_dict["broker_latency_ms"] = broker_latency_ms
        if agent_latency_ms is not UNSET:
            field_dict["agent_latency_ms"] = agent_latency_ms
        if rerouted_from is not UNSET:
            field_dict["rerouted_from"] = rerouted_from
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if magic is not UNSET:
            field_dict["magic"] = magic
        if comment is not UNSET:
            field_dict["comment"] = comment
        if venue is not UNSET:
            field_dict["venue"] = venue
        if venue_code is not UNSET:
            field_dict["venue_code"] = venue_code
        if deals is not UNSET:
            field_dict["deals"] = deals
        if volume_units is not UNSET:
            field_dict["volume_units"] = volume_units
        if close_by_emulated is not UNSET:
            field_dict["close_by_emulated"] = close_by_emulated
        if protection_not_set is not UNSET:
            field_dict["protection_not_set"] = protection_not_set

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.command_result_deals_type_0_item import (
            CommandResultDealsType0Item,
        )
        from ..models.command_tickets import CommandTickets

        d = dict(src_dict)
        ok = d.pop("ok")

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        retryable = d.pop("retryable")

        tickets = CommandTickets.from_dict(d.pop("tickets"))

        attempts = d.pop("attempts")

        def _parse_mt5_retcode(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        mt5_retcode = _parse_mt5_retcode(d.pop("mt5_retcode", UNSET))

        def _parse_retcode_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        retcode_text = _parse_retcode_text(d.pop("retcode_text", UNSET))

        def _parse_comment_raw(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment_raw = _parse_comment_raw(d.pop("comment_raw", UNSET))

        def _parse_terminal_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        terminal_state = _parse_terminal_state(d.pop("terminal_state", UNSET))

        def _parse_exec_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        exec_price = _parse_exec_price(d.pop("exec_price", UNSET))

        def _parse_exec_volume(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        exec_volume = _parse_exec_volume(d.pop("exec_volume", UNSET))

        def _parse_broker_latency_ms(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        broker_latency_ms = _parse_broker_latency_ms(d.pop("broker_latency_ms", UNSET))

        def _parse_agent_latency_ms(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        agent_latency_ms = _parse_agent_latency_ms(d.pop("agent_latency_ms", UNSET))

        def _parse_rerouted_from(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rerouted_from_type_0 = UUID(data)

                return rerouted_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        rerouted_from = _parse_rerouted_from(d.pop("rerouted_from", UNSET))

        idempotency_key = d.pop("idempotency_key", UNSET)

        def _parse_magic(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        magic = _parse_magic(d.pop("magic", UNSET))

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        _venue = d.pop("venue", UNSET)
        venue: Union[Unset, CommandResultVenue]
        if isinstance(_venue, Unset):
            venue = UNSET
        else:
            venue = CommandResultVenue(_venue)

        def _parse_venue_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        venue_code = _parse_venue_code(d.pop("venue_code", UNSET))

        def _parse_deals(data: object) -> Union[None, Unset, list["CommandResultDealsType0Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                deals_type_0 = []
                _deals_type_0 = data
                for deals_type_0_item_data in _deals_type_0:
                    deals_type_0_item = CommandResultDealsType0Item.from_dict(
                        deals_type_0_item_data
                    )

                    deals_type_0.append(deals_type_0_item)

                return deals_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CommandResultDealsType0Item"]], data)

        deals = _parse_deals(d.pop("deals", UNSET))

        def _parse_volume_units(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        volume_units = _parse_volume_units(d.pop("volume_units", UNSET))

        close_by_emulated = d.pop("close_by_emulated", UNSET)

        protection_not_set = d.pop("protection_not_set", UNSET)

        command_result = cls(
            ok=ok,
            reason=reason,
            retryable=retryable,
            tickets=tickets,
            attempts=attempts,
            mt5_retcode=mt5_retcode,
            retcode_text=retcode_text,
            comment_raw=comment_raw,
            terminal_state=terminal_state,
            exec_price=exec_price,
            exec_volume=exec_volume,
            broker_latency_ms=broker_latency_ms,
            agent_latency_ms=agent_latency_ms,
            rerouted_from=rerouted_from,
            idempotency_key=idempotency_key,
            magic=magic,
            comment=comment,
            venue=venue,
            venue_code=venue_code,
            deals=deals,
            volume_units=volume_units,
            close_by_emulated=close_by_emulated,
            protection_not_set=protection_not_set,
        )

        command_result.additional_properties = d
        return command_result

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
