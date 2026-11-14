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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_activity_page_stats_kinds import RiskActivityPageStatsKinds


T = TypeVar("T", bound="RiskActivityPageStats")


@_attrs_define
class RiskActivityPageStats:
    """The filtered set

    Attributes:
        rows (int):
        unresolved (int):
        kinds (RiskActivityPageStatsKinds): Rows per kind, every kind named
    """

    rows: int
    unresolved: int
    kinds: "RiskActivityPageStatsKinds"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_activity_page_stats_kinds import RiskActivityPageStatsKinds

        rows = self.rows

        unresolved = self.unresolved

        kinds = self.kinds.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rows": rows,
                "unresolved": unresolved,
                "kinds": kinds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_activity_page_stats_kinds import RiskActivityPageStatsKinds

        d = dict(src_dict)
        rows = d.pop("rows")

        unresolved = d.pop("unresolved")

        kinds = RiskActivityPageStatsKinds.from_dict(d.pop("kinds"))

        risk_activity_page_stats = cls(
            rows=rows,
            unresolved=unresolved,
            kinds=kinds,
        )

        risk_activity_page_stats.additional_properties = d
        return risk_activity_page_stats

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
