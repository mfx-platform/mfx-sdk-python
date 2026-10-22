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

from ..models.terminal_operation_kind import TerminalOperationKind
from ..models.terminal_operation_state import TerminalOperationState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.operation_queue import OperationQueue
    from ..models.terminal_operation_timeline_item import TerminalOperationTimelineItem


T = TypeVar("T", bound="TerminalOperation")


@_attrs_define
class TerminalOperation:
    """A governed lifecycle operation; done only when the terminal produces ticks again

    Attributes:
        operation_id (UUID):
        kind (TerminalOperationKind):
        terminal_id (UUID):
        state (TerminalOperationState): QUEUED is a state of the operation, never of the terminal: the terminal's own
            state and its lifecycle record are untouched while the operation waits. A queued operation ends by starting
            (ACCEPTED, then as before) or in one of four ways in which nothing ran: NOT_STARTED (its turn came and the
            guard, run again on the terminal as it was then, refused it; `step` carries the refusal's code), EXPIRED (still
            waiting at `queue.expires_at`; it is never run late), CANCELLED, or SUPERSEDED (a stronger ask took its place;
            `superseded_by`).
        requested_by (str): key:<key id>, admin.<email> for an operator, or system.healing for an automatic recovery
            step
        reason (str):
        forced_stop (Union[None, bool]): True when the terminal would not close and its job was stopped; null until the
            cell says
        step (Union[None, str]): The last step the cell reached; on FAILED, what failed (e.g. shutdown_timeout,
            deadline, cooldown)
        timeline (list['TerminalOperationTimelineItem']):
        cooldown_until (Union[None, datetime.datetime]): When the next restart of this terminal is allowed (rule 2)
        created_at (datetime.datetime):
        finished_at (Union[None, datetime.datetime]):
        queue (Union['OperationQueue', None, Unset]): Where it waits, while QUEUED. Kept as it last stood, with a null
            `position`, once it has left the line; null for an operation that never waited
        superseded_by (Union[None, UUID, Unset]): The operation that replaced this one; set only on SUPERSEDED
    """

    operation_id: UUID
    kind: TerminalOperationKind
    terminal_id: UUID
    state: TerminalOperationState
    requested_by: str
    reason: str
    forced_stop: Union[None, bool]
    step: Union[None, str]
    timeline: list["TerminalOperationTimelineItem"]
    cooldown_until: Union[None, datetime.datetime]
    created_at: datetime.datetime
    finished_at: Union[None, datetime.datetime]
    queue: Union["OperationQueue", None, Unset] = UNSET
    superseded_by: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.operation_queue import OperationQueue
        from ..models.terminal_operation_timeline_item import (
            TerminalOperationTimelineItem,
        )

        operation_id = str(self.operation_id)

        kind = self.kind.value

        terminal_id = str(self.terminal_id)

        state = self.state.value

        requested_by = self.requested_by

        reason = self.reason

        forced_stop: Union[None, bool]
        forced_stop = self.forced_stop

        step: Union[None, str]
        step = self.step

        timeline = []
        for timeline_item_data in self.timeline:
            timeline_item = timeline_item_data.to_dict()
            timeline.append(timeline_item)

        cooldown_until: Union[None, str]
        if isinstance(self.cooldown_until, datetime.datetime):
            cooldown_until = self.cooldown_until.isoformat()
        else:
            cooldown_until = self.cooldown_until

        created_at = self.created_at.isoformat()

        finished_at: Union[None, str]
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        queue: Union[None, Unset, dict[str, Any]]
        if isinstance(self.queue, Unset):
            queue = UNSET
        elif isinstance(self.queue, OperationQueue):
            queue = self.queue.to_dict()
        else:
            queue = self.queue

        superseded_by: Union[None, Unset, str]
        if isinstance(self.superseded_by, Unset):
            superseded_by = UNSET
        elif isinstance(self.superseded_by, UUID):
            superseded_by = str(self.superseded_by)
        else:
            superseded_by = self.superseded_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation_id": operation_id,
                "kind": kind,
                "terminal_id": terminal_id,
                "state": state,
                "requested_by": requested_by,
                "reason": reason,
                "forced_stop": forced_stop,
                "step": step,
                "timeline": timeline,
                "cooldown_until": cooldown_until,
                "created_at": created_at,
                "finished_at": finished_at,
            }
        )
        if queue is not UNSET:
            field_dict["queue"] = queue
        if superseded_by is not UNSET:
            field_dict["superseded_by"] = superseded_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.operation_queue import OperationQueue
        from ..models.terminal_operation_timeline_item import (
            TerminalOperationTimelineItem,
        )

        d = dict(src_dict)
        operation_id = UUID(d.pop("operation_id"))

        kind = TerminalOperationKind(d.pop("kind"))

        terminal_id = UUID(d.pop("terminal_id"))

        state = TerminalOperationState(d.pop("state"))

        requested_by = d.pop("requested_by")

        reason = d.pop("reason")

        def _parse_forced_stop(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        forced_stop = _parse_forced_stop(d.pop("forced_stop"))

        def _parse_step(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        step = _parse_step(d.pop("step"))

        timeline = []
        _timeline = d.pop("timeline")
        for timeline_item_data in _timeline:
            timeline_item = TerminalOperationTimelineItem.from_dict(timeline_item_data)

            timeline.append(timeline_item)

        def _parse_cooldown_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cooldown_until_type_0 = isoparse(data)

                return cooldown_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        cooldown_until = _parse_cooldown_until(d.pop("cooldown_until"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_finished_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        def _parse_queue(data: object) -> Union["OperationQueue", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                queue_type_0 = OperationQueue.from_dict(data)

                return queue_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OperationQueue", None, Unset], data)

        queue = _parse_queue(d.pop("queue", UNSET))

        def _parse_superseded_by(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                superseded_by_type_0 = UUID(data)

                return superseded_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        superseded_by = _parse_superseded_by(d.pop("superseded_by", UNSET))

        terminal_operation = cls(
            operation_id=operation_id,
            kind=kind,
            terminal_id=terminal_id,
            state=state,
            requested_by=requested_by,
            reason=reason,
            forced_stop=forced_stop,
            step=step,
            timeline=timeline,
            cooldown_until=cooldown_until,
            created_at=created_at,
            finished_at=finished_at,
            queue=queue,
            superseded_by=superseded_by,
        )

        terminal_operation.additional_properties = d
        return terminal_operation

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
