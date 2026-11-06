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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_daily_loss import RiskDailyLoss
    from ..models.risk_drawdown import RiskDrawdown
    from ..models.risk_exposure import RiskExposure
    from ..models.risk_loss_at_stops import RiskLossAtStops
    from ..models.risk_profile import RiskProfile
    from ..models.risk_schedule import RiskSchedule


T = TypeVar("T", bound="RiskRules")


@_attrs_define
class RiskRules:
    """Every rule is optional; a rule present is evaluated. Nothing has a default the platform chose

    Attributes:
        daily_loss (Union[Unset, RiskDailyLoss]):
        drawdown (Union[Unset, RiskDrawdown]):
        exposure (Union[Unset, RiskExposure]):
        loss_at_stops (Union[Unset, RiskLossAtStops]):
        schedule (Union[Unset, RiskSchedule]):
        profile (Union[Unset, RiskProfile]): A template the tenant confirmed: it filled the rules and adds its own
            labelled rules. Updating a template never changes an active version
    """

    daily_loss: Union[Unset, "RiskDailyLoss"] = UNSET
    drawdown: Union[Unset, "RiskDrawdown"] = UNSET
    exposure: Union[Unset, "RiskExposure"] = UNSET
    loss_at_stops: Union[Unset, "RiskLossAtStops"] = UNSET
    schedule: Union[Unset, "RiskSchedule"] = UNSET
    profile: Union[Unset, "RiskProfile"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_daily_loss import RiskDailyLoss
        from ..models.risk_drawdown import RiskDrawdown
        from ..models.risk_exposure import RiskExposure
        from ..models.risk_loss_at_stops import RiskLossAtStops
        from ..models.risk_profile import RiskProfile
        from ..models.risk_schedule import RiskSchedule

        daily_loss: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.daily_loss, Unset):
            daily_loss = self.daily_loss.to_dict()

        drawdown: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.drawdown, Unset):
            drawdown = self.drawdown.to_dict()

        exposure: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exposure, Unset):
            exposure = self.exposure.to_dict()

        loss_at_stops: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.loss_at_stops, Unset):
            loss_at_stops = self.loss_at_stops.to_dict()

        schedule: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schedule, Unset):
            schedule = self.schedule.to_dict()

        profile: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if daily_loss is not UNSET:
            field_dict["daily_loss"] = daily_loss
        if drawdown is not UNSET:
            field_dict["drawdown"] = drawdown
        if exposure is not UNSET:
            field_dict["exposure"] = exposure
        if loss_at_stops is not UNSET:
            field_dict["loss_at_stops"] = loss_at_stops
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_daily_loss import RiskDailyLoss
        from ..models.risk_drawdown import RiskDrawdown
        from ..models.risk_exposure import RiskExposure
        from ..models.risk_loss_at_stops import RiskLossAtStops
        from ..models.risk_profile import RiskProfile
        from ..models.risk_schedule import RiskSchedule

        d = dict(src_dict)
        _daily_loss = d.pop("daily_loss", UNSET)
        daily_loss: Union[Unset, RiskDailyLoss]
        if isinstance(_daily_loss, Unset):
            daily_loss = UNSET
        else:
            daily_loss = RiskDailyLoss.from_dict(_daily_loss)

        _drawdown = d.pop("drawdown", UNSET)
        drawdown: Union[Unset, RiskDrawdown]
        if isinstance(_drawdown, Unset):
            drawdown = UNSET
        else:
            drawdown = RiskDrawdown.from_dict(_drawdown)

        _exposure = d.pop("exposure", UNSET)
        exposure: Union[Unset, RiskExposure]
        if isinstance(_exposure, Unset):
            exposure = UNSET
        else:
            exposure = RiskExposure.from_dict(_exposure)

        _loss_at_stops = d.pop("loss_at_stops", UNSET)
        loss_at_stops: Union[Unset, RiskLossAtStops]
        if isinstance(_loss_at_stops, Unset):
            loss_at_stops = UNSET
        else:
            loss_at_stops = RiskLossAtStops.from_dict(_loss_at_stops)

        _schedule = d.pop("schedule", UNSET)
        schedule: Union[Unset, RiskSchedule]
        if isinstance(_schedule, Unset):
            schedule = UNSET
        else:
            schedule = RiskSchedule.from_dict(_schedule)

        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, RiskProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = RiskProfile.from_dict(_profile)

        risk_rules = cls(
            daily_loss=daily_loss,
            drawdown=drawdown,
            exposure=exposure,
            loss_at_stops=loss_at_stops,
            schedule=schedule,
            profile=profile,
        )

        return risk_rules
