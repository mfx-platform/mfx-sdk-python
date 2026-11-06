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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_period import RiskPeriod


T = TypeVar("T", bound="RiskPeriodClosed")


@_attrs_define
class RiskPeriodClosed:
    """`data` of `risk.period_closed`: one period of one enrolled account, with its statistics

    Attributes:
        schema_version (str):
        challenge_id (UUID):
        terminal_id (UUID):
        period (RiskPeriod):
        at (datetime.datetime):
    """

    schema_version: str
    challenge_id: UUID
    terminal_id: UUID
    period: "RiskPeriod"
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_period import RiskPeriod

        schema_version = self.schema_version

        challenge_id = str(self.challenge_id)

        terminal_id = str(self.terminal_id)

        period = self.period.to_dict()

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "challenge_id": challenge_id,
                "terminal_id": terminal_id,
                "period": period,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_period import RiskPeriod

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        challenge_id = UUID(d.pop("challenge_id"))

        terminal_id = UUID(d.pop("terminal_id"))

        period = RiskPeriod.from_dict(d.pop("period"))

        at = isoparse(d.pop("at"))

        risk_period_closed = cls(
            schema_version=schema_version,
            challenge_id=challenge_id,
            terminal_id=terminal_id,
            period=period,
            at=at,
        )

        risk_period_closed.additional_properties = d
        return risk_period_closed

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
