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

from ..models.billing_last_failure_decline import BillingLastFailureDecline
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingLastFailure")


@_attrs_define
class BillingLastFailure:
    """The profile's last failed charge; null when there is none since the last success

    Attributes:
        at (datetime.datetime):
        method_id (UUID):
        method_label (str): e.g. Visa ending 4242
        decline (BillingLastFailureDecline):
        backup_tried (bool):
    """

    at: datetime.datetime
    method_id: UUID
    method_label: str
    decline: BillingLastFailureDecline
    backup_tried: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        method_id = str(self.method_id)

        method_label = self.method_label

        decline = self.decline.value

        backup_tried = self.backup_tried

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "method_id": method_id,
                "method_label": method_label,
                "decline": decline,
                "backup_tried": backup_tried,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = isoparse(d.pop("at"))

        method_id = UUID(d.pop("method_id"))

        method_label = d.pop("method_label")

        decline = BillingLastFailureDecline._read(d.pop("decline"))

        backup_tried = d.pop("backup_tried")

        billing_last_failure = cls(
            at=at,
            method_id=method_id,
            method_label=method_label,
            decline=decline,
            backup_tried=backup_tried,
        )

        billing_last_failure.additional_properties = d
        return billing_last_failure

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
