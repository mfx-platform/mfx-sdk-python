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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskCoverageSummaryNotHealthyItem")


@_attrs_define
class RiskCoverageSummaryNotHealthyItem:
    """
    Attributes:
        terminal_id (UUID):
        kind (str):
        state (str):
        reason (Union[None, str]):
    """

    terminal_id: UUID
    kind: str
    state: str
    reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_id = str(self.terminal_id)

        kind = self.kind

        state = self.state

        reason: Union[None, str]
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "kind": kind,
                "state": state,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        kind = d.pop("kind")

        state = d.pop("state")

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        risk_coverage_summary_not_healthy_item = cls(
            terminal_id=terminal_id,
            kind=kind,
            state=state,
            reason=reason,
        )

        risk_coverage_summary_not_healthy_item.additional_properties = d
        return risk_coverage_summary_not_healthy_item

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
