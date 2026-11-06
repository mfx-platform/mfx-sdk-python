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

from ..models.risk_schedule_windows_item_days_item import (
    RiskScheduleWindowsItemDaysItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskScheduleWindowsItem")


@_attrs_define
class RiskScheduleWindowsItem:
    """
    Attributes:
        days (list[RiskScheduleWindowsItemDaysItem]):
        from_ (str):
        to (str):
    """

    days: list[RiskScheduleWindowsItemDaysItem]
    from_: str
    to: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days = []
        for days_item_data in self.days:
            days_item = days_item_data.value
            days.append(days_item)

        from_ = self.from_

        to = self.to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "from": from_,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        days = []
        _days = d.pop("days")
        for days_item_data in _days:
            days_item = RiskScheduleWindowsItemDaysItem(days_item_data)

            days.append(days_item)

        from_ = d.pop("from")

        to = d.pop("to")

        risk_schedule_windows_item = cls(
            days=days,
            from_=from_,
            to=to,
        )

        risk_schedule_windows_item.additional_properties = d
        return risk_schedule_windows_item

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
