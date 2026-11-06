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

T = TypeVar("T", bound="RiskExposure")


@_attrs_define
class RiskExposure:
    """
    Attributes:
        gross_limit (Union[Unset, str]):
        per_symbol_limit (Union[Unset, str]):
        include_pending (Union[Unset, bool]):
        max_positions (Union[Unset, int]):
        max_pending (Union[Unset, int]):
    """

    gross_limit: Union[Unset, str] = UNSET
    per_symbol_limit: Union[Unset, str] = UNSET
    include_pending: Union[Unset, bool] = UNSET
    max_positions: Union[Unset, int] = UNSET
    max_pending: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gross_limit = self.gross_limit

        per_symbol_limit = self.per_symbol_limit

        include_pending = self.include_pending

        max_positions = self.max_positions

        max_pending = self.max_pending

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if gross_limit is not UNSET:
            field_dict["gross_limit"] = gross_limit
        if per_symbol_limit is not UNSET:
            field_dict["per_symbol_limit"] = per_symbol_limit
        if include_pending is not UNSET:
            field_dict["include_pending"] = include_pending
        if max_positions is not UNSET:
            field_dict["max_positions"] = max_positions
        if max_pending is not UNSET:
            field_dict["max_pending"] = max_pending

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gross_limit = d.pop("gross_limit", UNSET)

        per_symbol_limit = d.pop("per_symbol_limit", UNSET)

        include_pending = d.pop("include_pending", UNSET)

        max_positions = d.pop("max_positions", UNSET)

        max_pending = d.pop("max_pending", UNSET)

        risk_exposure = cls(
            gross_limit=gross_limit,
            per_symbol_limit=per_symbol_limit,
            include_pending=include_pending,
            max_positions=max_positions,
            max_pending=max_pending,
        )

        risk_exposure.additional_properties = d
        return risk_exposure

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
