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

from ..models.position_trailing_stop_changed_state import (
    PositionTrailingStopChangedState,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PositionTrailingStopChanged")


@_attrs_define
class PositionTrailingStopChanged:
    """`data` of a `position.trailing_stop_changed` message on the `events` channel: sent once each time a position's
    trailing stop becomes active, paused or ended. Each move of the stop is a `position.modified`, as for any change of
    a stop.

        Attributes:
            schema_version (str):
            terminal_id (UUID):
            ticket (str): The position's MT5 ticket, an integer as text, as on `position.opened`
            distance (str):
            state (PositionTrailingStopChangedState):
            reason (Union[None, str]): As `TrailingStop.reason`; on the stream empty while active
            at (datetime.datetime):
    """

    schema_version: str
    terminal_id: UUID
    ticket: str
    distance: str
    state: PositionTrailingStopChangedState
    reason: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        ticket = self.ticket

        distance = self.distance

        state = self.state.value

        reason: Union[None, str]
        reason = self.reason

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "ticket": ticket,
                "distance": distance,
                "state": state,
                "reason": reason,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        ticket = d.pop("ticket")

        distance = d.pop("distance")

        state = PositionTrailingStopChangedState(d.pop("state"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        at = isoparse(d.pop("at"))

        position_trailing_stop_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            ticket=ticket,
            distance=distance,
            state=state,
            reason=reason,
            at=at,
        )

        position_trailing_stop_changed.additional_properties = d
        return position_trailing_stop_changed

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
