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

from ..models.risk_plan_state import RiskPlanState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_plan_step import RiskPlanStep


T = TypeVar("T", bound="RiskPlan")


@_attrs_define
class RiskPlan:
    """
    Attributes:
        id (UUID):
        terminal_id (UUID):
        ticket (Union[None, str]): null until the order becomes a position
        version (int):
        state (RiskPlanState):
        one_r (Union[None, str]): The initial risk in money, recorded at arm; never redefined
        entry_price (Union[None, str]):
        initial_sl (Union[None, str]):
        original_volume (Union[None, str]):
        steps (list['RiskPlanStep']):
        command_id (Union[None, UUID]): The command that placed the order, when the plan came with one
        created_at (datetime.datetime):
        reason (Union[None, Unset, str]): Why paused, failed or ended: stop_changed, position_closed, terminal_retired,
            by_tenant
    """

    id: UUID
    terminal_id: UUID
    ticket: Union[None, str]
    version: int
    state: RiskPlanState
    one_r: Union[None, str]
    entry_price: Union[None, str]
    initial_sl: Union[None, str]
    original_volume: Union[None, str]
    steps: list["RiskPlanStep"]
    command_id: Union[None, UUID]
    created_at: datetime.datetime
    reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_plan_step import RiskPlanStep

        id = str(self.id)

        terminal_id = str(self.terminal_id)

        ticket: Union[None, str]
        ticket = self.ticket

        version = self.version

        state = self.state.value

        one_r: Union[None, str]
        one_r = self.one_r

        entry_price: Union[None, str]
        entry_price = self.entry_price

        initial_sl: Union[None, str]
        initial_sl = self.initial_sl

        original_volume: Union[None, str]
        original_volume = self.original_volume

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        created_at = self.created_at.isoformat()

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "terminal_id": terminal_id,
                "ticket": ticket,
                "version": version,
                "state": state,
                "one_r": one_r,
                "entry_price": entry_price,
                "initial_sl": initial_sl,
                "original_volume": original_volume,
                "steps": steps,
                "command_id": command_id,
                "created_at": created_at,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_plan_step import RiskPlanStep

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        terminal_id = UUID(d.pop("terminal_id"))

        def _parse_ticket(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ticket = _parse_ticket(d.pop("ticket"))

        version = d.pop("version")

        state = RiskPlanState(d.pop("state"))

        def _parse_one_r(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        one_r = _parse_one_r(d.pop("one_r"))

        def _parse_entry_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        entry_price = _parse_entry_price(d.pop("entry_price"))

        def _parse_initial_sl(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        initial_sl = _parse_initial_sl(d.pop("initial_sl"))

        def _parse_original_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        original_volume = _parse_original_volume(d.pop("original_volume"))

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = RiskPlanStep.from_dict(steps_item_data)

            steps.append(steps_item)

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

        created_at = isoparse(d.pop("created_at"))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        risk_plan = cls(
            id=id,
            terminal_id=terminal_id,
            ticket=ticket,
            version=version,
            state=state,
            one_r=one_r,
            entry_price=entry_price,
            initial_sl=initial_sl,
            original_volume=original_volume,
            steps=steps,
            command_id=command_id,
            created_at=created_at,
            reason=reason,
        )

        risk_plan.additional_properties = d
        return risk_plan

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
