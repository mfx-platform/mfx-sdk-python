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

from ..models.risk_programme_result_result import RiskProgrammeResultResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskProgrammeResult")


@_attrs_define
class RiskProgrammeResult:
    """`data` of `risk.programme_result`: an enrolled account passed, failed or ended

    Attributes:
        schema_version (str):
        challenge_id (UUID):
        version (int):
        terminal_id (UUID):
        result (RiskProgrammeResultResult):
        rule (Union[None, str]):
        at (datetime.datetime):
    """

    schema_version: str
    challenge_id: UUID
    version: int
    terminal_id: UUID
    result: RiskProgrammeResultResult
    rule: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        challenge_id = str(self.challenge_id)

        version = self.version

        terminal_id = str(self.terminal_id)

        result = self.result.value

        rule: Union[None, str]
        rule = self.rule

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "challenge_id": challenge_id,
                "version": version,
                "terminal_id": terminal_id,
                "result": result,
                "rule": rule,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        challenge_id = UUID(d.pop("challenge_id"))

        version = d.pop("version")

        terminal_id = UUID(d.pop("terminal_id"))

        result = RiskProgrammeResultResult(d.pop("result"))

        def _parse_rule(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rule = _parse_rule(d.pop("rule"))

        at = isoparse(d.pop("at"))

        risk_programme_result = cls(
            schema_version=schema_version,
            challenge_id=challenge_id,
            version=version,
            terminal_id=terminal_id,
            result=result,
            rule=rule,
            at=at,
        )

        risk_programme_result.additional_properties = d
        return risk_programme_result

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
