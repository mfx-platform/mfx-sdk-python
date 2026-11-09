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

from ..models.bulk_action_kind import BulkActionKind
from ..models.bulk_action_state import BulkActionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bulk_action_counts import BulkActionCounts
    from ..models.bulk_action_refusal import BulkActionRefusal


T = TypeVar("T", bound="BulkAction")


@_attrs_define
class BulkAction:
    """A bulk restart, retire or swap: judged once, answered at once, and carried out at the pace of the cells it touches.
    Each accepted terminal is one ordinary operation with `bulk_action_id` set, in its cell's line; a refused one is
    listed in `refused` and never queued. Its items never expire: each waits for its cell or is cancelled. Cancel
    settles every item still QUEUED as CANCELLED and lets running ones finish; the line is never reordered.

        Attributes:
            id (UUID):
            kind (BulkActionKind): cell_relogin: the platform's own, opened when a cell comes back from a restart and logs
                its terminals in again
            state (BulkActionState): RUNNING while any item waits or runs; DONE when every item succeeded; PARTIAL when
                every item has ended and some did not succeed; CANCELLED when it was cancelled
            requested_by (str): As on TerminalOperation
            reason (str):
            requested_n (int): Terminals the filter named
            accepted_n (int):
            refused_n (int):
            refused (list['BulkActionRefusal']):
            counts (BulkActionCounts):
            expected_finish_at (Union[None, datetime.datetime]): When the last item is expected to end, at each cell's load
                now and the measured time an item takes: an expectation, not a promise. Null once it has ended, or when a cell
                it waits on has no plan
            late (bool): True once it has run past the slow end of its expectation (the console reads that end as
                `expected_finish_p95_at`)
            created_at (datetime.datetime):
            finished_at (Union[None, datetime.datetime]):
    """

    id: UUID
    kind: BulkActionKind
    state: BulkActionState
    requested_by: str
    reason: str
    requested_n: int
    accepted_n: int
    refused_n: int
    refused: list["BulkActionRefusal"]
    counts: "BulkActionCounts"
    expected_finish_at: Union[None, datetime.datetime]
    late: bool
    created_at: datetime.datetime
    finished_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_action_counts import BulkActionCounts
        from ..models.bulk_action_refusal import BulkActionRefusal

        id = str(self.id)

        kind = self.kind.value

        state = self.state.value

        requested_by = self.requested_by

        reason = self.reason

        requested_n = self.requested_n

        accepted_n = self.accepted_n

        refused_n = self.refused_n

        refused = []
        for refused_item_data in self.refused:
            refused_item = refused_item_data.to_dict()
            refused.append(refused_item)

        counts = self.counts.to_dict()

        expected_finish_at: Union[None, str]
        if isinstance(self.expected_finish_at, datetime.datetime):
            expected_finish_at = self.expected_finish_at.isoformat()
        else:
            expected_finish_at = self.expected_finish_at

        late = self.late

        created_at = self.created_at.isoformat()

        finished_at: Union[None, str]
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "state": state,
                "requested_by": requested_by,
                "reason": reason,
                "requested_n": requested_n,
                "accepted_n": accepted_n,
                "refused_n": refused_n,
                "refused": refused,
                "counts": counts,
                "expected_finish_at": expected_finish_at,
                "late": late,
                "created_at": created_at,
                "finished_at": finished_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_action_counts import BulkActionCounts
        from ..models.bulk_action_refusal import BulkActionRefusal

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        kind = BulkActionKind(d.pop("kind"))

        state = BulkActionState(d.pop("state"))

        requested_by = d.pop("requested_by")

        reason = d.pop("reason")

        requested_n = d.pop("requested_n")

        accepted_n = d.pop("accepted_n")

        refused_n = d.pop("refused_n")

        refused = []
        _refused = d.pop("refused")
        for refused_item_data in _refused:
            refused_item = BulkActionRefusal.from_dict(refused_item_data)

            refused.append(refused_item)

        counts = BulkActionCounts.from_dict(d.pop("counts"))

        def _parse_expected_finish_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expected_finish_at_type_0 = isoparse(data)

                return expected_finish_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expected_finish_at = _parse_expected_finish_at(d.pop("expected_finish_at"))

        late = d.pop("late")

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

        bulk_action = cls(
            id=id,
            kind=kind,
            state=state,
            requested_by=requested_by,
            reason=reason,
            requested_n=requested_n,
            accepted_n=accepted_n,
            refused_n=refused_n,
            refused=refused,
            counts=counts,
            expected_finish_at=expected_finish_at,
            late=late,
            created_at=created_at,
            finished_at=finished_at,
        )

        bulk_action.additional_properties = d
        return bulk_action

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
