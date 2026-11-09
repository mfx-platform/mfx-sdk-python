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
    from ..models.copy_bounds import CopyBounds
    from ..models.copy_follower_update_symbol_map import CopyFollowerUpdateSymbolMap
    from ..models.copy_options import CopyOptions
    from ..models.copy_risk_limits import CopyRiskLimits
    from ..models.copy_scaling import CopyScaling


T = TypeVar("T", bound="CopyFollowerUpdate")


@_attrs_define
class CopyFollowerUpdate:
    """
    Attributes:
        scaling (Union[Unset, CopyScaling]): The mode and the figure it needs: multiplier for balance_ratio,
            equity_ratio and fixed_multiplier (1 when absent for the ratios); volume for fixed_volume; risk_pct for
            fixed_risk. A missing figure the mode needs is 422 `validation_error`.
        bounds (Union[Unset, CopyBounds]): The follower's own limits on one copy, in its venue's unit; the broker's
            apply as well, and the tighter wins
        symbol_map (Union[Unset, CopyFollowerUpdateSymbolMap]):
        options (Union[Unset, CopyOptions]):
        risk_limits (Union[Unset, CopyRiskLimits]): The follower's copy limits, as a percentage of `basis`, in the
            follower account's currency. Reaching one stops the follower out; with close_on_stopout its copied volume of
            this leader is closed, never the account's own positions.
        close_on_stopout (Union[Unset, bool]):
    """

    scaling: Union[Unset, "CopyScaling"] = UNSET
    bounds: Union[Unset, "CopyBounds"] = UNSET
    symbol_map: Union[Unset, "CopyFollowerUpdateSymbolMap"] = UNSET
    options: Union[Unset, "CopyOptions"] = UNSET
    risk_limits: Union[Unset, "CopyRiskLimits"] = UNSET
    close_on_stopout: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_follower_update_symbol_map import CopyFollowerUpdateSymbolMap
        from ..models.copy_options import CopyOptions
        from ..models.copy_risk_limits import CopyRiskLimits
        from ..models.copy_scaling import CopyScaling

        scaling: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.scaling, Unset):
            scaling = self.scaling.to_dict()

        bounds: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.bounds, Unset):
            bounds = self.bounds.to_dict()

        symbol_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.symbol_map, Unset):
            symbol_map = self.symbol_map.to_dict()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        risk_limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.risk_limits, Unset):
            risk_limits = self.risk_limits.to_dict()

        close_on_stopout = self.close_on_stopout

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if scaling is not UNSET:
            field_dict["scaling"] = scaling
        if bounds is not UNSET:
            field_dict["bounds"] = bounds
        if symbol_map is not UNSET:
            field_dict["symbol_map"] = symbol_map
        if options is not UNSET:
            field_dict["options"] = options
        if risk_limits is not UNSET:
            field_dict["risk_limits"] = risk_limits
        if close_on_stopout is not UNSET:
            field_dict["close_on_stopout"] = close_on_stopout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_follower_update_symbol_map import CopyFollowerUpdateSymbolMap
        from ..models.copy_options import CopyOptions
        from ..models.copy_risk_limits import CopyRiskLimits
        from ..models.copy_scaling import CopyScaling

        d = dict(src_dict)
        _scaling = d.pop("scaling", UNSET)
        scaling: Union[Unset, CopyScaling]
        if isinstance(_scaling, Unset):
            scaling = UNSET
        else:
            scaling = CopyScaling.from_dict(_scaling)

        _bounds = d.pop("bounds", UNSET)
        bounds: Union[Unset, CopyBounds]
        if isinstance(_bounds, Unset):
            bounds = UNSET
        else:
            bounds = CopyBounds.from_dict(_bounds)

        _symbol_map = d.pop("symbol_map", UNSET)
        symbol_map: Union[Unset, CopyFollowerUpdateSymbolMap]
        if isinstance(_symbol_map, Unset):
            symbol_map = UNSET
        else:
            symbol_map = CopyFollowerUpdateSymbolMap.from_dict(_symbol_map)

        _options = d.pop("options", UNSET)
        options: Union[Unset, CopyOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = CopyOptions.from_dict(_options)

        _risk_limits = d.pop("risk_limits", UNSET)
        risk_limits: Union[Unset, CopyRiskLimits]
        if isinstance(_risk_limits, Unset):
            risk_limits = UNSET
        else:
            risk_limits = CopyRiskLimits.from_dict(_risk_limits)

        close_on_stopout = d.pop("close_on_stopout", UNSET)

        copy_follower_update = cls(
            scaling=scaling,
            bounds=bounds,
            symbol_map=symbol_map,
            options=options,
            risk_limits=risk_limits,
            close_on_stopout=close_on_stopout,
        )

        return copy_follower_update
