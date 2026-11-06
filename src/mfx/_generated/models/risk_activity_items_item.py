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

from ..models.risk_activity_items_item_outcome import RiskActivityItemsItemOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskActivityItemsItem")


@_attrs_define
class RiskActivityItemsItem:
    """
    Attributes:
        ticket (Union[None, str]):
        command_id (Union[None, UUID]):
        outcome (RiskActivityItemsItemOutcome):
        reason (Union[None, str]):
    """

    ticket: Union[None, str]
    command_id: Union[None, UUID]
    outcome: RiskActivityItemsItemOutcome
    reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket: Union[None, str]
        ticket = self.ticket

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        outcome = self.outcome.value

        reason: Union[None, str]
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket": ticket,
                "command_id": command_id,
                "outcome": outcome,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_ticket(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ticket = _parse_ticket(d.pop("ticket"))

        def _parse_command_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                command_id_type_0 = UUID(data)

                return command_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        command_id = _parse_command_id(d.pop("command_id"))

        outcome = RiskActivityItemsItemOutcome(d.pop("outcome"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        risk_activity_items_item = cls(
            ticket=ticket,
            command_id=command_id,
            outcome=outcome,
            reason=reason,
        )

        risk_activity_items_item.additional_properties = d
        return risk_activity_items_item

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
