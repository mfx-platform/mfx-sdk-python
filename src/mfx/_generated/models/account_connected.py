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

from ..models.account_connected_venue import AccountConnectedVenue
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountConnected")


@_attrs_define
class AccountConnected:
    """`data` of an `account.connected` message on the `events` channel: a trading account is connected and can be used

    Attributes:
        schema_version (str): The payload's version; 1
        account_id (UUID):
        venue (AccountConnectedVenue):
        ts (datetime.datetime): When it was connected
        grant_id (Union[None, UUID, Unset]): The grant it was connected through (cTrader); absent for MT5
    """

    schema_version: str
    account_id: UUID
    venue: AccountConnectedVenue
    ts: datetime.datetime
    grant_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        account_id = str(self.account_id)

        venue = self.venue.value

        ts = self.ts.isoformat()

        grant_id: Union[None, Unset, str]
        if isinstance(self.grant_id, Unset):
            grant_id = UNSET
        elif isinstance(self.grant_id, UUID):
            grant_id = str(self.grant_id)
        else:
            grant_id = self.grant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "account_id": account_id,
                "venue": venue,
                "ts": ts,
            }
        )
        if grant_id is not UNSET:
            field_dict["grant_id"] = grant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        account_id = UUID(d.pop("account_id"))

        venue = AccountConnectedVenue(d.pop("venue"))

        ts = isoparse(d.pop("ts"))

        def _parse_grant_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grant_id_type_0 = UUID(data)

                return grant_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        grant_id = _parse_grant_id(d.pop("grant_id", UNSET))

        account_connected = cls(
            schema_version=schema_version,
            account_id=account_id,
            venue=venue,
            ts=ts,
            grant_id=grant_id,
        )

        account_connected.additional_properties = d
        return account_connected

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
