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

if TYPE_CHECKING:
    from ..models.risk_proposed_order import RiskProposedOrder


T = TypeVar("T", bound="RiskCheckRequest")


@_attrs_define
class RiskCheckRequest:
    """
    Attributes:
        terminal_id (UUID):
        order (RiskProposedOrder):
    """

    terminal_id: UUID
    order: "RiskProposedOrder"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_proposed_order import RiskProposedOrder

        terminal_id = str(self.terminal_id)

        order = self.order.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "order": order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_proposed_order import RiskProposedOrder

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        order = RiskProposedOrder.from_dict(d.pop("order"))

        risk_check_request = cls(
            terminal_id=terminal_id,
            order=order,
        )

        risk_check_request.additional_properties = d
        return risk_check_request

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
