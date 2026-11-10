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

T = TypeVar("T", bound="CtraderGrantStarted")


@_attrs_define
class CtraderGrantStarted:
    """
    Attributes:
        grant_id (UUID):
        consent_url (str): cTrader's consent page for this grant; send the trader there
        expires_at (datetime.datetime): The consent must complete before this; after it the grant is EXPIRED and a new
            one is started
    """

    grant_id: UUID
    consent_url: str
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grant_id = str(self.grant_id)

        consent_url = self.consent_url

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grant_id": grant_id,
                "consent_url": consent_url,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_id = UUID(d.pop("grant_id"))

        consent_url = d.pop("consent_url")

        expires_at = isoparse(d.pop("expires_at"))

        ctrader_grant_started = cls(
            grant_id=grant_id,
            consent_url=consent_url,
            expires_at=expires_at,
        )

        ctrader_grant_started.additional_properties = d
        return ctrader_grant_started

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
