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

from ..models.command_state import CommandState
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandResolved")


@_attrs_define
class CommandResolved:
    """`data` of a `command.resolved` message on the `events` channel: sent when an UNKNOWN command reaches its outcome
    (SUCCEEDED, FAILED or REJECTED), beside the `command.completed` or `command.failed` that outcome sends as always.
    Values are text as in CommandOutcome and describe the outcome.

        Attributes:
            schema_version (str):
            command_id (UUID):
            idempotency_key (str):
            terminal_id (UUID): The join key: the terminal the command ran on
            state (CommandState): Final states are SUCCEEDED, FAILED, EXPIRED and REJECTED. UNKNOWN is visible and NOT
                final: the order may have reached the broker and its outcome could not be read (a timeout after send, a lost
                connection). The platform asks the terminal that ran it to read its deal and order history again, every minute,
                until `resolve_by` (15 minutes after it became UNKNOWN by default), and the answer resolves it to SUCCEEDED,
                FAILED or REJECTED. `command.unknown` is sent when it becomes UNKNOWN and `command.resolved` when it is
                resolved. One still UNKNOWN at `resolve_by` stays UNKNOWN, because it may have run, and is resolved by an
                operator with the tenant. A client must not re-send an order whose command is UNKNOWN, because that is how one
                fill becomes two. A NOT_EXECUTED answer from the terminal reads REJECTED with its reason. SUCCEEDED means the
                broker did what the command asked: for a market order, filled; for a pending order (limit, stop, stop_limit),
                accepted onto the broker's book with its ticket in `tickets.order` - not filled (OrderPlace).
            retcode (str): As CommandOutcome.retcode
            reason (str): As CommandOutcome.reason
            tickets (str): CommandTickets as JSON text
            exec_price (str): Decimal as a string; empty when nothing filled
            exec_volume (str): Lots, decimal as a string; empty when nothing filled
            latencies (str): JSON text: {"broker_ms": integer or null, "agent_ms": integer or null}
            terminal_state (str): As CommandOutcome.terminal_state
            unknown_since (datetime.datetime): When the command became UNKNOWN
            magic (Union[Unset, str]): As CommandOutcome.magic
            comment (Union[Unset, str]): As CommandOutcome.comment
    """

    schema_version: str
    command_id: UUID
    idempotency_key: str
    terminal_id: UUID
    state: CommandState
    retcode: str
    reason: str
    tickets: str
    exec_price: str
    exec_volume: str
    latencies: str
    terminal_state: str
    unknown_since: datetime.datetime
    magic: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        command_id = str(self.command_id)

        idempotency_key = self.idempotency_key

        terminal_id = str(self.terminal_id)

        state = self.state.value

        retcode = self.retcode

        reason = self.reason

        tickets = self.tickets

        exec_price = self.exec_price

        exec_volume = self.exec_volume

        latencies = self.latencies

        terminal_state = self.terminal_state

        unknown_since = self.unknown_since.isoformat()

        magic = self.magic

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "command_id": command_id,
                "idempotency_key": idempotency_key,
                "terminal_id": terminal_id,
                "state": state,
                "retcode": retcode,
                "reason": reason,
                "tickets": tickets,
                "exec_price": exec_price,
                "exec_volume": exec_volume,
                "latencies": latencies,
                "terminal_state": terminal_state,
                "unknown_since": unknown_since,
            }
        )
        if magic is not UNSET:
            field_dict["magic"] = magic
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        command_id = UUID(d.pop("command_id"))

        idempotency_key = d.pop("idempotency_key")

        terminal_id = UUID(d.pop("terminal_id"))

        state = CommandState(d.pop("state"))

        retcode = d.pop("retcode")

        reason = d.pop("reason")

        tickets = d.pop("tickets")

        exec_price = d.pop("exec_price")

        exec_volume = d.pop("exec_volume")

        latencies = d.pop("latencies")

        terminal_state = d.pop("terminal_state")

        unknown_since = isoparse(d.pop("unknown_since"))

        magic = d.pop("magic", UNSET)

        comment = d.pop("comment", UNSET)

        command_resolved = cls(
            schema_version=schema_version,
            command_id=command_id,
            idempotency_key=idempotency_key,
            terminal_id=terminal_id,
            state=state,
            retcode=retcode,
            reason=reason,
            tickets=tickets,
            exec_price=exec_price,
            exec_volume=exec_volume,
            latencies=latencies,
            terminal_state=terminal_state,
            unknown_since=unknown_since,
            magic=magic,
            comment=comment,
        )

        command_resolved.additional_properties = d
        return command_resolved

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
