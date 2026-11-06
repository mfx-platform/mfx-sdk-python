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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPreviewRequestAssumptions")


@_attrs_define
class RiskPreviewRequestAssumptions:
    """Costs the specification does not give, stated by the caller

    Attributes:
        commission_per_lot_round_trip (Union[Unset, str]):
    """

    commission_per_lot_round_trip: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        commission_per_lot_round_trip = self.commission_per_lot_round_trip

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commission_per_lot_round_trip is not UNSET:
            field_dict["commission_per_lot_round_trip"] = commission_per_lot_round_trip

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        commission_per_lot_round_trip = d.pop("commission_per_lot_round_trip", UNSET)

        risk_preview_request_assumptions = cls(
            commission_per_lot_round_trip=commission_per_lot_round_trip,
        )

        risk_preview_request_assumptions.additional_properties = d
        return risk_preview_request_assumptions

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
