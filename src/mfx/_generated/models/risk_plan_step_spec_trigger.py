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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.risk_plan_step_spec_trigger_kind import RiskPlanStepSpecTriggerKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPlanStepSpecTrigger")


@_attrs_define
class RiskPlanStepSpecTrigger:
    """
    Attributes:
        kind (RiskPlanStepSpecTriggerKind):
        value (Union[None, Unset, str]): The level in R, a price, money or percent; null for filled and after_step
        step (Union[None, Unset, int]): after_step: the step it follows
    """

    kind: RiskPlanStepSpecTriggerKind
    value: Union[None, Unset, str] = UNSET
    step: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        value: Union[None, Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        step: Union[None, Unset, int]
        if isinstance(self.step, Unset):
            step = UNSET
        else:
            step = self.step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if step is not UNSET:
            field_dict["step"] = step

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = RiskPlanStepSpecTriggerKind(d.pop("kind"))

        def _parse_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_step(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        step = _parse_step(d.pop("step", UNSET))

        risk_plan_step_spec_trigger = cls(
            kind=kind,
            value=value,
            step=step,
        )

        risk_plan_step_spec_trigger.additional_properties = d
        return risk_plan_step_spec_trigger

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
