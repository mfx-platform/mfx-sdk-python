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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.copy_scaling_mode import CopyScalingMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyScaling")


@_attrs_define
class CopyScaling:
    """The mode and the figure it needs: multiplier for balance_ratio, equity_ratio and fixed_multiplier (1 when absent for
    the ratios); volume for fixed_volume; risk_pct for fixed_risk. A missing figure the mode needs is 422
    `validation_error`.

        Attributes:
            mode (CopyScalingMode): How a leader volume becomes the follower's, in base units first (volume times the leader
                symbol's contract size), then the follower symbol's lots, rounded down to its step. balance_ratio: times
                follower balance over leader balance, times multiplier. equity_ratio: the same with equity. fixed_multiplier:
                times multiplier. contract_size: the same exposure in units. fixed_volume: always `volume`, in the follower
                venue's unit. fixed_risk: the follower's equity times `risk_pct`, over the distance to the leader's stop valued
                in the follower's currency. The leader's balance and equity are converted into the follower account's currency
                first.
            multiplier (Union[Unset, str]): A decimal as a string, never a JSON number
            volume (Union[Unset, str]): A decimal as a string, never a JSON number
            risk_pct (Union[Unset, str]): A decimal as a string, never a JSON number
    """

    mode: CopyScalingMode
    multiplier: Union[Unset, str] = UNSET
    volume: Union[Unset, str] = UNSET
    risk_pct: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        multiplier = self.multiplier

        volume = self.volume

        risk_pct = self.risk_pct

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
            }
        )
        if multiplier is not UNSET:
            field_dict["multiplier"] = multiplier
        if volume is not UNSET:
            field_dict["volume"] = volume
        if risk_pct is not UNSET:
            field_dict["risk_pct"] = risk_pct

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = CopyScalingMode(d.pop("mode"))

        multiplier = d.pop("multiplier", UNSET)

        volume = d.pop("volume", UNSET)

        risk_pct = d.pop("risk_pct", UNSET)

        copy_scaling = cls(
            mode=mode,
            multiplier=multiplier,
            volume=volume,
            risk_pct=risk_pct,
        )

        return copy_scaling
