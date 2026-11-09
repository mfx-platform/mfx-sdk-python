from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkActionCounts")


@_attrs_define
class BulkActionCounts:
    """
    Attributes:
        queued (int):
        running (int):
        succeeded (int):
        failed (int): Ended without succeeding: FAILED, NOT_STARTED
        cancelled (int):
    """

    queued: int
    running: int
    succeeded: int
    failed: int
    cancelled: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queued = self.queued

        running = self.running

        succeeded = self.succeeded

        failed = self.failed

        cancelled = self.cancelled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queued": queued,
                "running": running,
                "succeeded": succeeded,
                "failed": failed,
                "cancelled": cancelled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        queued = d.pop("queued")

        running = d.pop("running")

        succeeded = d.pop("succeeded")

        failed = d.pop("failed")

        cancelled = d.pop("cancelled")

        bulk_action_counts = cls(
            queued=queued,
            running=running,
            succeeded=succeeded,
            failed=failed,
            cancelled=cancelled,
        )

        bulk_action_counts.additional_properties = d
        return bulk_action_counts

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
