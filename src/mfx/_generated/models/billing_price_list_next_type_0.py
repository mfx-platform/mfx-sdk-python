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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_price_list_next_type_0_changes_item import (
        BillingPriceListNextType0ChangesItem,
    )


T = TypeVar("T", bound="BillingPriceListNextType0")


@_attrs_define
class BillingPriceListNextType0:
    """The next list version once it is released, with the date it starts and what changes

    Attributes:
        version (Union[Unset, str]):
        effective_from (Union[Unset, datetime.datetime]):
        changes (Union[Unset, list['BillingPriceListNextType0ChangesItem']]):
    """

    version: Union[Unset, str] = UNSET
    effective_from: Union[Unset, datetime.datetime] = UNSET
    changes: Union[Unset, list["BillingPriceListNextType0ChangesItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_price_list_next_type_0_changes_item import (
            BillingPriceListNextType0ChangesItem,
        )

        version = self.version

        effective_from: Union[Unset, str] = UNSET
        if not isinstance(self.effective_from, Unset):
            effective_from = self.effective_from.isoformat()

        changes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.changes, Unset):
            changes = []
            for changes_item_data in self.changes:
                changes_item = changes_item_data.to_dict()
                changes.append(changes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if version is not UNSET:
            field_dict["version"] = version
        if effective_from is not UNSET:
            field_dict["effective_from"] = effective_from
        if changes is not UNSET:
            field_dict["changes"] = changes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_price_list_next_type_0_changes_item import (
            BillingPriceListNextType0ChangesItem,
        )

        d = dict(src_dict)
        version = d.pop("version", UNSET)

        _effective_from = d.pop("effective_from", UNSET)
        effective_from: Union[Unset, datetime.datetime]
        if isinstance(_effective_from, Unset):
            effective_from = UNSET
        else:
            effective_from = isoparse(_effective_from)

        changes = []
        _changes = d.pop("changes", UNSET)
        for changes_item_data in _changes or []:
            changes_item = BillingPriceListNextType0ChangesItem.from_dict(changes_item_data)

            changes.append(changes_item)

        billing_price_list_next_type_0 = cls(
            version=version,
            effective_from=effective_from,
            changes=changes,
        )

        billing_price_list_next_type_0.additional_properties = d
        return billing_price_list_next_type_0

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
