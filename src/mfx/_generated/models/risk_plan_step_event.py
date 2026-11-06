import datetime
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
from dateutil.parser import isoparse

from ..models.risk_plan_step_event_plan_state import RiskPlanStepEventPlanState
from ..models.risk_plan_step_event_state_type_1 import RiskPlanStepEventStateType1
from ..models.risk_plan_step_event_state_type_2_type_1 import (
    RiskPlanStepEventStateType2Type1,
)
from ..models.risk_plan_step_event_state_type_3_type_1 import (
    RiskPlanStepEventStateType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPlanStepEvent")


@_attrs_define
class RiskPlanStepEvent:
    """`data` of `risk.plan_step`: a step changed state, or the plan did

    Attributes:
        schema_version (str):
        plan_id (UUID):
        terminal_id (UUID):
        ticket (Union[None, str]):
        version (int):
        step (Union[None, int]):
        state (Union[None, RiskPlanStepEventStateType1, RiskPlanStepEventStateType2Type1,
            RiskPlanStepEventStateType3Type1]):
        plan_state (RiskPlanStepEventPlanState):
        outcome (Union[None, str]):
        at (datetime.datetime):
    """

    schema_version: str
    plan_id: UUID
    terminal_id: UUID
    ticket: Union[None, str]
    version: int
    step: Union[None, int]
    state: Union[
        None,
        RiskPlanStepEventStateType1,
        RiskPlanStepEventStateType2Type1,
        RiskPlanStepEventStateType3Type1,
    ]
    plan_state: RiskPlanStepEventPlanState
    outcome: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        plan_id = str(self.plan_id)

        terminal_id = str(self.terminal_id)

        ticket: Union[None, str]
        ticket = self.ticket

        version = self.version

        step: Union[None, int]
        step = self.step

        state: Union[None, str]
        if isinstance(self.state, RiskPlanStepEventStateType1):
            state = self.state.value
        elif isinstance(self.state, RiskPlanStepEventStateType2Type1):
            state = self.state.value
        elif isinstance(self.state, RiskPlanStepEventStateType3Type1):
            state = self.state.value
        else:
            state = self.state

        plan_state = self.plan_state.value

        outcome: Union[None, str]
        outcome = self.outcome

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "plan_id": plan_id,
                "terminal_id": terminal_id,
                "ticket": ticket,
                "version": version,
                "step": step,
                "state": state,
                "plan_state": plan_state,
                "outcome": outcome,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        plan_id = UUID(d.pop("plan_id"))

        terminal_id = UUID(d.pop("terminal_id"))

        def _parse_ticket(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ticket = _parse_ticket(d.pop("ticket"))

        version = d.pop("version")

        def _parse_step(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        step = _parse_step(d.pop("step"))

        def _parse_state(
            data: object,
        ) -> Union[
            None,
            RiskPlanStepEventStateType1,
            RiskPlanStepEventStateType2Type1,
            RiskPlanStepEventStateType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_1 = RiskPlanStepEventStateType1(data)

                return state_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_2_type_1 = RiskPlanStepEventStateType2Type1(data)

                return state_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_3_type_1 = RiskPlanStepEventStateType3Type1(data)

                return state_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    RiskPlanStepEventStateType1,
                    RiskPlanStepEventStateType2Type1,
                    RiskPlanStepEventStateType3Type1,
                ],
                data,
            )

        state = _parse_state(d.pop("state"))

        plan_state = RiskPlanStepEventPlanState(d.pop("plan_state"))

        def _parse_outcome(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        outcome = _parse_outcome(d.pop("outcome"))

        at = isoparse(d.pop("at"))

        risk_plan_step_event = cls(
            schema_version=schema_version,
            plan_id=plan_id,
            terminal_id=terminal_id,
            ticket=ticket,
            version=version,
            step=step,
            state=state,
            plan_state=plan_state,
            outcome=outcome,
            at=at,
        )

        risk_plan_step_event.additional_properties = d
        return risk_plan_step_event

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
