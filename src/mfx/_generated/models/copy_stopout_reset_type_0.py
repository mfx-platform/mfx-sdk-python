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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyStopoutResetType0")


@_attrs_define
class CopyStopoutResetType0:
    """Who reset it, when and why; null unless reset

    Attributes:
        by (str):
        at (datetime.datetime):
        reason (str):
    """

    by: str
    at: datetime.datetime
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        by = self.by

        at = self.at.isoformat()

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "by": by,
                "at": at,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        by = d.pop("by")

        at = isoparse(d.pop("at"))

        reason = d.pop("reason")

        copy_stopout_reset_type_0 = cls(
            by=by,
            at=at,
            reason=reason,
        )

        copy_stopout_reset_type_0.additional_properties = d
        return copy_stopout_reset_type_0

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
