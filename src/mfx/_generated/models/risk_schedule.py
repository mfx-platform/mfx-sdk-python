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

from ..models.risk_schedule_mode import RiskScheduleMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_schedule_windows_item import RiskScheduleWindowsItem


T = TypeVar("T", bound="RiskSchedule")


@_attrs_define
class RiskSchedule:
    """
    Attributes:
        mode (RiskScheduleMode):
        zone (str): An IANA time zone, or broker for the broker's clock
        windows (list['RiskScheduleWindowsItem']):
    """

    mode: RiskScheduleMode
    zone: str
    windows: list["RiskScheduleWindowsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_schedule_windows_item import RiskScheduleWindowsItem

        mode = self.mode.value

        zone = self.zone

        windows = []
        for windows_item_data in self.windows:
            windows_item = windows_item_data.to_dict()
            windows.append(windows_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "zone": zone,
                "windows": windows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_schedule_windows_item import RiskScheduleWindowsItem

        d = dict(src_dict)
        mode = RiskScheduleMode(d.pop("mode"))

        zone = d.pop("zone")

        windows = []
        _windows = d.pop("windows")
        for windows_item_data in _windows:
            windows_item = RiskScheduleWindowsItem.from_dict(windows_item_data)

            windows.append(windows_item)

        risk_schedule = cls(
            mode=mode,
            zone=zone,
            windows=windows,
        )

        risk_schedule.additional_properties = d
        return risk_schedule

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
