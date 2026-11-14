from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskChallengeAccountPageStats")


@_attrs_define
class RiskChallengeAccountPageStats:
    """Counts over the filtered set, before paging. events_today counts the challenge's Activity rows since 00:00 UTC.

    Attributes:
        accounts (int):
        in_progress (int):
        passed (int):
        failed (int):
        ended (int):
        below_min_days (int):
        events_today (int):
    """

    accounts: int
    in_progress: int
    passed: int
    failed: int
    ended: int
    below_min_days: int
    events_today: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts

        in_progress = self.in_progress

        passed = self.passed

        failed = self.failed

        ended = self.ended

        below_min_days = self.below_min_days

        events_today = self.events_today

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "in_progress": in_progress,
                "passed": passed,
                "failed": failed,
                "ended": ended,
                "below_min_days": below_min_days,
                "events_today": events_today,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accounts = d.pop("accounts")

        in_progress = d.pop("in_progress")

        passed = d.pop("passed")

        failed = d.pop("failed")

        ended = d.pop("ended")

        below_min_days = d.pop("below_min_days")

        events_today = d.pop("events_today")

        risk_challenge_account_page_stats = cls(
            accounts=accounts,
            in_progress=in_progress,
            passed=passed,
            failed=failed,
            ended=ended,
            below_min_days=below_min_days,
            events_today=events_today,
        )

        risk_challenge_account_page_stats.additional_properties = d
        return risk_challenge_account_page_stats

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
