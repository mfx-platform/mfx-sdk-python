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

from ..models.copy_limit_kind import CopyLimitKind
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_stopout_event_closed_item import CopyStopoutEventClosedItem


T = TypeVar("T", bound="CopyStopoutEvent")


@_attrs_define
class CopyStopoutEvent:
    """`data` of `copy.stopout`: a follower reached a copy limit and is stopped out

    Attributes:
        schema_version (str):
        stopout_id (UUID):
        follower_id (UUID):
        leader_id (UUID):
        account_id (UUID):
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        limit (CopyLimitKind):
        used (str): In the follower account's currency
        closed (list['CopyStopoutEventClosedItem']): The copied volume closed, when close_on_stopout is set
        at (datetime.datetime):
    """

    schema_version: str
    stopout_id: UUID
    follower_id: UUID
    leader_id: UUID
    account_id: UUID
    venue: Venue
    limit: CopyLimitKind
    used: str
    closed: list["CopyStopoutEventClosedItem"]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_stopout_event_closed_item import CopyStopoutEventClosedItem

        schema_version = self.schema_version

        stopout_id = str(self.stopout_id)

        follower_id = str(self.follower_id)

        leader_id = str(self.leader_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        limit = self.limit.value

        used = self.used

        closed = []
        for closed_item_data in self.closed:
            closed_item = closed_item_data.to_dict()
            closed.append(closed_item)

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "stopout_id": stopout_id,
                "follower_id": follower_id,
                "leader_id": leader_id,
                "account_id": account_id,
                "venue": venue,
                "limit": limit,
                "used": used,
                "closed": closed,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_stopout_event_closed_item import CopyStopoutEventClosedItem

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        stopout_id = UUID(d.pop("stopout_id"))

        follower_id = UUID(d.pop("follower_id"))

        leader_id = UUID(d.pop("leader_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        limit = CopyLimitKind(d.pop("limit"))

        used = d.pop("used")

        closed = []
        _closed = d.pop("closed")
        for closed_item_data in _closed:
            closed_item = CopyStopoutEventClosedItem.from_dict(closed_item_data)

            closed.append(closed_item)

        at = isoparse(d.pop("at"))

        copy_stopout_event = cls(
            schema_version=schema_version,
            stopout_id=stopout_id,
            follower_id=follower_id,
            leader_id=leader_id,
            account_id=account_id,
            venue=venue,
            limit=limit,
            used=used,
            closed=closed,
            at=at,
        )

        copy_stopout_event.additional_properties = d
        return copy_stopout_event

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
