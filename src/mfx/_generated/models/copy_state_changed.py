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

from ..models.copy_follower_state import CopyFollowerState
from ..models.venue import Venue
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyStateChanged")


@_attrs_define
class CopyStateChanged:
    """`data` of `copy.state_changed`: a follower's state changed

    Attributes:
        schema_version (str):
        follower_id (UUID):
        leader_id (UUID):
        account_id (UUID):
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        from_ (CopyFollowerState): copying: receives the leader's deals. paused: by you, its entries are not copied,
            closes of what it copied still are. stopped_out: a copy limit was reached; it copies nothing new until the
            period ends or the stop-out is reset. unfollowed: final.
        to (CopyFollowerState): copying: receives the leader's deals. paused: by you, its entries are not copied, closes
            of what it copied still are. stopped_out: a copy limit was reached; it copies nothing new until the period ends
            or the stop-out is reset. unfollowed: final.
        why (str): For example paused, resumed, stopout, stopout_reset, stopout_expired, unfollowed, leader_retired. A
            new word may be added; read one you do not know as text
        at (datetime.datetime):
    """

    schema_version: str
    follower_id: UUID
    leader_id: UUID
    account_id: UUID
    venue: Venue
    from_: CopyFollowerState
    to: CopyFollowerState
    why: str
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        follower_id = str(self.follower_id)

        leader_id = str(self.leader_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        from_ = self.from_.value

        to = self.to.value

        why = self.why

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "follower_id": follower_id,
                "leader_id": leader_id,
                "account_id": account_id,
                "venue": venue,
                "from": from_,
                "to": to,
                "why": why,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        follower_id = UUID(d.pop("follower_id"))

        leader_id = UUID(d.pop("leader_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        from_ = CopyFollowerState(d.pop("from"))

        to = CopyFollowerState(d.pop("to"))

        why = d.pop("why")

        at = isoparse(d.pop("at"))

        copy_state_changed = cls(
            schema_version=schema_version,
            follower_id=follower_id,
            leader_id=leader_id,
            account_id=account_id,
            venue=venue,
            from_=from_,
            to=to,
            why=why,
            at=at,
        )

        copy_state_changed.additional_properties = d
        return copy_state_changed

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
