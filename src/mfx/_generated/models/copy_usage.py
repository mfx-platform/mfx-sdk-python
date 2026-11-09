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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_limit import UsageLimit


T = TypeVar("T", bound="CopyUsage")


@_attrs_define
class CopyUsage:
    """Copy Trading's limits of your plan. Copied orders are counted here and are limited by these, not by commands_per_s:
    one leader deal may be copied to more followers at once than the command burst allows.

        Attributes:
            leaders (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies it yet,
                and how much of it is in use where that is measured. Under `key` it is the figure for the calling key; under
                `tenant` the ceiling for all the tenant's keys together.
            followers (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies it
                yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
                under `tenant` the ceiling for all the tenant's keys together.
            signals_per_day (UsageLimit): One limit: the figure in force, where it comes from, whether the platform applies
                it yet, and how much of it is in use where that is measured. Under `key` it is the figure for the calling key;
                under `tenant` the ceiling for all the tenant's keys together.
            log_retention_days (Union[None, int]): How long the copy log keeps a row; null when your contract sets it
            copied_commands_today (Union[None, int]): Orders copied in the current UTC day; null where not yet measured
    """

    leaders: "UsageLimit"
    followers: "UsageLimit"
    signals_per_day: "UsageLimit"
    log_retention_days: Union[None, int]
    copied_commands_today: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_limit import UsageLimit

        leaders = self.leaders.to_dict()

        followers = self.followers.to_dict()

        signals_per_day = self.signals_per_day.to_dict()

        log_retention_days: Union[None, int]
        log_retention_days = self.log_retention_days

        copied_commands_today: Union[None, int]
        copied_commands_today = self.copied_commands_today

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "leaders": leaders,
                "followers": followers,
                "signals_per_day": signals_per_day,
                "log_retention_days": log_retention_days,
                "copied_commands_today": copied_commands_today,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_limit import UsageLimit

        d = dict(src_dict)
        leaders = UsageLimit.from_dict(d.pop("leaders"))

        followers = UsageLimit.from_dict(d.pop("followers"))

        signals_per_day = UsageLimit.from_dict(d.pop("signals_per_day"))

        def _parse_log_retention_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        log_retention_days = _parse_log_retention_days(d.pop("log_retention_days"))

        def _parse_copied_commands_today(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        copied_commands_today = _parse_copied_commands_today(d.pop("copied_commands_today"))

        copy_usage = cls(
            leaders=leaders,
            followers=followers,
            signals_per_day=signals_per_day,
            log_retention_days=log_retention_days,
            copied_commands_today=copied_commands_today,
        )

        copy_usage.additional_properties = d
        return copy_usage

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
