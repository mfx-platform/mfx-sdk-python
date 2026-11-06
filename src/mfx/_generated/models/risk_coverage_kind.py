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

from ..models.risk_coverage_kind_state import RiskCoverageKindState
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskCoverageKind")


@_attrs_define
class RiskCoverageKind:
    """
    Attributes:
        state (RiskCoverageKindState):
        reason (Union[None, str]): Why it is not healthy, in words the tenant can act on
        since (Union[None, datetime.datetime]):
    """

    state: RiskCoverageKindState
    reason: Union[None, str]
    since: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        reason: Union[None, str]
        reason = self.reason

        since: Union[None, str]
        if isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "reason": reason,
                "since": since,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = RiskCoverageKindState(d.pop("state"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_since(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        since = _parse_since(d.pop("since"))

        risk_coverage_kind = cls(
            state=state,
            reason=reason,
            since=since,
        )

        risk_coverage_kind.additional_properties = d
        return risk_coverage_kind

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
