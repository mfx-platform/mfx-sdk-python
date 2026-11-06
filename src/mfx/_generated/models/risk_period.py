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

from ..models.risk_period_kind import RiskPeriodKind
from ..models.risk_period_state import RiskPeriodState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_period_stats import RiskPeriodStats


T = TypeVar("T", bound="RiskPeriod")


@_attrs_define
class RiskPeriod:
    """
    Attributes:
        kind (RiskPeriodKind): day and week are 24 h and 7 days from the start; date and the -to-date kinds are calendar
            periods on the challenge's clock; lifetime never resets
        start (datetime.datetime):
        end (Union[None, datetime.datetime]):
        state (RiskPeriodState):
        stats (RiskPeriodStats):
    """

    kind: RiskPeriodKind
    start: datetime.datetime
    end: Union[None, datetime.datetime]
    state: RiskPeriodState
    stats: "RiskPeriodStats"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_period_stats import RiskPeriodStats

        kind = self.kind.value

        start = self.start.isoformat()

        end: Union[None, str]
        if isinstance(self.end, datetime.datetime):
            end = self.end.isoformat()
        else:
            end = self.end

        state = self.state.value

        stats = self.stats.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "start": start,
                "end": end,
                "state": state,
                "stats": stats,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_period_stats import RiskPeriodStats

        d = dict(src_dict)
        kind = RiskPeriodKind(d.pop("kind"))

        start = isoparse(d.pop("start"))

        def _parse_end(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_type_0 = isoparse(data)

                return end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        end = _parse_end(d.pop("end"))

        state = RiskPeriodState(d.pop("state"))

        stats = RiskPeriodStats.from_dict(d.pop("stats"))

        risk_period = cls(
            kind=kind,
            start=start,
            end=end,
            state=state,
            stats=stats,
        )

        risk_period.additional_properties = d
        return risk_period

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
