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

from ..models.condition_status import ConditionStatus
from ..models.terminal_condition_changed_attributed_to import (
    TerminalConditionChangedAttributedTo,
)
from ..models.terminal_condition_changed_condition import (
    TerminalConditionChangedCondition,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalConditionChanged")


@_attrs_define
class TerminalConditionChanged:
    """`data` of a `terminal.condition_changed` message on the `events` channel: sent once when one of a terminal's
    observed conditions changes status, and when `TicksFresh` moves between its two named `failed` reasons, `slow_feed`
    and `broker_quiet`. A reason reworded under a status that stands sends nothing. The fields are those of `Condition`.
    On the stream every value is text, as on every event, and a value that does not exist is empty.

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID):
            condition (TerminalConditionChangedCondition):
            status (ConditionStatus): Tri-state on purpose. `unknown` is what an unreachable agent produces, and collapsing
                it into `failed` invents an outage while collapsing it into `ok` hides one.
            reason (str): Why, as in `Condition.reason`; empty when `ok` with nothing to say
            since (datetime.datetime): When it took this status, UTC
            attributed_to (TerminalConditionChangedAttributedTo): As `Condition.attributed_to`: `broker` for a broker's feed
                fault, empty when not attributed
    """

    schema_version: str
    terminal_id: UUID
    condition: TerminalConditionChangedCondition
    status: ConditionStatus
    reason: str
    since: datetime.datetime
    attributed_to: TerminalConditionChangedAttributedTo
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        condition = self.condition.value

        status = self.status.value

        reason = self.reason

        since = self.since.isoformat()

        attributed_to = self.attributed_to.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "condition": condition,
                "status": status,
                "reason": reason,
                "since": since,
                "attributed_to": attributed_to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        condition = TerminalConditionChangedCondition(d.pop("condition"))

        status = ConditionStatus(d.pop("status"))

        reason = d.pop("reason")

        since = isoparse(d.pop("since"))

        attributed_to = TerminalConditionChangedAttributedTo(d.pop("attributed_to"))

        terminal_condition_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            condition=condition,
            status=status,
            reason=reason,
            since=since,
            attributed_to=attributed_to,
        )

        terminal_condition_changed.additional_properties = d
        return terminal_condition_changed

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
