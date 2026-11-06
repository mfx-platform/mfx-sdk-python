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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.risk_preview_reason_type_1 import RiskPreviewReasonType1
from ..models.risk_preview_reason_type_2_type_1 import RiskPreviewReasonType2Type1
from ..models.risk_preview_reason_type_3_type_1 import RiskPreviewReasonType3Type1
from ..models.risk_preview_verdict import RiskPreviewVerdict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_preview_inputs import RiskPreviewInputs
    from ..models.risk_rule_check import RiskRuleCheck


T = TypeVar("T", bound="RiskPreview")


@_attrs_define
class RiskPreview:
    """
    Attributes:
        volume (Union[None, str]): Rounded down to the step; null when even the minimum is over the budget
        volume_unrounded (Union[None, str]):
        reason (Union[None, RiskPreviewReasonType1, RiskPreviewReasonType2Type1, RiskPreviewReasonType3Type1]):
        budget (str):
        loss_at_stop (Union[None, str]):
        commission (Union[None, str]):
        slippage (Union[None, str]):
        estimated_loss (Union[None, str]):
        reward_to_risk (Union[None, str]): Net of commission; null without a take profit
        margin_required (Union[None, str]):
        free_margin_after (Union[None, str]):
        checks (list['RiskRuleCheck']):
        verdict (RiskPreviewVerdict):
        assumptions (list[str]): What the figures assume that the broker did not give
        inputs (RiskPreviewInputs):
        expires_at (datetime.datetime):
    """

    volume: Union[None, str]
    volume_unrounded: Union[None, str]
    reason: Union[
        None, RiskPreviewReasonType1, RiskPreviewReasonType2Type1, RiskPreviewReasonType3Type1
    ]
    budget: str
    loss_at_stop: Union[None, str]
    commission: Union[None, str]
    slippage: Union[None, str]
    estimated_loss: Union[None, str]
    reward_to_risk: Union[None, str]
    margin_required: Union[None, str]
    free_margin_after: Union[None, str]
    checks: list["RiskRuleCheck"]
    verdict: RiskPreviewVerdict
    assumptions: list[str]
    inputs: "RiskPreviewInputs"
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_preview_inputs import RiskPreviewInputs
        from ..models.risk_rule_check import RiskRuleCheck

        volume: Union[None, str]
        volume = self.volume

        volume_unrounded: Union[None, str]
        volume_unrounded = self.volume_unrounded

        reason: Union[None, str]
        if isinstance(self.reason, RiskPreviewReasonType1):
            reason = self.reason.value
        elif isinstance(self.reason, RiskPreviewReasonType2Type1):
            reason = self.reason.value
        elif isinstance(self.reason, RiskPreviewReasonType3Type1):
            reason = self.reason.value
        else:
            reason = self.reason

        budget = self.budget

        loss_at_stop: Union[None, str]
        loss_at_stop = self.loss_at_stop

        commission: Union[None, str]
        commission = self.commission

        slippage: Union[None, str]
        slippage = self.slippage

        estimated_loss: Union[None, str]
        estimated_loss = self.estimated_loss

        reward_to_risk: Union[None, str]
        reward_to_risk = self.reward_to_risk

        margin_required: Union[None, str]
        margin_required = self.margin_required

        free_margin_after: Union[None, str]
        free_margin_after = self.free_margin_after

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        verdict = self.verdict.value

        assumptions = self.assumptions

        inputs = self.inputs.to_dict()

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "volume": volume,
                "volume_unrounded": volume_unrounded,
                "reason": reason,
                "budget": budget,
                "loss_at_stop": loss_at_stop,
                "commission": commission,
                "slippage": slippage,
                "estimated_loss": estimated_loss,
                "reward_to_risk": reward_to_risk,
                "margin_required": margin_required,
                "free_margin_after": free_margin_after,
                "checks": checks,
                "verdict": verdict,
                "assumptions": assumptions,
                "inputs": inputs,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_preview_inputs import RiskPreviewInputs
        from ..models.risk_rule_check import RiskRuleCheck

        d = dict(src_dict)

        def _parse_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume = _parse_volume(d.pop("volume"))

        def _parse_volume_unrounded(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume_unrounded = _parse_volume_unrounded(d.pop("volume_unrounded"))

        def _parse_reason(
            data: object,
        ) -> Union[
            None, RiskPreviewReasonType1, RiskPreviewReasonType2Type1, RiskPreviewReasonType3Type1
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = RiskPreviewReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = RiskPreviewReasonType2Type1(data)

                return reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = RiskPreviewReasonType3Type1(data)

                return reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    RiskPreviewReasonType1,
                    RiskPreviewReasonType2Type1,
                    RiskPreviewReasonType3Type1,
                ],
                data,
            )

        reason = _parse_reason(d.pop("reason"))

        budget = d.pop("budget")

        def _parse_loss_at_stop(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        loss_at_stop = _parse_loss_at_stop(d.pop("loss_at_stop"))

        def _parse_commission(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        commission = _parse_commission(d.pop("commission"))

        def _parse_slippage(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        slippage = _parse_slippage(d.pop("slippage"))

        def _parse_estimated_loss(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        estimated_loss = _parse_estimated_loss(d.pop("estimated_loss"))

        def _parse_reward_to_risk(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reward_to_risk = _parse_reward_to_risk(d.pop("reward_to_risk"))

        def _parse_margin_required(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        margin_required = _parse_margin_required(d.pop("margin_required"))

        def _parse_free_margin_after(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        free_margin_after = _parse_free_margin_after(d.pop("free_margin_after"))

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = RiskRuleCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        verdict = RiskPreviewVerdict(d.pop("verdict"))

        assumptions = cast(list[str], d.pop("assumptions"))

        inputs = RiskPreviewInputs.from_dict(d.pop("inputs"))

        expires_at = isoparse(d.pop("expires_at"))

        risk_preview = cls(
            volume=volume,
            volume_unrounded=volume_unrounded,
            reason=reason,
            budget=budget,
            loss_at_stop=loss_at_stop,
            commission=commission,
            slippage=slippage,
            estimated_loss=estimated_loss,
            reward_to_risk=reward_to_risk,
            margin_required=margin_required,
            free_margin_after=free_margin_after,
            checks=checks,
            verdict=verdict,
            assumptions=assumptions,
            inputs=inputs,
            expires_at=expires_at,
        )

        risk_preview.additional_properties = d
        return risk_preview

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
