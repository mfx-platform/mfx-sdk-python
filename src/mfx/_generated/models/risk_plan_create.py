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
    from ..models.risk_plan_step_spec import RiskPlanStepSpec
    from ..models.risk_proposed_order import RiskProposedOrder


T = TypeVar("T", bound="RiskPlanCreate")


@_attrs_define
class RiskPlanCreate:
    """
    Attributes:
        terminal_id (UUID):
        steps (list['RiskPlanStepSpec']):
        ticket (Union[None, Unset, str]): An open position; or give order
        order (Union[Unset, RiskProposedOrder]):
        replace (Union[Unset, bool]): Take over a position another manager holds Default: False.
    """

    terminal_id: UUID
    steps: list["RiskPlanStepSpec"]
    ticket: Union[None, Unset, str] = UNSET
    order: Union[Unset, "RiskProposedOrder"] = UNSET
    replace: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_plan_step_spec import RiskPlanStepSpec
        from ..models.risk_proposed_order import RiskProposedOrder

        terminal_id = str(self.terminal_id)

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        ticket: Union[None, Unset, str]
        if isinstance(self.ticket, Unset):
            ticket = UNSET
        else:
            ticket = self.ticket

        order: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.to_dict()

        replace = self.replace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "steps": steps,
            }
        )
        if ticket is not UNSET:
            field_dict["ticket"] = ticket
        if order is not UNSET:
            field_dict["order"] = order
        if replace is not UNSET:
            field_dict["replace"] = replace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_plan_step_spec import RiskPlanStepSpec
        from ..models.risk_proposed_order import RiskProposedOrder

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = RiskPlanStepSpec.from_dict(steps_item_data)

            steps.append(steps_item)

        def _parse_ticket(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ticket = _parse_ticket(d.pop("ticket", UNSET))

        _order = d.pop("order", UNSET)
        order: Union[Unset, RiskProposedOrder]
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = RiskProposedOrder.from_dict(_order)

        replace = d.pop("replace", UNSET)

        risk_plan_create = cls(
            terminal_id=terminal_id,
            steps=steps,
            ticket=ticket,
            order=order,
            replace=replace,
        )

        risk_plan_create.additional_properties = d
        return risk_plan_create

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
