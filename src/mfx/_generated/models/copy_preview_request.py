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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_bounds import CopyBounds
    from ..models.copy_options import CopyOptions
    from ..models.copy_preview_request_rows_item import CopyPreviewRequestRowsItem
    from ..models.copy_preview_request_symbol_map import CopyPreviewRequestSymbolMap
    from ..models.copy_scaling import CopyScaling


T = TypeVar("T", bound="CopyPreviewRequest")


@_attrs_define
class CopyPreviewRequest:
    """
    Attributes:
        account_id (UUID): The account that would follow
        leader_id (UUID):
        scaling (CopyScaling): The mode and the figure it needs: multiplier for balance_ratio, equity_ratio and
            fixed_multiplier (1 when absent for the ratios); volume for fixed_volume; risk_pct for fixed_risk. A missing
            figure the mode needs is 422 `validation_error`.
        rows (list['CopyPreviewRequestRowsItem']): The leader deals to try, each a leader symbol and a volume in the
            leader venue's unit
        bounds (Union[Unset, CopyBounds]): The follower's own limits on one copy, in its venue's unit; the broker's
            apply as well, and the tighter wins
        symbol_map (Union[Unset, CopyPreviewRequestSymbolMap]):
        options (Union[Unset, CopyOptions]):
    """

    account_id: UUID
    leader_id: UUID
    scaling: "CopyScaling"
    rows: list["CopyPreviewRequestRowsItem"]
    bounds: Union[Unset, "CopyBounds"] = UNSET
    symbol_map: Union[Unset, "CopyPreviewRequestSymbolMap"] = UNSET
    options: Union[Unset, "CopyOptions"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_options import CopyOptions
        from ..models.copy_preview_request_rows_item import CopyPreviewRequestRowsItem
        from ..models.copy_preview_request_symbol_map import CopyPreviewRequestSymbolMap
        from ..models.copy_scaling import CopyScaling

        account_id = str(self.account_id)

        leader_id = str(self.leader_id)

        scaling = self.scaling.to_dict()

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        bounds: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.bounds, Unset):
            bounds = self.bounds.to_dict()

        symbol_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.symbol_map, Unset):
            symbol_map = self.symbol_map.to_dict()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "account_id": account_id,
                "leader_id": leader_id,
                "scaling": scaling,
                "rows": rows,
            }
        )
        if bounds is not UNSET:
            field_dict["bounds"] = bounds
        if symbol_map is not UNSET:
            field_dict["symbol_map"] = symbol_map
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_options import CopyOptions
        from ..models.copy_preview_request_rows_item import CopyPreviewRequestRowsItem
        from ..models.copy_preview_request_symbol_map import CopyPreviewRequestSymbolMap
        from ..models.copy_scaling import CopyScaling

        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        leader_id = UUID(d.pop("leader_id"))

        scaling = CopyScaling.from_dict(d.pop("scaling"))

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = CopyPreviewRequestRowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        _bounds = d.pop("bounds", UNSET)
        bounds: Union[Unset, CopyBounds]
        if isinstance(_bounds, Unset):
            bounds = UNSET
        else:
            bounds = CopyBounds.from_dict(_bounds)

        _symbol_map = d.pop("symbol_map", UNSET)
        symbol_map: Union[Unset, CopyPreviewRequestSymbolMap]
        if isinstance(_symbol_map, Unset):
            symbol_map = UNSET
        else:
            symbol_map = CopyPreviewRequestSymbolMap.from_dict(_symbol_map)

        _options = d.pop("options", UNSET)
        options: Union[Unset, CopyOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = CopyOptions.from_dict(_options)

        copy_preview_request = cls(
            account_id=account_id,
            leader_id=leader_id,
            scaling=scaling,
            rows=rows,
            bounds=bounds,
            symbol_map=symbol_map,
            options=options,
        )

        return copy_preview_request
