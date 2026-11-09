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

T = TypeVar("T", bound="CopyLeaderLimits")


@_attrs_define
class CopyLeaderLimits:
    """Limits on the leader's own deals. A deal over one is copied to no follower, and every follower's log row says
    `refused` with reason `risk_rule`.

        Attributes:
            max_risk_pct (Union[None, Unset, str]): The most a deal may risk to its stop loss, as a percentage of the leader
                account's equity; null is no limit
            max_leverage (Union[None, Unset, str]): The most notional exposure the leader account may hold after the deal,
                as a multiple of its equity; null is no limit
    """

    max_risk_pct: Union[None, Unset, str] = UNSET
    max_leverage: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        max_risk_pct: Union[None, Unset, str]
        if isinstance(self.max_risk_pct, Unset):
            max_risk_pct = UNSET
        else:
            max_risk_pct = self.max_risk_pct

        max_leverage: Union[None, Unset, str]
        if isinstance(self.max_leverage, Unset):
            max_leverage = UNSET
        else:
            max_leverage = self.max_leverage

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if max_risk_pct is not UNSET:
            field_dict["max_risk_pct"] = max_risk_pct
        if max_leverage is not UNSET:
            field_dict["max_leverage"] = max_leverage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_max_risk_pct(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_risk_pct = _parse_max_risk_pct(d.pop("max_risk_pct", UNSET))

        def _parse_max_leverage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_leverage = _parse_max_leverage(d.pop("max_leverage", UNSET))

        copy_leader_limits = cls(
            max_risk_pct=max_risk_pct,
            max_leverage=max_leverage,
        )

        return copy_leader_limits
