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

from ..models.billing_profile_scope_item_kind import BillingProfileScopeItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingProfileScopeItem")


@_attrs_define
class BillingProfileScopeItem:
    """
    Attributes:
        kind (BillingProfileScopeItemKind):
        id (UUID):
        from_day (datetime.date):
        name (Union[Unset, str]):
        accounts (Union[Unset, int]):
    """

    kind: BillingProfileScopeItemKind
    id: UUID
    from_day: datetime.date
    name: Union[Unset, str] = UNSET
    accounts: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        id = str(self.id)

        from_day = self.from_day.isoformat()

        name = self.name

        accounts = self.accounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "id": id,
                "from_day": from_day,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = BillingProfileScopeItemKind._read(d.pop("kind"))

        id = UUID(d.pop("id"))

        from_day = isoparse(d.pop("from_day")).date()

        name = d.pop("name", UNSET)

        accounts = d.pop("accounts", UNSET)

        billing_profile_scope_item = cls(
            kind=kind,
            id=id,
            from_day=from_day,
            name=name,
            accounts=accounts,
        )

        billing_profile_scope_item.additional_properties = d
        return billing_profile_scope_item

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
