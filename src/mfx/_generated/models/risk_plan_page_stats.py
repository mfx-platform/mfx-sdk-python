from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPlanPageStats")


@_attrs_define
class RiskPlanPageStats:
    """The filtered set

    Attributes:
        plans (int):
        draft (int):
        armed (int):
        managing (int):
        paused (int):
        completed (int):
        failed (int):
        ended (int):
    """

    plans: int
    draft: int
    armed: int
    managing: int
    paused: int
    completed: int
    failed: int
    ended: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plans = self.plans

        draft = self.draft

        armed = self.armed

        managing = self.managing

        paused = self.paused

        completed = self.completed

        failed = self.failed

        ended = self.ended

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plans": plans,
                "draft": draft,
                "armed": armed,
                "managing": managing,
                "paused": paused,
                "completed": completed,
                "failed": failed,
                "ended": ended,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plans = d.pop("plans")

        draft = d.pop("draft")

        armed = d.pop("armed")

        managing = d.pop("managing")

        paused = d.pop("paused")

        completed = d.pop("completed")

        failed = d.pop("failed")

        ended = d.pop("ended")

        risk_plan_page_stats = cls(
            plans=plans,
            draft=draft,
            armed=armed,
            managing=managing,
            paused=paused,
            completed=completed,
            failed=failed,
            ended=ended,
        )

        risk_plan_page_stats.additional_properties = d
        return risk_plan_page_stats

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
