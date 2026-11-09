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
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.terminal_queue_reason_type_1 import TerminalQueueReasonType1
from ..models.terminal_queue_reason_type_2_type_1 import TerminalQueueReasonType2Type1
from ..models.terminal_queue_reason_type_3_type_1 import TerminalQueueReasonType3Type1
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalQueue")


@_attrs_define
class TerminalQueue:
    """Where a QUEUED terminal waits for its start. Each cell has one line, ordered by what the platform must do first
    (stops that relieve a busy cell, then recovery, then what was asked, then background work), then by class
    (streaming, dedicated, shared), then who waited longest. The order is never changed by hand.

        Attributes:
            queued_at (datetime.datetime): When it entered its cell's line
            position (Union[None, int]): Its place in its cell's line: 1 is next. Null when the platform has no current plan
                for the cell (unknown, never 0)
            expected_start_at (Union[None, datetime.datetime]): When the last plan expects its slot, at the cell's load now:
                an expectation, not a promise. Null when unknown
            reason (Union[None, TerminalQueueReasonType1, TerminalQueueReasonType2Type1, TerminalQueueReasonType3Type1]):
                Why it waits, a coarse code: `cell_busy` its cell is busy now; `cell_settling` its cell started others a moment
                ago and lets them settle first; `cell_at_stop_line` its cell is at its limit and starts nothing new until it is
                lighter; `cell_silent` its cell has not reported for a minute; `broker_budget` the broker's logins a minute are
                spent; `broker_cap` the broker has as many logins in flight as it takes; `broker_maintenance` the broker is in
                maintenance; `platform_ceiling` the platform's own limit; `backoff` waiting after a failed attempt; `bulk_pace`
                a bulk action's items go at the pace of their cells. Never a figure, never the cell. Null when nothing holds it
                but its place in line
    """

    queued_at: datetime.datetime
    position: Union[None, int]
    expected_start_at: Union[None, datetime.datetime]
    reason: Union[
        None, TerminalQueueReasonType1, TerminalQueueReasonType2Type1, TerminalQueueReasonType3Type1
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queued_at = self.queued_at.isoformat()

        position: Union[None, int]
        position = self.position

        expected_start_at: Union[None, str]
        if isinstance(self.expected_start_at, datetime.datetime):
            expected_start_at = self.expected_start_at.isoformat()
        else:
            expected_start_at = self.expected_start_at

        reason: Union[None, str]
        if isinstance(self.reason, TerminalQueueReasonType1):
            reason = self.reason.value
        elif isinstance(self.reason, TerminalQueueReasonType2Type1):
            reason = self.reason.value
        elif isinstance(self.reason, TerminalQueueReasonType3Type1):
            reason = self.reason.value
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queued_at": queued_at,
                "position": position,
                "expected_start_at": expected_start_at,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        queued_at = isoparse(d.pop("queued_at"))

        def _parse_position(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        position = _parse_position(d.pop("position"))

        def _parse_expected_start_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expected_start_at_type_0 = isoparse(data)

                return expected_start_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expected_start_at = _parse_expected_start_at(d.pop("expected_start_at"))

        def _parse_reason(
            data: object,
        ) -> Union[
            None,
            TerminalQueueReasonType1,
            TerminalQueueReasonType2Type1,
            TerminalQueueReasonType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = TerminalQueueReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = TerminalQueueReasonType2Type1(data)

                return reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = TerminalQueueReasonType3Type1(data)

                return reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TerminalQueueReasonType1,
                    TerminalQueueReasonType2Type1,
                    TerminalQueueReasonType3Type1,
                ],
                data,
            )

        reason = _parse_reason(d.pop("reason"))

        terminal_queue = cls(
            queued_at=queued_at,
            position=position,
            expected_start_at=expected_start_at,
            reason=reason,
        )

        terminal_queue.additional_properties = d
        return terminal_queue

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
