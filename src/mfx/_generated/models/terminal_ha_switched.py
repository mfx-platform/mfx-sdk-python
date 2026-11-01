from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.terminal_ha_switched_reason import TerminalHaSwitchedReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalHaSwitched")


@_attrs_define
class TerminalHaSwitched:
    """`data` of a `terminal.ha_switched` message on the `events` channel: MFX Hub HA moved the terminal to its second
    terminal, which now carries its orders, quotes and account. The terminal's id is the same before and after; nothing
    about the second terminal is sent. On the stream every value is text, as on every event.

        Example:
            {'schema_version': '1', 'terminal_id': '0e6a51a8-65f1-4f4c-9c53-3d6a2f6a0101', 'reason': 'broker_lost', 'at':
                '2026-11-01T22:04:31.120Z', 'took_ms': '40'}

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID): The terminal, as you address it
            reason (TerminalHaSwitchedReason): Why it switched. order: an order arrived while the first terminal could not
                carry it, and it was placed through the second. broker_lost: the first terminal lost its broker connection.
                unresponsive: the first terminal stopped reporting. terminal_failed and process_gone: the first terminal failed
                or its MetaTrader 5 process ended. operator: MFX Hub support switched it.
            at (str): UTC date-time of the switch, to the millisecond
            took_ms (str): Milliseconds the switch took, an integer as text
    """

    schema_version: str
    terminal_id: UUID
    reason: TerminalHaSwitchedReason
    at: str
    took_ms: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        reason = self.reason.value

        at = self.at

        took_ms = self.took_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "reason": reason,
                "at": at,
                "took_ms": took_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        reason = TerminalHaSwitchedReason(d.pop("reason"))

        at = d.pop("at")

        took_ms = d.pop("took_ms")

        terminal_ha_switched = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            reason=reason,
            at=at,
            took_ms=took_ms,
        )

        terminal_ha_switched.additional_properties = d
        return terminal_ha_switched

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
