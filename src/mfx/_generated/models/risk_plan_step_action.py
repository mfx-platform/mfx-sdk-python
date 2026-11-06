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

from ..models.risk_plan_step_action_kind import RiskPlanStepActionKind
from ..models.risk_plan_step_action_pct_of_type_1 import RiskPlanStepActionPctOfType1
from ..models.risk_plan_step_action_pct_of_type_2_type_1 import (
    RiskPlanStepActionPctOfType2Type1,
)
from ..models.risk_plan_step_action_pct_of_type_3_type_1 import (
    RiskPlanStepActionPctOfType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPlanStepAction")


@_attrs_define
class RiskPlanStepAction:
    """
    Attributes:
        kind (RiskPlanStepActionKind):
        sl (Union[None, Unset, str]): set_stops and move_stop: a price, or entry for the entry price
        tp (Union[None, Unset, str]):
        plus_costs (Union[Unset, bool]): move_stop to entry: add the known costs
        pct (Union[None, Unset, str]): close_part: percent
        pct_of (Union[None, RiskPlanStepActionPctOfType1, RiskPlanStepActionPctOfType2Type1,
            RiskPlanStepActionPctOfType3Type1, Unset]):
        distance (Union[None, Unset, str]): trail: the trailing stop's distance
    """

    kind: RiskPlanStepActionKind
    sl: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    plus_costs: Union[Unset, bool] = UNSET
    pct: Union[None, Unset, str] = UNSET
    pct_of: Union[
        None,
        RiskPlanStepActionPctOfType1,
        RiskPlanStepActionPctOfType2Type1,
        RiskPlanStepActionPctOfType3Type1,
        Unset,
    ] = UNSET
    distance: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        sl: Union[None, Unset, str]
        if isinstance(self.sl, Unset):
            sl = UNSET
        else:
            sl = self.sl

        tp: Union[None, Unset, str]
        if isinstance(self.tp, Unset):
            tp = UNSET
        else:
            tp = self.tp

        plus_costs = self.plus_costs

        pct: Union[None, Unset, str]
        if isinstance(self.pct, Unset):
            pct = UNSET
        else:
            pct = self.pct

        pct_of: Union[None, Unset, str]
        if isinstance(self.pct_of, Unset):
            pct_of = UNSET
        elif isinstance(self.pct_of, RiskPlanStepActionPctOfType1):
            pct_of = self.pct_of.value
        elif isinstance(self.pct_of, RiskPlanStepActionPctOfType2Type1):
            pct_of = self.pct_of.value
        elif isinstance(self.pct_of, RiskPlanStepActionPctOfType3Type1):
            pct_of = self.pct_of.value
        else:
            pct_of = self.pct_of

        distance: Union[None, Unset, str]
        if isinstance(self.distance, Unset):
            distance = UNSET
        else:
            distance = self.distance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if sl is not UNSET:
            field_dict["sl"] = sl
        if tp is not UNSET:
            field_dict["tp"] = tp
        if plus_costs is not UNSET:
            field_dict["plus_costs"] = plus_costs
        if pct is not UNSET:
            field_dict["pct"] = pct
        if pct_of is not UNSET:
            field_dict["pct_of"] = pct_of
        if distance is not UNSET:
            field_dict["distance"] = distance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = RiskPlanStepActionKind(d.pop("kind"))

        def _parse_sl(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sl = _parse_sl(d.pop("sl", UNSET))

        def _parse_tp(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tp = _parse_tp(d.pop("tp", UNSET))

        plus_costs = d.pop("plus_costs", UNSET)

        def _parse_pct(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pct = _parse_pct(d.pop("pct", UNSET))

        def _parse_pct_of(
            data: object,
        ) -> Union[
            None,
            RiskPlanStepActionPctOfType1,
            RiskPlanStepActionPctOfType2Type1,
            RiskPlanStepActionPctOfType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pct_of_type_1 = RiskPlanStepActionPctOfType1(data)

                return pct_of_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pct_of_type_2_type_1 = RiskPlanStepActionPctOfType2Type1(data)

                return pct_of_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pct_of_type_3_type_1 = RiskPlanStepActionPctOfType3Type1(data)

                return pct_of_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    RiskPlanStepActionPctOfType1,
                    RiskPlanStepActionPctOfType2Type1,
                    RiskPlanStepActionPctOfType3Type1,
                    Unset,
                ],
                data,
            )

        pct_of = _parse_pct_of(d.pop("pct_of", UNSET))

        def _parse_distance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        distance = _parse_distance(d.pop("distance", UNSET))

        risk_plan_step_action = cls(
            kind=kind,
            sl=sl,
            tp=tp,
            plus_costs=plus_costs,
            pct=pct,
            pct_of=pct_of,
            distance=distance,
        )

        risk_plan_step_action.additional_properties = d
        return risk_plan_step_action

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
