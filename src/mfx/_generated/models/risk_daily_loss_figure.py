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

from ..models.risk_daily_loss_figure_basis import RiskDailyLossFigureBasis
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskDailyLossFigure")


@_attrs_define
class RiskDailyLossFigure:
    """
    Attributes:
        used (Union[None, str]):
        limit (Union[None, str]):
        warn_at (Union[None, str]):
        act_at (Union[None, str]):
        reference (Union[None, str]):
        basis (RiskDailyLossFigureBasis):
        day_start_at (Union[None, datetime.datetime]):
        next_reset_at (Union[None, datetime.datetime]):
        late (bool): The day's first read came after the reset's late line; start_balance was rebuilt from deal history
    """

    used: Union[None, str]
    limit: Union[None, str]
    warn_at: Union[None, str]
    act_at: Union[None, str]
    reference: Union[None, str]
    basis: RiskDailyLossFigureBasis
    day_start_at: Union[None, datetime.datetime]
    next_reset_at: Union[None, datetime.datetime]
    late: bool
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

        reference: Union[None, str]
        reference = self.reference

        basis = self.basis.value

        day_start_at: Union[None, str]
        if isinstance(self.day_start_at, datetime.datetime):
            day_start_at = self.day_start_at.isoformat()
        else:
            day_start_at = self.day_start_at

        next_reset_at: Union[None, str]
        if isinstance(self.next_reset_at, datetime.datetime):
            next_reset_at = self.next_reset_at.isoformat()
        else:
            next_reset_at = self.next_reset_at

        late = self.late

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "limit": limit,
                "warn_at": warn_at,
                "act_at": act_at,
                "reference": reference,
                "basis": basis,
                "day_start_at": day_start_at,
                "next_reset_at": next_reset_at,
                "late": late,
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

        def _parse_reference(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reference = _parse_reference(d.pop("reference"))

        basis = RiskDailyLossFigureBasis(d.pop("basis"))

        def _parse_day_start_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                day_start_at_type_0 = isoparse(data)

                return day_start_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        day_start_at = _parse_day_start_at(d.pop("day_start_at"))

        def _parse_next_reset_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_reset_at_type_0 = isoparse(data)

                return next_reset_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_reset_at = _parse_next_reset_at(d.pop("next_reset_at"))

        late = d.pop("late")

        risk_daily_loss_figure = cls(
            used=used,
            limit=limit,
            warn_at=warn_at,
            act_at=act_at,
            reference=reference,
            basis=basis,
            day_start_at=day_start_at,
            next_reset_at=next_reset_at,
            late=late,
        )

        risk_daily_loss_figure.additional_properties = d
        return risk_daily_loss_figure

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
