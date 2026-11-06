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

from ..models.risk_challenge_account_detail_state import RiskChallengeAccountDetailState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_challenge_account_detail_result_type_0 import (
        RiskChallengeAccountDetailResultType0,
    )
    from ..models.risk_period import RiskPeriod


T = TypeVar("T", bound="RiskChallengeAccountDetail")


@_attrs_define
class RiskChallengeAccountDetail:
    """
    Attributes:
        terminal_id (UUID):
        version (int):
        state (RiskChallengeAccountDetailState):
        started_at (datetime.datetime):
        period_ends_at (Union[None, datetime.datetime]):
        start_balance (str):
        day_pnl (Union[None, str]):
        daily_loss_used (Union[None, str]):
        drawdown_used (Union[None, str]):
        profit_pct (Union[None, str]):
        trading_days (int):
        result (Union['RiskChallengeAccountDetailResultType0', None]):
        periods (list['RiskPeriod']):
    """

    terminal_id: UUID
    version: int
    state: RiskChallengeAccountDetailState
    started_at: datetime.datetime
    period_ends_at: Union[None, datetime.datetime]
    start_balance: str
    day_pnl: Union[None, str]
    daily_loss_used: Union[None, str]
    drawdown_used: Union[None, str]
    profit_pct: Union[None, str]
    trading_days: int
    result: Union["RiskChallengeAccountDetailResultType0", None]
    periods: list["RiskPeriod"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_challenge_account_detail_result_type_0 import (
            RiskChallengeAccountDetailResultType0,
        )
        from ..models.risk_period import RiskPeriod

        terminal_id = str(self.terminal_id)

        version = self.version

        state = self.state.value

        started_at = self.started_at.isoformat()

        period_ends_at: Union[None, str]
        if isinstance(self.period_ends_at, datetime.datetime):
            period_ends_at = self.period_ends_at.isoformat()
        else:
            period_ends_at = self.period_ends_at

        start_balance = self.start_balance

        day_pnl: Union[None, str]
        day_pnl = self.day_pnl

        daily_loss_used: Union[None, str]
        daily_loss_used = self.daily_loss_used

        drawdown_used: Union[None, str]
        drawdown_used = self.drawdown_used

        profit_pct: Union[None, str]
        profit_pct = self.profit_pct

        trading_days = self.trading_days

        result: Union[None, dict[str, Any]]
        if isinstance(self.result, RiskChallengeAccountDetailResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        periods = []
        for periods_item_data in self.periods:
            periods_item = periods_item_data.to_dict()
            periods.append(periods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "version": version,
                "state": state,
                "started_at": started_at,
                "period_ends_at": period_ends_at,
                "start_balance": start_balance,
                "day_pnl": day_pnl,
                "daily_loss_used": daily_loss_used,
                "drawdown_used": drawdown_used,
                "profit_pct": profit_pct,
                "trading_days": trading_days,
                "result": result,
                "periods": periods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_challenge_account_detail_result_type_0 import (
            RiskChallengeAccountDetailResultType0,
        )
        from ..models.risk_period import RiskPeriod

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        version = d.pop("version")

        state = RiskChallengeAccountDetailState(d.pop("state"))

        started_at = isoparse(d.pop("started_at"))

        def _parse_period_ends_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                period_ends_at_type_0 = isoparse(data)

                return period_ends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        period_ends_at = _parse_period_ends_at(d.pop("period_ends_at"))

        start_balance = d.pop("start_balance")

        def _parse_day_pnl(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        day_pnl = _parse_day_pnl(d.pop("day_pnl"))

        def _parse_daily_loss_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        daily_loss_used = _parse_daily_loss_used(d.pop("daily_loss_used"))

        def _parse_drawdown_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        drawdown_used = _parse_drawdown_used(d.pop("drawdown_used"))

        def _parse_profit_pct(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profit_pct = _parse_profit_pct(d.pop("profit_pct"))

        trading_days = d.pop("trading_days")

        def _parse_result(data: object) -> Union["RiskChallengeAccountDetailResultType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = RiskChallengeAccountDetailResultType0.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RiskChallengeAccountDetailResultType0", None], data)

        result = _parse_result(d.pop("result"))

        periods = []
        _periods = d.pop("periods")
        for periods_item_data in _periods:
            periods_item = RiskPeriod.from_dict(periods_item_data)

            periods.append(periods_item)

        risk_challenge_account_detail = cls(
            terminal_id=terminal_id,
            version=version,
            state=state,
            started_at=started_at,
            period_ends_at=period_ends_at,
            start_balance=start_balance,
            day_pnl=day_pnl,
            daily_loss_used=daily_loss_used,
            drawdown_used=drawdown_used,
            profit_pct=profit_pct,
            trading_days=trading_days,
            result=result,
            periods=periods,
        )

        risk_challenge_account_detail.additional_properties = d
        return risk_challenge_account_detail

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
