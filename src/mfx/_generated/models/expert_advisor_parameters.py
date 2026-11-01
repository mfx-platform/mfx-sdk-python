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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.expert_advisor_parameters_params import ExpertAdvisorParametersParams


T = TypeVar("T", bound="ExpertAdvisorParameters")


@_attrs_define
class ExpertAdvisorParameters:
    """The newest parameter set for a terminal, and how far its EA has taken it up

    Attributes:
        terminal_id (UUID):
        version (int): Assigned by the platform; one more than the set before
        enabled (bool):
        params (ExpertAdvisorParametersParams):
        accepted_at (datetime.datetime):
        applied_version (Union[None, int]): The version your EA last said it runs, from its heartbeat line as the
            terminal reported it; null until it has said
        applied_seen_at (Union[None, datetime.datetime]): When the platform first heard that applied_version
        converged (bool): True when applied_version equals version. False past the grace window (60 s unless an operator
            changed it) raises the terminal condition EaParamsNotApplied
    """

    terminal_id: UUID
    version: int
    enabled: bool
    params: "ExpertAdvisorParametersParams"
    accepted_at: datetime.datetime
    applied_version: Union[None, int]
    applied_seen_at: Union[None, datetime.datetime]
    converged: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.expert_advisor_parameters_params import (
            ExpertAdvisorParametersParams,
        )

        terminal_id = str(self.terminal_id)

        version = self.version

        enabled = self.enabled

        params = self.params.to_dict()

        accepted_at = self.accepted_at.isoformat()

        applied_version: Union[None, int]
        applied_version = self.applied_version

        applied_seen_at: Union[None, str]
        if isinstance(self.applied_seen_at, datetime.datetime):
            applied_seen_at = self.applied_seen_at.isoformat()
        else:
            applied_seen_at = self.applied_seen_at

        converged = self.converged

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "version": version,
                "enabled": enabled,
                "params": params,
                "accepted_at": accepted_at,
                "applied_version": applied_version,
                "applied_seen_at": applied_seen_at,
                "converged": converged,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.expert_advisor_parameters_params import (
            ExpertAdvisorParametersParams,
        )

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        version = d.pop("version")

        enabled = d.pop("enabled")

        params = ExpertAdvisorParametersParams.from_dict(d.pop("params"))

        accepted_at = isoparse(d.pop("accepted_at"))

        def _parse_applied_version(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        applied_version = _parse_applied_version(d.pop("applied_version"))

        def _parse_applied_seen_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applied_seen_at_type_0 = isoparse(data)

                return applied_seen_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        applied_seen_at = _parse_applied_seen_at(d.pop("applied_seen_at"))

        converged = d.pop("converged")

        expert_advisor_parameters = cls(
            terminal_id=terminal_id,
            version=version,
            enabled=enabled,
            params=params,
            accepted_at=accepted_at,
            applied_version=applied_version,
            applied_seen_at=applied_seen_at,
            converged=converged,
        )

        expert_advisor_parameters.additional_properties = d
        return expert_advisor_parameters

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
