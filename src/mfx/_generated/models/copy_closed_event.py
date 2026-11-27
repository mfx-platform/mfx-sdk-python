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
from ..models.copy_closed_event_state import CopyClosedEventState
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_closed_event_closed_item import CopyClosedEventClosedItem
    from ..models.copy_closed_event_not_closed_item import CopyClosedEventNotClosedItem


T = TypeVar("T", bound="CopyClosedEvent")


@_attrs_define
class CopyClosedEvent:
    """`data` of `copy.closed`: a requested close stopped being pending. Sent once; a failure between the send and its
    record can send it again with the same close_id, never not at all

        Attributes:
            schema_version (str):
            close_id (UUID):
            follower_id (UUID):
            leader_id (UUID):
            account_id (UUID):
            venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
                read one it does not know
            cause (CopyCloseCause):
            state (CopyClosedEventState):
            closed (list['CopyClosedEventClosedItem']): Each copied position closed (volume the venue closed) or found
                closed already (volume 0, no command)
            not_closed (list['CopyClosedEventNotClosedItem']): Each copied position not closed, with why
            at (datetime.datetime):
    """

    schema_version: str
    close_id: UUID
    follower_id: UUID
    leader_id: UUID
    account_id: UUID
    venue: Venue
    cause: CopyCloseCause
    state: CopyClosedEventState
    closed: list["CopyClosedEventClosedItem"]
    not_closed: list["CopyClosedEventNotClosedItem"]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_closed_event_closed_item import CopyClosedEventClosedItem
        from ..models.copy_closed_event_not_closed_item import (
            CopyClosedEventNotClosedItem,
        )

        schema_version = self.schema_version

        close_id = str(self.close_id)

        follower_id = str(self.follower_id)

        leader_id = str(self.leader_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        cause = self.cause.value

        state = self.state.value

        closed = []
        for closed_item_data in self.closed:
            closed_item = closed_item_data.to_dict()
            closed.append(closed_item)

        not_closed = []
        for not_closed_item_data in self.not_closed:
            not_closed_item = not_closed_item_data.to_dict()
            not_closed.append(not_closed_item)

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "close_id": close_id,
                "follower_id": follower_id,
                "leader_id": leader_id,
                "account_id": account_id,
                "venue": venue,
                "cause": cause,
                "state": state,
                "closed": closed,
                "not_closed": not_closed,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_closed_event_closed_item import CopyClosedEventClosedItem
        from ..models.copy_closed_event_not_closed_item import (
            CopyClosedEventNotClosedItem,
        )

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        close_id = UUID(d.pop("close_id"))

        follower_id = UUID(d.pop("follower_id"))

        leader_id = UUID(d.pop("leader_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue._read(d.pop("venue"))

        cause = CopyCloseCause._read(d.pop("cause"))

        state = CopyClosedEventState._read(d.pop("state"))

        closed = []
        _closed = d.pop("closed")
        for closed_item_data in _closed:
            closed_item = CopyClosedEventClosedItem.from_dict(closed_item_data)

            closed.append(closed_item)

        not_closed = []
        _not_closed = d.pop("not_closed")
        for not_closed_item_data in _not_closed:
            not_closed_item = CopyClosedEventNotClosedItem.from_dict(not_closed_item_data)

            not_closed.append(not_closed_item)

        at = isoparse(d.pop("at"))

        copy_closed_event = cls(
            schema_version=schema_version,
            close_id=close_id,
            follower_id=follower_id,
            leader_id=leader_id,
            account_id=account_id,
            venue=venue,
            cause=cause,
            state=state,
            closed=closed,
            not_closed=not_closed,
            at=at,
        )

        copy_closed_event.additional_properties = d
        return copy_closed_event

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
