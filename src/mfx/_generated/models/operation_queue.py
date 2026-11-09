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

from ..models.operation_queue_class import OperationQueueClass
from ..models.operation_queue_held_by import OperationQueueHeldBy
from ..models.operation_queue_reason_type_1 import OperationQueueReasonType1
from ..models.operation_queue_reason_type_2_type_1 import OperationQueueReasonType2Type1
from ..models.operation_queue_reason_type_3_type_1 import OperationQueueReasonType3Type1
from ..types import UNSET, Unset

T = TypeVar("T", bound="OperationQueue")


@_attrs_define
class OperationQueue:
    """Where a QUEUED operation waits. It waits in a line, behind other operations, or on a clock. Order in a line is class
    first (automatic recovery, then operator, then tenant), then who asked first.

        Attributes:
            held_by (OperationQueueHeldBy): The rule that holds it. farm_capacity (rule 6) and tenant_concurrency (rule 5)
                are lines: it starts when one of the farm's, or the tenant's, operations settles. cooldown (rule 2) and
                tenant_rate (rule 4) are clocks: it starts at `starts_after`. cell_slots is its cell's line: it starts when the
                cell, paced by its own load, has a slot for it
            expected_start_at (Union[None, datetime.datetime]): Held by cell_slots: when the cell's last plan expects its
                slot, an expectation and not a promise. Null for any other hold, and when unknown
            reason (Union[None, OperationQueueReasonType1, OperationQueueReasonType2Type1, OperationQueueReasonType3Type1]):
                Held by cell_slots: Why it waits, a coarse code: `cell_busy` its cell is busy now; `cell_settling` its cell
                started others a moment ago and lets them settle first; `cell_at_stop_line` its cell is at its limit and starts
                nothing new until it is lighter; `cell_silent` its cell has not reported for a minute; `broker_budget` the
                broker's logins a minute are spent; `broker_cap` the broker has as many logins in flight as it takes;
                `broker_maintenance` the broker is in maintenance; `platform_ceiling` the platform's own limit; `backoff`
                waiting after a failed attempt; `bulk_pace` a bulk action's items go at the pace of their cells. Never a figure,
                never the cell. Null for any other hold
            class_ (OperationQueueClass): Whose ask it is; it sets the order in a line
            position (Union[None, int]): Its place in line: 1 is next, 2 has one ahead of it. It is a place, not how many
                wait. Null when held by a clock, and once it has left the line
            starts_after (Union[None, datetime.datetime]): When a clock hold ends. Null for a line
            queued_at (datetime.datetime):
            expires_at (Union[None, datetime.datetime]): Not started by then, it settles EXPIRED and is never run late.
                queued_at plus the longest wait, 900 s unless an operator has changed it. Null for an item of a bulk action,
                which never expires: it waits for its cell or is cancelled
            bulk_action_id (Union[None, UUID, Unset]): The bulk action it is an item of; null for an operation asked on its
                own
    """

    held_by: OperationQueueHeldBy
    expected_start_at: Union[None, datetime.datetime]
    reason: Union[
        None,
        OperationQueueReasonType1,
        OperationQueueReasonType2Type1,
        OperationQueueReasonType3Type1,
    ]
    class_: OperationQueueClass
    position: Union[None, int]
    starts_after: Union[None, datetime.datetime]
    queued_at: datetime.datetime
    expires_at: Union[None, datetime.datetime]
    bulk_action_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        held_by = self.held_by.value

        expected_start_at: Union[None, str]
        if isinstance(self.expected_start_at, datetime.datetime):
            expected_start_at = self.expected_start_at.isoformat()
        else:
            expected_start_at = self.expected_start_at

        reason: Union[None, str]
        if isinstance(self.reason, OperationQueueReasonType1):
            reason = self.reason.value
        elif isinstance(self.reason, OperationQueueReasonType2Type1):
            reason = self.reason.value
        elif isinstance(self.reason, OperationQueueReasonType3Type1):
            reason = self.reason.value
        else:
            reason = self.reason

        class_ = self.class_.value

        position: Union[None, int]
        position = self.position

        starts_after: Union[None, str]
        if isinstance(self.starts_after, datetime.datetime):
            starts_after = self.starts_after.isoformat()
        else:
            starts_after = self.starts_after

        queued_at = self.queued_at.isoformat()

        expires_at: Union[None, str]
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        bulk_action_id: Union[None, Unset, str]
        if isinstance(self.bulk_action_id, Unset):
            bulk_action_id = UNSET
        elif isinstance(self.bulk_action_id, UUID):
            bulk_action_id = str(self.bulk_action_id)
        else:
            bulk_action_id = self.bulk_action_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "held_by": held_by,
                "expected_start_at": expected_start_at,
                "reason": reason,
                "class": class_,
                "position": position,
                "starts_after": starts_after,
                "queued_at": queued_at,
                "expires_at": expires_at,
            }
        )
        if bulk_action_id is not UNSET:
            field_dict["bulk_action_id"] = bulk_action_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        held_by = OperationQueueHeldBy(d.pop("held_by"))

        def _parse_expected_start_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expected_start_at_type_0 = isoparse(data)

                return expected_start_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expected_start_at = _parse_expected_start_at(d.pop("expected_start_at"))

        def _parse_reason(
            data: object,
        ) -> Union[
            None,
            OperationQueueReasonType1,
            OperationQueueReasonType2Type1,
            OperationQueueReasonType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = OperationQueueReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = OperationQueueReasonType2Type1(data)

                return reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = OperationQueueReasonType3Type1(data)

                return reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    OperationQueueReasonType1,
                    OperationQueueReasonType2Type1,
                    OperationQueueReasonType3Type1,
                ],
                data,
            )

        reason = _parse_reason(d.pop("reason"))

        class_ = OperationQueueClass(d.pop("class"))

        def _parse_position(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        position = _parse_position(d.pop("position"))

        def _parse_starts_after(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                starts_after_type_0 = isoparse(data)

                return starts_after_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        starts_after = _parse_starts_after(d.pop("starts_after"))

        queued_at = isoparse(d.pop("queued_at"))

        def _parse_expires_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        def _parse_bulk_action_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                bulk_action_id_type_0 = UUID(data)

                return bulk_action_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        bulk_action_id = _parse_bulk_action_id(d.pop("bulk_action_id", UNSET))

        operation_queue = cls(
            held_by=held_by,
            expected_start_at=expected_start_at,
            reason=reason,
            class_=class_,
            position=position,
            starts_after=starts_after,
            queued_at=queued_at,
            expires_at=expires_at,
            bulk_action_id=bulk_action_id,
        )

        operation_queue.additional_properties = d
        return operation_queue

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
