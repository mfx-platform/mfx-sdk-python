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
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.command_state import CommandState
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandOutcome")


@_attrs_define
class CommandOutcome:
    """`data` of a `command.completed` or `command.failed` message on the `events` channel and on `results:{terminal_id}`:
    sent once when a command reaches an outcome, `command.completed` for SUCCEEDED and `command.failed` for every other
    end (FAILED, EXPIRED, REJECTED). It carries what `GET /commands/{id}` serves as `result`. On the stream every value
    is text, `tickets` and `latencies` are JSON objects as text, and a value that does not exist is empty.

        Attributes:
            schema_version (str):
            command_id (UUID):
            idempotency_key (str):
            terminal_id (UUID): The join key: the terminal the command ran on
            state (CommandState): Final states are SUCCEEDED, FAILED, EXPIRED and REJECTED. UNKNOWN is visible and NOT
                final: the order may have reached the broker and its outcome could not be read (a timeout after send, a lost
                connection). Reconciliation against the terminal's deal history resolves it to SUCCEEDED or FAILED on its own. A
                client must not re-send an order whose command is UNKNOWN, because that is how one fill becomes two. A
                NOT_EXECUTED answer from the terminal reads REJECTED with its reason. SUCCEEDED means the broker did what the
                command asked: for a market order, filled; for a pending order (limit, stop, stop_limit), accepted onto the
                broker's book with its ticket in `tickets.order` - not filled (OrderPlace).
            retcode (str): MT5 TRADE_RETCODE_*; empty when the command never reached the terminal
            reason (str): Granular reason, never a bucket
            tickets (str): CommandTickets as JSON text
            exec_price (str): Decimal as a string; empty when nothing filled
            exec_volume (str): Lots, decimal as a string; empty when nothing filled
            latencies (str): JSON text: {"broker_ms": integer or null, "agent_ms": integer or null}
            terminal_state (str): The terminal's lifecycle state when the outcome was recorded: when the cell's result
                arrived, or when the platform expired the command. Empty only when the terminal no longer exists
            magic (Union[Unset, str]): CommandResult.magic as text: the magic number the command sent, as an integer in
                text; empty where CommandResult.magic is null. Always sent
            comment (Union[Unset, str]): CommandResult.comment: the comment the command sent; empty where it is null or the
                order was placed without one. Always sent
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

        magic = d.pop("magic", UNSET)

        comment = d.pop("comment", UNSET)

        command_outcome = cls(
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
            magic=magic,
            comment=comment,
        )

        command_outcome.additional_properties = d
        return command_outcome

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
