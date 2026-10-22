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

from ..models.own_contact_role import OwnContactRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="OwnContact")


@_attrs_define
class OwnContact:
    """A person at the tenant and what they are told. The representative is emailed about code and confirms live trading on
    a real-money account.

        Attributes:
            id (UUID):
            role (OwnContactRole):
            name (str):
            email (str):
            mobile (Union[None, str]): In international form; null when none was given. Nothing is sent to it
            updated_at (datetime.datetime):
    """

    id: UUID
    role: OwnContactRole
    name: str
    email: str
    mobile: Union[None, str]
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        role = self.role.value

        name = self.name

        email = self.email

        mobile: Union[None, str]
        mobile = self.mobile

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "role": role,
                "name": name,
                "email": email,
                "mobile": mobile,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        role = OwnContactRole(d.pop("role"))

        name = d.pop("name")

        email = d.pop("email")

        def _parse_mobile(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mobile = _parse_mobile(d.pop("mobile"))

        updated_at = isoparse(d.pop("updated_at"))

        own_contact = cls(
            id=id,
            role=role,
            name=name,
            email=email,
            mobile=mobile,
            updated_at=updated_at,
        )

        own_contact.additional_properties = d
        return own_contact

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
