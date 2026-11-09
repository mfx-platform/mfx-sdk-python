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

from ..models.copy_risk_limits_basis import CopyRiskLimitsBasis
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyRiskLimits")


@_attrs_define
class CopyRiskLimits:
    """The follower's copy limits, as a percentage of `basis`, in the follower account's currency. Reaching one stops the
    follower out; with close_on_stopout its copied volume of this leader is closed, never the account's own positions.

        Attributes:
            daily_pct (Union[None, Unset, str]):
            monthly_pct (Union[None, Unset, str]):
            lifetime_pct (Union[None, Unset, str]):
            basis (Union[Unset, CopyRiskLimitsBasis]):  Default: CopyRiskLimitsBasis.EQUITY.
    """

    daily_pct: Union[None, Unset, str] = UNSET
    monthly_pct: Union[None, Unset, str] = UNSET
    lifetime_pct: Union[None, Unset, str] = UNSET
    basis: Union[Unset, CopyRiskLimitsBasis] = CopyRiskLimitsBasis.EQUITY

    def to_dict(self) -> dict[str, Any]:
        daily_pct: Union[None, Unset, str]
        if isinstance(self.daily_pct, Unset):
            daily_pct = UNSET
        else:
            daily_pct = self.daily_pct

        monthly_pct: Union[None, Unset, str]
        if isinstance(self.monthly_pct, Unset):
            monthly_pct = UNSET
        else:
            monthly_pct = self.monthly_pct

        lifetime_pct: Union[None, Unset, str]
        if isinstance(self.lifetime_pct, Unset):
            lifetime_pct = UNSET
        else:
            lifetime_pct = self.lifetime_pct

        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if daily_pct is not UNSET:
            field_dict["daily_pct"] = daily_pct
        if monthly_pct is not UNSET:
            field_dict["monthly_pct"] = monthly_pct
        if lifetime_pct is not UNSET:
            field_dict["lifetime_pct"] = lifetime_pct
        if basis is not UNSET:
            field_dict["basis"] = basis

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_daily_pct(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        daily_pct = _parse_daily_pct(d.pop("daily_pct", UNSET))

        def _parse_monthly_pct(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monthly_pct = _parse_monthly_pct(d.pop("monthly_pct", UNSET))

        def _parse_lifetime_pct(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lifetime_pct = _parse_lifetime_pct(d.pop("lifetime_pct", UNSET))

        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, CopyRiskLimitsBasis]
        if isinstance(_basis, Unset):
            basis = UNSET
        else:
            basis = CopyRiskLimitsBasis(_basis)

        copy_risk_limits = cls(
            daily_pct=daily_pct,
            monthly_pct=monthly_pct,
            lifetime_pct=lifetime_pct,
            basis=basis,
        )

        return copy_risk_limits
