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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.risk_coverage_changed_from import RiskCoverageChangedFrom
from ..models.risk_coverage_changed_kind import RiskCoverageChangedKind
from ..models.risk_coverage_changed_to import RiskCoverageChangedTo
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskCoverageChanged")


@_attrs_define
class RiskCoverageChanged:
    """`data` of `risk.coverage_changed`

    Attributes:
        schema_version (str):
        terminal_id (UUID):
        kind (RiskCoverageChangedKind):
        from_ (RiskCoverageChangedFrom):
        to (RiskCoverageChangedTo):
        reason (Union[None, str]):
        at (datetime.datetime):
    """

    schema_version: str
    terminal_id: UUID
    kind: RiskCoverageChangedKind
    from_: RiskCoverageChangedFrom
    to: RiskCoverageChangedTo
    reason: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        kind = self.kind.value

        from_ = self.from_.value

        to = self.to.value

        reason: Union[None, str]
        reason = self.reason

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "kind": kind,
                "from": from_,
                "to": to,
                "reason": reason,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        kind = RiskCoverageChangedKind(d.pop("kind"))

        from_ = RiskCoverageChangedFrom(d.pop("from"))

        to = RiskCoverageChangedTo(d.pop("to"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        at = isoparse(d.pop("at"))

        risk_coverage_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            kind=kind,
            from_=from_,
            to=to,
            reason=reason,
            at=at,
        )

        risk_coverage_changed.additional_properties = d
        return risk_coverage_changed

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
