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

from ..models.copy_limit_kind import CopyLimitKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyLimitsUseLimitsItem")


@_attrs_define
class CopyLimitsUseLimitsItem:
    """
    Attributes:
        limit (CopyLimitKind):
        used (str): The loss counted against the limit in its period, in the account's currency
        allowed (str): What the limit allows in its period, in the account's currency
        period_start (datetime.datetime):
        as_of (datetime.datetime): When the copy host's read of the account measured it (when the platform heard it,
            from a host that does not say)
    """

    limit: CopyLimitKind
    used: str
    allowed: str
    period_start: datetime.datetime
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit.value

        used = self.used

        allowed = self.allowed

        period_start = self.period_start.isoformat()

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "used": used,
                "allowed": allowed,
                "period_start": period_start,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = CopyLimitKind._read(d.pop("limit"))

        used = d.pop("used")

        allowed = d.pop("allowed")

        period_start = isoparse(d.pop("period_start"))

        as_of = isoparse(d.pop("as_of"))

        copy_limits_use_limits_item = cls(
            limit=limit,
            used=used,
            allowed=allowed,
            period_start=period_start,
            as_of=as_of,
        )

        copy_limits_use_limits_item.additional_properties = d
        return copy_limits_use_limits_item

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
