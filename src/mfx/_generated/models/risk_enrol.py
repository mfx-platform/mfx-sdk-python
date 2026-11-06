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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskEnrol")


@_attrs_define
class RiskEnrol:
    """
    Attributes:
        terminal_ids (list[UUID]):
    """

    terminal_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_ids = []
        for terminal_ids_item_data in self.terminal_ids:
            terminal_ids_item = str(terminal_ids_item_data)
            terminal_ids.append(terminal_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_ids": terminal_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_ids = []
        _terminal_ids = d.pop("terminal_ids")
        for terminal_ids_item_data in _terminal_ids:
            terminal_ids_item = UUID(terminal_ids_item_data)

            terminal_ids.append(terminal_ids_item)

        risk_enrol = cls(
            terminal_ids=terminal_ids,
        )

        risk_enrol.additional_properties = d
        return risk_enrol

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
