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

from ..models.operation_queue_class import OperationQueueClass
from ..models.operation_queue_held_by import OperationQueueHeldBy
from ..types import UNSET, Unset

T = TypeVar("T", bound="OperationQueue")


@_attrs_define
class OperationQueue:
    """Where a QUEUED operation waits. It waits in a line, behind other operations, or on a clock. Order in a line is class
    first (automatic recovery, then operator, then tenant), then who asked first.

        Attributes:
            held_by (OperationQueueHeldBy): The rule that holds it. farm_capacity (rule 6) and tenant_concurrency (rule 5)
                are lines: it starts when one of the farm's, or the tenant's, operations settles. cooldown (rule 2) and
                tenant_rate (rule 4) are clocks: it starts at `starts_after`
            class_ (OperationQueueClass): Whose ask it is; it sets the order in a line
            position (Union[None, int]): Its place in line: 1 is next, 2 has one ahead of it. It is a place, not how many
                wait. Null when held by a clock, and once it has left the line
            starts_after (Union[None, datetime.datetime]): When a clock hold ends. Null for a line
            queued_at (datetime.datetime):
            expires_at (datetime.datetime): Not started by then, it settles EXPIRED and is never run late. queued_at plus
                the longest wait, 900 s unless an operator has changed it
    """

    held_by: OperationQueueHeldBy
    class_: OperationQueueClass
    position: Union[None, int]
    starts_after: Union[None, datetime.datetime]
    queued_at: datetime.datetime
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        held_by = self.held_by.value

        class_ = self.class_.value

        position: Union[None, int]
        position = self.position

        starts_after: Union[None, str]
        if isinstance(self.starts_after, datetime.datetime):
            starts_after = self.starts_after.isoformat()
        else:
            starts_after = self.starts_after

        queued_at = self.queued_at.isoformat()

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "held_by": held_by,
                "class": class_,
                "position": position,
                "starts_after": starts_after,
                "queued_at": queued_at,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        held_by = OperationQueueHeldBy(d.pop("held_by"))

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

        expires_at = isoparse(d.pop("expires_at"))

        operation_queue = cls(
            held_by=held_by,
            class_=class_,
            position=position,
            starts_after=starts_after,
            queued_at=queued_at,
            expires_at=expires_at,
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
