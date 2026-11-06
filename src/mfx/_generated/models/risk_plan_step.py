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

from ..models.risk_plan_step_held_by import RiskPlanStepHeldBy
from ..models.risk_plan_step_state import RiskPlanStepState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_plan_step_action import RiskPlanStepAction
    from ..models.risk_plan_step_trigger import RiskPlanStepTrigger


T = TypeVar("T", bound="RiskPlanStep")


@_attrs_define
class RiskPlanStep:
    """
    Attributes:
        trigger (RiskPlanStepTrigger):
        action (RiskPlanStepAction):
        held_by (RiskPlanStepHeldBy): broker: survives MFX Hub being down. mfx: needs the cell and the terminal
        n (int):
        state (RiskPlanStepState):
        outcome (Union[None, str]): What happened, in words, with the broker's reason where there is one
        command_id (Union[None, UUID]):
    """

    trigger: "RiskPlanStepTrigger"
    action: "RiskPlanStepAction"
    held_by: RiskPlanStepHeldBy
    n: int
    state: RiskPlanStepState
    outcome: Union[None, str]
    command_id: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_plan_step_action import RiskPlanStepAction
        from ..models.risk_plan_step_trigger import RiskPlanStepTrigger

        trigger = self.trigger.to_dict()

        action = self.action.to_dict()

        held_by = self.held_by.value

        n = self.n

        state = self.state.value

        outcome: Union[None, str]
        outcome = self.outcome

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger": trigger,
                "action": action,
                "held_by": held_by,
                "n": n,
                "state": state,
                "outcome": outcome,
                "command_id": command_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_plan_step_action import RiskPlanStepAction
        from ..models.risk_plan_step_trigger import RiskPlanStepTrigger

        d = dict(src_dict)
        trigger = RiskPlanStepTrigger.from_dict(d.pop("trigger"))

        action = RiskPlanStepAction.from_dict(d.pop("action"))

        held_by = RiskPlanStepHeldBy(d.pop("held_by"))

        n = d.pop("n")

        state = RiskPlanStepState(d.pop("state"))

        def _parse_outcome(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        outcome = _parse_outcome(d.pop("outcome"))

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

        risk_plan_step = cls(
            trigger=trigger,
            action=action,
            held_by=held_by,
            n=n,
            state=state,
            outcome=outcome,
            command_id=command_id,
        )

        risk_plan_step.additional_properties = d
        return risk_plan_step

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
