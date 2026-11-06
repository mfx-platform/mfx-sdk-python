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

from ..models.risk_period_kind import RiskPeriodKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_actions import RiskActions
    from ..models.risk_amount import RiskAmount
    from ..models.risk_challenge_rules_daily_loss import RiskChallengeRulesDailyLoss
    from ..models.risk_challenge_rules_max_drawdown import RiskChallengeRulesMaxDrawdown


T = TypeVar("T", bound="RiskChallengeRules")


@_attrs_define
class RiskChallengeRules:
    """
    Attributes:
        daily_loss (RiskChallengeRulesDailyLoss):
        max_drawdown (RiskChallengeRulesMaxDrawdown):
        profit_target (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's
            reference; exactly one
        min_trading_days (int):
        period_days (Union[None, int]): null: no end
        clock (str): broker or an IANA zone
        period_kinds (list[RiskPeriodKind]):
        on_fail (RiskActions):
    """

    daily_loss: "RiskChallengeRulesDailyLoss"
    max_drawdown: "RiskChallengeRulesMaxDrawdown"
    profit_target: "RiskAmount"
    min_trading_days: int
    period_days: Union[None, int]
    clock: str
    period_kinds: list[RiskPeriodKind]
    on_fail: "RiskActions"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount
        from ..models.risk_challenge_rules_daily_loss import RiskChallengeRulesDailyLoss
        from ..models.risk_challenge_rules_max_drawdown import (
            RiskChallengeRulesMaxDrawdown,
        )

        daily_loss = self.daily_loss.to_dict()

        max_drawdown = self.max_drawdown.to_dict()

        profit_target = self.profit_target.to_dict()

        min_trading_days = self.min_trading_days

        period_days: Union[None, int]
        period_days = self.period_days

        clock = self.clock

        period_kinds = []
        for period_kinds_item_data in self.period_kinds:
            period_kinds_item = period_kinds_item_data.value
            period_kinds.append(period_kinds_item)

        on_fail = self.on_fail.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "daily_loss": daily_loss,
                "max_drawdown": max_drawdown,
                "profit_target": profit_target,
                "min_trading_days": min_trading_days,
                "period_days": period_days,
                "clock": clock,
                "period_kinds": period_kinds,
                "on_fail": on_fail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount
        from ..models.risk_challenge_rules_daily_loss import RiskChallengeRulesDailyLoss
        from ..models.risk_challenge_rules_max_drawdown import (
            RiskChallengeRulesMaxDrawdown,
        )

        d = dict(src_dict)
        daily_loss = RiskChallengeRulesDailyLoss.from_dict(d.pop("daily_loss"))

        max_drawdown = RiskChallengeRulesMaxDrawdown.from_dict(d.pop("max_drawdown"))

        profit_target = RiskAmount.from_dict(d.pop("profit_target"))

        min_trading_days = d.pop("min_trading_days")

        def _parse_period_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        period_days = _parse_period_days(d.pop("period_days"))

        clock = d.pop("clock")

        period_kinds = []
        _period_kinds = d.pop("period_kinds")
        for period_kinds_item_data in _period_kinds:
            period_kinds_item = RiskPeriodKind(period_kinds_item_data)

            period_kinds.append(period_kinds_item)

        on_fail = RiskActions.from_dict(d.pop("on_fail"))

        risk_challenge_rules = cls(
            daily_loss=daily_loss,
            max_drawdown=max_drawdown,
            profit_target=profit_target,
            min_trading_days=min_trading_days,
            period_days=period_days,
            clock=clock,
            period_kinds=period_kinds,
            on_fail=on_fail,
        )

        risk_challenge_rules.additional_properties = d
        return risk_challenge_rules

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
