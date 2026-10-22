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

from ..models.trailing_stop_state import TrailingStopState
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrailingStop")


@_attrs_define
class TrailingStop:
    """A position's trailing stop as the platform holds it. `active`: the platform is trailing it; `paused`: the record
    stands and nothing trails it now (the terminal is not ACTIVE, or the broker refused the last five moves); `ended`:
    it stopped, `reason` says why. While nothing trails it the stop stays where it last was, at the broker: never no
    stop.

        Attributes:
            distance (str):
            state (TrailingStopState):
            since (datetime.datetime): When it took this state
            reason (Union[None, str]): Why it is paused or ended: stop_changed (a stop set by anyone else), position_closed,
                cleared, terminal_retired, terminal_not_active, or the broker's words for a refused move; null while active
    """

    distance: str
    state: TrailingStopState
    since: datetime.datetime
    reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        distance = self.distance

        state = self.state.value

        since = self.since.isoformat()

        reason: Union[None, str]
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "distance": distance,
                "state": state,
                "since": since,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        distance = d.pop("distance")

        state = TrailingStopState(d.pop("state"))

        since = isoparse(d.pop("since"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        trailing_stop = cls(
            distance=distance,
            state=state,
            since=since,
            reason=reason,
        )

        trailing_stop.additional_properties = d
        return trailing_stop

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
