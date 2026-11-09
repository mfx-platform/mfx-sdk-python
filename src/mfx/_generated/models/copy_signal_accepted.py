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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopySignalAccepted")


@_attrs_define
class CopySignalAccepted:
    """
    Attributes:
        signal_id (UUID): MFX Hub's id for the signal; the copy log names it
        id (str): Your id, as sent
        leader_id (UUID):
        duplicate (bool): True when this leader sent this id before; the original signal is returned and nothing is
            copied again
        iat (datetime.datetime): When MFX Hub made the signal, UTC
        exp (datetime.datetime): After this no follower copies it (signal_expired)
    """

    signal_id: UUID
    id: str
    leader_id: UUID
    duplicate: bool
    iat: datetime.datetime
    exp: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        signal_id = str(self.signal_id)

        id = self.id

        leader_id = str(self.leader_id)

        duplicate = self.duplicate

        iat = self.iat.isoformat()

        exp = self.exp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signal_id": signal_id,
                "id": id,
                "leader_id": leader_id,
                "duplicate": duplicate,
                "iat": iat,
                "exp": exp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signal_id = UUID(d.pop("signal_id"))

        id = d.pop("id")

        leader_id = UUID(d.pop("leader_id"))

        duplicate = d.pop("duplicate")

        iat = isoparse(d.pop("iat"))

        exp = isoparse(d.pop("exp"))

        copy_signal_accepted = cls(
            signal_id=signal_id,
            id=id,
            leader_id=leader_id,
            duplicate=duplicate,
            iat=iat,
            exp=exp,
        )

        copy_signal_accepted.additional_properties = d
        return copy_signal_accepted

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
