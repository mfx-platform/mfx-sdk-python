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

from ..models.venue import Venue
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyDrift")


@_attrs_define
class CopyDrift:
    """`data` of `copy.drift`: the follower's copied positions differ from what the leader's open positions and the mandate
    say it should hold, found when the copied positions are healed from the account. Resync after correcting the cause;
    MFX Hub trades nothing to close the gap.

        Attributes:
            schema_version (str):
            follower_id (UUID):
            leader_id (UUID):
            account_id (UUID):
            venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
                read one it does not know
            drift_pct (str): How far the copied exposure is from the expected, as a percentage of the expected
            at (datetime.datetime):
    """

    schema_version: str
    follower_id: UUID
    leader_id: UUID
    account_id: UUID
    venue: Venue
    drift_pct: str
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        follower_id = str(self.follower_id)

        leader_id = str(self.leader_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        drift_pct = self.drift_pct

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
                "drift_pct": drift_pct,
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

        drift_pct = d.pop("drift_pct")

        at = isoparse(d.pop("at"))

        copy_drift = cls(
            schema_version=schema_version,
            follower_id=follower_id,
            leader_id=leader_id,
            account_id=account_id,
            venue=venue,
            drift_pct=drift_pct,
            at=at,
        )

        copy_drift.additional_properties = d
        return copy_drift

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
