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
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.terminal_state_changed_from import TerminalStateChangedFrom
from ..models.terminal_state_changed_to import TerminalStateChangedTo
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalStateChanged")


@_attrs_define
class TerminalStateChanged:
    """`data` of a `terminal.state_changed` message on the `events` channel: sent once for each move of a terminal's
    lifecycle state, after the move is recorded, whoever made it (you, an operator or the platform). `transition_id`
    names the move in the terminal's history. On the stream every value is text, as on every event.

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID):
            from_ (TerminalStateChangedFrom): The state it left (`Terminal.state` explains each)
            to (TerminalStateChangedTo): The state it is now in
            reason (str): Why it moved, in words (for example `account verified, broker connected`, `its tenant's suspension
                grace ended`)
            transition_id (UUID): The move's id in the terminal's state history
            ts (datetime.datetime): When it moved, UTC
    """

    schema_version: str
    terminal_id: UUID
    from_: TerminalStateChangedFrom
    to: TerminalStateChangedTo
    reason: str
    transition_id: UUID
    ts: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        from_ = self.from_.value

        to = self.to.value

        reason = self.reason

        transition_id = str(self.transition_id)

        ts = self.ts.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "from": from_,
                "to": to,
                "reason": reason,
                "transition_id": transition_id,
                "ts": ts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        from_ = TerminalStateChangedFrom(d.pop("from"))

        to = TerminalStateChangedTo(d.pop("to"))

        reason = d.pop("reason")

        transition_id = UUID(d.pop("transition_id"))

        ts = isoparse(d.pop("ts"))

        terminal_state_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            from_=from_,
            to=to,
            reason=reason,
            transition_id=transition_id,
            ts=ts,
        )

        terminal_state_changed.additional_properties = d
        return terminal_state_changed

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
