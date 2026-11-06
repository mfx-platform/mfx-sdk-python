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

T = TypeVar("T", bound="RiskActionCompletedUnresolvedItem")


@_attrs_define
class RiskActionCompletedUnresolvedItem:
    """
    Attributes:
        terminal_id (UUID):
        ticket (str):
        command_id (UUID):
        reserved (Union[None, Unset, str]):
    """

    terminal_id: UUID
    ticket: str
    command_id: UUID
    reserved: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminal_id = str(self.terminal_id)

        ticket = self.ticket

        command_id = str(self.command_id)

        reserved: Union[None, Unset, str]
        if isinstance(self.reserved, Unset):
            reserved = UNSET
        else:
            reserved = self.reserved

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "ticket": ticket,
                "command_id": command_id,
            }
        )
        if reserved is not UNSET:
            field_dict["reserved"] = reserved

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        ticket = d.pop("ticket")

        command_id = UUID(d.pop("command_id"))

        def _parse_reserved(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reserved = _parse_reserved(d.pop("reserved", UNSET))

        risk_action_completed_unresolved_item = cls(
            terminal_id=terminal_id,
            ticket=ticket,
            command_id=command_id,
            reserved=reserved,
        )

        risk_action_completed_unresolved_item.additional_properties = d
        return risk_action_completed_unresolved_item

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
