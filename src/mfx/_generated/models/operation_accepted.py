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

from ..models.operation_accepted_state import OperationAcceptedState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.operation_queue import OperationQueue


T = TypeVar("T", bound="OperationAccepted")


@_attrs_define
class OperationAccepted:
    """
    Attributes:
        operation_id (UUID):
        state (OperationAcceptedState): QUEUED when the ask was valid and only busy: held, and started by the platform
            when it can. An operator's asks always queue; a tenant's only with `queue: true`
        queue (Union['OperationQueue', None, Unset]): Where it waits, while QUEUED; null otherwise
        duplicate (Union[Unset, bool]): True when this Idempotency-Key was seen before, or when the terminal already had
            the same kind of operation waiting (a stronger kind replaces a waiting one, as described on restartTerminal);
            the original operation is returned
    """

    operation_id: UUID
    state: OperationAcceptedState
    queue: Union["OperationQueue", None, Unset] = UNSET
    duplicate: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.operation_queue import OperationQueue

        operation_id = str(self.operation_id)

        state = self.state.value

        queue: Union[None, Unset, dict[str, Any]]
        if isinstance(self.queue, Unset):
            queue = UNSET
        elif isinstance(self.queue, OperationQueue):
            queue = self.queue.to_dict()
        else:
            queue = self.queue

        duplicate = self.duplicate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation_id": operation_id,
                "state": state,
            }
        )
        if queue is not UNSET:
            field_dict["queue"] = queue
        if duplicate is not UNSET:
            field_dict["duplicate"] = duplicate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.operation_queue import OperationQueue

        d = dict(src_dict)
        operation_id = UUID(d.pop("operation_id"))

        state = OperationAcceptedState(d.pop("state"))

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

        duplicate = d.pop("duplicate", UNSET)

        operation_accepted = cls(
            operation_id=operation_id,
            state=state,
            queue=queue,
            duplicate=duplicate,
        )

        operation_accepted.additional_properties = d
        return operation_accepted

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
