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

if TYPE_CHECKING:
    from ..models.copy_limits_use_limits_item import CopyLimitsUseLimitsItem


T = TypeVar("T", bound="CopyLimitsUse")


@_attrs_define
class CopyLimitsUse:
    """
    Attributes:
        as_of (datetime.datetime): When the platform heard it from the copy host
        limits (list['CopyLimitsUseLimitsItem']): Each limit measured within the last 180 seconds; a follower with none
            measured that recently has limits_use null, never stale figures
    """

    as_of: datetime.datetime
    limits: list["CopyLimitsUseLimitsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_limits_use_limits_item import CopyLimitsUseLimitsItem

        as_of = self.as_of.isoformat()

        limits = []
        for limits_item_data in self.limits:
            limits_item = limits_item_data.to_dict()
            limits.append(limits_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "as_of": as_of,
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_limits_use_limits_item import CopyLimitsUseLimitsItem

        d = dict(src_dict)
        as_of = isoparse(d.pop("as_of"))

        limits = []
        _limits = d.pop("limits")
        for limits_item_data in _limits:
            limits_item = CopyLimitsUseLimitsItem.from_dict(limits_item_data)

            limits.append(limits_item)

        copy_limits_use = cls(
            as_of=as_of,
            limits=limits,
        )

        copy_limits_use.additional_properties = d
        return copy_limits_use

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
