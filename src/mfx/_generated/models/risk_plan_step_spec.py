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

from ..models.risk_plan_step_spec_held_by import RiskPlanStepSpecHeldBy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_plan_step_spec_action import RiskPlanStepSpecAction
    from ..models.risk_plan_step_spec_trigger import RiskPlanStepSpecTrigger


T = TypeVar("T", bound="RiskPlanStepSpec")


@_attrs_define
class RiskPlanStepSpec:
    """
    Attributes:
        trigger (RiskPlanStepSpecTrigger):
        action (RiskPlanStepSpecAction):
        held_by (RiskPlanStepSpecHeldBy): broker: survives MFX Hub being down. mfx: needs the cell and the terminal
    """

    trigger: "RiskPlanStepSpecTrigger"
    action: "RiskPlanStepSpecAction"
    held_by: RiskPlanStepSpecHeldBy
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_plan_step_spec_action import RiskPlanStepSpecAction
        from ..models.risk_plan_step_spec_trigger import RiskPlanStepSpecTrigger

        trigger = self.trigger.to_dict()

        action = self.action.to_dict()

        held_by = self.held_by.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger": trigger,
                "action": action,
                "held_by": held_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_plan_step_spec_action import RiskPlanStepSpecAction
        from ..models.risk_plan_step_spec_trigger import RiskPlanStepSpecTrigger

        d = dict(src_dict)
        trigger = RiskPlanStepSpecTrigger.from_dict(d.pop("trigger"))

        action = RiskPlanStepSpecAction.from_dict(d.pop("action"))

        held_by = RiskPlanStepSpecHeldBy(d.pop("held_by"))

        risk_plan_step_spec = cls(
            trigger=trigger,
            action=action,
            held_by=held_by,
        )

        risk_plan_step_spec.additional_properties = d
        return risk_plan_step_spec

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
