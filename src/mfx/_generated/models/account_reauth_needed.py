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

from ..models.account_reauth_needed_reason import AccountReauthNeededReason
from ..models.account_reauth_needed_venue import AccountReauthNeededVenue
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountReauthNeeded")


@_attrs_define
class AccountReauthNeeded:
    """`data` of an `account.reauth_needed` message on the `events` channel: the account's access was refused (the trader
    withdrew the grant at cTrader, or it was revoked); start a new grant for it

        Attributes:
            schema_version (str): The payload's version; 1
            account_id (UUID):
            venue (AccountReauthNeededVenue):
            reason (AccountReauthNeededReason):
            ts (datetime.datetime): When its access was refused
    """

    schema_version: str
    account_id: UUID
    venue: AccountReauthNeededVenue
    reason: AccountReauthNeededReason
    ts: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        account_id = str(self.account_id)

        venue = self.venue.value

        reason = self.reason.value

        ts = self.ts.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "account_id": account_id,
                "venue": venue,
                "reason": reason,
                "ts": ts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        account_id = UUID(d.pop("account_id"))

        venue = AccountReauthNeededVenue(d.pop("venue"))

        reason = AccountReauthNeededReason(d.pop("reason"))

        ts = isoparse(d.pop("ts"))

        account_reauth_needed = cls(
            schema_version=schema_version,
            account_id=account_id,
            venue=venue,
            reason=reason,
            ts=ts,
        )

        account_reauth_needed.additional_properties = d
        return account_reauth_needed

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
