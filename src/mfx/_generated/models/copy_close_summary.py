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

from ..models.copy_close_cause import CopyCloseCause
from ..models.copy_close_state import CopyCloseState
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyCloseSummary")


@_attrs_define
class CopyCloseSummary:
    """
    Attributes:
        id (UUID):
        state (CopyCloseState): pending: still being closed. done: every copied position closed or found closed.
            incomplete: any not closed. superseded: a newer request for the follower took over its open positions
        cause (CopyCloseCause):
        positions (int): Copied positions it covers
        closed (int): Of them, closed or found closed already
        attempt (int):
        created_at (datetime.datetime):
    """

    id: UUID
    state: CopyCloseState
    cause: CopyCloseCause
    positions: int
    closed: int
    attempt: int
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        state = self.state.value

        cause = self.cause.value

        positions = self.positions

        closed = self.closed

        attempt = self.attempt

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "state": state,
                "cause": cause,
                "positions": positions,
                "closed": closed,
                "attempt": attempt,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        state = CopyCloseState._read(d.pop("state"))

        cause = CopyCloseCause._read(d.pop("cause"))

        positions = d.pop("positions")

        closed = d.pop("closed")

        attempt = d.pop("attempt")

        created_at = isoparse(d.pop("created_at"))

        copy_close_summary = cls(
            id=id,
            state=state,
            cause=cause,
            positions=positions,
            closed=closed,
            attempt=attempt,
            created_at=created_at,
        )

        copy_close_summary.additional_properties = d
        return copy_close_summary

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
