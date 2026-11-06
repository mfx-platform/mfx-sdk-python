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

if TYPE_CHECKING:
    from ..models.risk_equity_series_points_item import RiskEquitySeriesPointsItem


T = TypeVar("T", bound="RiskEquitySeries")


@_attrs_define
class RiskEquitySeries:
    """
    Attributes:
        terminal_id (UUID):
        currency (Union[None, str]):
        points (list['RiskEquitySeriesPointsItem']):
    """

    terminal_id: UUID
    currency: Union[None, str]
    points: list["RiskEquitySeriesPointsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_equity_series_points_item import RiskEquitySeriesPointsItem

        terminal_id = str(self.terminal_id)

        currency: Union[None, str]
        currency = self.currency

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "currency": currency,
                "points": points,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_equity_series_points_item import RiskEquitySeriesPointsItem

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        def _parse_currency(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        currency = _parse_currency(d.pop("currency"))

        points = []
        _points = d.pop("points")
        for points_item_data in _points:
            points_item = RiskEquitySeriesPointsItem.from_dict(points_item_data)

            points.append(points_item)

        risk_equity_series = cls(
            terminal_id=terminal_id,
            currency=currency,
            points=points,
        )

        risk_equity_series.additional_properties = d
        return risk_equity_series

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
