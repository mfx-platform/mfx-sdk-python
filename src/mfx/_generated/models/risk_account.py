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

from ..models.risk_account_activation_state import RiskAccountActivationState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_account_challenges_item import RiskAccountChallengesItem
    from ..models.risk_account_exposure import RiskAccountExposure
    from ..models.risk_account_inputs import RiskAccountInputs
    from ..models.risk_account_open_breaches_item import RiskAccountOpenBreachesItem
    from ..models.risk_account_policy_type_0 import RiskAccountPolicyType0
    from ..models.risk_account_restriction import RiskAccountRestriction
    from ..models.risk_coverage import RiskCoverage
    from ..models.risk_daily_loss_figure import RiskDailyLossFigure
    from ..models.risk_drawdown_figure import RiskDrawdownFigure


T = TypeVar("T", bound="RiskAccount")


@_attrs_define
class RiskAccount:
    """
    Attributes:
        terminal_id (UUID):
        policy (Union['RiskAccountPolicyType0', None]):
        activation_state (RiskAccountActivationState):
        daily_loss (Union['RiskDailyLossFigure', None]):
        drawdown (Union['RiskDrawdownFigure', None]):
        exposure (RiskAccountExposure):
        open_breaches (list['RiskAccountOpenBreachesItem']):
        restriction (RiskAccountRestriction):
        coverage (RiskCoverage): Per kind. A green terminal is not full coverage
        inputs (RiskAccountInputs):
        challenges (list['RiskAccountChallengesItem']):
    """

    terminal_id: UUID
    policy: Union["RiskAccountPolicyType0", None]
    activation_state: RiskAccountActivationState
    daily_loss: Union["RiskDailyLossFigure", None]
    drawdown: Union["RiskDrawdownFigure", None]
    exposure: "RiskAccountExposure"
    open_breaches: list["RiskAccountOpenBreachesItem"]
    restriction: "RiskAccountRestriction"
    coverage: "RiskCoverage"
    inputs: "RiskAccountInputs"
    challenges: list["RiskAccountChallengesItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_account_challenges_item import RiskAccountChallengesItem
        from ..models.risk_account_exposure import RiskAccountExposure
        from ..models.risk_account_inputs import RiskAccountInputs
        from ..models.risk_account_open_breaches_item import RiskAccountOpenBreachesItem
        from ..models.risk_account_policy_type_0 import RiskAccountPolicyType0
        from ..models.risk_account_restriction import RiskAccountRestriction
        from ..models.risk_coverage import RiskCoverage
        from ..models.risk_daily_loss_figure import RiskDailyLossFigure
        from ..models.risk_drawdown_figure import RiskDrawdownFigure

        terminal_id = str(self.terminal_id)

        policy: Union[None, dict[str, Any]]
        if isinstance(self.policy, RiskAccountPolicyType0):
            policy = self.policy.to_dict()
        else:
            policy = self.policy

        activation_state = self.activation_state.value

        daily_loss: Union[None, dict[str, Any]]
        if isinstance(self.daily_loss, RiskDailyLossFigure):
            daily_loss = self.daily_loss.to_dict()
        else:
            daily_loss = self.daily_loss

        drawdown: Union[None, dict[str, Any]]
        if isinstance(self.drawdown, RiskDrawdownFigure):
            drawdown = self.drawdown.to_dict()
        else:
            drawdown = self.drawdown

        exposure = self.exposure.to_dict()

        open_breaches = []
        for open_breaches_item_data in self.open_breaches:
            open_breaches_item = open_breaches_item_data.to_dict()
            open_breaches.append(open_breaches_item)

        restriction = self.restriction.to_dict()

        coverage = self.coverage.to_dict()

        inputs = self.inputs.to_dict()

        challenges = []
        for challenges_item_data in self.challenges:
            challenges_item = challenges_item_data.to_dict()
            challenges.append(challenges_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "policy": policy,
                "activation_state": activation_state,
                "daily_loss": daily_loss,
                "drawdown": drawdown,
                "exposure": exposure,
                "open_breaches": open_breaches,
                "restriction": restriction,
                "coverage": coverage,
                "inputs": inputs,
                "challenges": challenges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_account_challenges_item import RiskAccountChallengesItem
        from ..models.risk_account_exposure import RiskAccountExposure
        from ..models.risk_account_inputs import RiskAccountInputs
        from ..models.risk_account_open_breaches_item import RiskAccountOpenBreachesItem
        from ..models.risk_account_policy_type_0 import RiskAccountPolicyType0
        from ..models.risk_account_restriction import RiskAccountRestriction
        from ..models.risk_coverage import RiskCoverage
        from ..models.risk_daily_loss_figure import RiskDailyLossFigure
        from ..models.risk_drawdown_figure import RiskDrawdownFigure

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        def _parse_policy(data: object) -> Union["RiskAccountPolicyType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                policy_type_0 = RiskAccountPolicyType0.from_dict(data)

                return policy_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RiskAccountPolicyType0", None], data)

        policy = _parse_policy(d.pop("policy"))

        activation_state = RiskAccountActivationState(d.pop("activation_state"))

        def _parse_daily_loss(data: object) -> Union["RiskDailyLossFigure", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                daily_loss_type_0 = RiskDailyLossFigure.from_dict(data)

                return daily_loss_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RiskDailyLossFigure", None], data)

        daily_loss = _parse_daily_loss(d.pop("daily_loss"))

        def _parse_drawdown(data: object) -> Union["RiskDrawdownFigure", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                drawdown_type_0 = RiskDrawdownFigure.from_dict(data)

                return drawdown_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RiskDrawdownFigure", None], data)

        drawdown = _parse_drawdown(d.pop("drawdown"))

        exposure = RiskAccountExposure.from_dict(d.pop("exposure"))

        open_breaches = []
        _open_breaches = d.pop("open_breaches")
        for open_breaches_item_data in _open_breaches:
            open_breaches_item = RiskAccountOpenBreachesItem.from_dict(open_breaches_item_data)

            open_breaches.append(open_breaches_item)

        restriction = RiskAccountRestriction.from_dict(d.pop("restriction"))

        coverage = RiskCoverage.from_dict(d.pop("coverage"))

        inputs = RiskAccountInputs.from_dict(d.pop("inputs"))

        challenges = []
        _challenges = d.pop("challenges")
        for challenges_item_data in _challenges:
            challenges_item = RiskAccountChallengesItem.from_dict(challenges_item_data)

            challenges.append(challenges_item)

        risk_account = cls(
            terminal_id=terminal_id,
            policy=policy,
            activation_state=activation_state,
            daily_loss=daily_loss,
            drawdown=drawdown,
            exposure=exposure,
            open_breaches=open_breaches,
            restriction=restriction,
            coverage=coverage,
            inputs=inputs,
            challenges=challenges,
        )

        risk_account.additional_properties = d
        return risk_account

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
