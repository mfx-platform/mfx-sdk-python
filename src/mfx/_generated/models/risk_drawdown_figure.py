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

from ..models.risk_drawdown_figure_kind import RiskDrawdownFigureKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskDrawdownFigure")


@_attrs_define
class RiskDrawdownFigure:
    """
    Attributes:
        used (Union[None, str]):
        limit (Union[None, str]):
        warn_at (Union[None, str]):
        act_at (Union[None, str]):
        kind (RiskDrawdownFigureKind):
        peak (Union[None, str]):
        peak_at (Union[None, datetime.datetime]):
        initial (str):
    """

    used: Union[None, str]
    limit: Union[None, str]
    warn_at: Union[None, str]
    act_at: Union[None, str]
    kind: RiskDrawdownFigureKind
    peak: Union[None, str]
    peak_at: Union[None, datetime.datetime]
    initial: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used: Union[None, str]
        used = self.used

        limit: Union[None, str]
        limit = self.limit

        warn_at: Union[None, str]
        warn_at = self.warn_at

        act_at: Union[None, str]
        act_at = self.act_at

        kind = self.kind.value

        peak: Union[None, str]
        peak = self.peak

        peak_at: Union[None, str]
        if isinstance(self.peak_at, datetime.datetime):
            peak_at = self.peak_at.isoformat()
        else:
            peak_at = self.peak_at

        initial = self.initial

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "limit": limit,
                "warn_at": warn_at,
                "act_at": act_at,
                "kind": kind,
                "peak": peak,
                "peak_at": peak_at,
                "initial": initial,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        used = _parse_used(d.pop("used"))

        def _parse_limit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit = _parse_limit(d.pop("limit"))

        def _parse_warn_at(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        warn_at = _parse_warn_at(d.pop("warn_at"))

        def _parse_act_at(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        act_at = _parse_act_at(d.pop("act_at"))

        kind = RiskDrawdownFigureKind(d.pop("kind"))

        def _parse_peak(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        peak = _parse_peak(d.pop("peak"))

        def _parse_peak_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                peak_at_type_0 = isoparse(data)

                return peak_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        peak_at = _parse_peak_at(d.pop("peak_at"))

        initial = d.pop("initial")

        risk_drawdown_figure = cls(
            used=used,
            limit=limit,
            warn_at=warn_at,
            act_at=act_at,
            kind=kind,
            peak=peak,
            peak_at=peak_at,
            initial=initial,
        )

        risk_drawdown_figure.additional_properties = d
        return risk_drawdown_figure

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
