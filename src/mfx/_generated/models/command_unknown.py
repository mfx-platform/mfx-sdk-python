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

T = TypeVar("T", bound="CommandUnknown")


@_attrs_define
class CommandUnknown:
    """`data` of a `command.unknown` message on the `events` channel: sent when a command becomes UNKNOWN, from any state.
    Its outcome could not be read and it may have reached the broker, so it must not be sent again. The platform asks
    the terminal that ran it to read the outcome again until `resolve_by`; `command.resolved` follows when it is
    resolved. Values are text as in CommandOutcome; `state` is UNKNOWN.

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
            resolve_by (datetime.datetime): Until when the platform asks the terminal again (the moment it became UNKNOWN
                plus the resolve window, 15 minutes by default). Still UNKNOWN after it, an operator resolves it with the
                tenant, and a later answer still sends command.resolved
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
    resolve_by: datetime.datetime
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

        resolve_by = self.resolve_by.isoformat()

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
                "resolve_by": resolve_by,
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

        resolve_by = isoparse(d.pop("resolve_by"))

        magic = d.pop("magic", UNSET)

        comment = d.pop("comment", UNSET)

        command_unknown = cls(
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
            resolve_by=resolve_by,
            magic=magic,
            comment=comment,
        )

        command_unknown.additional_properties = d
        return command_unknown

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
