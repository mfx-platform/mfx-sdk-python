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

from ..models.risk_loss_at_stops_no_stop import RiskLossAtStopsNoStop
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskLossAtStops")


@_attrs_define
class RiskLossAtStops:
    """
    Attributes:
        limit (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        no_stop (RiskLossAtStopsNoStop):
    """

    limit: "RiskAmount"
    no_stop: RiskLossAtStopsNoStop
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_amount import RiskAmount

        limit = self.limit.to_dict()

        no_stop = self.no_stop.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "limit": limit,
                "no_stop": no_stop,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        limit = RiskAmount.from_dict(d.pop("limit"))

        no_stop = RiskLossAtStopsNoStop(d.pop("no_stop"))

        risk_loss_at_stops = cls(
            limit=limit,
            no_stop=no_stop,
        )

        risk_loss_at_stops.additional_properties = d
        return risk_loss_at_stops

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
