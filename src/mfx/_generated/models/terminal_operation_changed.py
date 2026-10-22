from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.terminal_operation_changed_forced_stop import (
    TerminalOperationChangedForcedStop,
)
from ..models.terminal_operation_changed_kind import TerminalOperationChangedKind
from ..models.terminal_operation_changed_state import TerminalOperationChangedState
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalOperationChanged")


@_attrs_define
class TerminalOperationChanged:
    """`data` of a `terminal.operation_changed` message on the `events` channel: sent when a governed operation on a
    terminal (`TerminalOperation`: a restart, a rebuild, a move, a retire, a retried login, an attach or detach, a
    drain) is queued, when it starts, and when it ends: settled (SUCCEEDED or FAILED) or ended without running
    (NOT_STARTED, EXPIRED, CANCELLED, SUPERSEDED). The steps in between are not sent; read `GET
    /terminals/{id}/operations/{operation_id}` for its timeline. On the stream every value is text, as on every event,
    and a value that does not exist is empty.

        Attributes:
            schema_version (str): The payload's version; 1
            operation_id (UUID):
            terminal_id (UUID):
            kind (TerminalOperationChangedKind):
            state (TerminalOperationChangedState): As `TerminalOperation.state`
            step (str): As `TerminalOperation.step`: the last step the cell reached, or on FAILED and NOT_STARTED what
                failed or refused; empty when none
            forced_stop (TerminalOperationChangedForcedStop): As `TerminalOperation.forced_stop`; empty until the cell says
            cooldown_until (str): UTC date-time when the next restart of the terminal is allowed; empty when none
            finished_at (str): UTC date-time when it ended; empty while it runs
    """

    schema_version: str
    operation_id: UUID
    terminal_id: UUID
    kind: TerminalOperationChangedKind
    state: TerminalOperationChangedState
    step: str
    forced_stop: TerminalOperationChangedForcedStop
    cooldown_until: str
    finished_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        operation_id = str(self.operation_id)

        terminal_id = str(self.terminal_id)

        kind = self.kind.value

        state = self.state.value

        step = self.step

        forced_stop = self.forced_stop.value

        cooldown_until = self.cooldown_until

        finished_at = self.finished_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "operation_id": operation_id,
                "terminal_id": terminal_id,
                "kind": kind,
                "state": state,
                "step": step,
                "forced_stop": forced_stop,
                "cooldown_until": cooldown_until,
                "finished_at": finished_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        operation_id = UUID(d.pop("operation_id"))

        terminal_id = UUID(d.pop("terminal_id"))

        kind = TerminalOperationChangedKind(d.pop("kind"))

        state = TerminalOperationChangedState(d.pop("state"))

        step = d.pop("step")

        forced_stop = TerminalOperationChangedForcedStop(d.pop("forced_stop"))

        cooldown_until = d.pop("cooldown_until")

        finished_at = d.pop("finished_at")

        terminal_operation_changed = cls(
            schema_version=schema_version,
            operation_id=operation_id,
            terminal_id=terminal_id,
            kind=kind,
            state=state,
            step=step,
            forced_stop=forced_stop,
            cooldown_until=cooldown_until,
            finished_at=finished_at,
        )

        terminal_operation_changed.additional_properties = d
        return terminal_operation_changed

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
